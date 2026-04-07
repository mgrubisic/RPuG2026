# -*- coding: utf-8 -*-
# =============================================================================
#  Računalno programiranje u građevinarstvu (254810) | Tjedan 4/15
#  Radionica: NumPy nizovi i Matplotlib --- višestruke krivulje petljom
#  Izv. prof. dr. sc. Marin Grubišić | marin.grubisic@gfos.hr | GrAFOS
#  -----------------------------------------------------------------------
#  VERZIJA 1 --- Riješeni primjer (bez vlastitih funkcija)
# =============================================================================
#
#  UPUTA ZA STUDENTE:
#  ------------------
#  Svaka faza (%% blok) izvršava se ZASEBNO u Spyderu:
#    - Označite blok i pritisnite  Ctrl + Enter
#    - ili kliknite gumb "Run cell" u alatnoj traci
#  Izvršavajte faze REDOM. Ne preskačite!
#
#  CILJ RADIONICE:
#  ---------------
#  Korak po korak izgraditi NumPy + Matplotlib kod koji u jednoj petlji
#  crta progibne linije proste grede za VIŠE raspona odjednom.
#
#  TEORIJSKA PODLOGA:
#  ------------------
#  Progib proste grede pod jednolikim opterećenjem q [kN/m]:
#
#       w(x) = q * x * (L³ - 2L·x² + x³) / (24·E·I)
#
#  Maksimalni progib (na sredini raspona, x = L/2):
#
#       w_max = 5 * q * L⁴ / (384 * E * I)
#
#  Granični uvjet uporabivosti (GSU) prema EC2/EC3:
#
#       w_max ≤ L / 250
#
# =============================================================================


# %%  [FAZA 0]  Uvoz biblioteka
# -----------------------------------------------------------------------
#  Uvijek uvozite na vrhu datoteke. Pokrenite ovaj blok JEDNOM na početku.
# -----------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

print("Biblioteke uspješno uvezene.")
print(f"  NumPy verzija:      {np.__version__}")
print(f"  Matplotlib verzija: {plt.matplotlib.__version__}")


# %%  [FAZA 1]  Parametri presjeka i materijala
# -----------------------------------------------------------------------
#  Definiramo svojstva presjeka i materijala koji su ZAJEDNIČKI
#  za sve grede u analizi.
# -----------------------------------------------------------------------

# Materijal: beton C30/37
E = 32.0e6       # modul elastičnosti [kN/m²]

# Presjek: pravokutni AB presjek
b = 0.30         # širina presjeka [m]
h = 0.50         # visina presjeka [m]

# Izvedeni parametri presjeka
A = b * h                # površina [m²]
I = (b * h**3) / 12      # moment tromosti [m⁴]

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

q = 20.0    # jednoliko opterećenje [kN/m]
L = 6.0     # raspon grede [m]

# Diskretizacija osi grede
x = np.linspace(0, L, 300)    # 300 točaka od 0 do L

# Izračun progiba (vektorski --- bez petlje!)
w = q * x * (L**3 - 2*L*x**2 + x**3) / (24 * E * I)

# Analitička vrijednost maksimalnog progiba na sredini
w_max_an = 5 * q * L**4 / (384 * E * I)

# NumPy pronalazi maksimum numerički
w_max_np = np.max(w)

print("--- Provjera za jedan slučaj ---")
print(f"  q = {q} kN/m,  L = {L} m")
print(f"  w_max (analitički) = {w_max_an*1000:.3f} mm")
print(f"  w_max (np.max)     = {w_max_np*1000:.3f} mm")
print(f"  Relativna razlika  = {abs(w_max_an - w_max_np)/w_max_an*100:.4f} %")


# %%  [FAZA 3]  Crtanje jedne krivulje
# -----------------------------------------------------------------------
#  Vizualiziramo progibnu liniju za slučaj iz Faze 2.
#  Ovo je "kostur" grafa koji ćemo proširiti u Fazi 5.
# -----------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(9, 4))

