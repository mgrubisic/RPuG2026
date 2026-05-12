# %% ============================================================
# PRIMJER 3: Polinomijalna regresija — trendovi u nosivih konstrukcijama
# ===============================================================
#
# Kontekst:
#   Regresijska analiza mjerenih podataka iz laboratorija i terena.
#   Tri fizikalno motivirana trenda:
#
#   TREND 1 — LINEARNI:
#     Modul elastičnosti čelika E(T) u ovisnosti o temperaturi T.
#     Prema EN 1993-1-2 (Eurocode 3 — požarno projektiranje),
#     E opada gotovo linearno u opsegu 20–600 °C.
#     Regresija: E = a·T + b  (polinom stupnja 1)
#
#   TREND 2 — PARABOLIČNI (kvadratni):
#     Progib u sredini raspona slobodnooslonjene drvene grede
#     pri jednakomjernom opterećenju q:
#       w_max = 5·q·L⁴ / (384·E·I)
#     Za normalnu skupinu razreda raspona (pri fiksnom q/EI·L²)
#     dominira kvadratni trend po normaliziranom rasponu L.
#     Regresija: w = a·L² + b·L + c  (polinom stupnja 2)
#
#   TREND 3 — LOGARITAMSKI:
#     Koeficijent puzanja betona φ(t,t₀) u ovisnosti o vremenu t.
#     Prema CEB-FIP MC 2010 (pojednostavljena forma):
#       φ(t) ≈ φ∞ · βc(t),  gdje βc(t) = [(t-t₀)/(βH+t-t₀)]^0.3
#     Za dulje periode t ≫ βH → βc(t) ≈ A·ln(t) + B
#     Regresija: φ = a·ln(t) + b  (linearizacija supstitucijom u=ln(t))
#
# Svaki trend prikazan je s:
#   - Grafom mjerenja i regresijskog modela
#   - Grafom reziduala ili usporedbom modela različitih stupnjeva
#   - R² koeficijentom determinacije
# ===============================================================

import numpy as np
import matplotlib.pyplot as plt

# Postavljanje seed-a za reproducibilnost slučajnih šumova
np.random.seed(7)

# ===============================================================
# TREND 1: LINEARNI — Modul elastičnosti čelika E vs. temperatura T
# ===============================================================
# Temperatura u opsegu 20–600 °C (analiza požarnog scenarija)
T_mjere = np.array([20, 50, 100, 150, 200, 250, 300, 400, 500, 600])  # [°C]

# Referentne vrijednosti modula elastičnosti prema EN 1993-1-2
# (ky,θ reducira E proporcionalno temperaturi θ)
E_ref = np.array([210, 208, 205, 200, 189, 178, 168, 147, 126, 105])  # [GPa]

# Dodajemo Gaussov šum mjerenja (σ = ±3 GPa, simulira nesavršenosti mjerenja)
E_mjere = E_ref + np.random.normal(0, 3.0, len(T_mjere))

# Linearna regresija metodom najmanjih kvadrata (polinom stupnja 1)
# np.polyfit(x, y, deg) → vraća koeficijente [a, b] za a·T + b
koef_lin  = np.polyfit(T_mjere, E_mjere, 1)
poly_lin  = np.poly1d(koef_lin)          # objekt za evaluaciju polinoma

# Fina mreža za crtanje glatke linije regresije
T_fino = np.linspace(20, 600, 300)

# R² koeficijent determinacije (koliko varijance model objašnjava)
E_pred_lin = poly_lin(T_mjere)
SS_res_lin = np.sum((E_mjere - E_pred_lin)**2)       # suma kvadrata ostataka
SS_tot_lin = np.sum((E_mjere - np.mean(E_mjere))**2) # ukupna suma kvadrata
R2_lin     = 1.0 - SS_res_lin / SS_tot_lin

# ===============================================================
# TREND 2: PARABOLIČNI — Progib drvene grede w vs. raspon L
# ===============================================================
# Rasponi tipičnih drvenih greda u stambenoj gradnji: 2–12 m
L_mjere = np.array([2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 12.0])  # [m]

