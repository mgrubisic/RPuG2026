# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 10:03:52 2026

@author: mgrubisic
"""

# =============================================================================
#  Računalno programiranje u građevinarstvu (254810) | Tjedan 4/15
#  Radionica: NumPy nizovi i Matplotlib --- višestruke krivulje petljom
#  Izv. prof. dr. sc. Marin Grubišić | marin.grubisic@gfos.hr | GrAFOS
# =============================================================================
#
#  UPUTA ZA STUDENTE:
#  ------------------
#  Svaka faza (%%  blok) izvršava se ZASEBNO u Spyderu:
#    - Označite blok i pritisnite  Ctrl + Enter
#    - ili kliknite gumb "Run cell" u alatnoj traci
#  Izvršavajte faze REDOM. Ne preskačite!
#
#  CILJ RADIONICE:
#  ---------------
#  Korak po korak izgraditi NumPy + Matplotlib kod koji u jednoj petlji
#  crta progibne linije proste grede za VIŠE raspona odjednom.
#
# =============================================================================

# %%  [FAZA 0]  Uvoz biblioteka
# -----------------------------------------------------------------------
#  Uvijek uvozite na vrhu datoteke. Pokrenite ovaj blok JEDNOM na početku.
# -----------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt


# %%  [FAZA 1]  Parametri presjeka i materijala
# -----------------------------------------------------------------------
#  Definiramo svojstva presjeka i materijala koji su ZAJEDNIČKI
#  za sve grede u analizi.
# -----------------------------------------------------------------------

# Materijal: beton C30/37
E = 32.0E6      # modul elastičnosti [kN/m²]

# Presjek: pravokutni AB presjek
b = 0.30        # širina presjeka [m]
h = 0.50        # visina presjeka [m]

# Izvedeni parametri presjeka
A = b*h   # površina [m²]
I = (b*h**3)/12   # moment tromosti [m⁴]

print("--- Parametri presjeka ---")
print(f"  b = {b*100:.0f} cm,  h = {h*100:.0f} cm")
print(f"  A = {A*1e4:.1f} cm²")
print(f"  I = {I*1e8:.2f} cm⁴")
print(f"  E = {E/1e6:.0f} GPa   -->   EI = {E*I:.2f} kNm²")


# %%  [FAZA 2]  Progib za JEDAN raspon i JEDNO opterećenje
# -----------------------------------------------------------------------
#  Najprije riješimo problem za jedan par (L, q) da provjerimo formulu.
#  Progib proste grede pod jednolikim opterećenjem:
#
#       w(x) = q * x * (L³ - 2L·x² + x³) / (24·E·I)
#
# -----------------------------------------------------------------------

q = 20.0  # jednoliko opterećenje [kN/m]
L = 6.0   # raspon grede [m]

# Diskretizacija osi grede
x = np.linspace(0, L, 100)    # 300 točaka od 0 do L

# Izračun progiba (vektorski --- bez petlje!)
# w(x) = q * x * (L³ - 2L·x² + x³) / (24·E·I)
w = q * x * (L**3 - 2*L*x**2 + x**3) / (24*E*I)

# Analitička vrijednost maksimalnog progiba na sredini
w_max_analiticki = 5 * q * L**4 / (384 * E * I)
w_max_numericki = np.max(w)

           # NumPy pronalazi maksimum

print("--- Provjera za jedan slučaj ---")
print(f"  q = {q} kN/m,  L = {L} m")
print(f"  w_max (analitički) = {w_max_analiticki*1000:.6f} mm")
print(f"  w_max (np.max)     = {w_max_numericki*1000:.6f} mm")
print(f"  Relativna razlika  = {abs(w_max_analiticki - w_max_numericki)/w_max_analiticki*100:.4f} %")


# %%  [FAZA 3]  Crtanje jedne krivulje
# -----------------------------------------------------------------------
#  Vizualiziramo progibnu liniju za slučaj iz Faze 2.
#  Ovo je "kostur" grafa koji ćemo proširiti u Fazi 5.
# -----------------------------------------------------------------------

plt.figure(figsize=(9,4)) # širina/visina dimenzija u inčima

# plt.plot(x-os, y-os, color:boja, linewidth:debljina linije)
plt.plot(x, w*1000, color="blue", linewidth=3, marker='o')
# Progibna linija u milimetrima!

# Flipanje y-osi
plt.gca().invert_yaxis()

plt.grid(True, linestyle=":")

plt.xlabel("Raspon [m]")
plt.ylabel("Progib [mm]")
plt.title(f"Progib grede: q={q} kN/m, L={L} m, b/h={b}/{h} cm")
plt.show()


# %%  [FAZA 4]  NumPy array raspona i petlja
# -----------------------------------------------------------------------
#  Sada proširujemo analizu na VIŠE raspona.
#  Definiramo array L_arr i prolazimo petljom.
#
#  PITANJE ZA STUDENTE:
#  Što se dogodi ako L_arr zamijenimo s np.linspace(4, 8, 5)?
# -----------------------------------------------------------------------

# I = I/2 # ovdje smo prepolovili izno momenta inercije

q = 20.0 * 5   # kN/m (ostaje isto za sve grede)

L_i = np.array([4, 5, 6, 7, 8])   # rasponi [m]

for L_p in L_i:
    w_max_i = 5 * q * L_p**4 / (384 * E * I)
    L250_i = L_p / 250
    ok = "OK!" if w_max_i <= L250_i else "NOK!"
    print(f"{L_p:>7.1f} | {w_max_i*1000:>10.2f} | {L250_i*1000:>10.1f} | {ok:>9}")


# %%  [FAZA 5]  Višestruke krivulje petljom --- GLAVNI REZULTAT
# -----------------------------------------------------------------------
#  Za svaki raspon iz L_arr u JEDNOJ petlji:
#    1) diskretiziramo os x
#    2) vektorski računamo progib w(x)
#    3) dodajemo krivulju na isti graf
#    4) ucrtavamo graničnu vrijednost L/250
#
#  Primijetite: cmap (mapa boja) automatski dodjeljuje razlicite boje!
# -----------------------------------------------------------------------

q = 20.0 * 5 # [kN/m]

L_i = np.array([4,5,6,7,8]) # [m]

plt.figure(figsize=(10,5))

for k, L_p in enumerate(L_i):
    x_i = np.linspace(0, L_p, 100)
    w_i = q * x_i * (L_p**3 - 2*L_p*x_i**2 + x_i**3) / (24*E*I)
    L250_i = L_p / 250 # provjera za GSU
    
    plt.plot(x_i, w_i*1000,
             linewidth=2.5,
             label=f"L = {L_p:.0f} m, $w_{{max}}$ = {np.max(w_i)*1000:.1f} mm")

    plt.axhline(L250_i*1000,
                linewidth=2,
                linestyle="-.",
                alpha=0.5)


plt.xlabel("Rasponi [m]", fontsize=12)
plt.ylabel("Progibi [mm]", fontsize=12)
plt.title("Progibne linije različitih duljina greda")
plt.legend(fontsize=11, loc="lower right")
plt.grid(True, linestyle="--")

plt.gca().invert_yaxis()
    
plt.show()



# Formatiranje osi i naslova


# ax.invert_yaxis()


print("Graf s višestrukim krivuljama iscrtan i pohranjen.")


# %%  [FAZA 6]  Proširenje --- višestruka opterećenja
# -----------------------------------------------------------------------
#  ZADATAK ZA STUDENTE (riješiti na nastavi ili kao pripremu za DZ):
#  Sada fiksiramo raspon L = 6 m i mijenjamo jednoliko opterećenje q.
#
#  Dopunite kod ispod tako da:
#    (a) definirate q_arr = np.array([10, 15, 20, 25, 30]) kN/m
#    (b) u petlji crtate progib za svaki q iz q_arr
#    (c) dodate oznake osi, legendu i mrežu
#    (d) ucrtate jedinstvenu graničnu liniju L/250
# -----------------------------------------------------------------------

L_fix = 6.0     # raspon je FIKSIRAN

# --- OVDJE DOPUNITE KOD ---

# q_arr = np.array([10.0, 15.0, 20.0, 25.0, 30.0])   # kN/m

# Vaš kod ide ovdje:
# cmap2  = ...
# fig, ax = plt.subplots(...)
# for k, q_i in enumerate(q_arr):
#     x_i = ...
#     w_i = ...
#     ax.plot(...)
# ax.axhline(...)    # L/250 --- ucrtajte samo jedanput!
# ...

# -----------------------------------------------------------------------
# RJEŠENJE (otkrijte tek nakon što pokušate sami!):
# -----------------------------------------------------------------------
# q_arr = np.array([10.0, 15.0, 20.0, 25.0, 30.0])
# cmap2 = plt.cm.get_cmap('plasma', len(q_arr))
# fig, ax = plt.subplots(figsize=(10, 5))
# for k, q_i in enumerate(q_arr):
#     x_i = np.linspace(0, L_fix, 300)
#     w_i = q_i * x_i * (L_fix**3 - 2*L_fix*x_i**2 + x_i**3) / (24*E*I)
#     ax.plot(x_i, w_i*1000, color=cmap2(k), lw=2.2,
#             label=f'q = {q_i:.0f} kN/m  '
#                   f'(w_max = {np.max(w_i)*1000:.1f} mm)')
# ax.axhline(L_fix/250*1000, color='k', ls='--', lw=1.5,
#            label=f'L/250 = {L_fix/250*1000:.1f} mm')
# ax.set_xlabel('x [m]'); ax.set_ylabel('w [mm]')
# ax.set_title(f'Progib proste grede L={L_fix} m za različita q')
# ax.legend(fontsize=9); ax.grid(True, ls=':'); plt.tight_layout(); plt.show()


# %%  [FAZA 7]  Sažetak naučenih naredbi
# -----------------------------------------------------------------------
#  Ispisujemo pregled svih ključnih naredbi korištenih u radionici.
# -----------------------------------------------------------------------

sazetak = """
╔══════════════════════════════════════════════════════════════════════╗
║          SAŽETAK: NumPy + Matplotlib radionica (Tjedan 4/15)        ║
╠══════════════════════════════════════════════════════════════════════╣
║  NumPy:                                                              ║
║    np.array([...])          — kreiranje niza iz liste                ║
║    np.linspace(a, b, N)     — N ravnomjernih točaka od a do b        ║
║    np.max(arr)              — maksimum niza                          ║
║    Vektorske operacije      — bez petlji (arr**2, q*arr, ...)        ║
║                                                                      ║
║  Matplotlib:                                                         ║
║    plt.figure(figsize=...)  — nova slika zadanih dimenzija           ║
║    plt.subplots(...)        — mreža podgrafova (fig, ax)             ║
║    ax.plot(x, y, ...)       — crtanje krivulje                       ║
║    ax.axhline(y, ...)       — horizontalna linija na visini y        ║
║    ax.set_xlabel/ylabel     — oznake osi                             ║
║    ax.legend()              — legenda                                ║
║    ax.grid(True, ...)       — mreža                                  ║
║    plt.tight_layout()       — automatski razmaci                     ║
║    plt.savefig('naziv.pdf') — pohrana u datoteku                     ║
║                                                                      ║
║  Petlja za višestruke krivulje:                                      ║
║    cmap = plt.cm.get_cmap('viridis', N)   — N boja iz palete        ║
║    for k, val in enumerate(arr):          — indeks + vrijednost      ║
║        ax.plot(..., color=cmap(k), ...)   — svaka iteracija = boja  ║
╚══════════════════════════════════════════════════════════════════════╝
"""
print(sazetak)
