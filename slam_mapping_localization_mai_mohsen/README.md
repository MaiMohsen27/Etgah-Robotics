# slam_mapping_localization

A ROS 2 package demonstrating SLAM-based mapping and localization using **slam_toolbox** in a TurtleBot3 simulation environment.

---

## Step-by-Step Setup Instructions

1. make a ROS 2 workspace with a `src` file in it.
   ```bash
   mkdir -p ros2_ws/src
   ```
   
2.  **Clone the repository** into your ROS 2 workspace `src` folder:
   ```bash
   cd ~/ros2_ws/src
   git clone https://github.com/MaiMohsen27/slam_mapping_localization_mai_mohsen.git
   ```

3. **Build the package:**
   ```bash
   cd ~/ros2_ws
   colcon build --packages-select slam_toolbox_demo
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

## How to Test the Nodes

### 1. Mapping Mode
- Run SLAM to build a new map while driving the robot around:
```bash
source ~/workspaces/ros2_ws/install/setup.bash
ros2 launch slam_toolbox_demo slam_toolbox_online_async.launch.py
```
- Open RViz2:
```bash
rviz2
```
Set:
Fixed Frame = map

add:
TF
RobotModel
LaserScan #by topic
Map #by topic

- Drive the robot using teleop:
```bash
ros2 run turtlebot3_teleop teleop_keyboard
```

- Once the map looks complete, save it:
```bash
ros2 run nav2_map_server map_saver_cli -f turtlebot3_world_map
```

### 2. Localization Mode
- Run SLAM in localization mode using the previously saved map:
```bash
source ~/workspaces/ros2_ws/install/setup.bash
ros2 launch slam_toolbox_demo localization.launch.py
```
- Open RViz2:
```bash
rviz2
```
Set:
Fixed Frame = map

add:
TF
RobotModel
LaserScan #by topic
Map #by topic
MarkerArray #under graph_visualization
- Click the 2D Pose Estimate from the RViz toolbar and explore the map behavior point the arrow in different directions.
- Drive the robot using teleop:
```bash
ros2 run turtlebot3_teleop teleop_keyboard
```
- Check Odometry:
  ```bash
  ros2 topic echo /odom --once
  ```
---

## Expected Output

- **Mapping mode:** RViz2 displays a live-growing occupancy grid map as the robot explores the environment. Laser scan data aligns correctly with the map walls.
- **Localization mode:** RViz2 shows the pre-built map with the robot's estimated pose (particle cloud / pose arrow) tracking its real position as it moves.
- **Checking /odom:**
  a valid reading should look like this:
  ```
  header:
    stamp:
      sec: 3772
      nanosec: 440000000
    frame_id: odom
  child_frame_id: base_footprint
  pose:
    pose:
      position:
        x: 2.526625771953703
        y: 0.6923273744830754
        z: 0.0
      orientation:
        x: 0.0
        y: 0.0
        z: 0.7679761682596985
        w: 0.6404784188285748
  ```
---

## Demos and Screenshots

- Mapping Demo:
```
https://youtu.be/tGTdXOdIYr8
```
- TF tree:
  <img width="863" height="511" alt="image" src="https://github.com/user-attachments/assets/c3cdc0da-3053-4a4f-bb72-79874669da16" />

- Localiztion Demo:
  showing 2 wrong poses and 1 right pose.
```
https://youtu.be/dhuqXOlwx2M
```
- One Wrong Pose:
  <img width="1279" height="575" alt="image" src="https://github.com/user-attachments/assets/ba7f5a95-d4d5-4339-93f6-0ecf1c4559ef" />

  The map changes when you choose a position the robot is not facing.
  
- One Right Pose:
   <img width="1267" height="567" alt="image" src="https://github.com/user-attachments/assets/ed66c3b5-a63e-43a7-9fff-0ceaffd8ab71" />

   The map doesn't change or grow, only the pose updates.

- Moving Robot in Localization Mode Demo:
```
https://youtu.be/etjLBbbCOrk
```
---

**Author**: Mai Mohsen
