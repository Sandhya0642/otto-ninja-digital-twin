# Experiment protocol (proposed)

## Goal
Measure whether calibration improves the physical Otto Ninja robot's repeatability and turning accuracy. Do not use browser-preview values as physical or MuJoCo measurements.

## Control variables
- Robot firmware and servo calibration offsets
- Battery voltage/state of charge
- Floor material and slope
- Starting pose and orientation
- Command duration, target gait frequency, and amplitude
- Camera/tracking setup and measurement method

## Trial procedure
1. Inspect the robot, feet, fasteners, servo horns, and battery.
2. Record firmware version, battery voltage, and calibration values.
3. Place the robot on a clear, level surface with a marked starting pose.
4. Execute the same motion command for each trial.
5. Measure displacement and final heading from an external camera, fiducial tracking, or another repeatable method.
6. Repeat each condition at least 5–10 times where feasible.
7. Apply the proposed calibration procedure and repeat the exact same conditions.
8. Report all exclusions and failures, not just successful trials.

## Suggested metrics
- Heading error: absolute difference between commanded and measured final heading.
- Distance error: absolute difference between expected and measured displacement, only when an expected value is defensibly defined.
- Repeatability: mean and standard deviation across repeated trials.
- Relative improvement: compare baseline and calibrated errors with the same measurement setup.

## Data table fields
trial_id, date_time, condition, command_yaw_deg, command_frequency_hz, command_duration_s, battery_voltage, calibration_version, measured_heading_deg, measured_distance_m, step_period_s, notes

## Scientific caution
A MuJoCo model is only as useful as its measured geometry, inertial parameters, actuator limits, and contact assumptions. Document simplifications and validate them. A URDF or XML file alone is not evidence that a digital twin is synchronized with the physical system.