# %% ============================================================
# PRIMJER 1: Interpolacija mjerenih podataka nosive konstrukcije
# ===============================================================
#
# Kontekst:
#   Laboratorijsko ispitivanje armiranobetonske (AB) grede savijanjem.
#   Mjeri se progib (w) u sredini raspona pri diskretnim razinama
#   opterećenja (F). Zbog ograničenog broja mjernih točaka koristimo
#   interpolaciju da dobijemo glatku F–w krivulju i procjenimo
#   progib pri proizvoljnoj razini sile.
#
# Fizikalna pozadina:
#   - U linearno-elastičnom području: w = F·L³/(48·E·I)
#   - U nelinearnom području (nakon pukotine i tečenja armature)
#     odnos F–w više nije linearan → interpolacija je nužna za
#     procjenu krutosti i nosivosti na temelju mjerenih podataka.
#
# Metode interpolacije koje se prikazuju:
#   1. Linearna (interp1d, kind='linear')
#   2. Kvadratna / kvadratna spline (interp1d, kind='quadratic')
#   3. Kubna (interp1d, kind='cubic')
#   4. Prirodni kubni spline (scipy.interpolate.CubicSpline)
# ===============================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# ---------------------------------------------------------------
# IZMJERENI PODACI — laboratorijsko ispitivanje AB grede
# ---------------------------------------------------------------
# Sila F [kN] i progib w u sredini raspona [mm]
# 8 diskretnih mjernih točaka (tipičan broj u praksi)

F_mjereno = np.array([0.0,  10.0, 25.0, 45.0, 60.0, 80.0, 100.0, 120.0])  # [kN]
w_mjereno = np.array([0.0,   1.2,  3.8,  8.5, 13.2, 21.0,  32.5,  48.0])  # [mm]

# Napomena:
#   - Nelinearnost se pojačava iznad ~45 kN (nastanak pukotina)
#   - Nagli porast progiba između 100 i 120 kN → tečenje armature

# Fina jednolična mreža za prikaz interpoliranih krivulja
F_fino = np.linspace(F_mjereno[0], F_mjereno[-1], 500)

# ---------------------------------------------------------------
# 1. LINEARNA INTERPOLACIJA
# ---------------------------------------------------------------
# Svaki par susjednih točaka spaja se ravnim pravcem.
# Prednost:  jednostavna, uvijek stabilna
# Nedostatak: "lomovi" (diskontinuitet derivacije) u čvornim točkama
#             → nerealično za fizikalne pojave
interp_lin = interpolate.interp1d(F_mjereno, w_mjereno, kind='linear')
w_lin = interp_lin(F_fino)

# ---------------------------------------------------------------
# 2. KVADRATNA (KVADRATNA SPLINE) INTERPOLACIJA
# ---------------------------------------------------------------
# Između svaka dva čvora koristi polinom 2. stupnja.
# Glađa od linearne, ali može oscilirati na neravnomjernim podacima.
interp_kv = interpolate.interp1d(F_mjereno, w_mjereno, kind='quadratic')
w_kv = interp_kv(F_fino)

# ---------------------------------------------------------------
# 3. KUBNA INTERPOLACIJA (scipy.interpolate.interp1d)
# ---------------------------------------------------------------
# Polinomi 3. stupnja između čvorova, kontinuitet do 2. derivacije.
# Najčešće korištena metoda — glatka i stabilna za inženjerske podatke.
interp_kub = interpolate.interp1d(F_mjereno, w_mjereno, kind='cubic')
w_kub = interp_kub(F_fino)

# ---------------------------------------------------------------
# 4. PRIRODNI KUBNI SPLINE (scipy.interpolate.CubicSpline)
# ---------------------------------------------------------------
# Detaljnija kontrola rubnih uvjeta spline krivulje.
# bc_type='natural' → druga derivacija je nula na rubovima
# (odgovara slobodnoj osi savijanja, fizikalno opravdano za gredu)
cs = interpolate.CubicSpline(F_mjereno, w_mjereno, bc_type='natural')
w_cs = cs(F_fino)

# ---------------------------------------------------------------
# PROCJENA PROGIBA ZA SPECIFIČNE VRIJEDNOSTI SILE
# ---------------------------------------------------------------
# Primjena interpolacije za dobivanje w pri silama između mjernih točaka
F_upit_lista = [35.0, 55.0, 90.0, 110.0]  # [kN]

print("=" * 65)
print("PRIMJER 1: Interpolacija F–w dijagrama AB grede")
print("=" * 65)
print(f"\n{'Sila F [kN]':<15} {'Linearna':>12} {'Kvadratna':>12} "
      f"{'Kubna':>12} {'Kub. spline':>12}")
print("-" * 65)
for F_upit in F_upit_lista:
    print(f"{F_upit:<15.1f} "
          f"{interp_lin(F_upit):>12.3f} "
          f"{interp_kv(F_upit):>12.3f} "
          f"{interp_kub(F_upit):>12.3f} "
          f"{cs(F_upit):>12.3f}")
print("(sve vrijednosti u mm)")

# ---------------------------------------------------------------
# KRUTOST — derivacija F–w krivulje (tangentna krutost)
# ---------------------------------------------------------------
# Tangentna krutost: K = dF/dw = 1 / (dw/dF) [kN/mm]
# Računamo derivaciju kubnog spline-a
dw_dF = cs(F_fino, 1)      # 1. derivacija CubicSpline
K_tang = 1.0 / dw_dF       # tangentna krutost [kN/mm]