ax.plot(x, w * 1000, color='tab:blue', linewidth=2.5,
        label=f'L = {L:.0f} m,  $w_{{max}}$ = {w_max_np*1000:.2f} mm')

ax.axhline(L / 250 * 1000, color='tab:red', linestyle='--', linewidth=1.5,
           label=f'L/250 = {L/250*1000:.1f} mm  (GSU granica)')

ax.invert_yaxis()
ax.set_xlabel('x  [m]', fontsize=11)
ax.set_ylabel('w  [mm]', fontsize=11)
ax.set_title(f'Progib proste grede:  q = {q} kN/m,  L = {L} m,  '
             f'b/h = {b*100:.0f}/{h*100:.0f} cm', fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, linestyle=':')
plt.tight_layout()
plt.show()

print("Graf jedne krivulje iscrtan.")


# %%  [FAZA 4]  NumPy array raspona i petlja
# -----------------------------------------------------------------------
#  Sada proširujemo analizu na VIŠE raspona.
#  Definiramo array L_arr i prolazimo petljom.
#
#  PITANJE ZA STUDENTE:
#  Što se dogodi ako L_arr zamijenimo s np.linspace(4, 8, 5)?
# -----------------------------------------------------------------------

q   = 20.0 * 5                         # kN/m (povećano opterećenje)
L_arr = np.array([4, 5, 6, 7, 8])      # rasponi [m]

print(f"--- Provjera GSU (q = {q:.0f} kN/m) ---")
print(f"{'L [m]':>7} | {'w_max [mm]':>10} | {'L/250 [mm]':>10} | {'Ocjena':>9}")
print("-" * 46)
for L_p in L_arr:
    w_max_i = 5 * q * L_p**4 / (384 * E * I)
    L250_i  = L_p / 250
    ok      = "OK!" if w_max_i <= L250_i else "NOK!"
    print(f"{L_p:>7.1f} | {w_max_i*1000:>10.2f} | {L250_i*1000:>10.1f} | {ok:>9}")


# %%  [FAZA 5]  Višestruke krivulje petljom --- GLAVNI REZULTAT
# -----------------------------------------------------------------------
#  Za svaki raspon iz L_arr u JEDNOJ petlji:
#    1) diskretiziramo os x
#    2) vektorski računamo progib w(x)
#    3) dodajemo krivulju na isti graf
#    4) ucrtavamo graničnu vrijednost L/250
#
#  Primijetite: cmap (mapa boja) automatski dodjeljuje različite boje!
# -----------------------------------------------------------------------

q     = 20.0 * 5                       # kN/m
L_arr = np.array([4, 5, 6, 7, 8])     # rasponi [m]
cmap  = plt.colormaps['viridis'].resampled(len(L_arr))

fig, ax = plt.subplots(figsize=(10, 5))

for k, L_p in enumerate(L_arr):
    x_i   = np.linspace(0, L_p, 300)
    w_i   = q * x_i * (L_p**3 - 2*L_p*x_i**2 + x_i**3) / (24 * E * I)
    L250_i = L_p / 250                 # GSU granica za ovaj raspon

    ax.plot(x_i, w_i * 1000,
            color=cmap(k), linewidth=2.5,
            label=f'L = {L_p:.0f} m,  $w_{{max}}$ = {np.max(w_i)*1000:.1f} mm')

    ax.axhline(L250_i * 1000,
               color=cmap(k), linestyle='-.', linewidth=1.2, alpha=0.5)

ax.invert_yaxis()
ax.set_xlabel('x  [m]', fontsize=12)
ax.set_ylabel('w  [mm]', fontsize=12)
ax.set_title('Progibne linije proste grede za različite raspone\n'
             f'(q = {q:.0f} kN/m,  b/h = {b*100:.0f}/{h*100:.0f} cm,  '
             f'C30/37)', fontsize=11)
ax.legend(fontsize=10, loc='lower center')
ax.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig('tjedan4_greda_rasponi.png', dpi=200)
plt.show()

print("Graf s višestrukim krivuljama iscrtan i pohranjen.")


