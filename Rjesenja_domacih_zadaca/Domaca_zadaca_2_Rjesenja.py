# =============================================================================
# Računalno programiranje u građevinarstvu (254810)
# Domaća zadaća #2 — Analiza armiranobetonske grede
# =============================================================================
# Opis   : Program analizira jednu AB gredu definiranu rječnikom ulaznih
#          parametara. Računa moment savijanja, moment otpora, naprezanje
#          i stupanj iskorištenosti te klasificira gredu grananjima.
# =============================================================================

# -----------------------------------------------------------------------------
# 1. ULAZNI PARAMETRI — definirani kao rječnik
# -----------------------------------------------------------------------------

greda = {
    "L"  : 6.0,   # [m]    raspon grede
    "b"  : 0.30,  # [m]    širina presjeka
    "h"  : 0.50,  # [m]    visina presjeka
    "q"  : 18.0,  # [kN/m] jednoliko opterećenje
    "fcd": 20.0,  # [MPa]  projektna tlačna čvrstoća betona
}

# Dohvat vrijednosti iz rječnika u lokalne varijable (čitljiviji kôd)
L   = greda["L"]
b   = greda["b"]
h   = greda["h"]
q   = greda["q"]
fcd = greda["fcd"]

# -----------------------------------------------------------------------------
# 2. PRORAČUN
# -----------------------------------------------------------------------------

# Maksimalni moment savijanja proste grede pod jednolikim opterećenjem
# Formula: M_max = q * L^2 / 8
M_max = (q * L**2) / 8          # [kNm]

# Moment otpora pravokutnog presjeka
# Formula: Wy = b * h^2 / 6
Wy = (b * h**2) / 6             # [m³]

# Naprezanje od savijanja (M u kNm, Wy u m³ → faktor 1000 za MPa)
# Formula: sigma = M_max / (Wy * 1000)
sigma = M_max / (Wy * 1000)     # [MPa]

# Stupanj iskorištenosti presjeka u postocima
# Formula: eta = (sigma / fcd) * 100
eta = (sigma / fcd) * 100       # [%]

# Vitkost grede (omjer raspona i visine presjeka)
vitkost = L / h                 # [-]

# -----------------------------------------------------------------------------
# 3. KLASIFIKACIJA GRANANJIMA (if / elif / else)
# -----------------------------------------------------------------------------

# --- 3a. Status nosivosti ---
if sigma <= fcd:
    status_nosivosti = "OK"
else:
    status_nosivosti = "NOK"

# --- 3b. Razred iskorištenosti prema eta [%] ---
if eta <= 50.0:
    razred_iskor = "Nisko"
elif eta <= 80.0:
    razred_iskor = "Srednje"
elif eta <= 100.0:
    razred_iskor = "Visoko"
else:
    razred_iskor = "Prekoračenje!"

# --- 3c. Vitkost grede prema omjeru L/h ---
if vitkost <= 10.0:
    razred_vitkosti = "Kratka"
elif vitkost <= 20.0:
    razred_vitkosti = "Standardna"
else:
    razred_vitkosti = "Vitka – provjeriti progib!"

# --- 3d. Preporuka razreda betona prema eta [%] ---
if eta <= 50.0:
    preporuka_betona = "C20/25 dovoljan"
elif eta <= 80.0:
    preporuka_betona = "C25/30 preporučen"
elif eta <= 100.0:
    preporuka_betona = "C30/37 preporučen"
else:
    preporuka_betona = "Reprojektirati presjek!"

# -----------------------------------------------------------------------------
# 4. ISPIS REZULTATA
# -----------------------------------------------------------------------------

print("=" * 55)
print("  ANALIZA ARMIRANOBETONSKE GREDE")
print("=" * 55)

# Ulazni parametri
print("\n  ULAZNI PARAMETRI")
print(f"  {'Raspon grede':<30} L   = {L:.2f} m")
print(f"  {'Širina presjeka':<30} b   = {b:.2f} m")
print(f"  {'Visina presjeka':<30} h   = {h:.2f} m")
print(f"  {'Jednoliko opterećenje':<30} q   = {q:.2f} kN/m")
print(f"  {'Proj. čvrstoća betona':<30} fcd = {fcd:.1f} MPa")

# Rezultati proračuna
print("\n  REZULTATI PRORAČUNA")
print("-" * 55)
print(f"  {'Maks. moment savijanja':<30} M   = {M_max:.2f} kNm")
print(f"  {'Moment otpora':<30} Wy  = {Wy * 1e6:.1f} cm³")
print(f"  {'Naprezanje od savijanja':<30} σ   = {sigma:.2f} MPa")
print(f"  {'Stupanj iskorištenosti':<30} η   = {eta:.1f} %")
print(f"  {'Vitkost grede (L/h)':<30} L/h = {vitkost:.1f}")

# Klasifikacija
print("\n  KLASIFIKACIJA")
print("-" * 55)
print(f"  Status nosivosti      : {status_nosivosti}")
print(f"  Razred iskorištenosti : {razred_iskor} (η = {eta:.1f} %)")
print(f"  Vitkost grede         : {razred_vitkosti} (L/h = {vitkost:.1f})")
print(f"  Preporuka betona      : {preporuka_betona}")
print("=" * 55)
