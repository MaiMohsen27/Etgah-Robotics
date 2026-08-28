#!/usr/bin/env python3

"""
delivery_mission_node:

Handles 3-phase package delivery: Pickup Drive -> Loading Pause -> Delivery Drive.
Publishes to `/cmd_vel` and streams mission feedback (remaining time & progress).
"""

import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from geometry_msgs.msg import Twist

from delivery_mission_interfaces.action import DeliveryMission


class DeliveryMissionServer(Node):

    def __init__(self):
        super().__init__('delivery_mission_server')

        # Publisher
        self.velocity_publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # Action server
        self.mission_action_server = ActionServer(
            self,
            DeliveryMission,
            '/delivery_mission',
            execute_callback=self.execute_mission_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )

        # Mission state
        self.mission_active = False

        self.get_logger().info('Delivery Mission Server Started')

    def goal_callback(self, goal_request):
        """Accept or reject an incoming goal before execution starts."""

        if self.mission_active:
            self.get_logger().warn('REJECTED: a mission is already running')
            return GoalResponse.REJECT

        if goal_request.timeout <= 0.0:
            self.get_logger().warn('REJECTED: timeout must be greater than 0')
            return GoalResponse.REJECT

        self.get_logger().info(
            f'GOAL ACCEPTED: speed={goal_request.speed:.2f} '
            f'pickup_duration={goal_request.pickup_duration:.2f}s '
            f'delivery_duration={goal_request.delivery_duration:.2f}s '
            f'timeout={goal_request.timeout:.2f}s'
        )
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        """Allow the client to cancel a running mission."""

        self.get_logger().warn('CANCEL REQUEST received')
        return CancelResponse.ACCEPT

    def execute_mission_callback(self, goal_handle):
        """Execute 3-phase delivery: Drive to pickup -> Pause & simulate pickup -> Drive to delivery."""

        speed = goal_handle.request.speed
        pickup_duration = goal_handle.request.pickup_duration
        delivery_duration = goal_handle.request.delivery_duration
        timeout = goal_handle.request.timeout

        self.mission_active = True
        feedback_msg = DeliveryMission.Feedback()
        result = DeliveryMission.Result()

        start_time = time.time()
        rate_hz = 10.0
        sleep_duration = 1.0 / rate_hz

        # Helper internal function to handle cancellations & timeouts cleanly
        def check_status():
            elapsed = time.time() - start_time
            remaining = max(0.0, timeout - elapsed)

            if goal_handle.is_cancel_requested:
                self._publish_stop()
                goal_handle.canceled()
                result.success = False
                result.message = 'Mission canceled by client'
                self.mission_active = False
                self.get_logger().warn('MISSION CANCELED')
                return False, result

            if elapsed >= timeout:
                self._publish_stop()
                goal_handle.abort()
                result.success = False
                result.message = 'Mission aborted: timeout exceeded'
                self.mission_active = False
                self.get_logger().error('MISSION ABORTED: TIMEOUT EXCEEDED')
                return False, result

            return True, (elapsed, remaining)

        # PHASE 1: Drive Forward to Pickup Location
        self.get_logger().info('--- Phase 1: Driving to Pickup Location ---')
        phase1_start = time.time()
        while (time.time() - phase1_start) < pickup_duration:
            status, data = check_status()
            if not status:
                return data  # Returns result if canceled or aborted
            elapsed, remaining = data

            # Drive linear speed forward
            cmd = Twist()
            cmd.linear.x = float(speed)
            self.velocity_publisher.publish(cmd)

            # Feedback: Pickup progress scales 0% to 50% during Phase 1
            feedback_msg.remaining_time = remaining
            feedback_msg.pickup_progress = min(50.0, ((time.time() - phase1_start) / pickup_duration) * 50.0)
            goal_handle.publish_feedback(feedback_msg)

            time.sleep(sleep_duration)

        # PHASE 2: Stop and Simulate Pickup
        self.get_logger().info('--- Phase 2: Simulating Package Pickup ---')
        self._publish_stop()
        phase2_start = time.time()
        pickup_sim_duration = 3.0  # Pause duration to complete pickup action

        while (time.time() - phase2_start) < pickup_sim_duration:
            status, data = check_status()
            if not status:
                return data
            elapsed, remaining = data

            self._publish_stop()

            # Feedback: Pickup progress scales 50% to 100% during Phase 2
            pickup_pct = 50.0 + ((time.time() - phase2_start) / pickup_sim_duration) * 50.0
            feedback_msg.remaining_time = remaining
            feedback_msg.pickup_progress = min(100.0, pickup_pct)
            goal_handle.publish_feedback(feedback_msg)

            time.sleep(sleep_duration)

        feedback_msg.pickup_progress = 100.0

        # PHASE 3: Drive Forward to Delivery Location
        self.get_logger().info('--- Phase 3: Driving to Delivery Location ---')
        phase3_start = time.time()
        while (time.time() - phase3_start) < delivery_duration:
            status, data = check_status()
            if not status:
                return data
            elapsed, remaining = data

            # Drive linear speed forward
            cmd = Twist()
            cmd.linear.x = float(speed)
            self.velocity_publisher.publish(cmd)

            feedback_msg.remaining_time = remaining
            goal_handle.publish_feedback(feedback_msg)

            time.sleep(sleep_duration)

        # Mission Completion
        self._publish_stop()
        goal_handle.succeed()
        result.success = True
        result.message = f'Delivery completed successfully in {time.time() - start_time:.2f}s'
        self.mission_active = False
        self.get_logger().info('MISSION COMPLETED SUCCESSFULLY')
        return result

    def _publish_stop(self):
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0
        self.velocity_publisher.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    server = DeliveryMissionServer()

    try:
        rclpy.spin(server)
    except KeyboardInterrupt:
        pass
    finally:
        server.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()