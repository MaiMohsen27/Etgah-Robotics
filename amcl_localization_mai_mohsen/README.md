# AMCL Localization

A ROS 2 package demonstrating AMCL (Adaptive Monte Carlo Localization) using a previously saved map in a TurtleBot3 simulation environment (TurtleBot3 World)

---

## Project Overview

This project implements robot localization using **AMCL** on a map generated in a [previous SLAM assignment](https://github.com/MaiMohsen27/Etgah-Robotics/tree/main/slam_mapping_localization_mai_mohsen). The robot is launched in the Gazebo simulation, the saved map in RViz2, and AMCL estimates the robot's pose using LiDAR scan matching against the map.

The workflow demonstrates:
- Loading a previously saved map and confirming it displays correctly in RViz.
- Configuring and launching `amcl`.
- Testing localization with a wrong initial pose vs. the correct initial pose.
- Driving the robot and confirming the particle cloud converges and localization remains stable.

---

## Package Structure

```
amcl_localization_mai_mohsen/
└── robot_localization/
    ├── config/
    │   └── amcl.yaml
    ├── launch/
    │   └── amcl.launch.py
    ├── map/
    │   ├── turtlebot3_world_map.yaml
    │   └── turtlebot3_world_map.pgm
    ├── CMakeLists.txt
    └── package.xml
├── images/
└── README.md
```

- **config/amcl.yaml** — AMCL parameter configuration.
- **launch/amcl.launch.py** — Launch file that starts `map_server`, `amcl`, and `lifecycle_manager`.
- **map/** — Map files (`.yaml` + `.pgm`) generated in the previous SLAM assignment.
- **images/** — Screenshots and videos used in this README.

---

## Build Instructions

1. **Create a ROS 2 workspace** with a `src` folder in it.
   ```bash
   mkdir -p ros2_ws/src
   ```
   
2.  **Clone the repository** into your ROS 2 workspace `src` folder:
    ```bash
    cd ~/ros2_ws/src
    git clone https://github.com/MaiMohsen27/amcl_localization_mai_mohsen.git
    ```

3. **Build the package:**
   ```bash
   cd ~/ros2_ws
   colcon build --packages-select robot_localization
   source install/setup.bash
   ```

4. **Set the TurtleBot3 model** (add to `~/.bashrc` if needed):
   ```bash
   export TURTLEBOT3_MODEL=burger
   ```

5. **Launch the Gazebo simulation:**
   ```bash
   ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
   ```

---

## Commands Used to Launch the Simulator and AMCL

1. **Launch the Gazebo simulation:**
   In a terminal:
   ```bash
   ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
   ```

2. **Launch map_server, AMCL, and lifecycle_manager:**
   In a second terminal:
   ```bash
   source ~/ros2_ws/install/setup.bash
   ros2 launch robot_navigation amcl.launch.py
   ```
3. **Launch RViz:**
   In a third terminal:
   ```bash
   source ~/ros2_ws/install/setup.bash
   rviz2
   ```

---

## RViz Configuration
After opening RViz:

1. Set **Fixed Frame** to `map`.
2. Add **map**:
  Under QoS Settings, set:
 ```
  Durability Policy = Transient Local
 ```
 3. Add **TF**
 4. Add **RobotModel**:
   Under Description_model, choose:
   ```
   /robot_description
   ```
 5. Add **LaserScan**
 6. Add **ParticleCloud**:
   Set its topic to:
   ```
   /particle_cloud
   ```
   Under QoS Settings, set:
   ```
   Reliability Policy = Best Effort
   ```

### Testing Steps
1. Give the robot a **wrong initial pose**:
   - Using the 2D Pose Estimate tool, click on the map where the robot is located.
   - Then, hold and drag the arrow in a direction other than the one the robot is facing.
   - Now, observe the mismatch between the LiDAR scan and the saved map. It should look similar to the following picture:
     
   <img width="1920" height="692" alt="image" src="https://github.com/user-attachments/assets/b95f6241-64d2-43a2-8d67-69b78270c519" />

   [Watch the demo video](https://github.com/MaiMohsen27/Etgah-Robotics/blob/main/amcl_localization_mai_mohsen/src/images/wrong_and_right_initial_poses.mp4)

   **Observation:** With the wrong initial pose, the LiDAR scan mismatches with the walls of the saved map, and the particle cloud is highly scattered around the     robot's actual location.
   
2. Give the robot the **correct initial pose**:
   Follow the previous step, but point the arrow in the direction the robot is facing, and observe the LiDAR scan align with the map.
   It should look the same as the following picture:

   <img width="1918" height="696" alt="image" src="https://github.com/user-attachments/assets/cc074b78-9d02-48fb-a305-0886f3465756" />

   [Watch the demo video](https://github.com/MaiMohsen27/Etgah-Robotics/blob/main/amcl_localization_mai_mohsen/src/images/wrong_and_right_initial_poses.mp4)

   **Observation:** With the correct initial pose, the LiDAR scan lines up closely with the walls of the saved map, and the particle cloud is tightly clustered       around the robot's actual location.
   
3. Drive the robot with teleop and observe the particle cloud converge around the robot's true pose:
   ```bash
   ros2 run turtlebot3_teleop teleop_keyboard
   ```

   <img width="803" height="528" alt="image" src="https://github.com/user-attachments/assets/c2f82194-321a-472b-88e0-b4c18e25310d" />

   The particles should gradually converge around the robot’s correct position.

   [Watch the demo video](https://github.com/MaiMohsen27/Etgah-Robotics/blob/main/amcl_localization_mai_mohsen/src/images/moving_robot_in_the_map.mp4)

   **Observation:** As the robot moves, the particle cloud converges further, narrowing around the estimated pose, indicating AMCL is successfully tracking the       robot's position.
---

## TF Tree 
Check the Tf tree:
```bash
ros2 run tf2_tools view_frames
```
It should look the same as the following picture:

<img width="908" height="534" alt="image" src="https://github.com/user-attachments/assets/888b08a9-7800-42a7-8119-bede264a9ec0" />

**Observation:** The TF tree confirms the expected chain: `map → odom → base_footprint → base_link → ...`, with AMCL publishing the `map → odom` transform.

---

## Required Topic and Transform Outputs

- **Confirm `/scan` and `/odom` are available:**
  ```bash
  ros2 topic list
  ```

- **Confirm `/amcl_pose` updates while the robot moves:**
  ```bash
  ros2 topic echo /amcl_pose --once
  ```
  The output should look like this:
  ```
  header:
  stamp:
    sec: 1250
    nanosec: 800000000
  frame_id: map
  pose:
    pose:
      position:
        x: 3.773375913378755
        y: 1.1328219577562595
        z: 0.0
      orientation:
        x: 0.0
        y: 0.0
        z: 0.6656036218678322
        w: 0.7463054458842062
  ```
- **Confirm AMCL publishes the `map → odom` transform:**
  ```bash
  ros2 run tf2_ros tf2_echo map odom
  ```
  Expected output:
  ```
   Translation: [-2.072, -0.518, 0.000]
  - Rotation: in Quaternion (xyzw) [0.000, 0.000, 0.022, 1.000]
  - Rotation: in RPY (radian) [0.000, -0.000, 0.044]
  - Rotation: in RPY (degree) [0.000, -0.000, 2.497]
  - Matrix:
    0.999 -0.044  0.000 -2.072
    0.044  0.999  0.000 -0.518
    0.000  0.000  1.000  0.000
    0.000  0.000  0.000  1.000
  ```
- **Check the Map topic**:
  ```bash
  ros2 topic info -v /map
  ```
  Expected output:
  ```
  Type: nav_msgs/msg/OccupancyGrid

  Publisher count: 1
  
  Node name: map_server
  Node namespace: /
  Topic type: nav_msgs/msg/OccupancyGrid
  
  Subscription count: 1
  
  Node name: amcl
  Node namespace: /
  Topic type: nav_msgs/msg/OccupancyGrid
  ```
- **Check the Estimated Pose**:
  ```bash
  ros2 topic info -v /amcl_pose
  ```
  Expected output:
  ```
  root@ip-172-31-17-30:~/workspaces# ros2 topic info -v /amcl_pose
  Type: geometry_msgs/msg/PoseWithCovarianceStamped
  
  Publisher count: 1
  
  Node name: amcl
  ```
- **Check the Particle Cloud**:
  ```bash
  ros2 topic info -v /particle_cloud
  ```
  Expected output:
  ```
  Type: nav2_msgs/msg/ParticleCloud

  Publisher count: 1
  
  Node name: amcl
  
  Subscription count: 1
  
  Node name: rviz

  ```
---

## Common Problems Faced and How They Were Solved



---

**Author**: Mai Mohsen

