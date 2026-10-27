"""MuJoCo physics viewer + ROS 2 servo-command subscriber.

Topic /otto_ninja/servo_degrees uses seven integer servo positions in degrees:
[left foot, left leg, right foot, right leg, left arm, right arm, head].
The foot channels are continuous-rotation servos: 90 degrees means neutral;
commands above/below 90 map to wheel angular velocity. This conversion is an
initial calibration hypothesis and must be measured on the user's actual robot.
"""
import os
import time
import math

import mujoco
import mujoco.viewer
import rclpy
from ament_index_python.packages import get_package_share_directory
from rclpy.node import Node
from std_msgs.msg import Int16MultiArray


def clamp(value, low, high):
    return max(low, min(high, value))


class MuJoCoBridge(Node):
    def __init__(self):
        super().__init__('otto_ninja_mujoco_bridge')
        self.declare_parameter('model_path', '')
        custom_path = str(self.get_parameter('model_path').value)
        if custom_path:
            model_path = custom_path
        else:
            share = get_package_share_directory('otto_ninja_twin')
            model_path = os.path.join(share, 'mujoco', 'otto_ninja_humanoid.xml')
        self.model = mujoco.MjModel.from_xml_path(model_path)
        self.data = mujoco.MjData(self.model)
        self.command = [90, 60, 90, 120, 180, 0, 90]
        self.last_command_time = time.monotonic()
        self.timeout_s = 0.75
        self.sub = self.create_subscription(
            Int16MultiArray, '/otto_ninja/servo_degrees', self.on_command, 10
        )
        self.actuator_ids = {
            name: mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_ACTUATOR, name)
            for name in (
                'left_foot_servo', 'left_leg_servo', 'right_foot_servo',
                'right_leg_servo', 'left_arm_servo', 'right_arm_servo', 'head_servo'
            )
        }
        missing = [name for name, idx in self.actuator_ids.items() if idx < 0]
        if missing:
            raise RuntimeError(f'Missing MuJoCo actuators: {missing}')
        self.get_logger().info(f'Loaded MuJoCo model: {model_path}')
        self.get_logger().info(
            'Waiting for seven servo-degree commands on /otto_ninja/servo_degrees. '
            'Open the MuJoCo viewer to inspect physical contacts and motion.'
        )

    def on_command(self, msg):
        if len(msg.data) != 7:
            self.get_logger().warning(
                f'Ignoring command with {len(msg.data)} values; expected 7 servo degrees.'
            )
            return
        vals = [int(v) for v in msg.data]
        if any(v < 0 or v > 180 for v in vals):
            self.get_logger().warning('Ignoring servo command outside 0..180 degrees.')
            return
        self.command = vals
        self.last_command_time = time.monotonic()

    def apply_commands(self):
        lf, ll, rf, rl, la, ra, head = self.command
        # Continuous-rotation servo approximation: neutral 90, +/-45 deg -> +/-8 rad/s.
        # Right foot is inverted to account for mirrored mounting in the reconstruction.
        values = {
            'left_foot_servo': clamp((lf - 90.0) * 8.0 / 45.0, -8.0, 8.0),
            'left_leg_servo': clamp(math.radians(ll - 60.0), -1.40, 1.40),
            'right_foot_servo': clamp(-(rf - 90.0) * 8.0 / 45.0, -8.0, 8.0),
            'right_leg_servo': clamp(-math.radians(rl - 120.0), -1.40, 1.40),
            'left_arm_servo': clamp(math.radians(180.0 - la), -1.5708, 1.5708),
            'right_arm_servo': clamp(math.radians(ra), -1.5708, 1.5708),
            'head_servo': clamp(math.radians(head - 90.0), -1.5708, 1.5708),
        }
        # Watchdog: if commands stop arriving, stop the wheel channels and hold a neutral stance.
        if time.monotonic() - self.last_command_time > self.timeout_s:
            values['left_foot_servo'] = 0.0
            values['right_foot_servo'] = 0.0
        for name, value in values.items():
            self.data.ctrl[self.actuator_ids[name]] = value

    def run_viewer(self):
        with mujoco.viewer.launch_passive(self.model, self.data) as viewer:
            while viewer.is_running() and rclpy.ok():
                rclpy.spin_once(self, timeout_sec=0.001)
                self.apply_commands()
                # Viewer frame rate is lower than simulation rate; step physics at model timestep.
                for _ in range(5):
                    mujoco.mj_step(self.model, self.data)
                viewer.sync()
                time.sleep(0.008)


def main(args=None):
    rclpy.init(args=args)
    node = MuJoCoBridge()
    try:
        node.run_viewer()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
