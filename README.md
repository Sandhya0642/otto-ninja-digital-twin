# Otto Ninja Digital Twin — reconstructed seven-servo simulation starter

This repository combines (1) a static research dashboard, (2) a reconstructed URDF/MuJoCo robot model, and (3) a ROS 2 command publisher and MuJoCo physics viewer.

## Important honesty about geometry and validation
The source URLs supplied earlier point to the Otto Ninja product/build information and firmware, not to a direct CAD assembly with verified dimensions. The STL files in `meshes/` are reconstructed parametric placeholders, not the original Otto Ninja CAD. The URDF/MJCF use approximate dimensions, masses, inertias, and contact shapes. Treat them as a software integration prototype until replaced/calibrated against your exact hardware revision.

The official firmware does confirm seven servo channels for the Humanoid configuration and nominal positions for legs, arms, head, and foot servos. See `docs/model_provenance_and_calibration.md`. The foot servos are continuous-rotation servos: 90° is neutral and commands above/below 90° represent speed/direction, not absolute joint angles.

## Project structure
- `index.html` — deployed dashboard with preview, command inputs, trial log and CSV export
- `meshes/*.stl` — reconstructed link meshes (not source CAD)
- `urdf/otto_ninja_humanoid.urdf` — seven-joint/link ROS robot description
- `mujoco/otto_ninja_humanoid.xml` — MuJoCo model with floating base, contacts, actuators and sensors
- `ros2_ws/src/otto_ninja_twin/otto_ninja_twin/servo_command_node.py` — firmware-inspired servo-angle publisher
- `ros2_ws/src/otto_ninja_twin/otto_ninja_twin/mujoco_bridge.py` — ROS 2 subscriber controlling MuJoCo actuator targets
- `ros2_ws/src/otto_ninja_twin/launch/humanoid_sim.launch.py` — launches physics viewer and command node
- `ros2_ws/src/otto_ninja_twin/launch/display_robot.launch.py` — opens URDF in RViz with joint sliders
- `docs/model_provenance_and_calibration.md` — source references, servo mapping, and calibration checklist
- `docs/experiment_protocol.md` — suggested physical validation protocol

## What Vercel does (and does not do)
Vercel serves the web dashboard and downloadable model files. It does **not** run the native MuJoCo physics viewer, ROS 2 graph, or hardware connection. To see physics-based motion, run the MuJoCo bridge locally on Ubuntu/Linux with a graphical session.

## Local installation

Assumes a compatible Ubuntu + ROS 2 installation, `colcon`, and a graphical desktop for MuJoCo viewer. Confirm your ROS 2 distribution before following its official installation instructions.

```bash
sudo apt install python3-pip python3-venv
python3 -m pip install --user mujoco
cd ros2_ws
source /opt/ros/$ROS_DISTRO/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 launch otto_ninja_twin humanoid_sim.launch.py mode:=walk joystick_x:=0 joystick_y:=55
```

The default command node starts a forward-walk pattern to demonstrate the command pipeline. The unbalanced biped can tip/fall in physics; this is a useful simulation result, not a guarantee of stable walking. Set `joystick_y:=0` to hold the walk-mode home pose. For roll mode, use `mode:=roll`.

### Open the URDF in RViz

```bash
cd ros2_ws
source /opt/ros/$ROS_DISTRO/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 launch otto_ninja_twin display_robot.launch.py
```

### Run MuJoCo only / inspect the XML

From the repository root, in an environment with the `mujoco` Python package installed:

```bash
python -m mujoco.viewer --mjcf mujoco/otto_ninja_humanoid.xml
```

For ROS bridge execution, the package installs the MJCF and mesh assets into its share directory and loads them from there.

## Servo channel order and mapping
Topic: `/otto_ninja/servo_degrees` (`std_msgs/msg/Int16MultiArray`), exactly seven values:
`[left_foot, left_leg, right_foot, right_leg, left_arm, right_arm, head]`.

- Foot servos: initial mapping 90° -> 0 rad/s; +/-45° -> +/-8 rad/s. Right side inverted for mirrored mounting.
- Left leg: `radians(degrees - 60)`
- Right leg: `-radians(degrees - 120)`
- Left arm: `radians(180 - degrees)`
- Right arm: `radians(degrees)`
- Head: `radians(degrees - 90)`

The mapping is based on firmware home values plus explicit assumptions about joint directions. It is not yet calibrated to the user's actual servo horn orientation or measured wheel speed. Check `docs/model_provenance_and_calibration.md`.

## Validation checklist before making thesis claims
1. Confirm the exact physical model revision (Starter 4-servo vs Humanoid 7-servo).
2. Replace reconstructed STL placeholders with the matching official part files and record attribution/licence.
3. Measure dimensions, servo axes, offsets, masses, wheel radius and servo speed response.
4. Check XML loads in MuJoCo; inspect contacts and model stability.
5. Verify URDF visuals and joint axes in RViz.
6. Run each channel individually at low amplitude; confirm command signs.
7. Compare repeatable real-robot turning/walking measurements with simulated outputs.
8. Report errors and calibration improvements over repeated trials.

## Safety and research integrity
The example ROS node publishes commands only to the simulation topic. No physical servo driver is included. Do not connect this topic to real hardware until servo mapping, pulse limits, watchdog, and emergency-stop behavior are verified. The browser animation and CSV export are command-preview data, not MuJoCo or physical measurements.

## Source and licensing
- Official product description: https://www.ottodiy.com/ninja
- Official firmware repository: https://github.com/OttoDIY/OttoNinja
- Official 3D print resources page: https://www.ottodiy.com/academy
- Official Printables creator page: https://www.printables.com/@hprobots

The Otto Ninja project indicates CC-BY-SA terms. Preserve attribution and share-alike terms for adapted project material. Reconstructed meshes here are not official CAD. Review the licence of each official part file before redistribution.
