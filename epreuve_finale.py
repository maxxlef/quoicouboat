import time
import numpy as np
import datetime
import quoicouroblib as rb

def attendre_exact_heure(heure, minute):
    # Obtenir l'heure actuelle
    maintenant = datetime.datetime.now()
    heure_actuelle = maintenant.hour
    minute_actuelle = maintenant.minute

    # Calculer le temps restant avant 9h53

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

A = [48.1996872,-3.0153766666666666]
ly , lx= A[0],A[1]

def epreuve_finale(ly, lx):
    if attendre_exact_heure(11,26):
        rb.reach_point(ly, lx, 40)
    if attendre_exact_heure(11,28):
        rb.reach_point(ly,lx,1)
    return

epreuve_finale(ly,lx)