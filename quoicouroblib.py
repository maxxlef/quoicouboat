import time
import sys
import os
import time
import numpy as np
import datetime
import csv
import json
import ast

# Assure-toi que les modules sont correctement importés
sys.path.append(os.path.join(os.path.dirname(__file__), 'drivers-ddboat-v2'))

import imu9_driver_v2 as imudrv
import arduino_driver_v2 as arddrv
import gps_driver_v2 as gpsdrv


# Création des objets IMU et Arduino et GPS
imu = imudrv.Imu9IO()
ard = arddrv.ArduinoIO()
gps=gpsdrv.GpsIO()
gps.set_filter_speed("0")

def sawtooth(x):
    return (x+np.pi)%(2*np.pi)-np.pi

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

def angles_euler(acc, mag):
    # Conversion de l'angle I en radians
    I = np.radians(64)  # Inclinaison magnétique en radians
    # Vecteurs de référence
    a0 = np.array([[0], [0], [1]])  # Vecteur vertical
    y0 = np.array([[np.cos(I)], [0], [-np.sin(I)]])  # Vecteur magnétique
    # Calcul des angles phi (roulis) et theta (tangage)
    #print("acc[1]: {}".format(acc[1]))
    #print("acc[0]: {}".format(acc[0]))
    phi = np.arcsin(acc[1]/np.linalg.norm(acc))  # Angle de roulis
    theta = -np.arcsin(acc[0]/np.linalg.norm(acc))  # Angle de tangage
    # Calcul de la matrice de rotation à partir de l'accéléromètre
    #  
    # Rotation du vecteur magnétique
    yh2 = mag
    yh1 = y0
    # Calcul de l'angle de lacet (psi)
    psi = -np.arctan2(yh2[0], yh1[0])
    psi = np.arctan2(mag[1],mag[0])
    return [phi, theta, psi]

def maintien_cap(acc,mag,cap,spd_base):
    psi = angles_euler(acc,mag)[2]
    err = sawtooth(cap-psi)
    Kd = 100
    correction = Kd*err
    spd_left = spd_base + correction
    spd_right = spd_base - correction
    if spd_left < 0:
        spd_left = 0
    if spd_right < 0:
        spd_right = 0
    if spd_left > 255:
        spd_left = 255
    if spd_right > 255:
        spd_right = 255
    print("Cap actuel du bateau: {}°, erreur: {}°".format(psi*180/np.pi,err*180/np.pi))
    print("Speed left = {}".format(spd_left))
    print("Speed right = {}".format(spd_right))
    #moteur droit qui pousse 
    ard.send_arduino_cmd_motor(spd_left,spd_right)

def depart():
    t0=time.time()
    while True:
        xaccel=accel()
        print(abs(time.time()-t0))
        if abs(xaccel[0])>8:
            break
        time.sleep(0.1)

def cap_waypoint(a,p):
    d = p - a
    cap_d = -np.arctan2(d[1],d[0])
    return cap_d

def arret_waypoint(a,p, distance_min = 2):
    d = np.linalg.norm(p - a)
    if d < distance_min:
        return True
    else:
        return False

