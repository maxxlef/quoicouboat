import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), 'drivers-ddboat-v2'))
import gps_driver_v2 as gpsdrv
gps=gpsdrv.GpsIO()
gps.set_filter_speed("0")

"""
Ce fichier permet de comprendre ce que nous renvoie la boussole, 
renvoie un fichier .txt avec les données reçues, elles peuvent être converties en fichier
geojson grâce au fichier 'geojson.py'
"""

data=[]
t0=time.time()
while True:
    if time.time()-t0>300:
        break
    gll_ok,gll_data=gps.read_gll_non_blocking()
    if gll_ok:
        data.append(gll_data)
        time.sleep(5)
        
with open('data_stade.txt', 'w') as file:
    for line in data:
        file.write(str(line) + '\n')
