# =============================================================================
#  Računalno programiranje u građevinarstvu (254810)
#  Tjedan 3/15 --- Funkcije i modularnost
#  Sveučilište J. J. Strossmayera u Osijeku
#  Građevinski i arhitektonski fakultet Osijek (GrAFOS)
#  Izv. prof. dr. sc. Marin Grubišić | marin.grubisic@gfos.hr
# =============================================================================

# =============================================================================
#  NAPOMENA: Svaka sekcija (#%%) je zasebna ćelija u Spyderu.
#  Pokretanje pojedine ćelije: Ctrl+Enter
#  Pokretanje cijele skripte: F5
# =============================================================================


# %% [1] Definiranje i pozivanje funkcije
# Osnovna sintaksa def, return i višestruki pozivi funkcije za moment otpora.

def moment_otpora(b, h):
    """Vraća moment otpora pravokutnog presjeka [m³]."""
    Wy = (b * h**2) / 6
    return Wy

# Pozivanje funkcije s različitim argumentima
Wy1 = moment_otpora(0.30, 0.50)
Wy2 = moment_otpora(0.25, 0.45)
Wy3 = moment_otpora(0.40, 0.70)

print(f"Wy1 = {Wy1 * 1e6:.1f} cm³")
print(f"Wy2 = {Wy2 * 1e6:.1f} cm³")
print(f"Wy3 = {Wy3 * 1e6:.1f} cm³")


# %% [2] Argumenti funkcije --- pozicijski i imenovani
# Razlika između pozicijskog i imenovanog (keyword) poziva funkcije.

def naprezanje_savijanje(M_Ed, b, h):
    """Naprezanje od savijanja u pravokutnom presjeku [MPa]."""
    Wy    = (b * h**2) / 6
    sigma = (M_Ed / Wy) / 1000   # M [kNm] -> sigma [MPa]
    return sigma

# Pozicijski poziv --- redoslijed je bitan
sigma1 = naprezanje_savijanje(150.0, 0.30, 0.50)

# Poziv s imenovanim argumentima (keyword arguments)
sigma2 = naprezanje_savijanje(M_Ed=150.0, b=0.30, h=0.50)

# Kod imenovanog poziva redoslijed NE mora biti isti
sigma3 = naprezanje_savijanje(h=0.50, b=0.30, M_Ed=150.0)

print(f"sigma1 = {sigma1:.2f} MPa")
print(f"sigma2 = {sigma2:.2f} MPa")
print(f"sigma3 = {sigma3:.2f} MPa")
# Sva tri poziva daju isti rezultat


# %% [3] Zadane (default) vrijednosti argumenata
# Argument s default vrijednosti --- nije ga potrebno navesti pri pozivu.

import math

def svojstva_kružnog_presjeka(D, jedinice="m"):
    """
    Geometrijska svojstva punog kružnog presjeka.
    D       : promjer [m]
    jedinice: 'm' ili 'cm' (zadano: 'm')
    """
    A = math.pi * D**2 / 4
    I = math.pi * D**4 / 64
    W = math.pi * D**3 / 32
    i = D / 4

    if jedinice == "cm":
        return A*1e4, I*1e8, W*1e6, i*1e2   # pretvorba u cm
    return A, I, W, i                        # ostaje u metrima

# Poziv bez navođenja 'jedinice' --- koristi se zadana vrijednost "m"
A, I, W, i = svojstva_kružnog_presjeka(0.40)
print(f"A = {A:.4f} m²,  I = {I:.6f} m⁴")

# Eksplicitni poziv s cm
A, I, W, i = svojstva_kružnog_presjeka(0.40, jedinice="cm")
print(f"A = {A:.2f} cm²,  I = {I:.2f} cm⁴")


# %% [4] Višestruke povratne vrijednosti
# Funkcija vraća više vrijednosti kao n-torku, raspakiranje pri pozivu.

