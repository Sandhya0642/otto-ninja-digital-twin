# Otto Ninja Digital Twin — M.Tech Thesis Starter

This repository is a starting point for developing a digital-twin workflow for an Otto Ninja biped robot.

## Aim
Develop a virtual robot model and compare its commanded motions with the physical Otto Ninja robot, then quantify the mismatch and investigate simple calibration or correction methods.

## Proposed workflow
1. Assemble and test the physical Otto Ninja robot.
2. Create a robot description (URDF) and visualize it in ROS 2/RViz.
3. Send repeatable motion commands to the physical robot and the virtual model.
4. Record measurable outputs (e.g., joint/servo commands, step timing, distance travelled, and turning angle).
5. Compare physical and simulated outcomes using error metrics.
6. Evaluate whether calibration or command adjustment reduces the mismatch.

## Possible thesis contribution
A practical, low-cost digital-twin framework for a small biped robot, with quantitative physical-versus-virtual motion comparison and a repeatable calibration procedure.

This is a proposed research direction, not a demonstrated novelty yet. The contribution must be validated experimentally and compared with relevant literature.

## Current status and limitations
This repository is currently being initialized. Any robot model added later should be treated as an approximate visualization model until its geometry, joint limits, servo positions, and motion are checked against the actual robot. A visual model alone is not a synchronized digital twin.

## Planned repository structure
- `urdf/` — robot description
- `meshes/` — visual/collision meshes, if needed
- `launch/` — ROS 2 launch files
- `rviz/` — RViz configuration
- `docs/` — setup notes, experiments, and results

## Requirements (planned)
- Ubuntu with a compatible ROS 2 distribution
- RViz2
- Physical Otto Ninja robot and its controller/firmware for hardware experiments

Exact ROS 2 package metadata and launch commands will be added after the target ROS 2 distribution and hardware-control interface are confirmed.

## Research questions
- How closely does the virtual model reproduce the robot's commanded pose and motion?
- Which factors contribute most to the physical-versus-virtual mismatch?
- Can a simple calibration or command-correction method reduce the measured error?

## Experimental metrics (suggested)
- Mean absolute error in measured turning angle
- Distance travelled per command
- Step-cycle duration
- Repeatability across repeated trials

## Safety and reproducibility
Test the physical robot on a clear, level surface. Record firmware, servo calibration, battery state, ROS 2 distribution, command parameters, and trial conditions for each experiment.
