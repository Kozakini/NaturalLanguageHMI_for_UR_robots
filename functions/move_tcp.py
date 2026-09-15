import os
import subprocess

import rtde_control
import rtde_receive
from google.genai import types

schema_move_tcp = types.FunctionDeclaration(
    name="move_tcp",
    description="Move the TCP in the specified direction",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "direction": types.Schema(
                type=types.Type.STRING,
                description="direction to move the TCP in input is limited to 'up', 'down', 'forward', 'back', 'right', 'left'",

            ),
            "step": types.Schema(
                type=types.Type.NUMBER,
                description="how much to move tcp by for example 0.1=5cm, so when user asks for how much movment to do you just divide provided amount by 5cm and multiply 0.1 by the result",
            ),
        },
    ),
)

ctrl = rtde_control.RTDEControlInterface("127.0.0.1")
recv = rtde_receive.RTDEReceiveInterface("127.0.0.1")
STEP = 0.1  # 5 cm


def move_tcp(direction, step):
    STEP = step
    match direction:
        case "up":
            move_up()
        case "down":
            move_down()
        case "forward":
            move_forward()
        case "back":
            move_back()
        case "right":
            move_right()
        case "left":
            move_left()
        case _:
            pass


def move_up():
    pose = recv.getActualTCPPose()
    pose[2] += STEP
    ctrl.moveL(pose, speed=0.1, acceleration=0.3)


def move_down():
    pose = recv.getActualTCPPose()
    pose[2] -= STEP
    ctrl.moveL(pose, speed=0.1, acceleration=0.3)


def move_forward():
    pose = recv.getActualTCPPose()
    pose[1] -= STEP
    ctrl.moveL(pose, speed=0.1, acceleration=0.3)


def move_back():
    pose = recv.getActualTCPPose()
    pose[1] += STEP
    ctrl.moveL(pose, speed=0.1, acceleration=0.3)


def move_right():
    pose = recv.getActualTCPPose()
    pose[0] -= STEP
    ctrl.moveL(pose, speed=0.1, acceleration=0.3)


def move_left():
    pose = recv.getActualTCPPose()
    pose[0] += STEP
    ctrl.moveL(pose, speed=0.1, acceleration=0.3)
