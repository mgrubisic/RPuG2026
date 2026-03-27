# =============================================================================
#  Računalno programiranje u građevinarstvu (254810) | Tjedan 4/15
#  Radionica: NumPy + Matplotlib --- Eulerova kritična sila izvijanja
#  Izv. prof. dr. sc. Marin Grubišić | marin.grubisic@gfos.hr | GrAFOS
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
#  crta krivulje kritične sile izvijanja Euler-ovih stupova za RAZLIČITE
#  rubne uvjete i uspoređuje ih na jednom grafu.
#
#  TEORIJSKA PODLOGA:
#  ------------------
#  Eulerova kritična sila izvijanja (prema EN 1993-1-1, tj. EC3):
#
#       N_cr = pi² * E * I / (beta * L)²
#
#  gdje je:
#       E    --- modul elastičnosti čelika [kN/m²]
#       I    --- moment tromosti poprečnog presjeka [m⁴]
#       L    --- visina (duljina) stupa [m]
#       beta --- faktor ekvivalentne duljine izvijanja [-]
#
#  Faktor beta ovisi o rubnim uvjetima:
#
#       Rubni uvjeti                   | beta
#       -------------------------------|------
#       Zglobno - Zglobno  (Z-Z)       | 1.00
#       Upeto - Slobodno   (U-Sl)      | 2.00
#       Upeto - Zglobno    (U-Z)       | 0.70
#       Upeto - Upeto      (U-U)       | 0.50
#
#  Vitkoća stupa: lambda = beta * L / i_min
#  gdje je i_min = sqrt(I_min / A) --- minimalni polumjer tromosti [m]
#
# =============================================================================


# %%  [FAZA 0]  Uvoz biblioteka
# -----------------------------------------------------------------------
#  Uvijek uvozite na vrhu datoteke.
# -----------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

print("Biblioteke uspješno uvezene.")
print(f"  NumPy verzija:      {np.__version__}")
print(f"  Matplotlib verzija: {plt.matplotlib.__version__}")


# %%  [FAZA 1]  Parametri čeličnog stupa --- IPE 300
# -----------------------------------------------------------------------
#  Koristimo standardni IPE 300 profil iz tablica EN 1993.
#  Svi podaci su iz kataloga ArcelorMittal.
#
#  PITANJE: Zašto koristimo I_z (manji moment tromosti), a ne I_y?
# -----------------------------------------------------------------------

# Materijal: čelik S235
E   = 210.0e6    # modul elastičnosti [kN/m²]
fyk = 235.0      # karakteristična granica popuštanja [MPa]

# Profil: IPE 300 (izvijanje oko slabe osi z-z!)
  # površina presjeka [cm²]
  # moment tromosti oko z-osi [cm⁴]  <-- slaba os!
  # moment tromosti oko y-osi [cm⁴]  <-- jaka os

# Pretvorba u SI jedinice [m]
   # m²
   # m⁴  <-- koristimo za izvijanje!
   # m⁴

# Polumjeri tromosti
  # m  --- relevantan za izvijanje!
  # m

print("--- IPE 300 | Čelik S235 ---")
print(f"  A   = {A*1e4:.2f} cm²")
print(f"  I_z = {I_z*1e8:.0f} cm⁴   (slaba os --- mjerodavna!)")
print(f"  I_y = {I_y*1e8:.0f} cm⁴   (jaka os)")
print(f"  i_z = {i_z*100:.2f} cm")
print(f"  i_y = {i_y*100:.2f} cm")


# %%  [FAZA 2]  Kritična sila za JEDAN rubni uvjet i JEDAN raspon
# -----------------------------------------------------------------------
#  Najprije izračunamo N_cr za slučaj Zglobno-Zglobno (beta=1.0)
#  za jedan stup visine L = 5 m --- provjera formule.
# -----------------------------------------------------------------------

beta = 1.0     # Zglobno - Zglobno
L    = 5.0     # visina stupa [m]

# Eulerova formula
   # kN

# Vitkoća
   # bezdimenzijska vitkoća

print("--- Provjera za jedan slučaj ---")
print(f"  Rubni uvjeti: Zglobno-Zglobno (beta = {beta})")
print(f"  L    = {L:.1f} m")
print(f"  N_cr = {N_cr:.2f} kN")
print(f"  lambda = {lam:.1f}  (vitkoća stupa)")

# Usporedba s plastičnom nosivošću presjeka
    # kN  (gamma_M0 = 1.0)
print(f"  N_pl = {N_pl:.1f} kN  (plastična nosivost presjeka)")
print(f"  N_cr / N_pl = {N_cr/N_pl:.3f}")


