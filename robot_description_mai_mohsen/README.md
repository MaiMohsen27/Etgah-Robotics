# robot_description

A ROS 2 robot description package for a two-wheeled differential-drive
mobile robot.

## Project Overview

This package defines the complete model of a simple two-wheeled mobile robot:
a rectangular chassis, two driven wheels, a passive front caster, 
and a LiDAR + camera mounted on top and up front. 
Every link has visual, collision, and inertial properties,
and the file is organized with reusable Xacro macros so the robot can
be resized or re-shaped by editing a small block of properties at the
top of `robot_description.urdf.xacro`, instead of touching every link by hand.

## Robot Structure

```
base_footprint                (on the ground plane)
└── base_link                 (chassis box)
    ├── left_wheel_link        (continuous joint)
    ├── right_wheel_link       (continuous joint)
    ├── caster_wheel_link       (fixed joint)
    ├── lidar_link              (fixed joint)
    └── camera_link             (fixed joint)
```

## Folder Structure

```
robot_description_mai-mohsen/
├── CMakeLists.txt
├── package.xml
├── README.md
├── urdf/
│   ├── robot_description.urdf.xacro        
├── meshes/
│   ├── lidar.STL                
│   └── camera.stl                
```

## How to Preview the Robot

### VS Code URDF Visualizer extension

1. Place this package inside your ROS 2 workspace, e.g.
   `~/ros2_ws/src/robot_description`.
2. build your workspace
   `colcon build`.
3. source the workspace
   `source install/setup.bash`.
4. Open the workspace folder in VS Code and make sure the **URDF
   Visualizer** extension is installed.
5. Open `urdf/robot_description.urdf.xacro`.
6. Run the command **"Preview URDF"** (Ctrl+Shift+P → *URDF Visualizer:
   Preview*) with this file active.
7. Confirm every link appears, all joints connect correctly, and the
   LiDAR/camera meshes render in the right place.

## Screenshot
<img width="648" height="357" alt="image" src="https://github.com/user-attachments/assets/84c51bce-5d5c-4218-8089-c9428ed1dea4" />

<img width="659" height="362" alt="image" src="https://github.com/user-attachments/assets/0ee32c41-45d8-4a1f-b102-f89d0293a57d" />

<img width="652" height="362" alt="image" src="https://github.com/user-attachments/assets/9536e6e0-582f-45ba-a43b-d5273574352b" />

------
**Author**: Mai Mohsen