def geometrijska_svojstva_pravokutnika(b, h):
    """
    Geometrijska svojstva pravokutnog presjeka.
    Ulaz : b [m], h [m]
    Izlaz: A [m²], I [m⁴], W [m³], i [m]
    """
    A = b * h
    I = (b * h**3) / 12
    W = (b * h**2) / 6
    i = (I / A)**0.5   # polumjer tromosti
    return A, I, W, i  # vraća n-torku

# Raspakiranje povratnih vrijednosti
A, I, W, i = geometrijska_svojstva_pravokutnika(0.30, 0.55)

print(f"A = {A*1e4:.1f} cm²")
print(f"I = {I*1e8:.1f} cm⁴")
print(f"W = {W*1e6:.1f} cm³")
print(f"i = {i*1e2:.2f} cm")

# Ili kao n-torka (bez raspakiravanja)
svojstva = geometrijska_svojstva_pravokutnika(0.30, 0.55)
print(f"\nKao n-torka: I = {svojstva[1]*1e8:.1f} cm⁴")


# %% [5] Doseg varijabli --- lokalne i globalne
# Razlika između lokalnih (unutar funkcije) i globalnih varijabli.

fcd = 20.0   # GLOBALNA varijabla (definirana izvan funkcije)

def provjeri_presjek(M_Ed, b, h):
    """Provjera nosivosti presjeka na savijanje."""
    # fcd je dostupna (globalna), ali je bolja praksa proslijediti je
    Wy    = (b * h**2) / 6       # LOKALNA varijabla
    sigma = (M_Ed / Wy) / 1000   # LOKALNA varijabla
    ok    = sigma <= fcd          # koristi globalnu fcd
    return sigma, ok

sigma, ok = provjeri_presjek(150.0, 0.30, 0.50)
print(f"sigma = {sigma:.2f} MPa,  OK = {ok}")

# Wy i sigma iz funkcije NISU dostupni ovdje:
# print(Wy)    # NameError: name 'Wy' is not defined


# %% [6] Dokumentacijski nizovi --- docstrings
# Pisanje i čitanje docstringa; pregled u Spyder Help prozoru (Ctrl+I).

def progib_proste_grede(q, L, E, I):
    """
    Izračunava maksimalni progib proste grede pod jednolikim
    opterećenjem prema formuli: w = 5*q*L^4 / (384*E*I).

    Argumenti:
        q : jednoliko opterećenje [kN/m]
        L : raspon grede [m]
        E : modul elastičnosti [kN/m²]
        I : moment tromosti [m⁴]

    Vraća:
        w_max : maksimalni progib na sredini raspona [m]
    """
    w_max = (5 * q * L**4) / (384 * E * I)
    return w_max

# Pristup docstringu
help(progib_proste_grede)          # puni ispis u konzoli
print(progib_proste_grede.__doc__) # izravni pristup

# Primjer poziva
b, h   = 0.30, 0.55    # [m]
E_kN   = 32000 * 1000  # [kN/m²]
I_m4   = (b * h**3) / 12
w      = progib_proste_grede(q=20.0, L=6.0, E=E_kN, I=I_m4)
print(f"\nProgib: w_max = {w*1000:.2f} mm")


# %% [7] Lambda funkcije
# Kratki zapis anonimne funkcije; primjena za sortiranje liste rječnika.

# Standardna funkcija:
def pretvori_u_cm4(I_m4):
    return I_m4 * 1e8

# Ekvivalentna lambda funkcija:
pretvori_u_cm4_lambda = lambda I_m4: I_m4 * 1e8

print(pretvori_u_cm4(0.003125))         # 312500.0 cm⁴
print(pretvori_u_cm4_lambda(0.003125))  # 312500.0 cm⁴

# Najčešća primjena: sortiranje složenih struktura
grede = [
    {"oznaka": "G1", "L": 6.5, "sigma": 18.2},
    {"oznaka": "G2", "L": 4.0, "sigma": 9.5},
    {"oznaka": "G3", "L": 5.5, "sigma": 14.7},
]