# Fizikalni model progiba (w = 5·q·L⁴/(384·E·I)), normaliziran s
# q/(E·I) = 0.015 kN/m / (GPa·cm⁴) → w u mm
# Za pedagoški prikaz, koristimo kvadratnu aproksimaciju u mjernom opsegu
w_ref   = 0.15 * L_mjere**2           # [mm] (kvadratni trend koji aproksimira L⁴)
w_mjere = w_ref + np.random.normal(0, 0.5, len(L_mjere))  # dodajemo mjerni šum

# mojaVarijabla, moja_varijabla, moja-kriva-varijabla

# Kvadratna regresija (polinom stupnja 2)
koef_par = np.polyfit(L_mjere, w_mjere, 2)
poly_par  = np.poly1d(koef_par)
L_fino    = np.linspace(2, 12, 300)

# R² za kvadratni model
w_pred_par = poly_par(L_mjere)
R2_par = (1.0 - np.sum((w_mjere - w_pred_par)**2) /
          np.sum((w_mjere - np.mean(w_mjere))**2))

# ===============================================================
# TREND 3: LOGARITAMSKI — Puzanje betona φ(t,t₀) vs. t
# ===============================================================
# Mjerenja koeficijenta puzanja u vremenskom periodu 7 dana – 3 godine
t_mjere = np.array([7, 14, 28, 60, 90, 180, 365, 730, 1095])   # [dani]

# Fizikalni model: φ ≈ 0.8·ln(t) – 0.5  (fitano prema EC2 tablici)
phi_ref   = 0.8 * np.log(t_mjere) - 0.5
phi_mjere = phi_ref + np.random.normal(0, 0.12, len(t_mjere))   # mjerni šum

# Linearizacija: supstitucija u = ln(t) → φ = a·u + b (linearna regresija po u)
# Ovo je ključna tehnika za logaritamske trendove!
u_mjere  = np.log(t_mjere)                              # transformacija varijable
koef_log = np.polyfit(u_mjere, phi_mjere, 1)            # linearna regresija po u

# Rekonstrukcija krivulje na originalnoj t-osi
t_fino    = np.linspace(7, 1095, 500)
phi_fino  = koef_log[0] * np.log(t_fino) + koef_log[1]

# R² za logaritamski model
phi_pred_log = koef_log[0] * u_mjere + koef_log[1]
R2_log = (1.0 - np.sum((phi_mjere - phi_pred_log)**2) /
          np.sum((phi_mjere - np.mean(phi_mjere))**2))

# ---------------------------------------------------------------
# ISPIS REZULTATA REGRESIJE
# ---------------------------------------------------------------
print("=" * 70)
print("PRIMJER 3: Rezultati regresijske analize")
print("=" * 70)
print(f"\n1. LINEARNI TREND — Modul elastičnosti čelika E(T):")
print(f"   E(T) = {koef_lin[0]:.4f}·T + {koef_lin[1]:.2f} GPa")
print(f"   R² = {R2_lin:.6f}")
print(f"   Prognoza E(350°C) = {poly_lin(350):.2f} GPa")

print(f"\n2. PARABOLIČNI TREND — Progib drvene grede w(L):")
print(f"   w(L) = {koef_par[0]:.5f}·L² + {koef_par[1]:.5f}·L + {koef_par[2]:.4f} mm")
print(f"   R² = {R2_par:.6f}")
print(f"   Prognoza w(8.5 m) = {poly_par(8.5):.2f} mm")

print(f"\n3. LOGARITAMSKI TREND — Puzanje betona φ(t):")
print(f"   φ(t) = {koef_log[0]:.4f}·ln(t) + {koef_log[1]:.4f}")
print(f"   R² = {R2_log:.6f}")
t_pred = 500
print(f"   Prognoza φ({t_pred} dana) = {koef_log[0]*np.log(t_pred)+koef_log[1]:.4f}")

# ---------------------------------------------------------------
# GRAFIČKI PRIKAZ — 3 × 2 raspored
# ---------------------------------------------------------------
fig, axes = plt.subplots(3, 2, figsize=(14, 15))
fig.suptitle(
    'Primjer 3 — Polinomijalna regresija u kontekstu nosivih konstrukcija\n'
    'Linearni · Parabolični · Logaritamski trend',
    fontsize=14, fontweight='bold'
)

