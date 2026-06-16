from setuptools import setup, find_packages

package_name = 'rover_sim'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/robot_launch.py']),
        ('share/' + package_name + '/worlds', ['worlds/my_world.wbt']),
        ('share/' + package_name + '/resource', ['resource/my_robot.urdf']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dronv',
    maintainer_email='dronv@todo.todo',
    description='Rover simulation package',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'rover_driver = rover_sim.rover_driver:main',
            'obstacle_avoider = rover_sim.obstacle_avoider:main',
            'odometry = rover_sim.odometry:main'
        ],
    },
)