# %%  [FAZA 3]  N_cr kao funkcija visine za JEDAN rubni uvjet
# -----------------------------------------------------------------------
#  Koristimo np.linspace za niz visina L, pa vektorski izračunamo N_cr.
#  Prikazujemo kako N_cr brzo pada s porastom visine (proporcionalno 1/L²).
# -----------------------------------------------------------------------

  # Zglobno - Zglobno

# Diskretizacija visina stupa: od 2 do 12 m
   # m

# Vektorski izračun --- bez petlje!
   # kN

# Horizontalna linija: plastična nosivost (gornja granica!)
   # kN


print("Graf jedne krivulje iscrtan.")


# %%  [FAZA 4]  NumPy array rubnih uvjeta + usporedna tablica
# -----------------------------------------------------------------------
#  Definiramo sve rubne uvjete kao NumPy array faktora beta.
#  Vektorski izračunamo N_cr za fiksnu visinu L = 5 m i ispišemo tablicu.
#
#  PITANJE ZA STUDENTE:
#  Zašto je N_cr za U-U četiri puta veći nego za Z-Z?
# -----------------------------------------------------------------------

   # m --- fiksna visina za tablicu

# Rubni uvjeti kao NumPy arraji (isti indeks = isti slučaj!)

# Vektorski izračun za sve rubne uvjete odjednom
                       # kN
                       # vitkost

  # kN

print(f"--- Usporedna tablica: IPE 300, L = {L_fix} m ---")
print(f"{'Rubni uvjeti':>16} | {'beta':>5} | "
      f"{'N_cr [kN]':>10} | {'lambda':>7} | {'N_cr/N_pl':>10}")
print("-" * 58)
for k in range(len(beta_arr)):
    print(f"{oznake[k]:>16} | {beta_arr[k]:>5.2f} | "
          f"{N_cr_sve[k]:>10.1f} | {lam_sve[k]:>7.1f} | "
          f"{N_cr_sve[k]/N_pl:>10.3f}")


# %%  [FAZA 5]  Višestruke krivulje petljom --- GLAVNI REZULTAT
# -----------------------------------------------------------------------
#  Za svaki rubni uvjet (svaki beta) u JEDNOJ petlji:
#    1) vektorski računamo N_cr za niz visina L_arr
#    2) dodajemo krivulju na isti graf s automatskom bojom
#    3) označavamo N_pl i granicu vitkoće lambda = 200 (EC3 preporuka)
#
#  Primijetite: enumerate() daje i indeks (k) i vrijednost (beta_i).
# -----------------------------------------------------------------------







# %%  [FAZA 8]  Sažetak naučenih naredbi
# -----------------------------------------------------------------------

sazetak = """
╔══════════════════════════════════════════════════════════════════════╗
║       SAŽETAK: Radionica izvijanja (NumPy + Matplotlib)             ║
╠══════════════════════════════════════════════════════════════════════╣
║  NumPy naredbe:                                                      ║
║    np.array([...])          — kreiranje niza rubnih uvjeta / profila ║
║    np.linspace(a, b, N)     — niz visina / vitkoća za krivulje       ║
║    np.sqrt(I / A)           — vektorski izračun polumjera tromosti   ║
║    np.pi                    — konstanta pi                           ║
║    arr[maska]               — booleovo indeksiranje (lambda <= 200)  ║
║                                                                      ║
║  Matplotlib naredbe:                                                 ║
║    ax.plot(x, y, ls='--')   — crtanje krivulje s linijskim stilom   ║
║    ax.axhline(y_val, ...)   — horizontalna referentna linija         ║
║    ax.axvline(x_val, ...)   — vertikalna referentna linija           ║
║    ax.text(x, y, 'tekst')   — tekstualna oznaka na grafu            ║
║    ax.set_xlim(left=0)      — postavljanje limita osi               ║
║    plt.savefig('f.pdf')     — pohrana u PDF/PNG                     ║
║                                                                      ║
║  Petlja za višestruke krivulje:                                      ║
║    zip(beta_arr, oznake)    — paralelna iteracija dvaju nizova       ║
║    enumerate(zip(...))      — indeks + para vrijednosti              ║
║    linestyle=stilovi[k]     — razliciti stilovi linije po k         ║
║                                                                      ║
║  Inženjerske spoznaje:                                               ║
║    N_cr ~ 1/L²              — brz pad nosivosti s visinom           ║
║    N_cr ~ beta^(-2)         — U-U nosi 4× više od Z-Z              ║
║    lambda = beta*L/i_z      — vitkoća = jedinstven mjerni par       ║
╚══════════════════════════════════════════════════════════════════════╝
"""
print(sazetak)
