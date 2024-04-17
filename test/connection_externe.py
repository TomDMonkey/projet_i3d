import requests

def connect_to_external_ips():

    octoprint_local_ip = "192.168.0.78"
    robot_local_ip = "192.168.0.148"
    octoprint_ip_externe = "btssnir.lycee-costebelle.fr:7651"
    robot_ip_externe = "192.168.0.148:40001"

  
    try:
        # Essayer de se connecter à l'adresse IP locale
        octoprint_response = requests.get(f"http://{octoprint_local_ip}")
        robot_response = requests.get(f"http://{robot_local_ip}")
        if octoprint_response.ok and robot_response.ok:
            
    except requests.exceptions.RequestException:
        pass

    try:
        # Si la connexion locale échoue, essayer les adresses IP externes
        octoprint_response = requests.get(octoprint_ip_externe)
        robot_response = requests.get(robot_ip_externe)
        if octoprint_response.ok and robot_response.ok:
            return octoprint_ip_externe, robot_ip_externe
    except requests.exceptions.RequestException:
        pass

    # Si aucune connexion n'a réussi, retourner None pour les deux IP
    return None, None

# Exemple d'utilisation de la fonction
octoprint_ip, robot_ip = connect_to_external_ips()
if octoprint_ip and robot_ip:
    print(f"Connexion réussie à octoprint : {octoprint_ip} et au robot : {robot_ip}")
else:
    print("Impossible de se connecter aux adresses IP.")



