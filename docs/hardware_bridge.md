# ROS 2 and hardware bridge notes

The included ROS 2 node publishes illustrative joint commands to `/otto_ninja/joint_command`. It is not a physical hardware driver and is not connected to MuJoCo automatically.

Before connecting a real Otto Ninja robot:
1. Identify the exact controller board, firmware, servo IDs, command units, and communication interface.
2. Confirm the actual joint/servo mapping and direction; the included order is only a placeholder.
3. Determine safe pulse/angle limits from the hardware documentation and test with the robot supported off the ground.
4. Add command validation, timeouts, an emergency-stop path, and a safe neutral command on shutdown.
5. Add a separate hardware adapter that subscribes to the ROS topic and uses the confirmed protocol.
6. Log commands and measured outputs with timestamps.

Do not run the example publisher into a hardware adapter until the mapping, limits, and stop behavior have been verified. The web dashboard does not currently connect to ROS over a WebSocket and cannot control the physical robot.