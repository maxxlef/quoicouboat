import sys
import os
import time
import numpy as np

# Assure-toi que les modules sont correctement importés
sys.path.append(os.path.join(os.path.dirname(__file__), 'drivers-ddboat-v2'))

import imu9_driver_v2 as imudrv
import arduino_driver_v2 as arddrv
import gps_driver_v2 as gpsdrv

# Création des objets IMU et Arduino
imu = imudrv.Imu9IO()
ard = arddrv.ArduinoIO()

"""
Fichier pour comprendre quelles sont les données renvoyées par les cateurs
"""

def mag():
    xmag, ymag, zmag = imu.read_mag_raw()
    x = np.array([xmag, ymag, zmag])
    b = np.load("b_mag.npy")
    A = np.load("A_mag.npy")
    A_inv = np.linalg.inv(A)
    y = np.dot(A_inv,(x+b))
    return y

def accel():
    xaccel, yaccel, zaccel = imu.read_accel_raw()
    #print(xaccel)
    x = np.array([xaccel, yaccel, zaccel])
    #("X={}".format(x))
    b = np.load("b_accel.npy")
    A = np.load("A_accel.npy")
    A_inv = np.linalg.inv(A)
    y = np.dot(A_inv,(x+b))
    return y

print("Début")
nb_s = input("Pendant combien de seconde vous voulez afficher les mesures ? ")
i=0
while i<nb_s:
    i+=1
    x_mag = mag()
    print("X_mag mesuré : {}".format(x_mag))
    x_accel = accel()
    #print("X_accel mesuré : {}".format(x_accel) )
    time.sleep(1)
    
