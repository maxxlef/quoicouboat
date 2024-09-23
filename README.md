# Projet DDBoat - Quoicoucodes

Bienvenue dans le projet DDBoat ! Ce robot bateau est équipé d'une boussole, d'un accéléromètre, d'un GPS et de deux moteurs brushless. Il a été développé pour naviguer de manière autonome en suivant un cap ou en rejoignant des points GPS précis.

## Structure des fichiers

Certains fichiers portent des noms inspirés de notre bateau, affectueusement appelé Quoicouboat. Voici un aperçu des principaux fichiers et de leur rôle dans le projet :

1. **`quoicouroblib.py`**  
   Ce fichier est notre bibliothèque principale, utilisée pour contrôler les mouvements du bateau. Toutes les fonctions essentielles liées au contrôle des capteurs et des moteurs y sont définies. Chaque fichier Python nécessitant de contrôler le robot importera cette bibliothèque.

2. **`epreuve_1.py`**  
   Ce fichier met en œuvre le suivi d'un cap défini. Après la calibration, il permet au bateau de maintenir un cap donné (`cap_desire_deg`) pendant 30 secondes, d'attendre 30 secondes, puis de faire demi-tour. La fonction `maintient_cap()` de la bibliothèque `quoicouroblib.py` est utilisée pour maintenir la direction souhaitée.

3. **`epreuve_2.py`**  
   Une fois le GPS maîtrisé, ce fichier permet au bateau de rejoindre un point GPS donné. Il utilise la fonction `reach_point()` de notre bibliothèque `quoicouroblib.py` pour assurer la navigation autonome.

4. **`epreuve_3.py`**  
   Ce script met en œuvre la troisième épreuve du projet : suivre un point GPS mobile, se déplaçant selon une courbe de Lissajous. Les étapes sont les suivantes :  
   - **Calcul de la Trajectoire :** Utilisation de la fonction `lissajou()` pour déterminer la position du point GPS à suivre.  
   - **Projection des Coordonnées :** La fonction `inverse_projection()` est utilisée pour transformer les coordonnées de la courbe de Lissajous en latitude et longitude.  
   - **Navigation et Ajustement :** Avec la fonction `info_nav()`, le bateau ajuste sa vitesse et son cap pour suivre le point GPS mobile tout en anticipant sa trajectoire.

5. **`epreuve_4_2.py`**  
   Ce fichier implémente la quatrième épreuve : suivre une ligne droite entre deux points GPS sans déviation, en particulier pour des trajets plus longs où il y a plusieurs lignes droites. Il s'appuie sur les fonctionnalités existantes de `quoicouroblib.py` :  
   - **Correction de Cap :** La fonction `cap_waypoint_2()` ajuste le cap du bateau en fonction de la distance par rapport à la ligne droite définie.  
   - **Erreur Minimale :** La correction de cap est optimisée par une fonction tangente hyperbolique, minimisant ainsi la déviation du bateau par rapport à la ligne droite cible.

6. **`epreuve_4_1.py`**  
    Première version de l'épreuve 4 qui permet de suivre une seule ligne droite et s'arrête après 30s une fois que le bateau a passé la bouée.

7. **`epreuve_finale.py`**
   
8. **`calibration.py`**  
   La calibration de l'IMU, comprenant la boussole et l'accéléromètre, est effectuée avec ce script. Une fois lancé, il guide l'utilisateur à travers les étapes de calibration et sauvegarde les matrices de calibration et les biais dans des fichiers (`b_mag.npy`, `A_mag.npy`, `b_accel.npy`, `A_accel.npy`) pour une utilisation future.

9. **`geojson.py`**  
   Ce script convertit les mesures GPS du bateau, stockées dans un fichier `.txt`, en un fichier `.geojson` compatible avec [geojson.io](https://geojson.io/), permettant une visualisation facile des trajectoires sur une carte.

10. **`test_cap.py`**
   Ce fichier permet de vérifier la calibration de la boussole. On doit rentrer le cap voulu et ensuite on affiche en boucle l'erreur entre le cap actuel et le cap désiré.

11. **`test_mesures.py`**  
   Ce script nous a permis d'analyser les données des capteurs du bateau, notamment l'IMU (boussole et accéléromètre). En l'utilisant, nous avons pu nous assurer que l'axe Z de l'IMU était correctement orienté vers le haut du bateau.

12. **`test_projection.py`**  
   Ce fichier projette les coordonnées GPS en un plan local et enregistre chaque point dans un fichier `.csv`. Ce fichier peut ensuite être tracé à l'aide du script `tracer.py` pour une analyse visuelle.

13. **`tracer_lissajous.py`**  
    Ce script trace la courbe de Lissajous prévue pour la troisième épreuve et permet de visualiser la trajectoire idéale sur un graphique. Il est utilisé pour :  
    - **Validation de la Trajectoire :** Vérifier si le point GPS mobile suit la courbe de Lissajous attendue.  
    - **Analyse Post-Épreuve :** Comparer la trajectoire théorique à la trajectoire réelle du bateau pour évaluer les performances du suivi.

14. **`tracer.py`**  
    Ce fichier génère des graphiques à partir des données GPS collectées, permettant de visualiser les différentes épreuves :  
    - **Affichage des Trajectoires :** Trace les points GPS enregistrés dans les fichiers `.csv` générés par `test_projection.py`.  
    - **Comparaison des Résultats :** Compare les trajectoires obtenues avec les trajectoires théoriques pour évaluer la précision et la performance du bateau.

15. **`tstgps.py`**
   Ce fichier permet d'afficher les coordonnées du bateau dans le terminal.

  
