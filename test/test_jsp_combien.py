from pyniryo import *
from colorama import *
import requests
import time
import os
import sys
import time
from pystyle import *

octoprint_ip = "btssnir.lycee-costebelle.fr:7651"
robot_ip ="btssnir.lycee-costebelle.fr:40001"
api_key = "2A21B813752B46978D9DC9AE9F12A3D8"
payload = {"command": "G1 Z60"}  # Exemple de commande pour déplacer la tête de 10 mm vers le haut
robot = NiryoRobot(robot_ip)

try:
    response = requests.post(f"http://{octoprint_ip}/api/printer/command", headers={"X-Api-Key": api_key}, json=payload)
    response.raise_for_status()
    robot.move_joints([-1.746, 0.071, -0.125, 1.021, 0.644, 0.207])
    time.sleep(2)
    robot.move_joints([0.238, 0.037, -0.986, -0.005, 0.644, 0.206])

    print("Tête d'impression déplacée vers le haut avec succès.")
except Exception as e:
    print("Une erreur s'est produite lors du déplacement de la tête d'impression :", e)
