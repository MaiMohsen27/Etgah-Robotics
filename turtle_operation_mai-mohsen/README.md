# Obstacle-Avoiding TurtleBot3 with Override Capability

A ROS 2 workspace with two packages that work together:

| Package | Type |
|---|---|
| `obstacle_direction_interfaces` | `ament_cmake` |
| `obstacle_direction_controller` | `ament_python` |

## 1. Step-by-Step Setup Instructions

1. **Create ROS 2 workspace**
   ```bash
   mkdir -p ~/ros2_ws/src
   cd ~/ros2_ws/src
   ```

2. **Copy the two packages into the workspace's `src/` folder**
   The paths should look like:
   ```
   ~/rps2_ws/src/obstacle_direction_controller
   ~/ros2_ws/src/obstacle_direction_interfaces
   ```

3. **Build the packages**
build the package inside the workspace folder
   ```bash
   cd ~/ros2_ws
   colcon build 
   ```

4. **Source the workspace** (do this in every new terminal you open)
   ```bash
   source install/setup.bash
   ````

---

## 2. Every ROS 2 Command Used (and what it does)

| Command | What it does |
|---|---|
| `colcon build --packages-select <package name>` | Compiles/installs only this package (faster than rebuilding the whole workspace). |
| `ros2 run obstacle_direction_controller obstacle_autopilot` | Runs the `obstacle_autopilot` node. |
| `ros2 service call /set_direction obstacle_direction_interfaces/srv/SetDirection "{direction: '<direction>'}"` | Overrides the robot motion from terminal. |

---

## 3. How to Test Your Nodes

1. **Turn on your simulation (I used Turtlebot3 - Burger model)**

2. **Terminal 1: 
   ```bash
   source install/setup.bash
   colcon build
   ros2 run obstacle_direction_controller obstacle_autopilot
   ```

3. **Terminal 2: **Override the robot**
   ```bash
   source install/setup.bash
   
   ros2 service call /set_direction obstacle_direction_interfaces/srv/SetDirection "{direction: 'left'}"
   ros2 service call /set_direction obstacle_direction_interfaces/srv/SetDirection "{direction: 'forward'}"
   ros2 service call /set_direction obstacle_direction_interfaces/srv/SetDirection "{direction: 'reverse'}"
   ros2 service call /set_direction obstacle_direction_interfaces/srv/SetDirection "{direction: 'right'}"
   ```
   An invalid direction (e.g. `"sideways"`) returns `success: false` with an explanatory message and does not affect the robot's motion.

---

## 4. Expected Output

**In the first terminal**, you should see log lines like:
```
[WARN] [1787938682.859136231] [direction_autopilot_node]: OVERRIDE ACTIVE: driving 'left'
[INFO] [1787938683.059204454] [direction_autopilot_node]: F:0.53m | L:0.70m | R:0.62m | MODE:OVERRIDE
[WARN] [1787938683.059817041] [direction_autopilot_node]: OVERRIDE ACTIVE: driving 'left'
[INFO] [1787938683.258391292] [direction_autopilot_node]: F:0.52m | L:0.72m | R:1.46m | MODE:OVERRIDE
[INFO] [1787938683.258844955] [direction_autopilot_node]: Override hold time elapsed. Resuming autonomous control.
[INFO] [1787938683.259218395] [direction_autopilot_node]: ACTION: FORWARD
[INFO] [1787938683.458092935] [direction_autopilot_node]: F:0.49m | L:0.70m | R:1.45m | MODE:AUTONOMOUS
[WARN] [1787938683.458583841] [direction_autopilot_node]: OBSTACLE: Front 0.49m <= 0.50m, switching to TURN state

```

**In the second terminal**, you should see log lines like:
```
waiting for service to become available...
requester: making request: obstacle_direction_interfaces.srv.SetDirection_Request(direction='left')

response:
obstacle_direction_interfaces.srv.SetDirection_Response(success=True, message="Override accepted: direction set to 'left' for 2.5s before autonomy resumes.")

ros2 service call /set_direction obstacle_direction_interfaces/srv/SetDirection "{direction: 'reverse'}"
waiting for service to become available...
requester: making request: obstacle_direction_interfaces.srv.SetDirection_Request(direction='reverse')

response:
obstacle_direction_interfaces.srv.SetDirection_Response(success=True, message="Override accepted: direction set to 'reverse' for 2.5s before autonomy resumes.")

ros2 service call /set_direction obstacle_direction_interfaces/srv/SetDirection "{direction: 'sideways'}"
waiting for service to become available...
requester: making request: obstacle_direction_interfaces.srv.SetDirection_Request(direction='sideways')

response:
obstacle_direction_interfaces.srv.SetDirection_Response(success=False, message='Unknown direction: sideways. Use forward, reverse, left, or right.')
```

## 5. Demo of the Project

https://youtu.be/InpKfpii3_s
