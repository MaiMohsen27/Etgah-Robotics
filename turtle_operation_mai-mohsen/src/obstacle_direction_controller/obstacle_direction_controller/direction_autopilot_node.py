#!/usr/bin/env python3

import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from obstacle_direction_interfaces.srv import SetDirection


class DirectionAutopilotNode(Node):

    def __init__(self):
        super().__init__('direction_autopilot_node')

        # Subscriber
        self.scan_subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        # Publisher
        self.velocity_publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # Service server 
        self.direction_service = self.create_service(
            SetDirection,
            '/set_direction',
            self.set_direction_callback
        )

        # Parameters
        self.obstacle_threshold = 0.50
        self.free_forward_threshold = 1.00
        self.forward_velocity = 0.20
        self.angular_velocity = 0.50
        self.turning_direction = 0
        self.state = 'forward'

        # Override parameters
        self.override_active = False
        self.override_direction = None
        self.override_started_at = None
        self.override_hold_time = 2.5  # override time in seconds

        self.get_logger().info('Direction Controller Started')

    def scan_callback(self, msg: LaserScan):
        """Process LiDAR scan and compute distances using angles."""

        ranges = msg.ranges
        angle_min = msg.angle_min
        angle_increment = msg.angle_increment

        front_distance = self._sector_distance(
            ranges, angle_min, angle_increment, 0.0, math.radians(30), 5.0
        )
        left_distance = self._sector_distance(
            ranges, angle_min, angle_increment, math.pi / 2, math.radians(30), 5.0
        )
        right_distance = self._sector_distance(
            ranges, angle_min, angle_increment, -math.pi / 2, math.radians(30), 5.0
        )

        mode_label = 'OVERRIDE' if self.override_active else 'AUTONOMOUS'
        self.get_logger().info(
            f'F:{front_distance:.2f}m | L:{left_distance:.2f}m | R:{right_distance:.2f}m | MODE:{mode_label}'
        )

        self._control_robot(front_distance, left_distance, right_distance)

    def _normalize_angle(self, angle: float) -> float:
        return math.atan2(math.sin(angle), math.cos(angle))

    def _angle_to_index(self, angle: float, angle_min: float, angle_increment: float, size: int) -> int:
        desired = self._normalize_angle(angle)
        base = self._normalize_angle(angle_min)
        delta = desired - base
        if delta < 0.0:
            delta += 2.0 * math.pi
        index = int(round(delta / angle_increment))
        return max(0, min(size - 1, index))

    def _sector_distance(
        self,
        ranges,
        angle_min: float,
        angle_increment: float,
        center_angle: float,
        width: float,
        max_distance: float,
    ) -> float:
        n = len(ranges)
        half_width = width / 2.0
        start_idx = self._angle_to_index(center_angle - half_width, angle_min, angle_increment, n)
        end_idx = self._angle_to_index(center_angle + half_width, angle_min, angle_increment, n)

        if start_idx <= end_idx:
            sector = ranges[start_idx:end_idx + 1]
        else:
            sector = ranges[start_idx:] + ranges[:end_idx + 1]

        valid = [r for r in sector if 0.1 < r < max_distance]
        return min(valid) if valid else max_distance

    def set_direction_callback(self, request, response):
        """Handle incoming /set_direction service requests"""

        direction = request.direction.lower().strip()
        valid_directions = ('forward', 'reverse', 'left', 'right')

        if direction not in valid_directions:
            response.success = False
            response.message = (
                f'Unknown direction: {direction}. Use forward, reverse, left, or right.'
            )
            self.get_logger().warn(f'OVERRIDE REJECTED: {response.message}')
            return response

        self.override_active = True
        self.override_direction = direction
        self.override_started_at = self.get_clock().now()

        response.success = True
        response.message = (
            f"Override accepted: direction set to '{direction}' for "
            f'{self.override_hold_time:.1f}s before autonomy resumes.'
        )

        self.get_logger().info(f'OVERRIDE REQUEST: {direction} -> success={response.success}')
        return response

    def _override_command(self) -> Twist:
        """Build the Twist command for the currently active override direction."""

        cmd = Twist()
        if self.override_direction == 'forward':
            cmd.linear.x = self.forward_velocity
        elif self.override_direction == 'reverse':
            cmd.linear.x = -self.forward_velocity
        elif self.override_direction == 'left':
            cmd.angular.z = self.angular_velocity
        elif self.override_direction == 'right':
            cmd.angular.z = -self.angular_velocity
        return cmd

    def _control_robot(self, front, left, right):
        """Simple, safe control logic, override-aware."""

        # An active operator override takes priority over autonomy.
        if self.override_active:
            elapsed = (self.get_clock().now() - self.override_started_at).nanoseconds / 1e9
            if elapsed < self.override_hold_time:
                cmd = self._override_command()
                self.velocity_publisher.publish(cmd)
                self.get_logger().warn(f"OVERRIDE ACTIVE: driving '{self.override_direction}'")
                return
            else:
                self.get_logger().info('Override hold time elapsed. Resuming autonomous control.')
                self.override_active = False
                self.override_direction = None
                self.state = 'forward'
                self.turning_direction = 0

        cmd = Twist()

        TURN_SAFETY = 0.40

        can_turn_left = left > TURN_SAFETY
        can_turn_right = right > TURN_SAFETY

        if self.state == 'forward':
            if front <= self.obstacle_threshold:
                self.state = 'turn'
                self.turning_direction = 1 if left >= right else -1
                side = 'LEFT' if self.turning_direction > 0 else 'RIGHT'
                self.get_logger().warn(
                    f'OBSTACLE: Front {front:.2f}m <= {self.obstacle_threshold:.2f}m, switching to TURN state'
                )
                self.get_logger().warn(f'ROTATE {side} until front path is free')
            else:
                cmd.linear.x = self.forward_velocity
                cmd.angular.z = 0.0
                self.get_logger().info('ACTION: FORWARD')

        if self.state == 'turn':
            if self.turning_direction > 0 and not can_turn_left and can_turn_right:
                self.turning_direction = -1
            elif self.turning_direction < 0 and not can_turn_right and can_turn_left:
                self.turning_direction = 1
            elif self.turning_direction > 0 and not can_turn_left:
                self.turning_direction = 0
            elif self.turning_direction < 0 and not can_turn_right:
                self.turning_direction = 0

            if self.turning_direction == 0:
                if can_turn_left or can_turn_right:
                    self.turning_direction = 1 if left >= right else -1
                else:
                    self.state = 'reverse'
                    self.get_logger().error(
                        f'TRAPPED! No safe turn direction (L:{left:.2f} R:{right:.2f}), switching to REVERSE'
                    )

            if self.state == 'turn':
                if front > self.free_forward_threshold:
                    self.state = 'forward'
                    self.turning_direction = 0
                    cmd.linear.x = self.forward_velocity
                    cmd.angular.z = 0.0
                    self.get_logger().info('PATH CLEAR. Stopping rotation and moving forward.')
                    self.get_logger().info('ACTION: FORWARD')
                else:
                    cmd.linear.x = 0.0
                    cmd.angular.z = self.angular_velocity * self.turning_direction
                    side = 'LEFT' if self.turning_direction > 0 else 'RIGHT'
                    self.get_logger().warn(f'ROTATE {side} until front path is free')

        if self.state == 'reverse':
            cmd.linear.x = -0.10
            cmd.angular.z = self.angular_velocity if left >= right else -self.angular_velocity
            self.get_logger().error(
                f'REVERSE and rotate to safer side (L:{left:.2f} R:{right:.2f})'
            )
            if front > self.free_forward_threshold and (can_turn_left or can_turn_right):
                self.state = 'forward'
                self.turning_direction = 0
                self.get_logger().info('RECOVERED. Switching back to FORWARD state.')

        self.velocity_publisher.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    controller = DirectionAutopilotNode()

    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        pass
    finally:
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