# Sortiraj po naprezanju (uzlazno)
grede_sort = sorted(grede, key=lambda g: g["sigma"])
print("\nGrede sortirane po naprezanju:")
for g in grede_sort:
    print(f"  {g['oznaka']}: sigma = {g['sigma']:.1f} MPa")


# %% [8] Uvoz modula --- načini importa
# Četiri načina uvoza modula; preporuke za inženjerski kod.

# 1) Uvoz cijelog modula --- pristup kao modul.funkcija
import math
print(math.sqrt(25))      # 5.0
print(math.pi)            # 3.14159...

# 2) Uvoz s aliasom --- kraći naziv
import math as m
print(m.sin(m.pi / 6))    # 0.5

# 3) Uvoz samo određenih funkcija --- direktan pristup
from math import sqrt, pi, sin, cos, log
print(sqrt(144))          # 12.0  (bez prefiksa math.)
print(sin(pi / 2))        # 1.0

# 4) Uvoz svega --- NE preporuča se (zagađuje namespace!)
# from math import *


# %% [9] Kreiranje vlastitog modula
# Simulacija vlastitog modula definiranjem funkcija u istoj skripti.
# U praksi bi ove funkcije bile u zasebnoj datoteci presjeci.py.

import math

# ---- sadržaj datoteke: presjeci.py ----

def pravokutnik(b, h):
    """Geometrijska svojstva pravokutnog presjeka."""
    A = b * h
    I = (b * h**3) / 12
    W = (b * h**2) / 6
    i = (I / A)**0.5
    return {"A": A, "I": I, "W": W, "i": i}

def krug(D):
    """Geometrijska svojstva punog kružnog presjeka."""
    A = math.pi * D**2 / 4
    I = math.pi * D**4 / 64
    W = math.pi * D**3 / 32
    i = D / 4
    return {"A": A, "I": I, "W": W, "i": i}

# ---- sadržaj datoteke: glavni_proracun.py ----
# import presjeci  <-- ovako bi glasio uvoz iz zasebne datoteke

s_prav = pravokutnik(0.30, 0.55)
s_krug = krug(0.40)

print(f"Pravokutnik 30×55: A = {s_prav['A']*1e4:.1f} cm²,"
      f"  I = {s_prav['I']*1e8:.1f} cm⁴")
print(f"Krug D=40 cm:      A = {s_krug['A']*1e4:.1f} cm²,"
      f"  I = {s_krug['I']*1e8:.1f} cm⁴")


# %% [10] Praktični primjer 1: Geometrijska svojstva poprečnih presjeka
# Dvije funkcije za različite oblike presjeka, poziv kroz petlju.

import math

def svojstva_pravokutnik(b, h):
    """Geometrijska svojstva pravokutnog AB presjeka [m]."""
    A = b * h
    I = (b * h**3) / 12
    W = (b * h**2) / 6
    i = (I / A)**0.5
    return A, I, W, i

def svojstva_krug(D):
    """Geometrijska svojstva kružnog presjeka (stup) [m]."""
    A = math.pi * D**2 / 4
    I = math.pi * D**4 / 64
    W = math.pi * D**3 / 32
    i = D / 4
    return A, I, W, i

# Serija presjeka: (naziv, tip, d1, d2)
# tip "P" = pravokutnik (d1=b, d2=h), tip "K" = krug (d1=D)
presjeci = [
    ("Pravok. 30×55", "P", 0.30, 0.55),
    ("Pravok. 40×70", "P", 0.40, 0.70),
    ("Krug  D=40cm",  "K", 0.40, None),
]

print(f"{'Presjek':>16} | {'A[cm²]':>8} | {'I[cm⁴]':>10} |"
      f" {'W[cm³]':>9} | {'i[cm]':>7}")
print("-" * 60)
for naziv, tip, d1, d2 in presjeci:
    if tip == "P":
        A, I, W, i = svojstva_pravokutnik(d1, d2)
    else:
        A, I, W, i = svojstva_krug(d1)
    print(f"{naziv:>16} | {A*1e4:>8.1f} | {I*1e8:>10.1f} |"
          f" {W*1e6:>9.1f} | {i*1e2:>7.2f}")


