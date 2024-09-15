import time
import sys
import os
import time
import numpy as np
import quoicouroblib as rb

"""
Fichier pour tester la calibration de notre boussole
"""

# Assure-toi que les modules sont correctement importés
sys.path.append(os.path.join(os.path.dirname(__file__), 'drivers-ddboat-v2'))

import imu9_driver_v2 as imudrv
import arduino_driver_v2 as arddrv

# Création des objets IMU et Arduino
imu = imudrv.Imu9IO()
ard = arddrv.ArduinoIO()

cap_desire_deg = input("Rentrer le cap désiré en degrés :")
cap_desire = float(cap_desire_deg)*np.pi/180
while True:
    print("Le cap voulu est : {}°".format(cap_desire_deg))
    acc = rb.accel()
    bouss = rb.mag()
    spd = 0
    rb.maintien_cap(acc,bouss,cap_desire,spd)
    time.sleep(0.5)