# %%  [FAZA 6]  Proširenje --- višestruka opterećenja
# -----------------------------------------------------------------------
#  Sada fiksiramo raspon L = 6 m i mijenjamo jednoliko opterećenje q.
# -----------------------------------------------------------------------

L_fix = 6.0    # raspon je FIKSIRAN [m]
q_arr = np.array([10.0, 15.0, 20.0, 25.0, 30.0])    # kN/m
cmap2 = plt.colormaps['plasma'].resampled(len(q_arr))

fig, ax = plt.subplots(figsize=(10, 5))

for k, q_i in enumerate(q_arr):
    x_i = np.linspace(0, L_fix, 300)
    w_i = q_i * x_i * (L_fix**3 - 2*L_fix*x_i**2 + x_i**3) / (24 * E * I)

    ax.plot(x_i, w_i * 1000, color=cmap2(k), lw=2.2,
            label=f'q = {q_i:.0f} kN/m   '
                  f'($w_{{max}}$ = {np.max(w_i)*1000:.1f} mm)')

# GSU granica --- samo jedanput, jednaka za sve (isti L_fix)
ax.axhline(L_fix / 250 * 1000, color='black', ls='--', lw=1.8,
           label=f'L/250 = {L_fix/250*1000:.1f} mm  (GSU)')

ax.invert_yaxis()
ax.set_xlabel('x  [m]', fontsize=12)
ax.set_ylabel('w  [mm]', fontsize=12)
ax.set_title(f'Progibne linije za različita opterećenja\n'
             f'(L = {L_fix:.0f} m,  b/h = {b*100:.0f}/{h*100:.0f} cm,  '
             f'C30/37)', fontsize=11)
ax.legend(fontsize=9, loc='lower center')
ax.grid(True, linestyle=':', alpha=0.5)
plt.tight_layout()
plt.savefig('tjedan4_greda_opterecenja.png', dpi=200)
plt.show()

print("Graf višestrukih opterećenja iscrtan i pohranjen.")


# %%  [FAZA 7]  Sažetak naučenih naredbi
# -----------------------------------------------------------------------
#  Ispisujemo pregled svih ključnih naredbi korištenih u radionici.
# -----------------------------------------------------------------------

# sazetak = """
# ╔══════════════════════════════════════════════════════════════════════╗
# ║          SAŽETAK: NumPy + Matplotlib radionica (Tjedan 4/15)        ║
# ╠══════════════════════════════════════════════════════════════════════╣
# ║  NumPy:                                                              ║
# ║    np.array([...])          — kreiranje niza iz liste                ║
# ║    np.linspace(a, b, N)     — N ravnomjernih točaka od a do b        ║
# ║    np.max(arr)              — maksimum niza                          ║
# ║    Vektorske operacije      — bez petlji (arr**2, q*arr, ...)        ║
# ║                                                                      ║
# ║  Matplotlib:                                                         ║
# ║    plt.subplots(figsize=.)  — nova slika s fig/ax objektima          ║
# ║    ax.plot(x, y, ...)       — crtanje krivulje                       ║
# ║    ax.axhline(y, ...)       — horizontalna linija na visini y        ║
# ║    ax.invert_yaxis()        — okretanje y-osi (progibi prema dolje)  ║
# ║    ax.set_xlabel/ylabel     — oznake osi                             ║
# ║    ax.legend()              — legenda                                ║
# ║    ax.grid(True, ...)       — mreža                                  ║
# ║    plt.tight_layout()       — automatski razmaci                     ║
# ║    plt.savefig('naziv.pdf') — pohrana u datoteku                     ║
# ║                                                                      ║
# ║  Petlja za višestruke krivulje:                                      ║
# ║    cmap = plt.colormaps['viridis'].resampled(N) — N boja iz palete          ║
# ║    for k, val in enumerate(arr):        — indeks + vrijednost        ║
# ║        ax.plot(..., color=cmap(k), ...) — svaka iteracija = boja    ║
# ╚══════════════════════════════════════════════════════════════════════╝
# """
# print(sazetak)
