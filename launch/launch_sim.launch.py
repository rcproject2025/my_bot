import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    package_name = 'my_server'
    robot_name = 'my_bot' # Make sure this matches '-entity' in the spawn node
    world_name = 'empty'  # Make sure this matches your Gazebo world (e.g., 'empty.sdf' -> 'empty')

    # Robot State Publisher (and RViz2)
    rsp_launch_path = os.path.join(get_package_share_directory(package_name), 'launch', 'rsp.launch.py')
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(rsp_launch_path),
        launch_arguments={'use_sim_time': 'true'}.items()
    )
    gz_bridge_params_path = os.path.join(
        get_package_share_directory(package_name),
        'config',
        'gz_bridge.yaml'
    )
    # Start Gazebo (ros_gz_sim)
    gazebo_launch_path = os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_path),
        launch_arguments={'gz_args': f'-r {world_name}.sdf'}.items()
    )

    # Spawn robot from /robot_description
    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description', '-entity', robot_name, '-z', '0.5'],
        output='screen'
    )


    gz_bridge_node = Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '--ros-args', '-p',
                f'config_file:={gz_bridge_params_path}'
            ],
            output='screen'
        )
    return LaunchDescription([rsp, gazebo, spawn, gz_bridge_node])