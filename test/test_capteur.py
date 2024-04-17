#!/usr/bin/env python

# Imports
from niryo_robot_python_ros_wrapper import *
import rospy

def run_conveyor(robot, conveyor):
robot.control_conveyor(conveyor, bool_control_on=True,
                      speed=50, direction=ConveyorDirection.FORWARD)

# -- Setting variables
sensor_pin_id = PinID.GPIO_1A 

niryo_robot = NiryoRosWrapper()

# Activating connexion with conveyor
conveyor_id = niryo_robot.set_conveyor()

# Run conveyor and wait until the IR sensor detects an object
run_conveyor(niryo_robot, conveyor_id)
while niryo_robot.digital_read(sensor_pin_id) == PinState.LOW:
    niryo_robot.wait(0.1)

# Stopping conveyor's motor
niryo_robot.control_conveyor(conveyor_id, True, 0, ConveyorDirection.FORWARD)

# Deactivating connexion with conveyor
niryo_robot.unset_conveyor(conveyor_id)