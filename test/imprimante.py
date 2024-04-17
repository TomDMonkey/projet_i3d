import requests
import time

# Configuration des adresses IP et de l'API key
octoprint_ip = "192.168.0.78"
api_key = "2A21B813752B46978D9DC9AE9F12A3D8"

# Fonction pour faire monter la tête d'impression
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
# def move_bed_forward():
#     try:
#         # Envoyer une commande Gcode pour avancer le plateau
#         payload = {"command": "G1 Y300"}  # Exemple de commande pour déplacer le plateau de 10 mm vers l'avant
#         response = requests.post(f"http://{octoprint_ip}/api/printer/command", headers={"X-Api-Key": api_key}, json=payload)
#         response.raise_for_status()
#         print("Plateau avancé avec succès.")
#     except Exception as e:
#         print("Une erreur s'est produite lors du déplacement du plateau :", e)
def move_bed_forward():
    try:
        # Envoyer une commande Gcode pour avancer le plateau
        payload = {"command": "G91"}  # Mode de positionnement relatif
        response = requests.post(f"http://{octoprint_ip}/api/printer/command", headers={"X-Api-Key": api_key}, json=payload)
        response.raise_for_status()

        # Avancer le plateau jusqu'à ce qu'il touche le capteur de collision
        payload = {"command": "G1 Y-300 F500"}  # Avancer le plateau de 300 mm/s
        response = requests.post(f"http://{octoprint_ip}/api/printer/command", headers={"X-Api-Key": api_key}, json=payload)
        response.raise_for_status()
        print("Plateau en mouvement vers l'arrière...")

        # Attendre que le mouvement soit terminé
        time.sleep(10)  # Vous pouvez ajuster le délai en fonction de la vitesse et de la distance

        # Retour à la position maximale
        payload = {"command": "G1 Y300 F500"}  # Reculer le plateau à sa position maximale
        response = requests.post(f"http://{octoprint_ip}/api/printer/command", headers={"X-Api-Key": api_key}, json=payload)
        response.raise_for_status()
        print("Plateau revenu à sa position maximale.")

    except Exception as e:
        print("Une erreur s'est produite lors du déplacement du plateau :", e)

# Fonction principale pour exécuter les mouvements
def execute_movements():
    move_head_up()
    time.sleep(10)
    move_bed_forward()

# Exécution des mouvements
execute_movements()
