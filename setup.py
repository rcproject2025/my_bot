from setuptools import setup

package_name = 'my_server'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/launch_sim.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rc-server',
    maintainer_email='rc-server@example.com',
    description='My ROS2 server package',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'odom_bridge = my_server.odom_bridge:main',
        ],
    },
)