# %% [11] Praktični primjer 2: Nosivost čelične grede --- IPE profil
# Moment nosivosti čeličnih IPE profila prema EN 1993-1-1.

def nosivost_IPE(Wy_cm3, fyk=355.0, gamma_M0=1.0):
    """
    Moment nosivosti čeličnog IPE profila prema EN 1993-1-1.
    Wy_cm3  : moment otpora [cm³] (iz tablica profila)
    fyk     : karakteristična granica popuštanja [MPa] (zad: S355)
    gamma_M0: parcijalni faktor sigurnosti (zad: 1.0)
    """
    fyd   = fyk / gamma_M0     # [MPa] projektna čvrstoća
    Wy_m3 = Wy_cm3 * 1e-6      # pretvorba cm³ -> m³
    Mc_Rd = Wy_m3 * fyd * 1000 # [kNm] moment nosivosti
    return Mc_Rd

# IPE profili: (oznaka, Wy [cm³], G [kg/m])
profili_IPE = [
    ("IPE 300", 557.0,  42.2),
    ("IPE 360", 903.0,  57.1),
    ("IPE 400", 1307.0, 66.3),
    ("IPE 450", 1702.0, 77.6),
]

print(f"Čelik S355 | gamma_M0 = 1.0")
print(f"{'Profil':>10} | {'Wy [cm³]':>10} | "
      f"{'Mc,Rd [kNm]':>12} | {'G [kg/m]':>9}")
print("-" * 50)
for naziv, Wy, G in profili_IPE:
    Mc = nosivost_IPE(Wy)
    print(f"{naziv:>10} | {Wy:>10.1f} | {Mc:>12.1f} | {G:>9.1f}")

# Usporedba S235 vs S355 za IPE 400
print("\nUsporedba čelika za IPE 400:")
for naziv_c, fyk in [("S235", 235.0), ("S275", 275.0), ("S355", 355.0)]:
    Mc = nosivost_IPE(1307.0, fyk=fyk)
    print(f"  {naziv_c}: Mc,Rd = {Mc:.1f} kNm")


# %% [12] Praktični primjer 3: Nosivost drvene grede
# Moment nosivosti drvene grede prema EN 1995-1-1 (EC5).

def nosivost_drvena_greda(b, h, fm_k, kmod=0.8,
                          gamma_M=1.3, kh=1.0):
    """
    Moment nosivosti drvene grede prema EN 1995-1-1 (EC5).
    b, h   : dimenzije presjeka [m]
    fm_k   : karakteristična čvrstoća na savijanje [MPa]
    kmod   : modifikacijski faktor (klasa trajanja, vlažnost)
    gamma_M: parcijalni faktor (zadano: 1.3 za rezano drvo)
    kh     : faktor visine (zadano: 1.0)
    """
    fm_d = kmod * kh * fm_k / gamma_M   # [MPa] projektna čvrstoća
    W    = (b * h**2) / 6               # [m³] moment otpora
    Md_R = W * fm_d * 1000              # [kNm] moment nosivosti
    return Md_R, fm_d

# Klase čvrstoće rezanog drva prema EN 338
razredi = [("C16", 16.0), ("C24", 24.0), ("C30", 30.0)]
b, h    = 0.10, 0.20   # [m]

print(f"Drvena greda: b = {b*100:.0f} cm × h = {h*100:.0f} cm")
print(f"kmod = 0.8 (klasa trajanja: srednje), gamma_M = 1.3")
print(f"\n{'Klasa':>6} | {'fm,k [MPa]':>10} | "
      f"{'fm,d [MPa]':>10} | {'Md,R [kNm]':>10}")
print("-" * 46)
for klasa, fm_k in razredi:
    Md_R, fm_d = nosivost_drvena_greda(b, h, fm_k)
    print(f"{klasa:>6} | {fm_k:>10.1f} | "
          f"{fm_d:>10.2f} | {Md_R:>10.3f}")


