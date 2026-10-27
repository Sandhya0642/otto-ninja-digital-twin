from glob import glob
import os
from setuptools import setup

package_name = 'otto_ninja_twin'
package_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(package_dir, '../../../'))

setup(
    name=package_name,
    version='0.2.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'mujoco'), glob(os.path.join(project_root, 'mujoco', '*.xml'))),
        (os.path.join('share', package_name, 'meshes'), glob(os.path.join(project_root, 'meshes', '*.stl'))),
        (os.path.join('share', package_name, 'urdf'), glob(os.path.join(project_root, 'urdf', '*.urdf'))),
    ],
    install_requires=['setuptools'],
    zip_safe=False,
    maintainer='OttoLab Thesis Project',
    maintainer_email='maintainer@example.com',
    description='Otto Ninja reconstructed humanoid model with MuJoCo physics and ROS 2 bridge.',
    license='CC-BY-SA-4.0',
    entry_points={
        'console_scripts': [
            'gait_command = otto_ninja_twin.gait_command:main',
            'servo_command = otto_ninja_twin.servo_command_node:main',
            'mujoco_bridge = otto_ninja_twin.mujoco_bridge:main',
        ],
    },
)
