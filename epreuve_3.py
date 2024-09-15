import time
import sys
import os
import time
import numpy as np
import quoicouroblib as rb


# Assure-toi que les modules sont correctement importés
sys.path.append(os.path.join(os.path.dirname(__file__), 'drivers-ddboat-v2'))

import imu9_driver_v2 as imudrv
import arduino_driver_v2 as arddrv

# Création des objets IMU et Arduino
imu = imudrv.Imu9IO()
ard = arddrv.ArduinoIO()


t0=time.time()
while True:
    ### Calcul du point A qui bouge###
    # Centre de la figure
    ly0,lx0 = 48.1996872, -3.0153766
    #calcul changement pts_a
    pd, pd_derivee, lya, lxa = rb.lissajou(ly0,lx0)
    a=rb.projection(lya,lxa)

    ### Calcul du cap ###
    #prise de données gps et conversion dans le plan
    ly,lx = rb.mesure_gps()
    p = rb.projection(ly,lx)
    # Calcul du cap
    cap_d, spd = rb.info_nav(a,p,pd_derivee)
    print("Cap visé par cap_d : {}°".format(cap_d*180/np.pi))
    print("La vitesse donné par norm_d : {}".format(spd))

    ### Calcul de la correction des moteurs ###
    # Récupération des mesures
    acc = rb.accel()
    bouss = rb.mag()
    # Calcul de la distance entre le point A et P
    dist = np.linalg.norm(a-p)
    print("Distance : {}m".format(dist))
    # Ajustement de la vitesse
    print("Speed : {}".format(spd))
    rb.maintien_cap(acc,bouss,cap_d,spd)
    # Condition d'arrêt
    if time.time()- t0>400:
        print("Arrêt pas le temps de gnaiser")
        ard.send_arduino_cmd_motor(0,0)
        break
    time.sleep(0.2)

print("finito pipo")