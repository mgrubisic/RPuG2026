# %% ============================================================
# PRIMJER 2: Numerička integracija i derivacija u mehanici konstrukcija
# ===============================================================
#
# Kontekst:
#   Analiza slobodnooslonjene armiranobetonske grede s trapeznim
#   opterećenjem q(x) (kombinacija stalnog i promjenjivog opterećenja
#   različitog intenziteta na lijevom i desnom kraju raspona).
#
# Schwedlerovi teoremi (veze između q, T i M):
#   dT/dx = -q(x)   →   T(x) = RA - ∫₀ˣ q(ξ) dξ
#   dM/dx =  T(x)   →   M(x) = ∫₀ˣ T(ξ) dξ
#   (uz rubne uvjete: T(0)=RA, M(0)=0, M(L)=0)
#
# Numeričke metode:
#   - Integracija:  scipy.integrate.cumulative_trapezoid (trapezno pravilo)
#   - Derivacija:   numpy.gradient (centralna konačna razlika)
#
# Pedagoški cilj:
#   Usporediti točnost numeričke integracije i derivacije
#   za GRUBA (N=5), SREDNJA (N=15) i FINA (N=50) diskretizacija
#   poprečnog presjeka duž osi grede.
# ===============================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate, integrate

# ---------------------------------------------------------------
# PARAMETRI GREDE I OPTEREĆENJA
# ---------------------------------------------------------------
L   = 6.0   # raspon grede [m]
q0  = 20.0  # intenzitet opterećenja — lijevi kraj [kN/m]
q1  = 8.0   # intenzitet opterećenja — desni kraj  [kN/m]

# ── Reakcije oslonaca iz uvjeta ravnoteže ──────────────────────
# Suma momenata oko B (desni oslonac):
# RA·L = q0·L²/2 + (q1–q0)·L²/6
RA = (q0 * L**2 / 2 + (q1 - q0) * L**2 / 6) / L  # [kN]
RB = (q0 + q1) * L / 2 - RA                         # [kN]

print("=" * 60)
print("PRIMJER 2: Numerička integracija i derivacija")
print("=" * 60)
print(f"\nParametri grede:")
print(f"  Raspon:       L  = {L:.2f} m")
print(f"  Opterećenje:  q0 = {q0:.2f} kN/m,  q1 = {q1:.2f} kN/m")
print(f"  Reakcije:     RA = {RA:.4f} kN,    RB = {RB:.4f} kN")

# ---------------------------------------------------------------
# EGZAKTNA RJEŠENJA (analitička, za provjeru točnosti)
# ---------------------------------------------------------------
def q_egzakt(x):
    """Trapezno opterećenje q(x) [kN/m]."""
    return q0 + (q1 - q0) * x / L

def T_egzakt(x):
    """Egzaktna poprečna sila T(x) [kN]."""
    return RA - q0 * x - (q1 - q0) * x**2 / (2.0 * L)

def M_egzakt(x):
    """Egzaktni moment savijanja M(x) [kNm]."""
    return RA * x - q0 * x**2 / 2.0 - (q1 - q0) * x**3 / (6.0 * L)

# Položaj maksimalnog momenta: T(x_max) = 0
# RA - q0*x - (q1-q0)*x²/(2L) = 0  →  kvadratna jednadžba
a_kv = -(q1 - q0) / (2.0 * L)
b_kv = -q0
c_kv = RA
diskriminanta = b_kv**2 - 4 * a_kv * c_kv
x_Mmax = (-b_kv - np.sqrt(diskriminanta)) / (2.0 * a_kv)  # manji korijen
M_max  = M_egzakt(x_Mmax)
print(f"\nEgzaktni maksimalni moment:")
print(f"  x(Mmax) = {x_Mmax:.4f} m")
print(f"  M_max   = {M_max:.4f} kNm")

# Referentna fina mreža za prikaz egzaktnih rješenja
x_ref = np.linspace(0, L, 1000)

