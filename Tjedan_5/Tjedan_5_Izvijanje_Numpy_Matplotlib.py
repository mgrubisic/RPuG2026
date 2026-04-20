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
#  Vitkost stupa: lambda = beta * L / i_min
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
print(f"Numpy verzija: {np.__version__}")
print(f"Matplotlib verzija: {plt.matplotlib.__version__}")

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
A_cm2 = 53.0     # površina presjeka [cm²]
Iz_cm4 = 604.0   # moment tromosti oko z-osi [cm⁴]  <-- slaba os!
Iy_cm4 = 8356.0  # moment tromosti oko y-osi [cm⁴]  <-- jaka os

# Pretvorba u SI jedinice [m]
A = A_cm2 * 1E-4      # m² (1/10000 ili 10**(-4))
I_z = Iz_cm4 * 1E-8    # m⁴  <-- koristimo za izvijanje!
I_y = Iy_cm4 * 1E-8    # m⁴

# Polumjeri tromosti
i_z = np.sqrt(I_z/A)  # m  --- relevantan za izvijanje!
i_y = np.sqrt(I_y/A)     # m

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
N_cr = np.pi**2 * E * I_z / (beta * L)**2    # kN

# Vitkost
lam = beta * L / i_z    # bezdimenzijska vitkost

print("--- Provjera za jedan slučaj ---")
print(f"  Rubni uvjeti: Zglobno-Zglobno (beta = {beta})")
print(f"  L    = {L:.1f} m")
print(f"  N_cr = {N_cr:.2f} kN")
print(f"  lambda = {lam:.1f}  (vitkoća stupa)")

# 1 kN/m2 = 1 kPa
# 1 MPa = 1000 kPa

# Usporedba s plastičnom nosivošću presjeka
N_pl = fyk * 1E3 * A # kN  (gamma_M0 = 1.0)
print(f"  N_pl = {N_pl:.1f} kN  (plastična nosivost presjeka)")
print(f"  N_cr / N_pl = {N_cr/N_pl:.3f}")


# %%  [FAZA 3]  N_cr kao funkcija visine za JEDAN rubni uvjet
# -----------------------------------------------------------------------
#  Koristimo np.linspace za niz visina L, pa vektorski izračunamo N_cr.
#  Prikazujemo kako N_cr brzo pada s porastom visine (proporcionalno 1/L²).
# -----------------------------------------------------------------------

beta = 1.0   # Zglobno - Zglobno

# Diskretizacija visina stupa: od 2 do 12 m
L_arr = np.linspace(2, 12, 200)    # m

# Vektorski izračun --- bez petlje!
N_cr_arr = np.pi**2 * E * I_z / (beta * L_arr)**2    # kN

# Horizontalna linija: plastična nosivost (gornja granica!)
N_pl = fyk * 1E3 * A # kN

# --- Crtanje ---
fig, ax = plt.subplots(figsize=(5,2.5)) # dimenzije u inčima
ax.plot(L_arr, N_cr_arr, color="blue", lw=3, label="N_cr (Z-Z, beta=1.0)")
ax.axhline(N_pl, color="red", ls="-.", lw=2, label=f"N_pl = {N_pl:.0f} kN - plastična nosivost")
ax.set_xlabel("Visina stupa, L [m]")
ax.set_ylabel("N_cr [kN]")
ax.set_title("Eulerova kritična sila - IPE 300, S235 (Z-Z)")
ax.set_xlim(0,8)
ax.set_ylim(0,1500)
ax.legend(loc="lower left")
ax.grid(True, alpha=0.5)
# plt.tight_layout()  plt.show()

plt.show()

print("Graf jedne krivulje iscrtan.")


# %%  [FAZA 4]  NumPy array rubnih uvjeta + usporedna tablica
# -----------------------------------------------------------------------
#  Definiramo sve rubne uvjete kao NumPy array faktora beta.
#  Vektorski izračunamo N_cr za fiksnu visinu L = 5 m i ispišemo tablicu.
#
#  PITANJE ZA STUDENTE:
#  Zašto je N_cr za U-U četiri puta veći nego za Z-Z?
# -----------------------------------------------------------------------

L_fix = 5.0  # m --- fiksna visina za tablicu

