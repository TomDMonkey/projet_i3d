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
        print(Fore.RED + "Une erreur s'est produite lors de la récupération de l'état de l'impression : " + Fore.RESET, e)
        return False

def launch_main_program(robot):
    global a
    while True:
        if check_print_status() and a == 1:
            move_robot(robot)
            time.sleep(10)
            a = 0
        elif check_print_status() and a == 0:
            a = 1
            print("Impression en cours, a = 1")
            time.sleep(10)
        else:
            a = 0
            print("en attente d'impression, a = 0")
            time.sleep(10)

def main_menu(robot):
    conveyor_id = None
    global a
    while True:
        print("        ")
        print("\######################## NIRYO ########################/")
        print("        ")
        print("Menu principal:")
        print("      1. Lancer le programme principal")
        print("      2. Programme test")
        print("      3. Position de base du robot")
        print("      4. Scan convoyeur")
        print("      6. Quitter ")
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
