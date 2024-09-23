# Projet DDBoat - Quoicoucodes

Bienvenue dans le projet DDBoat ! Ce robot bateau est équipé d'une boussole, d'un accéléromètre, d'un GPS et de deux moteurs brushless. Il a été développé pour naviguer de manière autonome en suivant un cap ou en rejoignant des points GPS précis.

## Structure des fichiers

Certains fichiers portent des noms inspirés de notre bateau, affectueusement appelé Quoicouboat. Voici un aperçu des principaux fichiers et de leur rôle dans le projet :

1. **`quoicouroblib.py`**  
   Ce fichier est notre bibliothèque principale, utilisée pour contrôler les mouvements du bateau. Toutes les fonctions essentielles liées au contrôle des capteurs et des moteurs y sont définies. Chaque fichier Python nécessitant de contrôler le robot importera cette bibliothèque.

2. **`test_mesures.py`**  
   Ce script nous a permis d'analyser les données des capteurs du bateau, notamment l'IMU (boussole et accéléromètre). En l'utilisant, nous avons pu nous assurer que l'axe Z de l'IMU était correctement orienté vers le haut du bateau.

3. **`calibration.py`**  
   La calibration de l'IMU, comprenant la boussole et l'accéléromètre, est effectuée avec ce script. Une fois lancé, il guide l'utilisateur à travers les étapes de calibration et sauvegarde les matrices de calibration et les biais dans des fichiers (`b_mag.npy`, `A_mag.npy`, `b_accel.npy`, `A_accel.npy`) pour une utilisation future.

4. **`epreuve_1.py`**  
   Ce fichier met en œuvre le suivi d'un cap défini. Après la calibration, il permet au bateau de maintenir un cap donné (`cap_desire_deg`) pendant 30 secondes, d'attendre 30 secondes, puis de faire demi-tour. La fonction `maintient_cap()` de la bibliothèque `quoicouroblib.py` est utilisée pour maintenir la direction souhaitée.

5. **`geojson.py`**  
   Ce script convertit les mesures GPS du bateau, stockées dans un fichier `.txt`, en un fichier `.geojson` compatible avec [geojson.io](https://geojson.io/), permettant une visualisation facile des trajectoires sur une carte.

6. **`test_projection.py`**  
   Ce fichier projette les coordonnées GPS en un plan local et enregistre chaque point dans un fichier `.csv`. Ce fichier peut ensuite être tracé à l'aide du script `tracer.py` pour une analyse visuelle.

7. **`epreuve_2.py`**  
   Une fois le GPS maîtrisé, ce fichier permet au bateau de rejoindre un point GPS donné. Il utilise la fonction `reach_point()` de notre bibliothèque `quoicouroblib.py` pour assurer la navigation autonome.

8. **`epreuve_3.py`**  
   Ce script met en œuvre la troisième épreuve du projet : suivre un point GPS mobile, se déplaçant selon une courbe de Lissajous. Les étapes sont les suivantes :  
   - **Calcul de la Trajectoire :** Utilisation de la fonction `lissajou()` pour déterminer la position du point GPS à suivre.  
   - **Projection des Coordonnées :** La fonction `inverse_projection()` est utilisée pour transformer les coordonnées de la courbe de Lissajous en latitude et longitude.  
   - **Navigation et Ajustement :** Avec la fonction `info_nav()`, le bateau ajuste sa vitesse et son cap pour suivre le point GPS mobile tout en anticipant sa trajectoire.

9. **`epreuve_4.py`**  
   Ce fichier implémente la quatrième épreuve : suivre une ligne droite entre deux points GPS sans déviation. Il s'appuie sur les fonctionnalités existantes de `quoicouroblib.py` :  
   - **Correction de Cap :** La fonction `cap_waypoint_2()` ajuste le cap du bateau en fonction de la distance par rapport à la ligne droite définie.  
   - **Erreur Minimale :** La correction de cap est optimisée par une fonction tangente hyperbolique, minimisant ainsi la déviation du bateau par rapport à la ligne droite cible.

10. **`epreuve_4_2.py`**  
    Cette variante de l'épreuve 4 vise à améliorer encore la précision du suivi de ligne droite, en particulier pour des trajets plus longs ou avec des conditions environnementales variables :  
    - **Correction Dynamique :** Utilisation d'une correction dynamique basée sur l'erreur accumulée au fil du temps.  
    - **Contrôle Avancé des Moteurs :** Ajustements supplémentaires de la vitesse des moteurs pour corriger les écarts, en fonction des conditions actuelles du bateau et de la distance au point GPS final.

11. **`tracer_lissajous.py`**  
    Ce script trace la courbe de Lissajous prévue pour la troisième épreuve et permet de visualiser la trajectoire idéale sur un graphique. Il est utilisé pour :  
    - **Validation de la Trajectoire :** Vérifier si le point GPS mobile suit la courbe de Lissajous attendue.  
    - **Analyse Post-Épreuve :** Comparer la trajectoire théorique à la trajectoire réelle du bateau pour évaluer les performances du suivi.

12. **`tracer.py`**  
    Ce fichier génère des graphiques à partir des données GPS collectées, permettant de visualiser les différentes épreuves :  
    - **Affichage des Trajectoires :** Trace les points GPS enregistrés dans les fichiers `.csv` générés par `test_projection.py`.  
    - **Comparaison des Résultats :** Compare les trajectoires obtenues avec les trajectoires théoriques pour évaluer la précision et la performance du bateau.

13. **`reach_point.py`**  
    Ce script est un module spécifique pour rejoindre un point GPS précis. Il est utilisé dans plusieurs épreuves pour s'assurer que le bateau atteint le point cible :  
    - **Calcul de la Distance :** Détermine la distance actuelle au point GPS cible.  
    - **Ajustement du Cap et de la Vitesse :** Modifie dynamiquement le cap et la vitesse du bateau pour converger vers le point souhaité.  
    - **Arrêt Automatique :** Si le bateau est suffisamment proche du point cible (`distance_min`), il coupe les moteurs pour arrêter le bateau.

14. **`info_nav.py`**  
    Ce fichier contient des fonctions utiles pour obtenir des informations de navigation en temps réel :  
    - **Cap Actuel :** Récupère le cap actuel du bateau en utilisant la boussole calibrée.  
    - **Position GPS :** Obtenir la latitude et la longitude actuelles du bateau.  
    - **Calcul du Cap Désiré :** Calcule le cap nécessaire pour atteindre un point GPS cible.

15. **`inverse_projection.py`**  
    Ce script est utilisé pour transformer les points de coordonnées locales ou projetées en coordonnées GPS (latitude et longitude). Il est particulièrement utile dans les épreuves nécessitant des projections précises comme la courbe de Lissajous :  
    - **Transformation Locale -> GPS :** Convertit les coordonnées du plan local en latitude et longitude pour navigation.  
    - **Trajectoire en Temps Réel :** Utilisé en temps réel pour ajuster la trajectoire du bateau en fonction de son suivi de trajectoire.

