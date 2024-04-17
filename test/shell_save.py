from pyniryo import *
from colorama import *
import requests
import time
import os
import sys
import time
from pystyle import *

octoprint_ip = "192.168.0.78"
robot_ip = "192.168.0.148"
octoprint_ip_externe = "btssnir.lycee-costebelle.fr:7651"
robot_ip_externe = "92.150.142.179:40001"
api_key = "2A21B813752B46978D9DC9AE9F12A3D8"
previous_print_completed = True
completion = None 
a = 0  

############################# IMPRIMANTE #############################
def move_head_up():
    try:
        payload = {"command": "G1 Z60"} 
        response = requests.post(f"http://{octoprint_ip}/api/printer/command", headers={"X-Api-Key": api_key}, json=payload)
        response.raise_for_status()
        print("Tête d'impression déplacée vers le haut avec succès.")
    except Exception as e:
        print(Fore.RED +" Une erreur s'est produite lors du déplacement de la tête d'impression :"+ Fore.RESET, e)

def move_bed_forward():
    try:
        payload = {"command": "G28 Y"} 
        response = requests.post(f"http://{octoprint_ip}/api/printer/command", headers={"X-Api-Key": api_key}, json=payload)
        payload = {"command": "G1 Y230"}  
        response = requests.post(f"http://{octoprint_ip}/api/printer/command", headers={"X-Api-Key": api_key}, json=payload)
        response.raise_for_status() 
        
        print("Plateau centré avec succès.")
    except Exception as e:
        print(Fore.RED + " Une erreur s'est produite lors du centrage du plateau :"+ Fore.RESET, e)

def execute_movements():
    move_head_up()
    time.sleep(10)
    move_bed_forward()
    time.sleep(8)

def check_print_status():
    global completion
    try:
        response = requests.get(f"http://{octoprint_ip}/api/job", headers={"X-Api-Key": api_key})
        data = response.json()
        completion = data["progress"]["completion"]
        if completion == 100:
            return True
        else:
            return False
    except Exception as e:
        print(Fore.RED + " Une erreur s'est produite lors de la récupération de l'état de l'impression : " + Fore.RESET, e)
        return False

############################# MOUVEMENT ROBOT #############################
def launch_main_program(robot):
    robot.move_joints([0.238, 0.037, -0.986, -0.005, 0.644, 0.206])

    global a
    while True:
        if check_print_status() and a == 1:
            move_robot(robot)
            time.sleep(10)
            a = 0
        elif 1 <= completion <= 10: 
            a = 1
            clear_console()

            print("Impression en cours, a = 1")
            time.sleep(2)
        elif a == 0:
            clear_console()
            print("en attente d'impression, a = 0")
            time.sleep(2)

            

def move_robot(robot):
    try:
        print("depart mouvement de la tete  ")
        robot.release_with_tool()
        execute_movements()
        print("demarage du mouvement ")
        robot.move_joints([0.238, 0.037, -0.986, -0.005, 0.644, 0.206])
        robot.open_gripper()
        time.sleep(0.5)
        robot.move_joints([0.171, -0.993, 0.183, -0.170, 0.644, 0.200])
        time.sleep(0.5)
        robot.close_gripper()
        time.sleep(0.5)
        robot.move_joints([0.171, 0.257, -1.108, -0.084, 0.644, 0.200])
        time.sleep(0.5)
        robot.move_joints([-0.728, -0.629, -0.492, -0.336, 0.650, 0.200])
        robot.open_gripper()
        time.sleep(0.5)
        robot.close_gripper()
        robot.move_joints([0.238, 0.037, -0.986, -0.005, 0.644, 0.206])
        robot.run_conveyor(conveyor_id, speed=80, direction=ConveyorDirection.BACKWARD)
        time.sleep(10)
        robot.stop_conveyor(conveyor_id)
        print( Fore.GREEN + "Mouvements exécutés avec succès sur le bras robot Niryo."+ Fore.RESET)
    except Exception as e:
        # clear_console()
        print(Fore.RED +"Une erreur s'est produite lors de l'exécution des mouvements sur le bras robot Niryo :" + Fore.RESET, e)

def test_move(robot):
    try:
        robot.release_with_tool()
        robot.move_joints([0.238, 0.037, -0.986, -0.005, 0.644, 0.206])
        robot.open_gripper()
        time.sleep(0.5)
        robot.move_joints([-1.746, 0.071, -0.125, 1.021, 0.644, 0.207])
        robot.close_gripper()
        robot.move_joints([0.238, 0.037, -0.986, -0.005, 0.644, 0.206])
        robot.run_conveyor(conveyor_id, speed=80, direction=ConveyorDirection.BACKWARD)
        time.sleep(10)
        robot.stop_conveyor(conveyor_id)

        print("Test mouvement exécuté.")
    except Exception as e:
        clear_console()

        print(Fore.RED + "Une erreur s'est produite lors de l'exécution du test :"+ Fore.RESET, e)

def position_base(robot):
    try:
        robot.move_joints([0.238, 0.037, -0.986, -0.005, 0.644, 0.206])
        print(Fore.GREEN + "Position de base du bras : OK" + Fore.RESET)
        
        clear_console()
        
    except Exception as e:
        print(Fore.RED + "Une erreur s'est produite lors de la remise en position de base du robot:" + Fore.RESET, e)

def leave(robot, conveyor_id):
    if conveyor_id is not None:
        robot.unset_conveyor(conveyor_id)
        robot.go_to_sleep()
        robot.close_connection()
        sys.exit()

############################# MENU  #############################
def main_menu(robot):
    # conveyor_id = None

    global a
    while True:
        clear_console()

        print("        ")
        print(Fore.BLUE+"\######################## NIRYO ########################/"+ Fore.RESET)
        print("        ")
        print("convoyeur : ", conveyor_id)

        print("     Menu principal:")
        print("         1. Lancer le programme principal")
        print("         2. Programme test")
        print("         3. Position de base du robot")
        print("         4. Scan convoyeur")
        print("         6. Quitter ")
        print("        ")
        choice = input("Entrez le numéro de votre choix: ")
        if choice == "1":
            launch_main_program(robot)
        elif choice == "2":
            test_move(robot)
        elif choice == "3":
            position_base(robot)
        elif choice == "4":
            conveyor_scan()
        elif choice == "6":
            leave(robot, conveyor_id)
        else:
            print(Fore.RED + "Choix invalide. Veuillez entrer un numéro valide." + Fore.RESET)

############################# ANNEXE #############################

# def switch_connexion():


def loading_bar(duration=1.3):
    start_time = time.time()
    sys.stdout.write("[") 
    while time.time() - start_time < duration:
        sys.stdout.write("|") 
        sys.stdout.flush()  
        time.sleep(0.02) 
    sys.stdout.write("\n")
    sys.stdout.flush()

def conveyor_scan():
    robot.update_tool()
    conveyor_id = robot.set_conveyor()
    print("convoyeur : ", conveyor_id)
    clear_console()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    


############################# MAIN PROGRAMME #############################
robot = NiryoRobot(robot_ip)
robot.calibrate_auto()
robot.update_tool()
conveyor_id = robot.set_conveyor()
print("convoyeur : ", conveyor_id)
loading_bar(1.3)
clear_console()
main_menu(robot)


