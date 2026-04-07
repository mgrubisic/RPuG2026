# =============================================================================
#  Računalno programiranje u građevinarstvu (254810) | Tjedan 3/15
#  Primjer 1: Izvijanje tlačnih štapova --- Eulerova kritična sila
#  Izv. prof. dr. sc. Marin Grubišić | GrAFOS Osijek | AY 2025./2026.
# =============================================================================
#
#  SADRŽAJ (korak po korak):
#   Korak 1 | Uvoz modula i definicija pomoćnih funkcija
#   Korak 2 | Funkcija za kritičnu silu (pozicijski i keyword argumenti)
#   Korak 3 | Funkcija s DEFAULT vrijednošću (uvjet oslonaca → faktor β)
#   Korak 4 | Višestruke povratne vrijednosti + raspakiranje
#   Korak 5 | Lambda funkcija za jediničnu pretvorbu
#   Korak 6 | Analiza serije stupova --- poziv u petlji
#   Korak 7 | Doseg varijabli (scope) --- lokalne vs. globalne
# =============================================================================

# %% ── Korak 1: Uvoz modula ──────────────────────────────────────────────────
#
#  Standardna biblioteka: math (uvijek dostupno)
#  Nema potrebe za NumPy/SciPy --- Euler je analitički!

import math

print("=" * 60)
print("  EULEROVA KRITIČNA SILA ZA TLAČNE ŠTAPOVE")
print("=" * 60)

# %% ── Korak 2: Osnovna funkcija --- pozicijski argumenti ───────────────────
#
#  Eulerova formula: N_cr = π² · E · I / (β · L)²
#  β   = faktor duljine izvijanja (ovisi o uvjetima oslanjanja)
#  L   = geometrijska duljina štapa [m]
#  E   = modul elastičnosti [kN/m²]
#  I   = moment tromosti [m⁴]

def kritična_sila(E, I, L, beta):
    """
    Eulerova kritična sila tlačnog štapa [kN].

    Argumenti:
        E    : modul elastičnosti [kN/m²]
        I    : moment tromosti poprečnog presjeka [m⁴]
        L    : geometrijska duljina štapa [m]
        beta : faktor duljine izvijanja (1.0, 0.7, 0.5, 2.0)

    Vraća:
        N_cr : Eulerova kritična sila [kN]
    """
    Lcr  = beta * L              # efektivna (izvijajuća) duljina [m]
    N_cr = (math.pi**2 * E * I) / Lcr**2
    return N_cr

# ── Testni poziv s pozicijskim argumentima ──
E_čelik = 210_000_000.0    # [kN/m²] = 210 GPa
I_test  = 8_356e-8         # [m⁴]  ~ HEA 200 oko slabe osi
L_test  = 4.0              # [m]

N_cr = kritična_sila(E_čelik, I_test, L_test, 1.0)
print(f"\nKorak 2 | N_cr (β=1.0) = {N_cr:.1f} kN")

# ── Isti poziv s imenovanim (keyword) argumentima ──
N_cr_kw = kritična_sila(E=E_čelik, I=I_test, L=L_test, beta=1.0)
print(f"          N_cr (kw)   = {N_cr_kw:.1f} kN  (isti rezultat)")

# %% ── Korak 3: DEFAULT vrijednosti --- faktor beta ─────────────────────────
#
#  Uvjeti oslanjanja prema EN 1993-1-1:
#   "obostrano zglobno"   → β = 1.0  (zadano, najčešći slučaj)
#   "konzola"             → β = 2.0
#   "upeto-zglobno"       → β = 0.7
#   "obostrano upeto"     → β = 0.5

def faktor_beta(uvjet="zglobno-zglobno"):
    """
    Vraća faktor duljine izvijanja β prema EN 1993-1-1.

    Argumenti:
        uvjet : string s opisom uvjeta oslanjanja
                Opcije: 'zglobno-zglobno', 'konzola',
                        'upeto-zglobno',   'obostrano-upeto'
                (zadano: 'zglobno-zglobno')

    Vraća:
        beta : faktor duljine izvijanja [-]
    """
    tablica = {
        "zglobno-zglobno" : 1.0,
        "konzola"         : 2.0,
        "upeto-zglobno"   : 0.7,
        "obostrano-upeto" : 0.5,
    }
    if uvjet not in tablica:
        raise ValueError(f"Nepoznat uvjet: '{uvjet}'. "
                         f"Dostupno: {list(tablica.keys())}")
    return tablica[uvjet]

# # ── Pozivi sa i bez argumenta (default!) ──
# print("\nKorak 3 | Faktori beta:")
# for uvjet in ["zglobno-zglobno", "konzola",
#               "upeto-zglobno", "obostrano-upeto"]:
#     beta = faktor_beta(uvjet)
#     print(f"  β({uvjet:>20}) = {beta:.1f}")

beta_default = faktor_beta()   # koristi DEFAULT vrijednost
print(f"\n  Poziv bez argumenta → β = {beta_default}  (default: 'zglobno-zglobno')")

# %% ── Korak 4: Višestruke povratne vrijednosti ─────────────────────────────
#
#  Funkcija vraća: N_cr, Lcr i vitkost λ --- sve kao n-torku

