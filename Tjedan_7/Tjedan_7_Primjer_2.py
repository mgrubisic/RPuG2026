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
#   za GRUBA (N=3), SREDNJA (N=6) i FINA (N=9) diskretizacija
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
q1  = 0.0   # intenzitet opterećenja — desni kraj  [kN/m]

# ── Reakcije oslonaca iz uvjeta ravnoteže ──────────────────────
# Suma momenata oko B (desni oslonac):
# RA·L = q0·L²/2 + (q1–q0)·L²/6
RA = (q0 * L**2 / 2 + (q1 - q0) * L**2 / 6) / L  # [kN]
RB = (q0 + q1) * L / 2 - RA                      # [kN]

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
N_lista  = [3, 6, 9]                              # broj intervala
boje     = ['#e74c3c', '#f39c12', '#27ae60']      # crvena, narančasta, zelena
stilovi  = ['-.', '--', '-']                      # stil linije
nazivi   = [f'Gruba mreža (N = {N_lista[0]})',
            f'Srednja mreža (N = {N_lista[1]})',
            f'Fina mreža (N = {N_lista[2]})']

# Pohrana grešaka za tablicu konvergencije
pogreske_T  = []
pogreske_M  = []
pogreske_dM = []   # greška dM/dx (trebala bi ≈ T)
x_Mmax_num  = []   # numerički pronađeni položaj Mmax

# ---------------------------------------------------------------
# GRAFIČKI PRIKAZ — 3 retka × 2 stupca
# ---------------------------------------------------------------
fig, axes = plt.subplots(3, 2, figsize=(10, 10))
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
    ax.plot(x_m, T_num, 'o', color=boja, markersize=7, zorder=6, label='Čvorovi mreže')
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
    ax.plot(x_m, M_num, 'o', color=boja, markersize=7, zorder=6, label='Čvorovi mreže')
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
    ax.invert_yaxis()
    ax.grid(True, alpha=0.3)
    
plt.tight_layout()
plt.savefig('primjer_02_integracija_derivacija.pdf',
            dpi=150, bbox_inches='tight')
plt.show()

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
print("=" * 70)
