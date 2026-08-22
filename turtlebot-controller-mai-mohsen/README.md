# turtlebot_controller Package

A ROS 2 Python package with **two nodes** that work together 
over the `/cmd_vel` topic:

- **`turtlebot_controller`** (Publisher):
reads keyboard input (W/A/S/D/Q) and publishes `geometry_msgs/Twist` 
velocity commands to TurtleBot3.
- **`turtlebot_monitor`** (Subscriber) :
listens to the same topic and prints, in real time, what the robot is being told to do.

---

## 1. Step-by-Step Setup Instructions

1. **Create ROS 2 workspace**
   ```bash
   mkdir -p ~/turtlebot_controller_ws/src
   cd ~/turtlebot_controller_ws/src
   ```

2. **Copy this package into the workspace's `src/` folder**
   Place the `turtlebot_controller` folder so the path looks like:
   ```
   ~/turtlebot_controller_ws/src/turtlebot_controller
   ```

3. **Build the package**
build the package inside the workspace folder
   ```bash
   cd ~/turtlebot_controller_ws
   colcon build --packages-select turtlebot_controller
   ```

4. **Source the workspace** (do this in every new terminal you open)
   ```bash
   source install/setup.bash
   ````

---

## 2. Every Linux Command Used (and what it does)

| Command | What it does |
|---|---|
| `mkdir -p ~/turtlebot_controller_ws/src` | Creates the workspace folder (and any missing parent folders) if it doesn't already exist. |
| `cd <path>` | Changes the current directory in the terminal to `<path>`. |
| `source install/setup.bash` | Loads the workspace's environment (paths to nodes, messages, etc.) into the current terminal session so `ros2 run` can find your package. |

---

## 3. Every ROS 2 Command Used (and what it does)

| Command | What it does |
|---|---|
| `colcon build --packages-select turtlebot_controller` | Compiles/installs only this package (faster than rebuilding the whole workspace). |
| `ros2 run turtlebot_controller controller` | Runs the publisher node (the keyboard controller). |
| `ros2 run turtlebot_controller monitor` | Runs the subscriber node (the monitor). |
| `ros2 node list` | Lists all currently running ROS 2 nodes and used to confirm both nodes are active. |
| `ros2 topic list` | Lists all currently active topics and used to confirm `/cmd_vel` exists. |
| `ros2 topic type /cmd_vel` | Shows the type of the message associated with the `/cmd_vel` topic. |
| `ros2 topic echo /cmd_vel` | Prints every message published on `/cmd_vel` live in the terminal. |

---

## 4. How to Test Your Nodes

1. **Turn on your simulation (I used Turtlebot3 - Burger model)**

2. **Terminal 1: Start the monitor node first** (so you can see messages as soon as they start)
   ```bash
   source install/setup.bash
   ros2 run turtlebot_controller controller
   ```

3. **Terminal 2: Start the controller node**
   ```bash
   source install/setup.bash
   ros2 run turtlebot_controller monitor
   ```

4. **Click into Terminal 1** (so it captures your keystrokes) and test each key:
   - Press `W` → robot should move forward
   - Press `S` → robot should move backward
   - Press `A` → robot should turn left in place
   - Press `D` → robot should turn right in place
   - Press `Q` → robot stops and the controller node exits

---

## 5. Expected Output

**In the controller (publisher) terminal**, you should see log lines like:
```
[INFO] [turtlebot_controller]: Turtlebot Controller started.
[INFO] [turtlebot_controller]: Use W/A/S/D to move, Q to stop and quit.
[INFO] [turtlebot_controller]: Forward
[INFO] [turtlebot_controller]: Turn left
[INFO] [turtlebot_controller]: Q pressed: stopping robot and exiting.
```

**In the monitor (subscriber) terminal**, you should see log lines like:
```
[INFO] [turtlebot_monitor]: Turtlebot Monitor started. Listening on /cmd_vel ...
[INFO] [turtlebot_monitor]: Moving FORWARD | linear.x=0.20 m/s, angular.z=0.00 rad/s
[INFO] [turtlebot_monitor]: Turning LEFT | linear.x=0.00 m/s, angular.z=0.50 rad/s
[INFO] [turtlebot_monitor]: STOPPED | linear.x=0.00 m/s, angular.z=0.00 rad/s
```

**In the simulation window**, the TurtleBot3 model should physically move forward/backward or rotate in place in sync with the keys you press, and stop immediately when `Q` is pressed.

---

## 6. Demo of the Project

https://youtu.be/xt-s-sHy1mA
