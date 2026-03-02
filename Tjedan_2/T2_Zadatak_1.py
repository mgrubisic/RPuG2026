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
