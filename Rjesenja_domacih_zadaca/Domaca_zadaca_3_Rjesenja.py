# =============================================================================
# Računalno programiranje u građevinarstvu (254810)
# Domaća zadaća #2 — Analiza AB stupova
# =============================================================================
# Opis   : Program analizira skup od četiri AB stupa definiranih kao lista
#          rječnika. Za svaki stup računa površinu presjeka, tlačno
#          naprezanje, moment tromosti, polumjer tromosti i vitkost.
#          Ugniježđenim grananjem (if/elif/else) klasificira nosivost
#          (OK/NOK) i razred vitkosti. Bonus: petlja while iterativno
#          povećava presjek NOK stupa za 5 cm dok uvjet nije zadovoljen.
# =============================================================================

import math  # učitavanje standardnog matematičkog modula

# %% ── 1. Ulazni podaci ───────────────────────────────────────────────────────
#
#  Svi podaci o stupovima definirani su kao lista rječnika.
#  Ključevi: "oznaka", "N_Ed" [kN], "L" [m], "b" [m], "h" [m]

stupovi = [
    {"oznaka": "S1", "N_Ed": 1200, "L": 2.5, "b": 0.40, "h": 0.40},
    {"oznaka": "S2", "N_Ed": 1800, "L": 4.0, "b": 0.40, "h": 0.40},
    {"oznaka": "S3", "N_Ed": 3500, "L": 5.0, "b": 0.35, "h": 0.35},
    {"oznaka": "S4", "N_Ed":  500, "L": 6.5, "b": 0.25, "h": 0.25},
]

# Globalna projektna čvrstoća betona [MPa]
fcd = 20.0

# %% ── 2. Zaglavlje tablice ───────────────────────────────────────────────────

print("=" * 78)
print("  ANALIZA ARMIRANOBETONSKIH STUPOVA")
print(f"  Projektna čvrstoća betona: fcd = {fcd:.1f} MPa")
print("=" * 78)
print(
    f"  {'Oznaka':>7} | {'N_Ed [kN]':>9} | {'A [cm²]':>8} | "
    f"{'σc [MPa]':>8} | {'λ [-]':>7} | {'Status':>5} | Razred vitkosti"
)
print("-" * 78)

# %% ── 3. Glavna for petlja ───────────────────────────────────────────────────
#
#  Za svaki stup iz liste:
#   (a) izračunaj geometrijska i mehanička svojstva
#   (b) provjeri nosivost (vanjska razina grananja)
#   (c) klasificiraj vitkost (unutarnja razina grananja)

for stup in stupovi:

    # ── Dohvat podataka iz rječnika ──
    oznaka = stup["oznaka"]
    N_Ed   = stup["N_Ed"]      # [kN]
    L      = stup["L"]         # [m]
    b      = stup["b"]         # [m]
    h      = stup["h"]         # [m]

    # ── Proračun (1–5) ──
    A      = b * h                          # [m²]  površina presjeka
    sigma_c = N_Ed / (A * 1000)             # [MPa] tlačno naprezanje
    I      = (b * h**3) / 12               # [m⁴]  moment tromosti
    i_pol  = math.sqrt(I / A)              # [m]   polumjer tromosti
    lam    = L / i_pol                     # [-]   vitkost stupa

    # ── Vanjska razina: provjera nosivosti ──
    if sigma_c <= fcd:
        status = "OK"

        # ── Unutarnja razina: razred vitkosti (samo za OK stupove) ──
        if lam <= 30:
            razred = "Kratki stup"
        elif lam <= 80:
            razred = "Srednje vitki stup"
        else:
            razred = "Vitki stup - provjeriti izvijanje!"

    else:
        status = "NOK"
        razred = "Povecati presjek!"

    # ── Ispis retka tablice (f-stringovi) ──
    print(
        f"  {oznaka:>7} | {N_Ed:>9.0f} | {A*1e4:>8.2f} | "
        f"{sigma_c:>8.2f} | {lam:>7.1f} | {status:>5} | {razred}"
    )

print("=" * 78)

# %% ── 4. BONUS --- petlja while: iterativno povećanje NOK presjeka ──────────
#
#  Pronalazimo stup koji je "NOK" (sigma_c > fcd) i povećavamo
#  kvadratni presjek (b = h) za delta = 5 cm dok uvjet ne bude zadovoljen.

delta = 0.05    # korak povećanja stranice [m] = 5 cm

# Pronalazak NOK stupa (uzimamo prvog koji ne zadovoljava uvjet)
nok_stup = None
for stup in stupovi:
    b_test = stup["b"]
    h_test = stup["h"]
    A_test = b_test * h_test
    if stup["N_Ed"] / (A_test * 1000) > fcd:
        nok_stup = stup
        break   # uzimamo samo prvog NOK stupa

if nok_stup is None:
    print("\n  Svi stupovi zadovoljavaju uvjet nosivosti. Bonus nije primjenjiv.")
else:
    print(f"\n  BONUS --- Iterativno povećanje presjeka stupa {nok_stup['oznaka']}")
    print(f"  Polazni presjek: b = h = {nok_stup['b']*100:.1f} cm")
    print(f"  Uvjet: σc ≤ fcd = {fcd:.1f} MPa,  korak Δ = {delta*100:.0f} cm")
    print("-" * 55)
    print(f"  {'Iter.':>6} | {'b = h [cm]':>10} | {'A [cm²]':>8} | {'σc [MPa]':>9}")
    print("-" * 55)

    # Radne kopije dimenzija (ne mijenjamo originalni rječnik)
    b_iter = nok_stup["b"]
    h_iter = nok_stup["h"]
    N_Ed   = nok_stup["N_Ed"]

    # Početno stanje (iteracija 0 = polazišni presjek)
    iteracija = 0
    A_iter    = b_iter * h_iter
    sigma_iter = N_Ed / (A_iter * 1000)

    print(
        f"  {iteracija:>6} | {b_iter*100:>10.1f} | "
        f"{A_iter*1e4:>8.2f} | {sigma_iter:>8.2f}  ← polazište (NOK)"
    )

    # ── while petlja: povećavaj sve dok σc > fcd ──
    while sigma_iter > fcd:
        b_iter    += delta          # povećaj stranicu za 5 cm
        h_iter     = b_iter         # kvadratni presjek: b = h
        A_iter     = b_iter * h_iter
        sigma_iter = N_Ed / (A_iter * 1000)
        iteracija += 1

        print(
            f"  {iteracija:>6} | {b_iter*100:>10.1f} | "
            f"{A_iter*1e4:>8.2f} | {sigma_iter:>8.2f}"
        )

    # ── Završni ispis ──
    print("-" * 55)
    print(f"\n  Rezultat optimizacije presjeka {nok_stup['oznaka']}:")
    print(f"  Broj iteracija      : {iteracija}")
    print(f"  Konačne dimenzije   : b = h = {b_iter*100:.1f} cm")
    print(f"  Konačna površina    : A = {A_iter*1e4:.2f} cm²")
    print(f"  Postignuto naprezanje: σc = {sigma_iter:.2f} MPa ≤ fcd = {fcd:.1f} MPa  ✓")

print("\n" + "=" * 78)
print("  Kraj proračuna --- DZ3 uspješno završena!")
print("=" * 78)