# ---------------------------------------------------------------
# NUMERIČKA ANALIZA — tri gustoće diskretizacije
# ---------------------------------------------------------------
N_lista  = [5, 15, 50]                               # broj intervala
boje     = ['#e74c3c', '#f39c12', '#27ae60']          # crvena, narančasta, zelena
stilovi  = ['-.', '--', '-']                           # stil linije
nazivi   = ['Gruba mreža (N = 5)',
            'Srednja mreža (N = 15)',
            'Fina mreža (N = 50)']

# Pohrana grešaka za tablicu konvergencije
pogreske_T  = []
pogreske_M  = []
pogreske_dM = []   # greška dM/dx (trebala bi ≈ T)
x_Mmax_num  = []   # numerički pronađeni položaj Mmax

# ---------------------------------------------------------------
# GRAFIČKI PRIKAZ — 3 retka × 2 stupca
# ---------------------------------------------------------------
fig, axes = plt.subplots(3, 2, figsize=(14, 15))
fig.suptitle(
    'Primjer 2 — Utjecaj gustoće diskretizacije na numeričku integraciju i derivaciju\n'
    f'AB greda s trapeznim opterećenjem  (q₀={q0} kN/m, q₁={q1} kN/m, L={L} m)',
    fontsize=13, fontweight='bold'
)

for i, (N, boja, stil, naziv) in enumerate(zip(N_lista, boje, stilovi, nazivi)):

    # Diskretne točke mreže (N+1 čvorova, N intervala)
    x_m = np.linspace(0, L, N + 1)
    q_m = q_egzakt(x_m)        # vrijednosti opterećenja u čvorovima

    # ── NUMERIČKA INTEGRACIJA: T(x) ───────────────────────────
    # Trapezno pravilo: kumulativna suma → ∫₀ˣ q dξ
    int_q = integrate.cumulative_trapezoid(q_m, x_m, initial=0.0)
    T_num = RA - int_q          # poprečna sila iz ravnoteže

    # ── NUMERIČKA INTEGRACIJA: M(x) ───────────────────────────
    M_num = integrate.cumulative_trapezoid(T_num, x_m, initial=0.0)
    # Napomena: rubni uvjet M(0)=0 je automatski zadovoljen (initial=0)
    # Rubni uvjet M(L)=0 je zadovoljen samo uz dovoljnu gustoću mreže

    # ── NUMERIČKA DERIVACIJA: dM/dx ≈ T(x) ───────────────────
    # numpy.gradient koristi centralnu konačnu razliku u unutarnjim
    # čvorovima, a jednostranu razliku na rubovima mreže.
    dM_dx_num = np.gradient(M_num, x_m)

    # ── INTERPOLACIJA na finu mrežu (za vizualizaciju) ────────
    spl_T  = interpolate.CubicSpline(x_m, T_num)
    spl_M  = interpolate.CubicSpline(x_m, M_num)
    spl_dM = interpolate.CubicSpline(x_m, dM_dx_num)

    # ── PROCJENA POLOŽAJA MAKSIMALNOG MOMENTA ─────────────────
    # Interpoliramo T(x) i tražimo nultočku
    nultocke_T = spl_T.roots()
    nultocke_unutar = nultocke_T[(nultocke_T > 0) & (nultocke_T < L)]
    if len(nultocke_unutar) > 0:
        x_Mmax_n = nultocke_unutar[0]
        M_max_n  = spl_M(x_Mmax_n)
    else:
        x_Mmax_n = np.nan
        M_max_n  = np.nan
    x_Mmax_num.append(x_Mmax_n)

    # ── RMS GREŠKA ────────────────────────────────────────────
    T_rms  = np.sqrt(np.mean((spl_T(x_ref)  - T_egzakt(x_ref))**2))
    M_rms  = np.sqrt(np.mean((spl_M(x_ref)  - M_egzakt(x_ref))**2))
    dM_rms = np.sqrt(np.mean((spl_dM(x_ref) - T_egzakt(x_ref))**2))
    pogreske_T.append(T_rms)
    pogreske_M.append(M_rms)
    pogreske_dM.append(dM_rms)

    # ── CRTANJE — lijevo: T(x), desno: M(x) ──────────────────

    # Dijagram poprečnih sila T(x)
    ax = axes[i, 0]
    ax.plot(x_ref, T_egzakt(x_ref), 'k-', linewidth=2.5, label='Egzaktno', zorder=5)
    ax.plot(x_ref, spl_T(x_ref), linestyle=stil, color=boja, linewidth=2.2,
            label=f'{naziv}\nRMS = {T_rms:.3f} kN', zorder=4)
    ax.plot(x_m, T_num, 'o', color=boja, markersize=5, zorder=6, label='Čvorovi mreže')
    ax.axhline(0, color='gray', linewidth=0.8, linestyle=':')
    # Obojenje zone ispod i iznad nule
    ax.fill_between(x_ref, 0, T_egzakt(x_ref),
                    where=(T_egzakt(x_ref) >= 0), alpha=0.08, color='#2980b9')
    ax.fill_between(x_ref, 0, T_egzakt(x_ref),
                    where=(T_egzakt(x_ref) <  0), alpha=0.08, color='#e74c3c')
    ax.set_title(f'{naziv}\nDijagram poprečnih sila T(x)', fontweight='bold', fontsize=10)
    ax.set_xlabel('x [m]')
    ax.set_ylabel('T [kN]')
    ax.legend(fontsize=8, loc='upper right')
    ax.grid(True, alpha=0.3)

    # Dijagram momenata savijanja M(x)
    ax = axes[i, 1]
    ax.plot(x_ref, M_egzakt(x_ref), 'k-', linewidth=2.5, label='Egzaktno', zorder=5)
    ax.plot(x_ref, spl_M(x_ref), linestyle=stil, color=boja, linewidth=2.2,
            label=f'{naziv}\nRMS = {M_rms:.3f} kNm', zorder=4)
    ax.plot(x_m, M_num, 'o', color=boja, markersize=5, zorder=6, label='Čvorovi mreže')
    ax.axhline(0, color='gray', linewidth=0.8, linestyle=':')
    ax.fill_between(x_ref, 0, M_egzakt(x_ref), alpha=0.10, color='#27ae60')
    # Označi numerički pronađeni maksimum
    if not np.isnan(x_Mmax_n):
        ax.plot(x_Mmax_n, float(M_max_n), '*', color=boja, markersize=12, zorder=7)
        ax.annotate(
            f'Mmax≈{float(M_max_n):.1f} kNm\nx≈{x_Mmax_n:.2f} m',
            xy=(x_Mmax_n, float(M_max_n)),
            xytext=(x_Mmax_n - 1.8, float(M_max_n) - 7),
            fontsize=7.5, color=boja,
            arrowprops=dict(arrowstyle='->', color=boja, lw=1.2),
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7)
        )
    ax.set_title(f'{naziv}\nDijagram momenata savijanja M(x)', fontweight='bold', fontsize=10)
    ax.set_xlabel('x [m]')
    ax.set_ylabel('M [kNm]')
    ax.legend(fontsize=8, loc='upper right')
    ax.grid(True, alpha=0.3)
    
