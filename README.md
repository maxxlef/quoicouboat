# Projet DDBoat - Quoicoucodes

Bienvenue dans le projet **DDBoat** ! Ce robot bateau est équipé d'une boussole, d'un accéléromètre, d'un GPS et de deux moteurs brushless. Il a été développé pour naviguer de manière autonome en suivant un cap ou en rejoignant des points GPS précis.

## Structure des fichiers
Certains fichiers portent des noms inspirés de notre bateau, affectueusement appelé **Quoicouboat**. Voici un aperçu des principaux fichiers et de leur rôle dans le projet :

### 1. `quoicouroblib.py`
Ce fichier est notre bibliothèque principale, utilisée pour contrôler les mouvements du bateau. Toutes les fonctions essentielles liées au contrôle des capteurs et des moteurs y sont définies. Chaque fichier Python nécessitant de contrôler le robot importera cette bibliothèque.

### 2. `test_mesures.py`
Ce script nous a permis d'analyser les données des capteurs du bateau, notamment l'IMU (boussole et accéléromètre). En l'utilisant, nous avons pu nous assurer que l'axe Z de l'IMU était correctement orienté vers le haut du bateau.

### 3. `calibration.py`
La calibration de l'IMU, comprenant la boussole et l'accéléromètre, est effectuée avec ce script. Une fois lancé, il guide l'utilisateur à travers les étapes de calibration et sauvegarde les matrices de calibration et les biais dans des fichiers (`b_mag.npy`, `A_mag.npy`, `b_accel.npy`, `A_accel.npy`) pour une utilisation future.

### 4. `epreuve_1.py`
Ce fichier met en œuvre le suivi d'un cap défini. Après la calibration, il permet au bateau de maintenir un cap donné (`cap_desire_deg`) pendant 30 secondes, d'attendre 30 secondes, puis de faire demi-tour. La fonction `maintient_cap()` de la bibliothèque `quoicouroblib.py` est utilisée pour maintenir la direction souhaitée.

### 5. `geojson.py`
Ce script convertit les mesures GPS du bateau, stockées dans un fichier .txt, en un fichier `.geojson` compatible avec [geojson.io](https://geojson.io/), permettant une visualisation facile des trajectoires sur une carte.

### 6. `test_projection.py`
Ce fichier projette les coordonnées GPS en un plan local et enregistre chaque point dans un fichier `.csv`. Ce fichier peut ensuite être tracé à l'aide du script `tracer.py` pour une analyse visuelle.

### 7. `epreuve_2.py`
Une fois le GPS maîtrisé, ce fichier permet au bateau de rejoindre un point GPS donné. Il utilise la fonction `reach_point()` de notre bibliothèque `quoicouroblib.py` pour assurer la navigation autonome.

### 8. Courbe de Lissajous
L'étape finale consiste à programmer le bateau pour qu'il suive un point GPS en mouvement, notamment une courbe de Lissajous. Ce challenge met en pratique tout ce qui a été développé précédemment.


