"""Example ROS 2 publisher for a simple alternating gait command.

This is a command-generation scaffold only. It does not communicate with MuJoCo
or a physical servo controller until an explicit bridge is implemented.
"""
import math

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray


class GaitCommand(Node):
    def __init__(self):
        super().__init__('otto_ninja_gait_command')
        self.declare_parameter('frequency_hz', 1.2)
        self.declare_parameter('amplitude_rad', 0.25)
        self.declare_parameter('topic', '/otto_ninja/joint_command')
        self.frequency = float(self.get_parameter('frequency_hz').value)
        self.amplitude = float(self.get_parameter('amplitude_rad').value)
        topic = str(self.get_parameter('topic').value)
        self.publisher = self.create_publisher(Float64MultiArray, topic, 10)
        self.phase = 0.0
        self.dt = 0.02
        self.timer = self.create_timer(self.dt, self.publish_command)
        self.get_logger().info(
            f'Publishing example gait to {topic}; f={self.frequency:.2f} Hz, '
            f'amplitude={self.amplitude:.2f} rad. No hardware bridge is active.'
        )

    def publish_command(self):
        self.phase += 2.0 * math.pi * self.frequency * self.dt
        msg = Float64MultiArray()
        # Order: left hip, left knee, right hip, right knee (illustrative only).
        msg.data = [
            self.amplitude * math.sin(self.phase),
            max(0.0, -0.35 * math.sin(self.phase)),
            self.amplitude * math.sin(self.phase + math.pi),
            max(0.0, -0.35 * math.sin(self.phase + math.pi)),
        ]
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = GaitCommand()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()