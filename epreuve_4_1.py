import time
import sys
import os
import numpy as np

import quoicouroblib as rb

# Assure-toi que les modules sont correctement importés
sys.path.append(os.path.join(os.path.dirname(__file__), 'drivers-ddboat-v2'))

import imu9_driver_v2 as imudrv
import arduino_driver_v2 as arddrv

# Création des objets IMU et Arduino
imu = imudrv.Imu9IO()
ard = arddrv.ArduinoIO()

# Coordonnées du ponton (M) et de la bouée (A)
M = np.array([48.199170, -3.014700])
A = np.array([48.1996872 , -3.0153766])

def suivre_droite(M, A):
    
    m = rb.projection(M[0],M[1])
    a = rb.projection(A[0], A[1])
    # Vecteur directeur de la droite (M,A)
    n = (a - m) / np.linalg.norm(a - m)

    # Temps après avoir passé la bouée
    temps_apres_bouee = None
    temps_suivi = 120  # 2 minutes = 120 secondes

    while True:
        # Lecture des coordonnées GPS actuelles
        ly, lx = rb.mesure_gps()
        p = rb.projection(ly,lx)

        # Calcul de l'erreur et du cap
        cap_d = rb.cap_waypoint_2(a, p, n)

        # Distance à la bouée
        distance_bouee = np.linalg.norm(a - p)
        print("Distance de la bouée: {}".format(distance_bouee))

        # Si le bateau a dépassé la bouée (position au-delà de A sur la droite)
        if np.dot(a-p, n) < 0:
            if temps_apres_bouee is None:
                temps_apres_bouee = time.time()  # Commencer le chronomètre après avoir passé la bouée

            # Vérifier si 2 minutes se sont écoulées depuis le passage de la bouée
            if time.time() - temps_apres_bouee >= temps_suivi:
                print("2 minutes écoulées, arrêt du bateau.")
                ard.send_arduino_cmd_motor(0, 0)  # Arrêter les moteurs
                break

        # Calcul de la correction de cap et ajustement de la vitesse
        acc = rb.accel()
        mag = rb.mag()
        rb.maintien_cap(acc, mag, cap_d, 150)  # Suivre la droite avec une vitesse de base de 150

        # Pause pour éviter une boucle trop rapide
        time.sleep(0.2)

# Lancer la fonction de suivi de la droite
suivre_droite(M, A)
