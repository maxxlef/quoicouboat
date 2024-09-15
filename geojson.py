import csv
import json
import os
import ast

"""
Ce fichier permet à partir d'un fichier txt contenant les données gps du capteurs de 
retourner un fichier geojson
"""
filename = 'gps_data.txt'


# Fonction pour convertir les coordonnées degré-minute en degrés décimaux
def dms_to_decimal(degree_minutes, direction):
    try:
        degrees = int(degree_minutes // 100)
        minutes = degree_minutes % 100
        decimal_degrees = degrees + minutes / 60
        if direction in ['S', 'W']:
            decimal_degrees *= -1
        return decimal_degrees
    except (ValueError, TypeError):
        print(f"Erreur lors de la conversion de {degree_minutes} en degrés décimaux")
        return None


def create_csv(input_file, output_csv_path):
    try:
        with open(input_file, 'r') as file:
            file_content = file.read()

        with open(output_csv_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Latitude', 'Longitude'])
            
            for line in file_content.strip().split('\n'):
                try:
                    data = ast.literal_eval(line.strip())  # Plus sûr que eval
                    latitude_dm, lat_dir, longitude_dm, long_dir = data[:4]
                    
                    latitude = dms_to_decimal(latitude_dm, lat_dir)
                    longitude = dms_to_decimal(longitude_dm, long_dir)
                    
                    if latitude is not None and longitude is not None:
                        csv_writer.writerow([latitude, longitude])
                except (SyntaxError, ValueError) as e:
                    print(f"Erreur lors du traitement de la ligne : {line}, {e}")
        print(f"Fichier CSV généré avec succès : {output_csv_path}")
    except FileNotFoundError:
        print(f"Erreur : fichier {input_file} introuvable.")
    except Exception as e:
        print(f"Erreur : {e}")


def afficher_data(csv_file, output_geojson_file):
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    try:
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    latitude = float(row['Latitude'])
                    longitude = float(row['Longitude'])
                    
                    feature = {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [longitude, latitude]  # GeoJSON [long, lat]
                        },
                        "properties": {}
                    }
                    geojson_data["features"].append(feature)
                except ValueError:
                    print(f"Erreur de conversion dans la ligne : {row}")
                    
        with open(output_geojson_file, 'w') as geojson_file:
            json.dump(geojson_data, geojson_file, indent=4)
        print(f"Fichier GeoJSON généré avec succès : {output_geojson_file}")
    except FileNotFoundError:
        print(f"Erreur : fichier {csv_file} introuvable.")
    except Exception as e:
        print(f"Erreur : {e}")

# Obtenir le chemin du dossier où se trouve le script Python
script_dir = os.path.dirname(os.path.realpath(__file__))

# Créer les chemins vers tes fichiers
input_file = os.path.join(script_dir, filename)
output_csv_file = os.path.join(script_dir, 'data_boat_converted.csv')
output_geojson_file = os.path.join(script_dir, 'points_gps.geojson')

# Exécuter les fonctions
create_csv(input_file, output_csv_file)
afficher_data(output_csv_file, output_geojson_file)
