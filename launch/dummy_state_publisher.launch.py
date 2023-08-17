import os
import xacro
import yaml
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    robot_description_config = xacro.process_file(os.path.join(get_package_share_directory('robotiq_140_description'), 'urdf', 'robotiq_140_gripper_instance.urdf.xacro'))
    robot_description = {'robot_description': robot_description_config.toxml()}


    joint_state_pub_gui_node = Node(
                                package='joint_state_publisher_gui',
                                executable='joint_state_publisher_gui',
                                name='joint_state_publisher_gui',
                                remappings=[("/joint_states", "/gripper/joint_states"),
                                            ("/robot_description", "/gripper_description")],
                                parameters=[robot_description],
                                )


    robot_state_pub_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        remappings=[("/joint_states", "/gripper/joint_states"),
                    ("/robot_description", "/gripper_description")],
        parameters=[robot_description]
    )

    return LaunchDescription([joint_state_pub_gui_node, robot_state_pub_node])