# %% [13] Praktični primjer 4: Nosivost ziđa na vertikalno opterećenje
# Vertikalna nosivost nearmirane zidane ploče prema EN 1996-1-1 (EC6).

def nosivost_zida(t, L, fk, gamma_M=2.5, Phi=0.8):
    """
    Vertikalna nosivost nearmirane zidane ploče prema EN 1996-1-1.
    t      : debljina zida [m]
    L      : duljina zida [m]
    fk     : karakteristična tlačna čvrstoća ziđa [MPa]
    gamma_M: parcijalni faktor sigurnosti (zad: 2.5)
    Phi    : faktor smanjenja kapaciteta --- ekscentricitet
    """
    fd  = fk / gamma_M           # [MPa] projektna čvrstoća
    A   = t * L                  # [m²] površina presjeka
    NRd = Phi * A * fd * 1000    # [kN] nosivost
    return NRd, fd

# Zidovi od opeke i blokova različitih klasa
zidovi = [
    ("Opeka M5",  2.5, 0.25, 2.0),
    ("Opeka M10", 5.0, 0.25, 2.0),
    ("Blok M5",   3.5, 0.20, 2.5),
]

print(f"{'Materijal':>12} | {'fk[MPa]':>8} | "
      f"{'t[m]':>5} | {'L[m]':>5} | {'fd[MPa]':>8} | {'NRd[kN]':>9}")
print("-" * 60)
for naziv, fk, t, L in zidovi:
    NRd, fd = nosivost_zida(t, L, fk)
    print(f"{naziv:>12} | {fk:>8.1f} | "
          f"{t:>5.2f} | {L:>5.1f} | {fd:>8.3f} | {NRd:>9.1f}")


# %% [14] Praktični primjer 5: Modularna knjižnica za proračun AB grede
# Funkcija koja poziva drugu funkciju; kompletna provjera GNS i GSU.

def moment_tromosti(b, h):
    """Moment tromosti pravokutnog presjeka oko težišne osi [m⁴]."""
    return (b * h**3) / 12

def naprezanje(M_Ed, b, h):
    """Naprezanje od savijanja u pravokutnom presjeku [MPa]."""
    W = (b * h**2) / 6
    return (M_Ed / W) / 1000

def progib(q, L, E, b, h):
    """Maksimalni progib proste grede pod jednolikim opterećenjem [m]."""
    I     = moment_tromosti(b, h)    # poziv druge funkcije!
    w_max = (5 * q * L**4) / (384 * E * I)
    return w_max

def provjera_grede(naziv, L, b, h, q, fcd=20.0, Ecm=32e6):
    """
    Kompletna provjera nosivosti i upotrebljivosti AB grede.
    GNS: sigma <= fcd
    GSU: w_max <= L/250
    """
    M_Ed  = q * L**2 / 8
    sigma = naprezanje(M_Ed, b, h)
    w_max = progib(q, L, Ecm, b, h)
    L250  = L / 250
    ok_N  = sigma <= fcd
    ok_U  = w_max <= L250
    print(f"\n{'='*48}")
    print(f"  Greda: {naziv}")
    print(f"  {'Veličina':<22} {'Vrijednost':>10}  {'Limit':>8}  Status")
    print(f"  {'-'*44}")
    print(f"  {'M_Ed [kNm]':<22} {M_Ed:>10.2f}")
    print(f"  {'sigma [MPa]':<22} {sigma:>10.2f}  {fcd:>8.1f}  "
          f"{'OK' if ok_N else 'NOK !'}")
    print(f"  {'w_max [mm]':<22} {w_max*1000:>10.2f}  {L250*1000:>8.1f}  "
          f"{'OK' if ok_U else 'NOK !'}")
    print(f"{'='*48}")

# Provjera za dvije grede
provjera_grede("G1 (30×55 cm)", L=6.0, b=0.30, h=0.55, q=25.0)
provjera_grede("G2 (25×45 cm)", L=4.5, b=0.25, h=0.45, q=18.0)
provjera_grede("G3 (25×40 cm)", L=5.0, b=0.25, h=0.40, q=30.0)