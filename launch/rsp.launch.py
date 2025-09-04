from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
import xacro


def generate_launch_description():
    # Launch argument for sim time
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Process the URDF/Xacro
    pkg_path = get_package_share_directory('my_server')   # replace with your package name
    xacro_file = os.path.join(pkg_path, 'description', 'robot.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)

    # Params for robot_state_publisher
    params = {
        'robot_description': robot_description_config.toxml(),
        'use_sim_time': use_sim_time
    }

    # Robot State Publisher
    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    # RViz2
    rviz =Node(
    package='rviz2',
    executable='rviz2',
    name='rviz2',
    output='screen',
    parameters=[params]
)


    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'
        ),
        rsp,
        rviz,  # Removed joint_state_publisher
    ])