plt.tight_layout()
plt.savefig('primjer_02_integracija_derivacija.pdf',
            dpi=150, bbox_inches='tight')
plt.show()

# # ---------------------------------------------------------------
# # GRAFIKON KONVERGENCIJE — pad greške s gustoćom mreže
# # ---------------------------------------------------------------
# fig2, axes2 = plt.subplots(1, 2, figsize=(13, 5))
# fig2.suptitle(
#     'Primjer 2 — Konvergencija numeričke integracije i derivacije\n'
#     's povećanjem broja intervala N',
#     fontsize=13, fontweight='bold'
# )

# # ── Lijevo: Usporedi RMS greške svih veličina po N ────────────
# ax = axes2[0]
# x_bar = np.arange(len(N_lista))
# sirina = 0.27
# ax.bar(x_bar - sirina, pogreske_T,  sirina, label='RMS greška T(x) [kN]',
#        color='#2980b9', edgecolor='black', linewidth=0.6)
# ax.bar(x_bar,          pogreske_M,  sirina, label='RMS greška M(x) [kNm]',
#        color='#27ae60', edgecolor='black', linewidth=0.6)
# ax.bar(x_bar + sirina, pogreske_dM, sirina, label='RMS greška dM/dx [kN]',
#        color='#e74c3c', edgecolor='black', linewidth=0.6)
# # Označi vrijednosti iznad stupaca
# for j, N in enumerate(N_lista):
#     for k, (err, col) in enumerate(zip(
#             [pogreske_T[j], pogreske_M[j], pogreske_dM[j]],
#             ['#2980b9', '#27ae60', '#e74c3c'])):
#         ax.text(x_bar[j] + (k - 1) * sirina, err + 0.002,
#                 f'{err:.4f}', ha='center', fontsize=7.5, color=col)
# ax.set_xticks(x_bar)
# ax.set_xticklabels([f'N = {N}' for N in N_lista], fontsize=11)
# ax.set_title('Usporedba RMS grešaka po gustoći mreže', fontweight='bold')
# ax.set_xlabel('Broj intervala N')
# ax.set_ylabel('RMS greška')
# ax.legend(fontsize=9)
# ax.grid(True, alpha=0.3, axis='y')

