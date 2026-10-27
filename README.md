# Otto Ninja Digital Twin — M.Tech Thesis Starter

An early-stage research workspace with an interactive web dashboard, a simplified MuJoCo XML model, and a ROS 2 command-generation package.

## Important status and limitations
This is a starter scaffold, not a completed or validated digital twin. The web robot animation and response chart are illustrative browser-generated data, not MuJoCo physics results or measurements from a physical robot. Vercel hosts the static dashboard only. MuJoCo and ROS 2 must run on a compatible local computer; no live web-to-ROS bridge or physical robot connection is implemented.

## Layout
- `index.html` — dashboard, controls, illustrative chart, experiment log and CSV export
- `mujoco/otto_ninja.xml` — approximate MuJoCo starter model
- `requirements-mujoco.txt` — Python dependencies
- `ros2_ws/src/otto_ninja_twin/` — ROS 2 Python package and example gait command publisher
- `docs/experiment_protocol.md` — proposed validation protocol
- `docs/hardware_bridge.md` — hardware integration and safety notes
- `vercel.json` — static hosting configuration

## Proposed research direction
Low-cost biped robots can show differences between commanded and actual movement because of servo offsets, mechanical asymmetry, battery variation, and foot contact. The proposed work is to quantify this mismatch and test whether a repeatable calibration procedure improves walking or turning accuracy.

Potential contribution to validate: a low-cost simulation-assisted calibration workflow supported by repeated baseline and post-calibration experiments. This is a hypothesis, not an established novelty claim.

## Run the website locally
Open `index.html` in a modern browser or serve the repository directory using any static file server.

## MuJoCo setup
With a compatible Python environment:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-mujoco.txt
python -m mujoco.viewer --mjcf mujoco/otto_ninja.xml
```
The XML is approximate and requires validation of geometry, inertia, contacts, joint ranges and actuator definitions.

## ROS 2 setup
With a compatible ROS 2 distribution and `colcon` installed:
```bash
cd ros2_ws
source /opt/ros/$ROS_DISTRO/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 launch otto_ninja_twin gait_command.launch.py
```
The node publishes an illustrative `Float64MultiArray` to `/otto_ninja/joint_command`. It is not a MuJoCo bridge or physical hardware driver. Verify the actual controller, servo mapping, units, safe limits and stop behavior before implementing any hardware connection.

## Proposed experimental procedure
1. Measure the physical robot's dimensions, servo ranges and calibration offsets.
2. Define repeatable straight-walk and turning commands.
3. Collect repeated physical trials using a consistent external measurement method.
4. Compare commanded and measured heading, displacement and step period.
5. Apply a documented calibration and repeat the same trials.
6. Report average errors, variability, failures and limitations.
7. Compare the approach with related literature before claiming novelty.

A visual model alone is not a digital twin; a defensible twin needs a validated model and measurable relationship with the physical system. Browser CSV exports contain command-preview metadata only, not scientific outcome measurements.

## Safety
Test on a clear, level surface. Add command validation, timeouts and emergency stop before autonomous physical experiments. Never send the example command topic to real hardware without verifying mapping and limits.

## License
MIT starter code; check third-party dependencies separately.