def analiza_izvijanja(E, I, A, L, uvjet="zglobno-zglobno"):
    """
    Potpuna analiza izvijanja tlačnog štapa prema EC3.

    Argumenti:
        E     : modul elastičnosti [kN/m²]
        I     : moment tromosti (slaba os) [m⁴]
        A     : površina presjeka [m²]
        L     : duljina štapa [m]
        uvjet : uvjet oslanjanja (default: 'zglobno-zglobno')

    Vraća:
        N_cr    : Eulerova kritična sila [kN]
        Lcr     : efektivna duljina izvijanja [m]
        lambda_ : vitkost štapa [-]
    """
    beta    = faktor_beta(uvjet)          # poziv druge funkcije!
    Lcr     = beta * L
    N_cr    = (math.pi**2 * E * I) / Lcr**2
    i_pol   = math.sqrt(I / A)           # polumjer tromosti [m]
    lam     = Lcr / i_pol               # vitkost [-]
    return N_cr, Lcr, lam            # n-torka

# ── Raspakiranje povratnih vrijednosti ──
I_HEA200 = 1_336e-8    # [m⁴]  HEA 200 --- slaba os (Iz)
A_HEA200 = 53.83e-4    # [m²]  HEA 200

N_cr, Lcr, lam = analiza_izvijanja(E_čelik, I_HEA200, A_HEA200, L=4.0)

print(f"\nKorak 4 | HEA 200, L=4.0 m, zglobno-zglobno:")
print(f"  N_cr    = {N_cr:.1f} kN")
print(f"  Lcr     = {Lcr:.2f} m")
print(f"  λ (vitkost) = {lam:.1f}")

# # ── Alternativno: kao n-torka (bez raspakiranja) ──
# rezultati = analiza_izvijanja(E_čelik, I_HEA200, A_HEA200, 4.0, "konzola")
# print(f"\n  Konzola → N_cr = {rezultati[0]:.1f} kN,  λ = {rezultati[2]:.1f}")

# %% ── Korak 5: Lambda funkcija --- pretvorba jedinica ──────────────────────
#
#  Kratki jednolinjski transformatori --- korisni za tablice

u_cm4   = lambda I_m4 : I_m4 * 1e8      # m⁴ → cm⁴
u_kNcm2 = lambda E_kNm2 : E_kNm2 * 1e-4 # kN/m² → kN/cm²

print(f"\nKorak 5 | Lambda pretvorbe:")
print(f"  I_HEA200 = {u_cm4(I_HEA200):.0f} cm⁴")
print(f"  E_čelik  = {u_kNcm2(E_čelik):.0f} kN/cm²")

# Sortiranje profila po kritičnoj sili (lambda kao ključ sortiranja)
profili = [
    {"naziv": "HEA 160", "I": 479e-8,  "A": 38.77e-4},
    {"naziv": "HEA 200", "I": 1336e-8, "A": 53.83e-4},
    {"naziv": "HEA 240", "I": 3923e-8, "A": 76.84e-4},
]
for p in profili:
    p["N_cr"], _, _ = analiza_izvijanja(E_čelik, p["I"], p["A"], L=4.0)

sortirano = sorted(profili, key=lambda p: p["N_cr"])
print("\n  Profili sortirani po N_cr (uzlazno):")
for p in sortirano:
    print(f"  {p['naziv']:>8}: N_cr = {p['N_cr']:>8.1f} kN")

# # %% ── Korak 6: Analiza serije stupova --- petlja + funkcije ────────────────

# stupovi = [
#     ("S1 (HEA 200, L=3m, zg-zg)", I_HEA200, A_HEA200, 3.0, "zglobno-zglobno"),
#     ("S2 (HEA 200, L=4m, kons.)", I_HEA200, A_HEA200, 4.0, "konzola"),
#     ("S3 (HEA 200, L=6m, zg-zg)", I_HEA200, A_HEA200, 6.0, "zglobno-zglobno"),
#     ("S4 (HEA 240, L=5m, up-zg)", I_HEA200, A_HEA200, 5.0, "upeto-zglobno"),
# ]

# print("\nKorak 6 | Analiza serije stupova:")
# print(f"  {'Stup':<30} {'N_cr [kN]':>10} {'Lcr [m]':>8} {'λ [-]':>8}")
# print("  " + "-" * 60)
# for naziv, I, A, L, uvjet in stupovi:
#     N_cr, Lcr, lam = analiza_izvijanja(E_čelik, I, A, L, uvjet)
#     print(f"  {naziv:<30} {N_cr:>10.1f} {Lcr:>8.2f} {lam:>8.1f}")

# # %% ── Korak 7: Doseg varijabli (scope) ─────────────────────────────────────
# #
# #  Demonstracija: globalna varijabla kao brojač poziva funkcije

# broj_analiza = 0    # GLOBALNA varijabla

# def analiziraj_i_broji(E, I, A, L, uvjet="zglobno-zglobno"):
#     """Omotač koji broji koliko je puta analiza pozvana."""
#     global broj_analiza        # deklariramo globalnu
#     broj_analiza += 1          # mijenjamo globalnu
#     return analiza_izvijanja(E, I, A, L, uvjet)

# # Tri poziva
# analiziraj_i_broji(E_čelik, I_HEA200, A_HEA200, 3.0)
# analiziraj_i_broji(E_čelik, I_HEA200, A_HEA200, 4.0, "konzola")
# analiziraj_i_broji(E_čelik, I_HEA200, A_HEA200, 5.0, "upeto-zglobno")

# print(f"\nKorak 7 | Ukupno provedenih analiza: {broj_analiza}")
# print("\n" + "=" * 60)
# print("  Kraj primjera 1 --- Eulerovo izvijanje")
# print("=" * 60)
