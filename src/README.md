# Rover Sim (ROS 2 + Webots)

This project is a ROS 2 Humble-based mobile robot simulation using Webots.  
It includes a custom rover robot with obstacle avoidance and simulation integration.

---

## 🚀 Features

- ROS 2 Humble integration
- Webots simulation environment (Debian installation, not Snap)
- Custom rover robot model (URDF-based)
- ROS 2 node for robot
- Launch file for full simulation startup
- Extensible structure for SLAM and navigation

---

## 🧱 Project Structure

```text
ros2_ws/
└── src/
    └── rover_sim/
        ├── launch/
        │   ├── robot_launch.py
        ├── worlds/
        │   ├── my_world.wbt
        ├── resource/
        │   ├── my_robot_urdf
        │   ├── rover_sim
        ├── rover_sim/
        │   ├── rover_driver.py
        │   ├── obstacle_avoider.py
        │   └── __init__.py
        ├── package.xml
        ├── setup.py
        └── setup.cfg
```
---
## ⚙️ Requirements
Ubuntu 22.04
ROS 2 Humble
Webots (installed via .deb, NOT Snap version)
colcon build tools

### 📦 Install Dependencies
sudo apt update
sudo apt install ros-humble-webots-ros2-driver

### 🔨 Build Workspace
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash

### ▶️ Run Simulation
ros2 launch rover_sim robot_launch.py
