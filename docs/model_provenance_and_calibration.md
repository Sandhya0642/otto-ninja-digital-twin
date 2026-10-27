# Model provenance and calibration

## Source references
- Otto Ninja product description and configuration: https://www.ottodiy.com/ninja
- Otto Ninja firmware repository: https://github.com/OttoDIY/OttoNinja
- Firmware command source: examples/App/OttoNinja_APP/OttoNinja_APP.ino
- Official Otto DIY 3D-print file directory: https://www.ottodiy.com/academy
- Official Printables creator page: https://www.printables.com/@hprobots

The official firmware defines seven servo channels in the Humanoid configuration: left foot, left leg, right foot, right leg, left arm, right arm, and head. The source includes these nominal servo calibration values:
- left/right leg home positions: 60° / 120°
- left/right arm down positions: 180° / 0°
- head neutral: 90°
- leg walking poses: LATR=5°, RATR=80°, LATL=100°, RATL=175°
- rolling pose: left leg 180°, right leg 0°
- foot servo neutral: 90°, walking speed offsets default 20°
- servo pulse range in firmware: 544–2400 microseconds

## Geometry status
The STL meshes in this repository are newly reconstructed parametric placeholders based on a small biped layout, not extracted original Otto Ninja CAD. The source links previously shared include a build video/product description and firmware; they do not identify a directly downloadable native CAD assembly with verified dimensions. The official Academy points to Printables files, but do not substitute a different Otto/HP model for the user's exact Ninja variant without checking the part revision.

Before claiming CAD accuracy, replace these meshes with the exact files for the user's physical revision and measure link/joint offsets. The current URDF and MJCF are suitable for software integration experiments after local validation, but are not manufacturing drawings or a verified replica.

## Servo-to-simulation mapping
ROS topic `/otto_ninja/servo_degrees` is a seven-element `Int16MultiArray` in this order:
`[left_foot, left_leg, right_foot, right_leg, left_arm, right_arm, head]`.

The two foot servos are continuous-rotation actuators in the firmware: 90° is neutral, and the difference from 90° is a speed/direction command, not a measured absolute wheel angle. The bridge uses an initial linear map of +/-45° to +/-8 rad/s, with right-foot direction inverted for mirrored mounting. This speed conversion is a tunable estimate; it must be measured using the real servo and wheel radius.

Positional channels use the firmware home angles as zero references:
- left leg: radians(servo degrees - 60)
- right leg: -radians(servo degrees - 120)
- left arm: radians(180 - servo degrees)
- right arm: radians(servo degrees)
- head: radians(servo degrees - 90)

The sign conventions are starting hypotheses. Confirm joint axes and servo-horn orientations on the real robot before quantitative comparisons.

## Calibration procedure
1. Measure robot dimensions and mass, and identify servo model/gear ratio.
2. With power disconnected, identify each joint axis and zero pose from the actual build.
3. Run each servo independently at low speed; record angle/pose for a known command.
4. Measure continuous-rotation wheel speed at 70°, 80°, 90°, 100°, and 110° under the robot's normal load.
5. Adjust mapping slopes, signs, offsets, joint limits, masses, inertias, contact friction, and wheel radius.
6. Validate the model with repeatable physical trials and report errors.

## License
The Otto Ninja source project states CC-BY-SA; preserve attribution and share-alike terms when redistributing adapted source/geometry. These reconstructed meshes are placeholders and must not be described as the original CAD.
