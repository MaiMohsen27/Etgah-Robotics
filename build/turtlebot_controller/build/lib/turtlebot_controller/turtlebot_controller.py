#!/usr/bin/env python3
"""
turtlebot_controller.py
------------------------
This is the PUBLISHER node ("the remote control").

Job: read keyboard keys (W/A/S/D/Q) from the terminal and turn them into
geometry_msgs/Twist messages that get PUBLISHED on the /cmd_vel topic.
TurtleBot3 (or our subscriber node) listens to /cmd_vel and reacts.

Key mapping:
    W -> move forward
    S -> move backward
    A -> turn left (rotate in place)
    D -> turn right (rotate in place)
    Q -> stop the robot and exit the program
"""

import sys
import termios
import tty

import rclpy                                   # Core ROS 2 Python client library
from rclpy.node import Node                     # Base class for all ROS 2 nodes
from geometry_msgs.msg import Twist             # Message type used to command robot velocity


def get_key():
    """
    Reads a single keypress from the terminal WITHOUT requiring the user
    to press Enter afterwards.

    We temporarily switch the terminal into "raw" mode (tty.setraw) so that
    every key press is delivered to us immediately, then we always restore
    the terminal's original settings afterwards (even if something goes
    wrong) so the user's shell isn't left in a broken state.
    """
    fd = sys.stdin.fileno()                     # File descriptor for the terminal
    old_settings = termios.tcgetattr(fd)         # Save current terminal settings
    try:
        tty.setraw(fd)                          # Switch terminal to raw (no buffering/echo)
        key = sys.stdin.read(1)                 # Block until exactly one character is typed
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # Always restore terminal
    return key


class TurtlebotController(Node):
    """The publisher node itself."""

    def __init__(self):
        super().__init__('turtlebot_controller')   # Node name as it will appear in `ros2 node list`

        # Create a publisher:
        #   - message type: Twist
        #   - topic name:  /cmd_vel   (TurtleBot3's standard velocity command topic)
        #   - queue size:  10          (how many messages to buffer if the subscriber is slow)
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

        # Linear speed (m/s) used when moving forward/backward
        self.linear_speed = 0.2
        # Angular speed (rad/s) used when turning left/right in place
        self.angular_speed = 0.5

        self.get_logger().info('Turtlebot Controller started.')
        self.get_logger().info('Use W/A/S/D to move, Q to stop and quit.')

    def publish_twist(self, linear_x, angular_z):
        """
        Builds a Twist message with the requested velocities and publishes it.
        A Twist message has two parts:
            linear.x  -> forward/backward speed (m/s)
            angular.z -> rotation speed around the vertical axis (rad/s)
        We only ever use linear.x and angular.z here; the other 4 fields
        (linear.y, linear.z, angular.x, angular.y) stay at 0.0 since a
        ground robot like TurtleBot3 can't move sideways or fly.
        """
        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        self.publisher_.publish(msg)             # Send the message out on /cmd_vel

    def stop_robot(self):
        """Publishes a zero-velocity Twist so the robot stops moving."""
        self.publish_twist(0.0, 0.0)

    def run(self):
        """
        Main loop: keep reading keys and publishing the matching Twist
        message until the user presses 'q' to quit.
        """
        try:
            while rclpy.ok():                    # Keep going as long as ROS 2 is running
                key = get_key().lower()           # Read one key, normalize to lowercase

                if key == 'w':                    # Forward
                    self.publish_twist(self.linear_speed, 0.0)
                    self.get_logger().info('Forward')
                elif key == 's':                  # Backward
                    self.publish_twist(-self.linear_speed, 0.0)
                    self.get_logger().info('Backward')
                elif key == 'a':                  # Turn left (rotate in place)
                    self.publish_twist(0.0, self.angular_speed)
                    self.get_logger().info('Turn left')
                elif key == 'd':                  # Turn right (rotate in place)
                    self.publish_twist(0.0, -self.angular_speed)
                    self.get_logger().info('Turn right')
                elif key == 'q':                  # Quit: stop the robot first, then exit
                    self.stop_robot()
                    self.get_logger().info('Q pressed: stopping robot and exiting.')
                    break
                elif key == '\x03':                # Ctrl+C also stops and exits cleanly
                    self.stop_robot()
                    break
                # Any other key is simply ignored
        except Exception as e:
            self.get_logger().error(f'Error in controller loop: {e}')
        finally:
            self.stop_robot()                     # Safety: always stop the robot on exit


def main(args=None):
    rclpy.init(args=args)                         # Start up the ROS 2 Python client library
    node = TurtlebotController()                  # Create our node
    try:
        node.run()                                 # Run the keyboard-reading loop
    finally:
        node.destroy_node()                        # Clean up the node
        rclpy.shutdown()                            # Shut down ROS 2 client library


if __name__ == '__main__':
    main()
