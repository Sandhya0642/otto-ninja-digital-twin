"""Seven-channel Otto Ninja command generator based on the public firmware timing.

This publishes servo-angle commands, not direct motor torques. The MuJoCo bridge
maps those angles to joint targets and wheel velocities. Hardware use requires
a separate, verified adapter and an emergency stop.
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int16MultiArray


def map_linear(value, in_min, in_max, out_min, out_max):
    return int(round((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min))


def clamp(value, low=0, high=180):
    return max(low, min(high, int(value)))


class ServoCommandNode(Node):
    def __init__(self):
        super().__init__('otto_ninja_servo_command')
        self.declare_parameter('mode', 'walk')  # walk or roll
        self.declare_parameter('joystick_x', 0)  # -100..100
        self.declare_parameter('joystick_y', 55) # -100..100; non-zero walks forward by default
        self.declare_parameter('left_arm_up', False)
        self.declare_parameter('right_arm_up', False)
        self.declare_parameter('head_degrees', 90)
        self.declare_parameter('left_forward_speed', 20)
        self.declare_parameter('right_forward_speed', 20)
        self.declare_parameter('left_backward_speed', 20)
        self.declare_parameter('right_backward_speed', 20)
        self.publisher = self.create_publisher(Int16MultiArray, '/otto_ninja/servo_degrees', 10)
        self.start_ns = self.get_clock().now().nanoseconds
        self.timer = self.create_timer(0.02, self.tick)
        self.get_logger().info(
            'Publishing firmware-inspired seven-servo commands. Set joystick_y=0 for idle.'
        )

    def tick(self):
        mode = str(self.get_parameter('mode').value).lower()
        x = max(-100, min(100, int(self.get_parameter('joystick_x').value)))
        y = max(-100, min(100, int(self.get_parameter('joystick_y').value)))
        left_arm = 90 if bool(self.get_parameter('left_arm_up').value) else 180
        right_arm = 90 if bool(self.get_parameter('right_arm_up').value) else 0
        head = clamp(self.get_parameter('head_degrees').value)
        # Firmware neutral/home positions.
        left_foot, left_leg, right_foot, right_leg = 90, 60, 90, 120

        if mode == 'roll':
            # Direct mapping from the public OttoNinja joystick firmware.
            left_wheel_speed = map_linear(y, 100, -100, 135, 45)
            right_wheel_speed = map_linear(y, 100, -100, 45, 135)
            left_wheel_direction = map_linear(x, 100, -100, 45, 0)
            right_wheel_direction = map_linear(x, 100, -100, 0, -45)
            left_foot = clamp(left_wheel_speed + left_wheel_direction)
            right_foot = clamp(right_wheel_speed + right_wheel_direction)
            # Roll posture from firmware: legs to the side, arms remain in home/down pose.
            left_leg, right_leg = 180, 0
        elif y > 10 or y < -10:
            # Match the firmware's staggered leg/foot phases and joystick-dependent intervals.
            lt = map_linear(x, 100, -100, 200, 700)
            rt = map_linear(x, 100, -100, 700, 200)
            i1 = 250
            i2 = i1 + rt
            i3 = i2 + 250
            i4 = i3 + lt
            i5 = i4 + 50
            elapsed_ms = (self.get_clock().now().nanoseconds - self.start_ns) / 1e6
            phase = elapsed_ms % i5
            if y > 0:
                if phase < i1:
                    left_leg, right_leg = 5, 80  # LATR, RATR
                elif phase < i2:
                    right_foot = clamp(90 - int(self.get_parameter('right_forward_speed').value))
                elif phase < i3:
                    left_leg, right_leg = 100, 175  # LATL, RATL
                elif phase < i4:
                    left_foot = clamp(90 + int(self.get_parameter('left_forward_speed').value))
            else:
                if phase < i1:
                    left_leg, right_leg = 5, 80
                elif phase < i2:
                    right_foot = clamp(90 + int(self.get_parameter('right_backward_speed').value))
                elif phase < i3:
                    left_leg, right_leg = 100, 175
                elif phase < i4:
                    left_foot = clamp(90 - int(self.get_parameter('left_backward_speed').value))
        # Firmware button A/B moves arms up to 90 degrees, otherwise down at 180/0.
        msg = Int16MultiArray()
        msg.data = [left_foot, left_leg, right_foot, right_leg, left_arm, right_arm, head]
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ServoCommandNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