# # ── Desno: Položaj Mmax — usporedba numeričke i egzaktne procjene ─
# ax = axes2[1]
# x_pos = np.arange(len(N_lista) + 1)
# M_max_vrijednosti  = [M_egzakt(xn) for xn in x_Mmax_num] + [M_max]
# xpos_vrijednosti   = list(x_Mmax_num) + [x_Mmax]
# boje_bar = boje + ['black']
# nazivi_bar = [f'N={N}' for N in N_lista] + ['Egzaktno']
# ax.bar(x_pos, M_max_vrijednosti,
#        color=boje_bar + ['#2c3e50'],
#        edgecolor='black', linewidth=0.7, alpha=0.8)
# ax.axhline(M_max, color='black', linestyle='--', linewidth=1.5,
#            label=f'Egzaktno: Mmax = {M_max:.3f} kNm')
# for j, (mp, xp) in enumerate(zip(M_max_vrijednosti, xpos_vrijednosti)):
#     ax.text(x_pos[j], mp + 0.05,
#             f'M={mp:.2f}\nx={xp:.3f} m',
#             ha='center', fontsize=8, va='bottom')
# ax.set_xticks(x_pos)
# ax.set_xticklabels(nazivi_bar, fontsize=10)
# ax.set_title('Procjena položaja i veličine Mmax\n'
#              'numeričkim vs. egzaktnim rješenjem', fontweight='bold')
# ax.set_ylabel('M_max [kNm]')
# ax.legend(fontsize=9)
# ax.grid(True, alpha=0.3, axis='y')
# ax.set_ylim(0, M_max * 1.15)

# plt.tight_layout()
# plt.savefig('primjer_02_konvergencija.pdf',
#             dpi=150, bbox_inches='tight')
# plt.show()

# ---------------------------------------------------------------
# TABLICA KONVERGENCIJE — ispis na konzolu
# ---------------------------------------------------------------
print(f"\n{'='*70}")
print("TABLICA KONVERGENCIJE NUMERIČKIH METODA")
print(f"{'='*70}")
print(f"{'Mreža':<18} {'RMS T [kN]':>14} {'RMS M [kNm]':>14} "
      f"{'RMS dM/dx [kN]':>16} {'x(Mmax) [m]':>13}")
print("-" * 70)
for N, eT, eM, edM, xM in zip(N_lista, pogreske_T, pogreske_M, pogreske_dM, x_Mmax_num):
    print(f"N = {N:<14} {eT:>14.6f} {eM:>14.6f} {edM:>16.6f} {xM:>13.6f}")
print(f"{'Egzaktno':<18} {'—':>14} {'—':>14} {'—':>16} {x_Mmax:>13.6f}")
print(f"\nKljučni zaključak:")
print(f"  → Derivacija (dM/dx) numerički je MANJE TOČNA od integracije.")
print(f"  → Greška integracije opada ~O(h²), derivacije ~O(h²) ali uz")
print(f"    veće konstante → potrebna finja mreža za isti nivo točnosti.")
print("=" * 70)
