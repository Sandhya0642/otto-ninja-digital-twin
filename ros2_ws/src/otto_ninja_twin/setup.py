from setuptools import setup

package_name = 'otto_ninja_twin'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='OttoLab Thesis Project',
    maintainer_email='maintainer@example.com',
    description='Starter ROS 2 command publisher for Otto Ninja digital-twin experiments.',
    license='MIT',
    entry_points={
        'console_scripts': [
            'gait_command = otto_ninja_twin.gait_command:main',
        ],
    },
)