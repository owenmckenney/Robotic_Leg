# 2 DOF Robotic Leg
Python code and CAD files for a single, 2 DOF robotic leg. This design uses 2 [3D printed robotic actuators](https://github.com/owenmckenney/Robotic_Actuator) as well as a Raspberry Pi to achieve planar leg motion. This leg mainly serves as a way to test the design of these actuators; a third DOF oriented orthagonal to the current 2 axis would be necessary for a more functional and realistic leg. The materials needed to replicate this design are listed in the [BOM](). 

## Media

## Specs

- Thigh joint to knee joint: 200mm
- Knee joint to center of foot: 185mm
- 

## Manufacturing and Assembly 

## Setup

Zero positions should be set for both the knee and calf joint using `sudo python3 -m moteus.moteus_tool --target 1 --zero-offset` and `python3 -m moteus.moteus_tool --target 2 --zero-offset` while the leg is oriented in a completed downward position (thigh and calf are colinear and pointed down). 

Set `servopos.position_min` and `servopos.position_max` to `-3.0`, `0.5` and `-3.2`, `0.5` for the thigh and knee servo, respectively. 

Reference the the [moteus documentation](https://github.com/mjbots/moteus/tree/main) for additional guidance.