# Fonction pour convertir les coordonnées degré-minute en degrés décimaux
def dms_to_decimal(degree_minutes, direction):
    degrees = int(degree_minutes // 100)
    minutes = degree_minutes % 100
    decimal_degrees = degrees + minutes / 60
    # Ajuster le signe selon la direction (N/S pour la latitude, E/W pour la longitude)
    if direction in ['S', 'W']:
        decimal_degrees *= -1
    return decimal_degrees

def mesure_gps(fichier="gps_data.txt"):
    data = []
    with open(fichier, "a") as file:  # Ouvrir le fichier en mode ajout (append)
        while True:
            gll_ok, gll_data = gps.read_gll_non_blocking()
            if gll_ok:
                # Écrire les données brutes dans le fichier
                file.write("{}\n".format(gll_data))
                # Conversion des coordonnées
                lat, long = dms_to_decimal(gll_data[0], 'N'), dms_to_decimal(gll_data[2], 'W')
                # Retourner les données actuelles si nécessaire
                return lat, long

    
def create_csv(input_file, output_csv_path):
    # Ouvrir le fichier d'entrée
    with open(input_file, 'r') as file:
        file_content = file.read()

    # Ouvrir le fichier CSV de sortie en écriture
    with open(output_csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Écrire l'en-tête
        csv_writer.writerow(['Latitude', 'Longitude'])
        
        # Lire chaque ligne du fichier et traiter les données
        for line in file_content.strip().split('\n'):
            # Convertir la ligne en une liste (suppression des crochets et découpage par virgules)
            data = eval(line.strip())
            
            # Extraire la latitude et la longitude au format degré-minute
            latitude_dm, lat_dir, longitude_dm, long_dir = data[:4]
            
            # Convertir en degrés décimaux
            latitude = (latitude_dm, lat_dir)
            longitude = (longitude_dm, long_dir)
            
            # Écrire les données converties dans le fichier CSV
            csv_writer.writerow([latitude, longitude])

    print("Fichier CSV généré avec succès : {}".format(output_csv_path))


def afficher_data(csv_file, output_geojson_file):
    # Initialiser une structure GeoJSON
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    # Ouvrir le fichier CSV et lire les coordonnées GPS
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            latitude = float(row['Latitude'])
            longitude = float(row['Longitude'])
            
            # Créer une nouvelle Feature (point) GeoJSON pour chaque ligne du CSV
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [longitude, latitude]  # Les coordonnées GeoJSON sont [long, lat]
                },
                "properties": {}  # Ajouter des propriétés supplémentaires ici si nécessaire
            }
            # Ajouter la feature à la collection
            geojson_data["features"].append(feature)

    # Écrire le GeoJSON dans un fichier
    with open(output_geojson_file, 'w') as geojson_file:
        json.dump(geojson_data, geojson_file, indent=4)

    print("Fichier GeoJSON généré avec succès : {}".format(output_geojson_file))

def deg_to_rad(angle):
    return angle*np.pi/180

# 48.1991663, -3.0146494 : point précédant du point M
def projection(ly,lx, lym = 48.199170, lxm = -3.014700, rho = 6371009.7714):
    """
    Convertit les coordonnées GPS (latitude, longitude) en coordonnées cartésiennes locales
    par rapport à un point M défini par lat_m et long_m, en ne retournant que x et y.
    """
    # Convertir les latitudes et longitudes en radians
    lat_m_rad = deg_to_rad(lym)
    long_m_rad = deg_to_rad(lxm)
    lat_rad = deg_to_rad(ly)
    long_rad = deg_to_rad(lx)
    # Conversion des coordonnées du point M (centre) en cartésiennes 2D (x_m, y_m)
    x_m = rho * np.cos(lat_m_rad) * np.cos(long_m_rad)
    y_m = rho * np.cos(lat_m_rad) * np.sin(long_m_rad)
    # Conversion des coordonnées du point P en cartésiennes 2D (x_p, y_p)
    x_p = rho * np.cos(lat_rad) * np.cos(long_rad)
    y_p = rho * np.cos(lat_rad) * np.sin(long_rad)
    # Calcul des coordonnées relatives par rapport au point M
    x = x_p - x_m
    y = y_p - y_m
    p = np.array([x,y])
    return p


def calculate_speed(d):
    # Limites des vitesses
    min_speed = 50
    max_speed = 200
    # Distance maximale considérée
    max_distance = 10  # Distance au-delà de laquelle la vitesse est maximale
    min_distance = 2
    # Calcul linéaire de la vitesse en fonction de d
    if d >= max_distance:
        return max_speed
    elif d <= min_distance:
        return min_speed
    # Vitesse linéairement proportionnelle à la distance
    speed = min_speed + (max_speed - min_speed) * (d / max_distance)
    return speed

