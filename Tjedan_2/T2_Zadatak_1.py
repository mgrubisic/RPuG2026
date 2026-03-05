# %% ZADATAK 1: Provjera vitkoće i razvrstavanje stupova
# =============================================================================
#
#  Zadano je 5 armiranobetonskih stupova kružnog poprečnog presjeka.
#  Za svaki stup poznati su: promjer D [m] i slobodna duljina izvijanja L0 [m].
#
#  Za svaki stup izračunajte:
#    1) Površinu presjeka:       A  = pi * D^2 / 4          [m²]
#    2) Moment tromosti:         I  = pi * D^4 / 64         [m⁴]
#    3) Polumjer tromosti:       i  = sqrt(I / A)           [m]
#    4) Vitkoću stupa:           λ  = L0 / i                [-]
#
#  Na temelju vitkoće razvrstajte svaki stup prema EC2 kriteriju:
#    - λ ≤ 25          -->  "Kratki stup   (izvijanje nije mjerodavno)"
#    - 25 < λ ≤ 50     -->  "Umjereno vitak (provjera 2. reda preporučena)"
#    - λ > 50          -->  "Vitak stup    (analiza 2. reda obavezna!)"
#
#  Ispis neka bude u tabličnoj formi. Na kraju ispišite koji je stup
#  NAJVITKIJI i koji je NAJKRAĆI (najmanja vitkoća).
#
# =============================================================================

import math

stupovi = [
    {"oznaka": "S1", "D": 0.40, "L0": 4.50},    
    {"oznaka": "S2", "D": 0.30, "L0": 6.00},    
    {"oznaka": "S3", "D": 0.50, "L0": 3.50},    
    {"oznaka": "S4", "D": 0.35, "L0": 7.50},    
    {"oznaka": "S5", "D": 0.45, "L0": 5.00},    
    ]

# lambda_vrijednosti = []

for s in stupovi:
    A = math.pi * s["D"]**2 / 4
    I = math.pi * s["D"]**4 / 64
    i = (I / A)**0.5
    lam = s["L0"] / i

    # lambda_vrijednosti.append((s["oznaka"]), lam)

    print(lam)
    
    if lam <= 25:
        kategorija = "Kratki stup (izvijanje nije mjerodavno!)"
        print("Kratki stup (izvijanje nije mjerodavno!)")
    elif lam <= 50:
        print("Umjereno vitak stup (paziti na P-delta efekte!)")
    else:
        print("Vrlo vitak stup (analiza P-delta OBAVEZNA!)")






