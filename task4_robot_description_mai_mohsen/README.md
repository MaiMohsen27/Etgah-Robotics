# robot_description (with Gazebo plugins)

A ROS 2 robot description package for a two-wheeled differential-drive
mobile robot, simulated in Gazebo and visualized in RViz2.

## Project Overview

This package defines the complete model of a simple two-wheeled mobile robot:
a rectangular chassis, two driven wheels, a passive front caster, 
and a LiDAR + camera mounted on top and up front. 
Every link has visual, collision, and inertial properties,
and the file is organized with reusable Xacro macros so the robot can
be resized or re-shaped by editing a small block of properties at the
top of `robot_description.urdf.xacro`, instead of touching every link by hand.

The package also includes a Gazebo simulation plugins,
a `ros_gz_bridge` config to expose sensor/actuator topics to ROS 2, and
launch files to bring everything up with a single command.

## Package Structure
```
robot_description_mai_mohsen/
├── CMakeLists.txt
├── package.xml
├── launch/
│ ├── display.launch.py # loads the robot + RViz
│ └── gazebo.launch.py # spawns the robot in Gazebo + bridge
├── urdf/
│ ├── robot_description.urdf.xacro # robot model (links, joints, macros)
│ └── robot_description.gazebo.xacro # Gazebo plugins (diff drive, sensors)
├── config/
│ └── gz_bridge.yaml # ros_gz_bridge topic mappings
├── meshes/
│ ├── lidar.STL
│ └── camera.stl
├── rviz/
│ └── robot_view.rviz
```
## 3. Linux Commands Used
| Command | Purpose |
|---|---|
| `cd ~/ros2_ws` | move into the workspace root |
| `colcon build` | build the package |
| `colcon build --packages-select robot_description_mai_mohsen` | build only this package |
| `source install/setup.bash` | source the workspace in any new terminal |

source Gazebo environment, if needed 

## 4. ROS 2 Commands Used
| Command | Purpose |
|---|---|
| `ros2 launch robot_description_mai_mohsen display.launch.py` | launch robot_state_publisher |
| `ros2 launch robot_description_mai_mohsen gazebo.launch.py` | launch Gazebo |
| `ros2 topic list` | list all active topics |
| `ros2 topic echo /odom` | inspect odometry data |
| `ros2 topic echo /scan` | inspect LiDAR scan data |
| `ros2 topic echo /scan --once` | inspect LiDAR scan data once |
| `ros2 run tf2_tools view_frames` | generate the TF tree PDF |
| `ros2 run teleop_twist_keyboard teleop_twist_keyboard` | drive the robot manually via keyboard |
| `rviz2` | launch RViz |

## How to Launch RViz
1. Build and source the workspace:
```bash
   cd ~/ros2_ws
   colcon build
   source install/setup.bash
```
2. Run `robot_state_publisher`:
```bash
   ros2 launch robot_description_mai_mohsen display.launch.py
```
or
```bash
   ros2 launch robot_description_mai_mohsen gazebo.launch.py
```
3. Run RViz:
```bash
   rviz2
```

## How to Launch Gazebo
1. Build and source the workspace (same as above).
2. Run:
```bash
   ros2 launch robot_description_mai_mohsen gazebo.launch.py
```
This will start Gazebo with the `turtlebot3_house.world` world.

## Expected Topics
| Topic | Type | Source |
|---|---|---|
| `/cmd_vel` | `geometry_msgs/msg/Twist` | input to DiffDrive plugin |
| `/odom` | `nav_msgs/msg/Odometry` | published by DiffDrive plugin |
| `/tf`, `/tf_static` | `tf2_msgs/msg/TFMessage` | robot_state_publisher + DiffDrive plugin |
| `/joint_states` | `sensor_msgs/msg/JointState` | JointStatePublisher plugin |
| `/scan` | `sensor_msgs/msg/LaserScan` | gpu_lidar sensor (`lidar_link`) |
| `/camera/image_raw` | `sensor_msgs/msg/Image` | camera sensor (`camera_link`) |
| `/robot_description` | `std_msgs/msg/String` | robot_state_publisher |

## How to Move the Robot
To move it manually:
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
Use the keys shown in the terminal (`i`/`,`/`j`/`l`/`k`) to send linear and
angular velocity commands. Alternatively, publish directly to move:
```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.2}, angular: {z: 0.0}}"
```
and to stop:
```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0}, angular: {z: 0.0}}"
```

## TF Tree Explanation
```
odom
└── base_footprint (published by the DiffDrive plugin, frame_id=odom, child_frame_id=base_footprint)
  └── base_link (fixed joint, from robot_state_publisher)
    ├── left_wheel_link
    ├── right_wheel_link
    ├── caster_wheel_link
    ├── lidar_link
    ├── imu #optional
    └── camera_link
```
you can add an imu link (static link) using this command:
```bash
  ros2 run tf2_ros static_transform_publisher \
  --x 0 \
  --y 0 \
  --z 0.08 \
  --roll 0 \
  --pitch 0 \
  --yaw 0 \
  --frame-id base_link \
  --child-frame-id imu_link
```

## Screenshots

<img width="627" height="472" alt="image" src="https://github.com/user-attachments/assets/a9a3a3c1-2679-47c2-84a6-cd224dce6311" />

<img width="1040" height="296" alt="image" src="https://github.com/user-attachments/assets/4056b4d6-9551-4519-8ea2-2af6b6206172" />

<img width="663" height="469" alt="image" src="https://github.com/user-attachments/assets/a21572d4-a0c9-4b84-b720-e4a47e72996e" />

<img width="631" height="480" alt="image" src="https://github.com/user-attachments/assets/227bf9bc-f7cf-47aa-9998-0c0253f38345" />

<img width="623" height="470" alt="image" src="https://github.com/user-attachments/assets/4a365952-a266-4bdf-acf2-9a45a91fe38f" />

<img width="1331" height="463" alt="image" src="https://github.com/user-attachments/assets/0197022e-f3d0-4779-99ef-ae6ae662de20" />

------
**Author**: Mai Mohsen

