import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.substitutions import FindPackageShare

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    OpaqueFunction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution


def launch_setup(context):
    gz_gui = LaunchConfiguration("gz_gui").perform(context)
    gz_headless_mode = LaunchConfiguration("gz_headless_mode").perform(context)
    gz_log_level = LaunchConfiguration("gz_log_level").perform(context)
    gz_world = LaunchConfiguration("gz_world").perform(context)

    gz_args = f"-r -v {gz_log_level} {gz_world}"
    if eval(gz_headless_mode):
        gz_args = "--headless-rendering -s " + gz_args
    if gz_gui:
        gz_args = f"--gui-config {gz_gui} " + gz_args

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare("ros_gz_sim"), "launch", "gz_sim.launch.py"])
        ),
        launch_arguments={"gz_args": gz_args, 'on_exit_shutdown': 'true'}.items()
    )

    return [gz_sim]


def generate_launch_description():
    declare_gz_gui = DeclareLaunchArgument(
        "gz_gui",
        default_value=PathJoinSubstitution(
            [FindPackageShare("husarion_gz_worlds"), "config", "teleop.config"]
        ),
        description="Run simulation with specific GUI layout.",
    )
    launch_file_dir = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'launch')
    ros_gz_sim = get_package_share_directory('ros_gz_sim')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    x_pose = LaunchConfiguration('x_pose', default='7.0')
    y_pose = LaunchConfiguration('y_pose', default='-6.0')

    declare_gz_headless_mode = DeclareLaunchArgument(
        "gz_headless_mode",
        default_value="False",
        description="Run the simulation in headless mode. Useful when a GUI is not needed or to reduce the amount of calculations.",
        choices=["True", "False"],
    )

    declare_gz_log_level = DeclareLaunchArgument(
        "gz_log_level",
        default_value="2",
        description="Adjust the level of console output.",
        choices=["0", "1", "2", "3", "4"],
    )

    declare_gz_world_arg = DeclareLaunchArgument(
        "gz_world",
        default_value=PathJoinSubstitution(
            [FindPackageShare("husarion_gz_worlds"), "worlds", "husarion_office.sdf"]
        ),
        description="Absolute path to SDF world file.",
    )
    spawn_turtlebot_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, 'spawn_turtlebot3.launch.py')
        ),
        launch_arguments={
            'x_pose': x_pose,
            'y_pose': y_pose,
        }.items()
    )

    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('turtlebot3_gazebo'),
                'launch',
                'robot_state_publisher.launch.py'
            )
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    return LaunchDescription(
        [
            declare_gz_gui,
            declare_gz_headless_mode,
            declare_gz_log_level,
            declare_gz_world_arg,
            robot_state_publisher_cmd,
            spawn_turtlebot_cmd,
            OpaqueFunction(function=launch_setup),
        ]
    )
