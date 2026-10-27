from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    mode = LaunchConfiguration('mode')
    joystick_x = LaunchConfiguration('joystick_x')
    joystick_y = LaunchConfiguration('joystick_y')
    return LaunchDescription([
        DeclareLaunchArgument('mode', default_value='walk',
                              description='Robot motion mode: walk or roll'),
        DeclareLaunchArgument('joystick_x', default_value='0',
                              description='Joystick X input in range -100..100'),
        DeclareLaunchArgument('joystick_y', default_value='55',
                              description='Joystick Y input in range -100..100; use 0 for idle in walk mode'),
        Node(
            package='otto_ninja_twin',
            executable='mujoco_bridge',
            name='otto_ninja_mujoco_bridge',
            output='screen',
        ),
        Node(
            package='otto_ninja_twin',
            executable='servo_command',
            name='otto_ninja_servo_command',
            output='screen',
            parameters=[{
                'mode': mode,
                'joystick_x': joystick_x,
                'joystick_y': joystick_y,
            }],
        ),
    ])
