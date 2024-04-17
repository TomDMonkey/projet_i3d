import time
from pyniryo import *

# Configuration des adresses IP et de l'API key
octoprint_ip = "192.168.0.78"
robot_ip = "192.168.0.148"
api_key = "2A21B813752B46978D9DC9AE9F12A3D8"


def move_robot(robot):
    # Exécuter les mouvements sur le bras robot Niryo
    try:
        # robot.calibrate_auto()
        # robot.release_with_tool()
        # robot.clear_collision_detected()
        conveyor_id = robot.set_conveyor()
     

        robot.move_joints([-0.138, 0.037, -1.022, -0.084, 0.644, 0.135])
        robot.open_gripper()
        time.sleep(0.5)
        robot.move_joints([-0.113, -0.953, 0.151, -0.152, 0.632, 0.140])
        time.sleep(0.5)
        robot.close_gripper()
        time.sleep(0.5)
        robot.move_joints([-0.138, 0.037, -1.022, -0.084, 0.644, 0.135])
        time.sleep(0.5)

        robot.move_joints([-0.929, -0.672, -0.402, -0.219, 0.644, 0.141])
        robot.open_gripper()
        time.sleep(0.5)
        robot.close_gripper()
        robot.move_joints([-0.138, 0.037, -1.022, -0.084, 0.644, 0.135])

        robot.run_conveyor(conveyor_id, speed=80, direction=ConveyorDirection.BACKWARD)
        time.sleep(10)
        robot.stop_conveyor(conveyor_id)
         # Désactiver la connexion avec le tapis roulant
        robot.unset_conveyor(conveyor_id)

        # Arrêter la connexion TCP
        robot.close_connection()

        print("Mouvements exécutés avec succès sur le bras robot Niryo.")
    except Exception as e:
        print("Une erreur s'est produite lors de l'exécution des mouvements sur le bras robot Niryo :", e)

robot = NiryoRobot(robot_ip)

# Boucle principale
while True:
    move_robot(robot)
    break