# commands foot to x/y coordinate based on x/y input
# calculates angles for thigh and knee, converts to positional values

import math
import time
import asyncio
import argparse
import moteus
import moteus_pi3hat
import sys

a = 200
b = 185

transport = moteus_pi3hat.Pi3HatRouter(
    servo_bus_map = {
        1:[11],
        2:[11]
    }
)

hip_servo = moteus.Controller(id=1, transport=transport)
knee_servo = moteus.Controller(id=2, transport=transport)

async def zero():
    commands = [
        hip_servo.make_position(
            position = 0,
            accel_limit = 2.0, 
            velocity_limit = 4.0,
            maximum_torque = 0.15, 
            watchdog_timeout = math.nan
            ),
        knee_servo.make_position(
            position = 0,
            accel_limit = 2.0,
            velocity_limit = 4.0,
            maximum_torque = 0.15,
            watchdog_timeout = math.nan
        )
    ]
    
    results = await transport.cycle(commands)

def calculate_positions(a, b, x, y, hip_pos, knee_pos):
    gamma = math.atan(x/y)
    theta = math.acos(((x**2 + y**2) + a**2 - b**2)/(2*a*math.sqrt(x**2 + y**2)))
    phi = math.acos((a**2 + b**2 - x**2 - y **2)/(2*a*b))

    previous_hip_pos = hip_pos
    previous_knee_pos = knee_pos

    hip_pos = math.degrees(theta + gamma) * 1/360 * -8 
    knee_pos = (180 - math.degrees(phi)) * 1/360 * 8

    return hip_pos, knee_pos, previous_hip_pos, previous_knee_pos


def calculate_velocities(hip_pos, knee_pos, previous_hip_pos, previous_knee_pos, vel_high, accel):
    hip_pos_diff = abs(hip_pos - previous_hip_pos)
    knee_pos_diff = abs(knee_pos - previous_knee_pos)

    #print("Hip pos diff: ", hip_pos_diff, "Knee pos diff: ", knee_pos_diff)

    t = round((-vel_high + math.sqrt(vel_high**2 - 4*(accel/2)*-max(hip_pos_diff, knee_pos_diff)))/(2*(accel/2)), 4)
    vel_low = (min(hip_pos_diff, knee_pos_diff) - accel/2 * t**2)/t

    #print("t: ", t, "vel low: ", vel_low)

    if hip_pos_diff > knee_pos_diff:
        hip_vel = vel_high
        knee_vel = vel_low
    elif hip_pos_diff < knee_pos_diff: 
        hip_vel = vel_low
        knee_vel = vel_high
    else:
        hip_vel = vel_high
        knee_vel = vel_high

    return hip_vel, knee_vel

async def move(hip_pos, knee_pos, hip_vel, knee_vel, accel):
    
    commands = [
        hip_servo.make_position(
            position = hip_pos,
            accel_limit = accel, 
            velocity_limit = hip_vel,
            maximum_torque = 0.15, 
            watchdog_timeout = math.nan,
            query = True
        ),
        knee_servo.make_position(
            position = knee_pos,
            accel_limit = accel,
            velocity_limit = knee_vel,
            maximum_torque = 0.15,
            watchdog_timeout = math.nan,
            query = True
        )
    ]

    results = await transport.cycle(commands)

async def main():

    await hip_servo.set_stop()
    await knee_servo.set_stop()
    await zero()

    mode = int(input("1 for coordinate controlled movement, 2 for walking sequence: "))
    
    if mode == 1:
        hip_pos = 0
        knee_pos = 0
        vel_high = 16.0
        accel = 8.0

        try:
            while True:
                y = round(float(input("enter desired y displacement: ")), 4)
                x = round(float(input("enter desired x displacement: ")), 4)

                positions = calculate_positions(a, b, x, y, hip_pos, knee_pos)
                hip_pos = positions[0]
                knee_pos = positions[1]

                print("Hip pos: ", hip_pos, "Knee pos: ", knee_pos)

                velocities = calculate_velocities(hip_pos, knee_pos, positions[2], positions[3], vel_high, accel)
                hip_vel = velocities[0]
                knee_vel = velocities[1]

                print("hip vel: ", hip_vel, "knee vel: ", knee_vel)

                await move(hip_pos, knee_pos, hip_vel, knee_vel, accel)

        except KeyboardInterrupt:
            await hip_servo.set_stop()
            await knee_servo.set_stop()
            sys.exit("interrupt")

    
    elif mode == 2:
        time.sleep(1)

        hip_pos = 0
        knee_pos = 0

        try:
            while True:
                x = -100
                y = 250

                initial_pos = calculate_positions(a, b, x, y, hip_pos, knee_pos)
                velocities = calculate_velocities(initial_pos[0], initial_pos[1], initial_pos[2], initial_pos[3], 16.0, 8.0)
                await move(initial_pos[0], initial_pos[1], velocities[0], velocities[1], 8.0)

                time.sleep(1)

                for x in range(-100, 201):
                    y = 250
                    positions = calculate_positions(a, b, x, y, hip_pos, knee_pos)
                    
                    await move(positions[0], positions[1], 10.0, 10.0, 8.0)

                c = 100
                d = 50
                k = 200

                for x in range(200, -99):                    
                    y = (d*math.sqrt(c**2 - x**2))/c + k
                    positions = calculate_positions(a, b, x, y, hip_pos, knee_pos)

        except KeyboardInterrupt:
            await hip_servo.set_stop()
            await knee_servo.set_stop()
            sys.exit("interrupt")

    else:
        await hip_servo.set_stop()
        await knee_servo.set_stop()
        sys.exit("invalid input")
        
if __name__ == '__main__':
    asyncio.run(main())