# Rubni uvjeti kao NumPy arraji (isti indeks = isti slučaj!)
beta_arr = np.array([1.0, 2.0, 0.7, 0.5])    # beta_arr = ...
oznake = ["Z-Z", "U-Sl", "U-Z", "U-U"]    # oznake   = ...

# Vektorski izračun za sve rubne uvjete odjednom
N_cr_sve = np.pi**2 * E * I_z / (beta_arr * L_fix)**2 # kN
lam_sve  = beta_arr * L_fix / i_z   # vitkost

N_pl = fyk * 1E3 * A  # kN

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

L_arr = np.linspace(1, 15, 300)    # m  — zajednički niz visina
boje  = ["blue", "orange", "green", "red"]    # boje = [...]

fig, ax = plt.subplots(figsize=(5,2.5))

for k, (beta_i, ozn_i) in enumerate(zip(beta_arr, oznake)):
    N_cr_i = np.pi**2 * E * I_z / (beta_i * L_arr)**2 # kN

    # Granica EC3: vitkost lambda <= 200  →  L <= 200 * i_z / beta_i
    L_lim_i = 200 * i_z / beta_i
    # maska    = ...

    # Punom linijom do granice vitkoće, isprekidanom iznad nje
    ax.plot(L_arr, N_cr_i, color=boje[k], lw=2, label=f"{ozn_i}, (beta={beta_i:.2f}")
    # ax.plot(L_arr[~maska], ..., ls='--', alpha=0.45)

ax.axhline(N_pl, color="black")          # horizontalna linija: N_pl
# ax.axvline(L_ref, ...)         # vertikalna linija: lambda=200 (Z-Z)
# ax.text(...)                   # tekstualne oznake
ax.set_xlabel("Duljine, L [m]")
ax.set_ylabel("N_cr [kN]")
# ax.set_title(...)
ax.set_xlim(0, 10)
ax.set_ylim(0, 2000)
ax.legend(loc="best")
ax.grid(True, alpha=0.5)
# plt.tight_layout()
plt.savefig('tjedan4_izvijanje.png', dpi=200)
plt.savefig('tjedan4_izvijanje.pdf', dpi=200)
plt.show()

print("Glavni graf s višestrukim krivuljama iscrtan i pohranjen.")


# %%  [FAZA 8]  Sažetak naučenih naredbi
# -----------------------------------------------------------------------

# sazetak = """
# ╔══════════════════════════════════════════════════════════════════════╗
# ║       SAŽETAK: Radionica izvijanja (NumPy + Matplotlib)             ║
# ╠══════════════════════════════════════════════════════════════════════╣
# ║  NumPy naredbe:                                                      ║
# ║    np.array([...])          — kreiranje niza rubnih uvjeta / profila ║
# ║    np.linspace(a, b, N)     — niz visina / vitkoća za krivulje       ║
# ║    np.sqrt(I / A)           — vektorski izračun polumjera tromosti   ║
# ║    np.pi                    — konstanta pi                           ║
# ║    arr[maska]               — booleovo indeksiranje (lambda <= 200)  ║
# ║                                                                      ║
# ║  Matplotlib naredbe:                                                 ║
# ║    ax.plot(x, y, ls='--')   — crtanje krivulje s linijskim stilom   ║
# ║    ax.axhline(y_val, ...)   — horizontalna referentna linija         ║
# ║    ax.axvline(x_val, ...)   — vertikalna referentna linija           ║
# ║    ax.text(x, y, 'tekst')   — tekstualna oznaka na grafu            ║
# ║    ax.set_xlim(left=0)      — postavljanje limita osi               ║
# ║    plt.savefig('f.pdf')     — pohrana u PDF/PNG                     ║
# ║                                                                      ║
# ║  Inženjerske spoznaje:                                               ║
# ║    N_cr ~ 1/L²              — brz pad nosivosti s visinom           ║
# ║    N_cr ~ beta^(-2)         — U-U nosi 4× više od Z-Z              ║
# ║    lambda = beta*L/i_z      — vitkoća = jedinstven mjerni par       ║
# ╚══════════════════════════════════════════════════════════════════════╝
# """
# print(sazetak)
