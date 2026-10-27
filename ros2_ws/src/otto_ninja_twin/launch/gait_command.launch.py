from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='otto_ninja_twin',
            executable='gait_command',
            name='otto_ninja_gait_command',
            output='screen',
            parameters=[{'frequency_hz': 1.2, 'amplitude_rad': 0.25}],
        )
    ])