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

### Test pour le départ ###
rb.depart()
print("Go!!!")

t0loop = time.time()
#### Maintient cap pendant 30s NW ###
time_start = time.time()
time_actuel = time.time()
cap_desire_deg = -45
cap_desire = float(cap_desire_deg)*np.pi/180
while time_actuel - time_start < 30:
    time_actuel = time.time()
    rb.mesure_gps()
    print("Le cap voulu est : {}°".format(cap_desire_deg))
    acc = rb.accel()
    bouss = rb.mag()
    spd = 200
    rb.maintien_cap(acc,bouss,cap_desire,spd)
    time.sleep(0.2)

### Attendre 30s à l'arrêt ###
spdleft = 0
spdright = 0
ard.send_arduino_cmd_motor(spdleft, spdright)
time_start = time.time()
time_actuel = time.time()
while time_actuel - time_start < 30:
    time_actuel = time.time()
    rb.mesure_gps()
    "ne rien faire"

### Maintient cap pendant 30s SE ###
time_start = time.time()
time_actuel = time.time()
cap_desire_deg = 135
cap_desire = float(cap_desire_deg)*np.pi/180
while time_actuel - time_start < 30:
    time_actuel = time.time()
    rb.mesure_gps()
    print("Le cap voulu est : {}°".format(cap_desire_deg))
    acc = rb.accel()
    bouss = rb.mag()
    spd = 200
    rb.maintien_cap(acc,bouss,cap_desire,spd)
    time.sleep(0.2)

### Arrêt du bateau ###
spdleft = 0
spdright = 0
ard.send_arduino_cmd_motor(spdleft, spdright)

print("fin")

