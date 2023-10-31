 # 2 DOF Robotic Leg
Python code and CAD files for a single, 2 DOF robotic leg. This design uses 2 [3D printed robotic actuators](https://github.com/owenmckenney/Robotic_Actuator) as well as a Raspberry Pi and mjbots pi3hat r4.5 to achieve planar leg motion. This leg mainly serves as a way to test the design of these actuators; a third DOF oriented orthagonal to the current axis of rotation of the actuators would be necessary for a more functional and realistic leg as this would allow for easier turning during walking and would add a significant amount of stability to a full quadruped. The materials needed to replicate this design are listed in the [BOM](BOM.md). 

[CAD Overview](https://youtu.be/-uwau5FXpTE?si=GULFIlkYwvTJMZq1)

## Media



## Specs

- Thigh joint to knee joint: 200mm
- Knee joint to center of foot: 185mm
- 

## Manufacturing and Assembly 

- Most components fit together intuitively as there is only one way that this leg can be assembled. Only STL files are provided. For access to specifc source files, email owen.mckenney1@gmail.com.
- Larger prints may need to be oriented diagonally across the printbed depending on the kind of 3D printer being used.
- The 3D printed components of the original implementation were printed on a Ender 3 using PLA. All components have a naturally built-in tolerance of 0.2mm; this value may not be perfect depending on the tuning of your printer.
- Use of large width brims when slicing larger prints could be useful to prevent any warping during printing
- Pulleys should likely be printed with no support material; the addition of support can alter the shape of the pulley teeth and lead to belt slippage and skippage. The belt tensioner must also be implented for the same reasons.
- 

## Setup

Ensure all libraries and dependencies are installed, following the [moteus documentation](https://github.com/mjbots/moteus/tree/main). 

Follow proper construction and setup processes for the [robotic actuators](https://github.com/owenmckenney/Robotic_Actuator).

Set the correct servo ids for both the knee and thigh actuators, which are 2 and 1, respectively. Connect only the thigh actuator to JC1 on the pi3hat and use `sudo python3 -m moteus.moteus_tool -t 1 -c` to enter console and set the `id.id` to 1 using `conf set id.id 1`. Once this is set, the knee actuator can be daisychained and its `id.id` can be set to 2. 

Zero positions should be set for both the knee and calf joints using `sudo python3 -m moteus.moteus_tool --target 1 --zero-offset` and `sudo python3 -m moteus.moteus_tool --target 2 --zero-offset` while the leg is oriented in a completed downward position (thigh and calf are colinear and pointed down). 

Set `servopos.position_min` and `servopos.position_max` to `-3.0`, `0.5` and `-3.2`, `0.5` for the thigh and knee servo, respectively. Without these limits set, the leg is susceptible to major failure as the joints may try to move to positions not physically allowed. 

Reference the moteus documentation for additional guidance on how to set up the pi3hat, configure the actuator ids, and set position limits.