# Zajednički stil za mjerene točke (ax.scatter parametri)
stil_mjere = dict(color='black', marker='o', s=65,
                  edgecolors='white', linewidths=0.5, zorder=5)

# ── 1A: LINEARNI trend — model + mjerenja ─────────────────────
ax = axes[0, 0]
ax.scatter(T_mjere, E_mjere, label='Mjerene vrijednosti', **stil_mjere)
ax.plot(T_fino, poly_lin(T_fino), color='#2980b9', linewidth=2.5,
        label=f'Lin. regresija\nE = {koef_lin[0]:.3f}·T + {koef_lin[1]:.1f}')
# Zona pouzdanosti (±σ reziduala)
sigma_lin = np.std(E_mjere - poly_lin(T_mjere))
ax.fill_between(T_fino,
                poly_lin(T_fino) - sigma_lin,
                poly_lin(T_fino) + sigma_lin,
                alpha=0.15, color='#2980b9', label=f'±σ zona ({sigma_lin:.1f} GPa)')
ax.set_title(f'LINEARNI TREND (R² = {R2_lin:.4f})\n'
             'Modul elastičnosti čelika vs. temperatura', fontweight='bold')
ax.set_xlabel('Temperatura T [°C]')
ax.set_ylabel('Modul elastičnosti E [GPa]')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
# Vertikalne linije za karakteristične temperature (EC3 granice)
for T_krit, lab in [(200, '200°C'), (400, '400°C'), (600, '600°C')]:
    ax.axvline(T_krit, color='gray', linestyle=':', alpha=0.5)
    ax.text(T_krit + 5, 105, lab, fontsize=7.5, color='gray')

# ── 1B: LINEARNI trend — reziduali ────────────────────────────
ax = axes[0, 1]
reziduali_lin = E_mjere - poly_lin(T_mjere)
boje_rez = ['#27ae60' if r >= 0 else '#e74c3c' for r in reziduali_lin]
ax.bar(T_mjere, reziduali_lin, color=boje_rez, alpha=0.75, width=35,
       edgecolor='black', linewidth=0.7)
ax.axhline(0, color='black', linewidth=1.2)
# Horizontalne linije ±σ
ax.axhline(sigma_lin,  color='#2980b9', linestyle='--', linewidth=1.2,
           label=f'+σ = +{sigma_lin:.2f} GPa')
ax.axhline(-sigma_lin, color='#2980b9', linestyle='--', linewidth=1.2,
           label=f'–σ = –{sigma_lin:.2f} GPa')
rmse_lin = np.sqrt(np.mean(reziduali_lin**2))
ax.text(0.05, 0.94, f'RMSE = {rmse_lin:.3f} GPa',
        transform=ax.transAxes, va='top', fontsize=9,
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6))
ax.set_title('Reziduali linearne regresije\n(mjereno − predviđeno)', fontweight='bold')
ax.set_xlabel('Temperatura T [°C]')
ax.set_ylabel('Rezidual [GPa]')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3, axis='y')

# ── 2A: PARABOLIČNI trend — model + mjerenja ──────────────────
ax = axes[1, 0]
ax.scatter(L_mjere, w_mjere, label='Mjerene vrijednosti', **stil_mjere)
ax.plot(L_fino, poly_par(L_fino), color='#8e44ad', linewidth=2.5,
        label=(f'Kv. regresija (R² = {R2_par:.4f})\n'
               f'w = {koef_par[0]:.3f}L² + {koef_par[1]:.3f}L + {koef_par[2]:.3f}'))
sigma_par = np.std(w_mjere - poly_par(L_mjere))
ax.fill_between(L_fino,
                poly_par(L_fino) - sigma_par,
                poly_par(L_fino) + sigma_par,
                alpha=0.15, color='#8e44ad', label=f'±σ zona ({sigma_par:.2f} mm)')
ax.set_title(f'PARABOLIČNI TREND (R² = {R2_par:.4f})\n'
             'Progib drvene grede vs. raspon', fontweight='bold')