def reach_point(ly, lx, distance_min = 2, filename ='points_p.csv'):
    # Ouvrir un fichier CSV en mode écriture
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['X', 'Y'])  # Écrire l'en-tête du fichier

        # Calcul du point cible A
        pts_a = projection(ly, lx)

        while True:
            ### Calcul du cap ###
            # Prise de données GPS et conversion dans le plan
            ly, lx = mesure_gps()
            pts_p = projection(ly, lx)

            # Écrire les coordonnées de P dans le fichier CSV
            writer.writerow([pts_p[0], pts_p[1]])

            # Calcul du cap
            cap_d = cap_waypoint(pts_a, pts_p, )
            print("Cap visé par cap_d : {}°".format(cap_d * 180 / np.pi))

            ### Calcul de la correction des moteurs ###
            # Récupération des mesures
            acc = accel()
            bouss = mag()

            # Calcul de la distance entre le point A et P
            d = np.linalg.norm(pts_a - pts_p)
            print("Distance : {}m".format(d))

            # Ajustement de la vitesse
            spd = calculate_speed(d)
            print("Vitesse nominale : {}".format(spd))

            # Maintien du cap
            maintien_cap(acc, bouss, cap_d, spd)

            # Condition d'arrêt
            if arret_waypoint(pts_a, pts_p, distance_min) == True:
                print("Arrêt car proche de la bouée")
                ard.send_arduino_cmd_motor(0, 0)
                return

            time.sleep(0.2)
            print("Finito pipo, points enregistrés dans {}".format(filename))


def lissajou(ly_bouee, lx_bouee, T=40, A=10, N=15, i=11):
    """lx_bouee est la longitude du centre de la figure,
    ly_bouee est la latitude du centre de la figure
    """
    # N Le nombre de points sur la boucle
    # i Numéro de notre point à suivre
    # A Amplitude en mètres (taille de la boucle)
    # T Période en secondes (temps nécessaire pour faire un tour complet)

    # Date et heure actuelle, puis calcul de midi aujourd'hui
    t0 = datetime.combine(datetime.today(), time(12, 0))
    t = datetime.now()

    # Delta de phase en fonction du point
    delta = T / N * i

    # Calcul des coordonnées (x, y) du point à un instant t
    elapsed_time = (t - t0).total_seconds()
    x = A * np.sin((elapsed_time + delta) / T * 2 * np.pi)
    y = A * np.sin(2 * (elapsed_time + delta) / T * 2 * np.pi)
    pd = np.array([x, y])
    # Calculer les coordonnées GPS en projetant les coordonnées de Lissajous
    lxa, lya = inverse_projection(pd, ly_bouee, lx_bouee)

    # Dérivées par rapport au temps (vitesse)
    x_derivee = (2 * np.pi / T) * A * np.cos((elapsed_time + delta) / T * 2 * np.pi)
    y_derivee = (4 * np.pi / T) * A * np.cos(2 * (elapsed_time + delta) / T * 2 * np.pi)
    pd_derivee = np.array([x_derivee, y_derivee])

    return pd, pd_derivee, lya, lxa

def inverse_projection(p, lym=48.1991663, lxm=-3.0146494, rho=6371009.7714):
    """Inverse la projection pour retourner les coordonnées GPS à partir des coordonnées locales."""
    # Convertir les latitudes et longitudes du point M en radians
    lat_m_rad = deg_to_rad(lym)
    long_m_rad = deg_to_rad(lxm)
    
    # Conversion des coordonnées du point P en coordonnées sphériques inverses
    x_p, y_p = p[0], p[1]
    x_m = rho * np.cos(lat_m_rad) * np.cos(long_m_rad)
    y_m = rho * np.cos(lat_m_rad) * np.sin(long_m_rad)

    # Inverser les calculs pour obtenir lat et long en radians
    x_abs = x_p + x_m
    y_abs = y_p + y_m

    lat_rad = np.arctan2(np.sin(lat_m_rad), np.cos(lat_m_rad))
    long_rad = np.arctan2(y_abs, x_abs)

    # Convertir en degrés
    lat = np.degrees(lat_rad)
    long = np.degrees(long_rad)

    return lat, long

