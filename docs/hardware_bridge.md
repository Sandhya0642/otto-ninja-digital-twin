# ROS 2, MuJoCo, and physical hardware bridge

## Current software path
The ROS 2 `servo_command` node publishes seven servo-degree values to `/otto_ninja/servo_degrees`. The `mujoco_bridge` node subscribes to that topic and maps the values to the seven MuJoCo actuators. This provides a local ROS 2 → MuJoCo command path when the model, dependencies, and viewer run successfully.

The bridge has not been executed or validated against the user's machine in this chat. Its model dimensions, joint signs, inertias, contact behavior, and continuous-servo speed conversion are starting estimates that require local verification.

## Servo command order
`[left_foot, left_leg, right_foot, right_leg, left_arm, right_arm, head]`

The foot channels are continuous-rotation servos, so 90° is neutral and +/- command offsets represent speed/direction. The bridge currently maps +/-45° to +/-8 rad/s and reverses the right foot for mirrored mounting. Measure the real wheel speed at several command values to calibrate this slope and verify signs.

Positional channels use firmware home positions as the reference:
- left leg home 60°
- right leg home 120° (right side sign inverted in the model)
- left arm down 180°, raised 90°
- right arm down 0°, raised 90°
- head neutral 90°

These mappings are explicit assumptions until checked on the physical robot.

## Before connecting physical hardware
The current package does NOT include a physical servo driver. Do not send the simulation topic to a hardware controller. First:
1. Identify the exact ESP/servo-controller firmware and communication protocol.
2. Confirm servo pins, physical servo type, gear ratio, pulse limits, and all joint directions.
3. Test each servo separately with the robot supported and with low-risk command limits.
4. Implement a separate hardware adapter that validates input range and has command timeout, neutral-on-shutdown behavior, and an accessible emergency stop.
5. Check current draw, mechanical end stops, and pinch hazards before full-motion tests.
6. Record command and measured response with timestamps.

## Local simulation
From the repository root, install MuJoCo in the Python environment and build the ROS 2 package as described in the root README. Then run `ros2 launch otto_ninja_twin humanoid_sim.launch.py mode:=walk joystick_y:=55`. The launch opens a native MuJoCo viewer and publishes a firmware-inspired walk command pattern. Set `joystick_y:=0` to hold the home pose; use `mode:=roll` to test the rolling servo mapping.

## Scientific limits
A valid simulation-to-hardware digital twin requires calibrated geometry, mass/inertia, contact parameters, servo response, and repeatable physical measurements. The web dashboard does not currently connect to ROS over a websocket. The Vercel deployment is a static dashboard and downloadable asset host; MuJoCo/ROS run locally.
