# =============================================================================
#  Računalno programiranje u građevinarstvu (254810)
#  Tjedan 2/15 --- Vježba: Petlje i grananja
#  Sveučilište J. J. Strossmayera u Osijeku
#  Građevinski i arhitektonski fakultet Osijek (GrAFOS)
#  Izv. prof. dr. sc. Marin Grubišić | marin.grubisic@gfos.hr
# =============================================================================


# %% ZADATAK --- Provjera nosivosti greda okvirne konstrukcije
# =============================================================================

"""
ZADATAK: Provjera nosivosti greda okvirne konstrukcije
======================================================

Zadane su četiri armiranobetonske grede jednokatne okvirne
konstrukcije. Za svaku gredu poznati su sljedeći podaci:

    Greda  |  L [m]  |  b [m]  |  h [m]  |  q [kN/m]
    -------|---------|---------|---------|----------
      G1   |   5.0   |  0.30   |  0.50   |   20.0
      G2   |   6.5   |  0.35   |  0.60   |   25.0
      G3   |   4.0   |  0.25   |  0.45   |   15.0
      G4   |   7.0   |  0.40   |  0.65   |   30.0

Projektna tlačna čvrstoća betona: fcd = 20.0 MPa

Pohranite podatke u listu rječnika. Zatim napišite petlju
koja za svaku gredu izračunava:

    1) Maksimalni moment savijanja:
            M_max = q * L² / 8          [kNm]

    2) Moment otpora presjeka:
            W = b * h² / 6              [m³]

    3) Naprezanje od savijanja:
            sigma = M_max / (W * 1000)  [MPa]

    4) Iskorištenost presjeka:
            eta = sigma / fcd * 100     [%]

Za svaku gredu ispišite rezultate u tabličnoj formi te
koristeći grananje (if/elif/else) odredite status:

    - eta <= 60 %          -->  "Nisko iskorišten"
    - 60 % < eta <= 85 %   -->  "Umjereno iskorišten"
    - 85 % < eta <= 100 %  -->  "Visoko iskorišten"
    - eta > 100 %          -->  "PREKORAČENJE !"

Na kraju pronađite i ispišite gredu s najvećim naprezanjem.
"""

grede = [
    {"oznaka": "G1", "duljina": 5.0, "sirina": 0.3, "visina": 0.5, "opterecenje": 20.0},
    {"oznaka": "G2", "duljina": 6.5, "sirina": 0.35, "visina": 0.6, "opterecenje": 25.0},
    {"oznaka": "G3", "duljina": 4.0, "sirina": 0.25, "visina": 0.45, "opterecenje": 15.0},
    {"oznaka": "G4", "duljina": 15.0, "sirina": 0.4, "visina": 0.65, "opterecenje": 30.0}
    ]

fcd = 20.0 # [MPa]

for g in grede:
    
    # Proračun
    M_max = g["opterecenje"] * g["duljina"]** 2 / 8  # [kNm]
    # print(M_max)
    W = (g["sirina"] * g["visina"]**2) / 6 # [m3]
    # print(W)
    naprezanje = M_max / (W*1000) # [MPa]
    # print(naprezanje)
    eta = (naprezanje / fcd) # Faktor iskorištenosti!
    # print(f"{eta:.1%}")
    
    if eta <= 0.6:
        status = "Nisko iskorišten!"
    elif eta <= 0.85:
        status = "Umjereno iskorišten!"
    elif eta <= 1:
        status = "Visoko iskorišten!"
    else:
        status = "PREKORAČENJE NOSIVOSTI!"
    
    
    print(f"{g['oznaka']:>5} | {M_max:>8.2f} | {eta:>7.1%} | {status}")