# ---------------------------------------------------------------
# GRAFIČKI PRIKAZ — 2×2 raspored
# ---------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(
    'Primjer 1 — Interpolacija F–w dijagrama armiranobetonske grede\n'
    'Laboratorijsko ispitivanje savijanjem',
    fontsize=14, fontweight='bold'
)

# Stil za izmjerene točke (zajednički za sve grafove)
stil_tocke = dict(
    color='black', marker='o', markersize=8,
    linestyle='None', label='Izmjerene vrijednosti', zorder=5
)

# ── GRAF 1: Linearna interpolacija ──────────────────────────────
ax = axes[0, 0]
ax.plot(F_fino, w_lin, color='#2980b9', linewidth=2, label='Linearna interpolacija')
ax.plot(F_mjereno, w_mjereno, **stil_tocke)
ax.set_title('Linearna interpolacija', fontweight='bold')
ax.set_xlabel('Sila F [kN]')
ax.set_ylabel('Progib w [mm]')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
# Oznaka nedostatka: lom u čvornoj točki
ax.annotate(
    '"Lom" — diskontinuitet\nkrivulje u čvornoj točki',
    xy=(45, 8.5), xytext=(55, 4.5),
    arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=1.5),
    color='#e74c3c', fontsize=8.5,
    bbox=dict(boxstyle='round,pad=0.3', facecolor='#fdecea', alpha=0.8)
)

# ── GRAF 2: Kvadratna interpolacija ─────────────────────────────
ax = axes[0, 1]
ax.plot(F_fino, w_kv, color='#27ae60', linewidth=2, label='Kvadratna interpolacija')
ax.plot(F_mjereno, w_mjereno, **stil_tocke)
ax.set_title('Kvadratna (kvadratna spline) interpolacija', fontweight='bold')
ax.set_xlabel('Sila F [kN]')
ax.set_ylabel('Progib w [mm]')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# ── GRAF 3: Kubna interpolacija (interp1d) ───────────────────────
ax = axes[1, 0]
ax.plot(F_fino, w_kub, color='#e74c3c', linewidth=2, label='Kubna interpolacija (interp1d)')
ax.plot(F_mjereno, w_mjereno, **stil_tocke)
ax.set_title('Kubna interpolacija (scipy.interp1d)', fontweight='bold')
ax.set_xlabel('Sila F [kN]')
ax.set_ylabel('Progib w [mm]')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# ── GRAF 4: Usporedba svih metoda + tangentna krutost ───────────
ax = axes[1, 1]
ax.plot(F_fino, w_lin, color='#2980b9',  linestyle='--',  linewidth=1.5,
        label='Linearna', alpha=0.85)
ax.plot(F_fino, w_kv,  color='#27ae60',  linestyle='-.',  linewidth=1.5,
        label='Kvadratna', alpha=0.85)
ax.plot(F_fino, w_kub, color='#e74c3c',  linestyle='-',   linewidth=2.0,
        label='Kubna (interp1d)')
ax.plot(F_fino, w_cs,  color='#8e44ad',  linestyle=':',   linewidth=2.5,
        label='Prirodni kubni spline')
ax.plot(F_mjereno, w_mjereno, **stil_tocke)
# Označi upitane vrijednosti
for F_upit in F_upit_lista:
    w_upit = cs(F_upit)
    ax.plot(F_upit, w_upit, 'v', color='#f39c12', markersize=10, zorder=6)
    ax.annotate(
        f'F={F_upit:.0f} kN\nw={w_upit:.1f} mm',
        xy=(F_upit, w_upit), xytext=(F_upit + 4, w_upit - 4),
        fontsize=7.5, color='#7f6000',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#fef9e7', alpha=0.8)
    )
ax.set_title('Usporedba svih metoda interpolacije', fontweight='bold')
ax.set_xlabel('Sila F [kN]')
ax.set_ylabel('Progib w [mm]')
ax.legend(loc='upper left', fontsize=8.5)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('primjer_01_interpolacija.pdf',
            dpi=150, bbox_inches='tight')
plt.show()

# ── DODATNI GRAF: Tangentna krutost K = dF/dw ───────────────────
fig2, ax2 = plt.subplots(figsize=(9, 4))
ax2.plot(F_fino, K_tang, color='#8e44ad', linewidth=2.5)
ax2.fill_between(F_fino, K_tang, alpha=0.15, color='#8e44ad')
ax2.set_title(
    'Tangentna krutost grede K = dF/dw  (iz derivacije kubnog spline-a)\n'
    'Opadanje krutosti → nastanak pukotina i tečenje armature',
    fontweight='bold'
)
ax2.set_xlabel('Sila F [kN]')
ax2.set_ylabel('Tangentna krutost K [kN/mm]')
ax2.grid(True, alpha=0.3)
# Označi liniju nastanka pukotina (aproximativno)
F_pcr = 25.0
ax2.axvline(F_pcr, color='#e74c3c', linestyle='--', linewidth=1.5,
            label=f'≈ Nastanak pukotina (F ≈ {F_pcr} kN)')
ax2.legend(fontsize=9)
plt.tight_layout()
plt.savefig('primjer_01_krutost.pdf',
            dpi=150, bbox_inches='tight')
plt.show()

print("\nGrafovi su pohranjeni.")