ax.set_xlabel('Raspon L [m]')
ax.set_ylabel('Progib w [mm]')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# ── 2B: Usporedba polinoma različitih stupnjeva ───────────────
ax = axes[1, 1]
ax.scatter(L_mjere, w_mjere, label='Mjerene vrijednosti', **stil_mjere)
za_usporedbu = [(1, '#e74c3c', '--'), (2, '#8e44ad', '-'),
                (3, '#27ae60', '-.'), (5, '#f39c12', ':')]
for stupanj, boja, stil in za_usporedbu:
    k = np.polyfit(L_mjere, w_mjere, stupanj)
    p = np.poly1d(k)
    r2_s = (1.0 - np.sum((w_mjere - p(L_mjere))**2) /
            np.sum((w_mjere - np.mean(w_mjere))**2))
    ax.plot(L_fino, p(L_fino), color=boja, linestyle=stil, linewidth=1.8,
            label=f'Stupanj {stupanj}  (R² = {r2_s:.4f})', alpha=0.85)
ax.set_title('Usporedba polinoma različitih stupnjeva\n'
             '→ Viši stupanj ≠ uvijek bolji model (prenaučenost)', fontweight='bold')
ax.set_xlabel('Raspon L [m]')
ax.set_ylabel('Progib w [mm]')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# ── 3A: LOGARITAMSKI trend — model + mjerenja ─────────────────
ax = axes[2, 0]
ax.scatter(t_mjere, phi_mjere, label='Mjerene vrijednosti', **stil_mjere)
ax.plot(t_fino, phi_fino, color='#e67e22', linewidth=2.5,
        label=f'Log. regresija (R² = {R2_log:.4f})\nφ = {koef_log[0]:.3f}·ln(t) + {koef_log[1]:.3f}')
sigma_log = np.std(phi_mjere - phi_pred_log)
ax.fill_between(t_fino,
                phi_fino - sigma_log,
                phi_fino + sigma_log,
                alpha=0.15, color='#e67e22', label=f'±σ zona ({sigma_log:.3f})')
ax.set_title(f'LOGARITAMSKI TREND (R² = {R2_log:.4f})\n'
             'Koeficijent puzanja betona vs. vrijeme', fontweight='bold')
ax.set_xlabel('Vrijeme t [dani]')
ax.set_ylabel('Koeficijent puzanja φ(t, t₀) [–]')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
# Označi karakteristične vremenske marke
for t_mark, opis in [(28, '28 d\n(normna čvrstoća)'),
                     (365, '1 god'),
                     (730, '2 god')]:
    ax.axvline(t_mark, color='gray', linestyle=':', alpha=0.6)
    ax.text(t_mark + 15, 0.08, opis, fontsize=7.5, color='gray', va='bottom')

# ── 3B: Linearizacija — log. os x → krivulja postaje pravac ──
ax = axes[2, 1]
ax.scatter(t_mjere, phi_mjere, label='Mjerene vrijednosti', **stil_mjere)
ax.plot(t_fino, phi_fino, color='#e67e22', linewidth=2.5, label='Log. regresija')
ax.set_xscale('log')   # logaritamska os x → krivulja postaje pravac!
ax.set_title('Linearizacija: logaritamska os x\n'
             '→ Log. trend na log. skali izgleda kao PRAVAC\n'
             '   (koristan trik za vizualnu provjeru modela)',
             fontweight='bold')
ax.set_xlabel('Vrijeme t [dani]  (log. skala)')
ax.set_ylabel('Koeficijent puzanja φ(t, t₀) [–]')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3, which='both')
ax.annotate(
    'Na log. skali log. trend\npostaje ravna linija!',
    xy=(150, koef_log[0] * np.log(150) + koef_log[1]),
    xytext=(15, 2.8),
    arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=1.5),
    color='#e74c3c', fontsize=9,
    bbox=dict(boxstyle='round,pad=0.3', facecolor='#fdecea', alpha=0.8)
)

plt.tight_layout()
plt.savefig('primjer_03_regresija.pdf',
            dpi=150, bbox_inches='tight')
plt.show()

print("\nGraf pohranjen.")
