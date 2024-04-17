import time
import requests
from pyniryo import *

# Configuration des adresses IP et de l'API key
octoprint_ip = "192.168.0.78"
robot_ip = "192.168.0.148"
api_key = "2A21B813752B46978D9DC9AE9F12A3D8"

# Variable pour garder une trace de l'état de l'impression précédente
previous_print_completed = True
a = 0
completion = None  # Définir completion en dehors du bloc try
def move_head_up():
    try:
        # Envoyer une commande Gcode pour monter la tête d'impression
        payload = {"command": "G1 Z60"}  # Exemple de commande pour déplacer la tête de 10 mm vers le haut
        response = requests.post(f"http://{octoprint_ip}/api/printer/command", headers={"X-Api-Key": api_key}, json=payload)
        response.raise_for_status()
        print("Tête d'impression déplacée vers le haut avec succès.")
    except Exception as e:
        print("Une erreur s'est produite lors du déplacement de la tête d'impression :", e)

# Fonction pour avancer le plateau
def move_bed_forward():
    try:
        # Envoyer une commande Gcode pour avancer le plateau
        payload = {"command": "G1 Y300"}  # Exemple de commande pour déplacer le plateau de 10 mm vers l'avant
        response = requests.post(f"http://{octoprint_ip}/api/printer/command", headers={"X-Api-Key": api_key}, json=payload)
        response.raise_for_status()
        print("Plateau avancé avec succès.")
    except Exception as e:
        print("Une erreur s'est produite lors du déplacement du plateau :", e)

# Fonction principale pour exécuter les mouvements
def execute_movements():
    move_head_up()
    time.sleep(10)
    move_bed_forward()
# Fonction pour exécuter les mouvements du bras robot
def move_robot(robot):
    # Exécuter les mouvements sur le bras robot Niryo
    try:
        execute_movements()
        conveyor_id = robot.set_conveyor()
        robot.move_joints([0.238, 0.037, -0.986,-0.005 , 0.644, 0.206])
        robot.open_gripper()
        time.sleep(0.5)
        robot.move_joints([0.171,-0.993 ,0.183 ,-0.170 ,0.644 ,0.200 ])
        time.sleep(0.5)
        robot.close_gripper()
        time.sleep(0.5)
        robot.move_joints([0.171,0.257 ,-1.108 ,-0.084 ,0.644 ,0.200 ])
        time.sleep(0.5)
        robot.move_joints([-0.728, -0.629, -0.492, -0.336, 0.650, 0.200])
        robot.open_gripper()
        time.sleep(0.5)
        robot.close_gripper()
        robot.move_joints([0.238, 0.037, -0.986,-0.005 , 0.644, 0.206])
        robot.run_conveyor(conveyor_id, speed=80, direction=ConveyorDirection.BACKWARD)
        time.sleep(10)
        robot.stop_conveyor(conveyor_id)

        print("Mouvements exécutés avec succès sur le bras robot Niryo.")
    except Exception as e:
        print("Une erreur s'est produite lors de l'exécution des mouvements sur le bras robot Niryo :", e)

# Fonction pour vérifier l'état de l'impression
def check_print_status():
    print("lancement")
    global a  # Déclarer a comme une variable globale
    global completion  # Déclarer completion comme une variable globale
    try:
        response = requests.get(f"http://{octoprint_ip}/api/job", headers={"X-Api-Key": api_key})
        data = response.json()  
        completion = data["progress"]["completion"]
        print("check du statut fait")
        if completion == 100 and a == 1:
            return True
        elif 1 <= completion <= 10:
            a = 1
            print("Impression en cours, a = 1")
    except Exception as e:
        print("Une erreur s'est produite lors de la récupération de l'état de l'impression :", e)
    return False

# Connexion au bras robot Niryo
robot = NiryoRobot(robot_ip)
print(robot)


#bouton home pour le plateau puis monter la tete puis avancer le plateau sans que ca tape


# Boucle principale
while True:
    if check_print_status():
        move_robot(robot)
        time.sleep(10) 
        a = 0
        print("En attente d'une nouvelle impression, a = 0")
    previous_print_completed = check_print_status()  # Mettre à jour l'état de l'impression précédente
    time.sleep(10)  # Attendre avant de vérifier à nouveau l'état de l'impression



banner = r"""
 .d8888888b.  
d88P"   "Y88b 
888  d8b  888 
888  888  888 
888  888bd88P 
888  Y8888P"  
Y88b.     .d8 
 "Y88888888P"
"""[1:]


# Anime.Fade(Center.Center(banner), Colors.purple_to_blue, Colorate.Vertical, time=1)



