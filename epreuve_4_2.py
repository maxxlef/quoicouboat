import numpy as np
import quoicouroblib as rb

# Coordonnées du ponton (M) et de la bouée (A)
M = np.array([48.199170, -3.014700])
A = np.array([48.1996872 , -3.0153766])
B = np.array([48.2006278, -3.0167036])
C = np.array([48.201944, -3.014722])

# Lancer la fonction de suivi de la droite
print("##################   Direction la bouéee A")
rb.suivre_droite(M,A)
print("##################   Arrivé à la bouée A")
print("##################   Direction la bouéee B")
rb.suivre_droite(A,B)
print("##################   Arrivé à la bouée B")
print("##################   Direction la bouéee C")
rb.suivre_droite(B,C)
print("##################   Arrivé à la bouée C")
print("##################   Direction la bouéee B")
rb.suivre_droite(C,B)
print("##################   Arrivé à la bouée B")
print("##################   Direction la bouéee A")
rb.suivre_droite(B,A)
print("##################   Arrivé à la bouée A")
print("##################   Direction la bouéee M")
rb.suivre_droite(A,M)
print("##################   Arrivé à la bouée M")