def info_nav(pd,p,pd_derivee):
    e= pd - p
    norm_e = np.linalg.norm(e)
    k=1
    d = k* (e/norm_e * np.tanh(norm_e/5)  +  pd_derivee)
    cap_d = np.arctan2(d[1],d[0])
    norm_d= np.linalg.norm(d)
    return cap_d, norm_d

def vect_dte(pt_m,pt_b):
    return (pt_b-pt_m)/np.linalg.norm(pt_b-pt_m)

def cap_waypoint_2(a,p,n):
    e = n[0]*(p[1]-a[1]) - n[1]*(p[0]-a[0])
    phi = np.arctan2(n[1],n[0])
    print("phi cap waypoints{}".format(phi*180/np.pi))
    k = 2
    cap_d = phi - k*np.tanh(e/4)
    print("cap_d cap waypoints{}".format(cap_d*180/np.pi))
    return cap_d

def depasse_bouee(pt_bouee, p, n):
    if np.dot(pt_bouee-p,n)<0:
        return True
    else:
        return False
    
def suivre_droite(M, A):
    
    m = projection(M[0],M[1])
    a = projection(A[0], A[1])
    # Vecteur directeur de la droite (M,A)
    n = (a - m) / np.linalg.norm(a - m)

    # Temps après avoir passé la bouée
    temps_apres_bouee = None
    temps_suivi = 120  # 2 minutes = 120 secondes

    while True:
        # Lecture des coordonnées GPS actuelles
        ly, lx = mesure_gps()
        p = projection(ly,lx)

        # Calcul de l'erreur et du cap
        cap_d = cap_waypoint_2(a, p, n)

        # Distance à la bouée
        n_perp = np.array([-n[1], n[0]])
        distance = np.abs(np.dot(p - a, n_perp)) / np.linalg.norm(n_perp)
        print("Distance de la bouée: {}".format(distance))

        # Si le bateau a dépassé la bouée (position au-delà de A sur la droite)
        if a_depasse_bouee(a, p, n):
            print("##### Le bateau a passé le point #####")
            ard.send_arduino_cmd_motor(0, 0)  # Arrêter les moteurs
            return 

        # Calcul de la correction de cap et ajustement de la vitesse
        acc = accel()
        bouss = mag()
        maintien_cap(acc, bouss, cap_d, 150)  # Suivre la droite avec une vitesse de base de 150

        # Pause pour éviter une boucle trop rapide
        time.sleep(0.2)


def a_depasse_bouee(a, p, n):
    # Calcul du vecteur perpendiculaire à n (vecteur directeur de la droite (M, A))
    n_perp = np.array([-n[1], n[0]])  # Rotation de 90° dans le plan 2D

    # Projeter (p - a) sur n_perp pour savoir de quel côté de la droite perpendiculaire est le bateau
    vecteur_pa = p - a
    projection = np.dot(vecteur_pa, n_perp)

    # Si la projection est positive, le bateau est après la bouée
    return projection > 0


def attendre_exact_heure(heure, minute):
    # Obtenir l'heure actuelle
    maintenant = datetime.datetime.now()
    heure_actuelle = maintenant.hour
    minute_actuelle = maintenant.minute

    # Calculer le temps restant

    while True:      
        maintenant = datetime.datetime.now()
        heure_actuelle = maintenant.hour
        minute_actuelle = maintenant.minute

        delta = ((heure - heure_actuelle) * 3600) + ((minute - minute_actuelle) * 60) - maintenant.second
        if delta > 0:
            print("Attente de {} secondes pour atteindre {}h{}.".format(delta,heure,minute))
            time.sleep(1)
        else:
            break
    print("Il est {}h{} !".format(heure,minute))
    return True