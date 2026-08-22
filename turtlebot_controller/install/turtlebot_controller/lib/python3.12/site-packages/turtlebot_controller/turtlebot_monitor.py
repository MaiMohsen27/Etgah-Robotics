#!/usr/bin/env python3
"""
turtlebot_monitor.py
---------------------
This is the SUBSCRIBER node ("the dashboard").

Job: listen to the /cmd_vel topic (the same topic turtlebot_controller.py
publishes to) and print, in real time, what command is currently being
sent to the robot -- i.e. its forward/backward speed and turning speed.
"""

import rclpy                                    # Core ROS 2 Python client library
from rclpy.node import Node                      # Base class for all ROS 2 nodes
from geometry_msgs.msg import Twist              # Same message type the publisher sends


class TurtlebotMonitor(Node):
    """The subscriber node itself."""

    def __init__(self):
        super().__init__('turtlebot_monitor')     # Node name shown in `ros2 node list`

        # Create a subscription:
        #   - message type: Twist
        #   - topic name:  /cmd_vel        (must match the publisher's topic exactly)
        #   - callback:    self.listener_callback  (called every time a message arrives)
        #   - queue size:  10
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.listener_callback,
            10
        )
        self.subscription  # prevent "unused variable" warning from linters

        self.get_logger().info('Turtlebot Monitor started. Listening on /cmd_vel ...')

    def listener_callback(self, msg):
        """
        This function is called AUTOMATICALLY by ROS 2 every time a new
        Twist message is published on /cmd_vel. We don't call it ourselves.
        """
        linear_x = msg.linear.x                  # Forward(+) / backward(-) speed in m/s
        angular_z = msg.angular.z                # Turning speed in rad/s (+ left, - right)

        # Turn the raw numbers into a human-readable description
        if linear_x > 0.0:
            motion = 'Moving FORWARD'
        elif linear_x < 0.0:
            motion = 'Moving BACKWARD'
        elif angular_z > 0.0:
            motion = 'Turning LEFT'
        elif angular_z < 0.0:
            motion = 'Turning RIGHT'
        else:
            motion = 'STOPPED'

        self.get_logger().info(
            f'{motion} | linear.x={linear_x:.2f} m/s, angular.z={angular_z:.2f} rad/s'
        )


def main(args=None):
    rclpy.init(args=args)                        # Start up the ROS 2 Python client library
    node = TurtlebotMonitor()                     # Create our node
    try:
        rclpy.spin(node)                          # Keep the node alive, waiting for messages
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()                       # Clean up the node
        rclpy.shutdown()                           # Shut down ROS 2 client library


if __name__ == '__main__':
    main()
