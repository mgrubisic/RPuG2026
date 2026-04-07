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

# Zaglavlje tablice
print(f"{'Stup':>4} | {'D[m]':>6} | {'L0[m]':>6} | {'A[cm²]':>8} | "
      f"{'i[cm]':>7} | {'λ[-]':>6} | Kategorija")
print("=" * 75)

lambda_vrijednosti = []

for s in stupovi:
    A   = math.pi * s["D"]**2 / 4
    I   = math.pi * s["D"]**4 / 64
    i   = (I / A)**0.5
    lam = s["L0"] / i

    lambda_vrijednosti.append((s["oznaka"], lam))  # ispravna sintaksa

    if lam <= 25:
        kategorija = "Kratki stup    (izvijanje nije mjerodavno)"
    elif lam <= 50:
        kategorija = "Umjereno vitak (provjera 2. reda preporučena)"
    else:
        kategorija = "Vitak stup     (analiza 2. reda obavezna!)"

    print(f"{s['oznaka']:>4} | {s['D']:>6.2f} | {s['L0']:>6.2f} | "
          f"{A*1e4:>8.2f} | {i*1e2:>7.3f} | {lam:>6.1f} | {kategorija}")

print("=" * 75)

# Pronalazak ekstrema
najvitkiji = max(lambda_vrijednosti, key=lambda x: x[1])
najkraci   = min(lambda_vrijednosti, key=lambda x: x[1])
print(f"\nNajvitkiji stup: {najvitkiji[0]}  (λ = {najvitkiji[1]:.1f})")
print(f"Najkraći stup:   {najkraci[0]}  (λ = {najkraci[1]:.1f})")

