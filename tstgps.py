import sys
import os



"""
Affiche 5 mesures du gps dès que le programme est lancé
"""

sys.path.append(os.path.join(os.path.dirname(__file__), 'drivers-ddboat-v2'))
import gps_driver_v2 as gpsdrv
gps=gpsdrv.GpsIO()
gps.set_filter_speed("0")
cnt=0
while True:
    gll_ok,gll_data=gps.read_gll_non_blocking()
    if gll_ok:
        print(gll_data)
        cnt+=1
        if cnt==5:
            break