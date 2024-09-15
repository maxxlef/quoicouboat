import time
import sys
import os
import numpy as np
import csv
import quoicouroblib as rb

# Assure-toi que les modules sont correctement importés
sys.path.append(os.path.join(os.path.dirname(__file__), 'drivers-ddboat-v2'))

import imu9_driver_v2 as imudrv
import arduino_driver_v2 as arddrv

# Création des objets IMU et Arduino
imu = imudrv.Imu9IO()
ard = arddrv.ArduinoIO()

"""
Ce fichier permet de comprendre comment fonctionne la projection dans un plan local,
le fichier csv qui est retourné peut être tracé grâce au ficher 'tracer.py'
"""

lya, lxa = 48.198724, -3.014025
a = rb.projection(lya, lxa)

print("Le point GPS voulu est : 48.198634, -3.014070 ")
print("Ces coordonnées dans le plan sont : {}".format(a))

filename = 'points_projection.csv'

# Ouvrir le fichier CSV en mode écriture
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['X', 'Y'])  # Écrire l'en-tête du fichier
    
    try:
        while True:
            time.sleep(0.5)
            ly, lx = rb.mesure_gps()
            print("Mesure GPS du point p: lx ={}, ly ={}".format(lx, ly))
            p = rb.projection(ly, lx)
            # Écrire les coordonnées de P dans le fichier CSV
            writer.writerow([p[0], p[1]])
            print("Les coordonnées de P dans le plan : {}".format(p))
            print("Les coordonnées de A dans le plan : {}".format(a))
            d = a - p
            distance = np.linalg.norm(a - p)
            print("Distance au point A : {}".format(distance))
                        # Calcul du cap
            cap_d = rb.cap_waypoint(a, p)
            print("Cap visé par cap_d : {}°".format(cap_d * 180 / np.pi))

            ### Calcul de la correction des moteurs ###
            # Récupération des mesures
            acc = rb.accel()
            bouss = rb.mag()
            # Ajustement de la vitesse
            spd = 0
            # Maintien du cap
            rb.maintien_cap(acc, bouss, cap_d, spd)

            # Condition d'arrêt
            if rb.arret_waypoint(a, p) == True:
                print("La bouée à atteint le point gps")
                ard.send_arduino_cmd_motor(0, 0)

    except KeyboardInterrupt:
        print("Programme interrompu par l'utilisateur.")
