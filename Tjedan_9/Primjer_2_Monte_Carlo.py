"""
╔══════════════════════════════════════════════════════════════════════════╗
║  SLOBODNO OSLONJENJA BETONSKA GREDA – Monte Carlo analiza pouzdanosti    ║
║  Kolegij: Računalno programiranje u građevinarstvu (GFOS)                ║
║  Predavač: izv. prof. dr. sc. Marin Grubišić                             ║
╚══════════════════════════════════════════════════════════════════════════╝

Granična stanja:
  GS-1  Ograničenje progiba     : δ_max  ≤  L / 250
  GS-2  Ograničenje rotacije    : θ_max  ≤  θ_lim  = 0.010 rad
  GS-3  Ograničenje naprezanja  : σ_max  ≤  f_c    (projektna čvrstoća betona)
"""

# ── Standardne biblioteke ─────────────────────────────────────────────────
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import warnings
warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════════════
# 0.  GLOBALNE STILSKE POSTAVKE
# ══════════════════════════════════════════════════════════════════════════
plt.rcParams.update({
    "font.family"       : "DejaVu Sans",
    "font.size"         : 9,
    "axes.titlesize"    : 10,
    "axes.labelsize"    : 9,
    "axes.spines.top"   : False,
    "axes.spines.right" : False,
    "axes.grid"         : True,
    "grid.alpha"        : 0.25,
    "grid.linestyle"    : "--",
    "legend.fontsize"   : 8,
    "figure.dpi"        : 130,
})

# Paleta boja
C_PASS = "#2ecc71"   # zelena – zadovoljava GS
C_FAIL = "#e74c3c"   # crvena  – ne zadovoljava GS
C_DET  = "#2c3e50"   # tamno   – deterministička vrijednost
C_LIM  = "#e67e22"   # narančasta – limitna linija
C_DIST = ["#3498db", "#9b59b6", "#1abc9c",
          "#e67e22", "#e74c3c", "#2ecc71"]   # histogrami

# ══════════════════════════════════════════════════════════════════════════
# 1.  DETERMINISTIČKI MODEL
# ══════════════════════════════════════════════════════════════════════════
# ─── Srednje vrijednosti ───────────────────────────────────────────────
L_mu   = 7.00        # [m]    raspon grede
b_mu   = 0.25        # [m]    širina pravokutnog presjeka
h_mu   = 0.40        # [m]    visina pravokutnog presjeka
E_mu   = 30.0e9      # [Pa]   modul elastičnosti betona (C30/37)
q_mu   = 22.0e3      # [N/m]  karakteristično jednoliko opterećenje
fc_mu  = 30.0e6      # [Pa]   karakteristična čvrstoća betona (f_ck, C30/37)

# ─── Koeficijenti varijacije (CoV) ────────────────────────────────────
CoV_L  = 0.01   # geometrija – mala mjerna nesigurnost
CoV_b  = 0.04
CoV_h  = 0.04
CoV_E  = 0.12   # materijalni parametar
CoV_q  = 0.20   # opterećenje – veća varijabilnost
CoV_fc = 0.15   # čvrstoća

# ─── Analitičke formule ───────────────────────────────────────────────
def moment_inercije(b, h):
    """Moment inercije pravokutnog presjeka [m⁴]."""
    return b * h**3 / 12

def progib_max(q, L, E, I):
    """Maksimalni progib slobodnooslonjene grede s UDL [m]."""
    return 5.0 * q * L**4 / (384.0 * E * I)

def rotacija_max(q, L, E, I):
    """Maksimalna rotacija uz oslonce [rad]."""
    return q * L**3 / (24.0 * E * I)

def napon_max(q, L, b, h):
    """Maksimalno normalno naprezanje od savijanja [Pa]."""
    M_max = q * L**2 / 8.0          # maksimalni moment savijanja
    W     = b * h**2 / 6.0          # moment otpora
    return M_max / W

def progibna_linija(q, L, E, I, n=300):
    """Elastična progibna linija – vektorizirano."""
    x = np.linspace(0.0, L, n)
    y = q * x * (L**3 - 2.0*L*x**2 + x**3) / (24.0 * E * I)
    return x, y

# ─── Deterministički rezultati ────────────────────────────────────────
I_det     = moment_inercije(b_mu, h_mu)
delta_det = progib_max(q_mu, L_mu, E_mu, I_det)
theta_det = rotacija_max(q_mu, L_mu, E_mu, I_det)
sigma_det = napon_max(q_mu, L_mu, b_mu, h_mu)
M_max_det = q_mu * L_mu**2 / 8.0

delta_lim_det = L_mu / 250.0    # GS-1 limitna vrijednost (m)
theta_lim     = 0.012           # GS-2 limitna rotacija (rad)
# GS-3: sigma_lim = fc (slučajna varijabla u MC)

print("=" * 62)
print("  SLOBODNOOSLONJENJA BETONSKA GREDA – deterministički proračun")
print("=" * 62)
print(f"  Raspon              L  = {L_mu:.2f} m")
print(f"  Poprečni presjek   b×h = {b_mu*100:.0f} × {h_mu*100:.0f} cm")
print(f"  Moment inercije     I  = {I_det*1e8:.0f} cm⁴")
print(f"  Modul elastičnosti  E  = {E_mu/1e9:.1f} GPa")
print(f"  UDL opterećenje     q  = {q_mu/1e3:.1f} kN/m")
print(f"  Projektna čvrstoća fc  = {fc_mu/1e6:.1f} MPa")
print("-" * 62)
print(f"  Maks. moment    M_max  = {M_max_det/1e3:.2f} kNm")
print(f"  Maks. progib   δ_max  = {delta_det*1e3:.2f} mm  "
      f"(lim = L/250 = {delta_lim_det*1e3:.2f} mm)")
print(f"  Maks. rotacija θ_max  = {theta_det*1e3:.4f} mrad "
      f"(lim = {theta_lim*1e3:.2f} mrad)")
print(f"  Maks. naprezanje σ_max = {sigma_det/1e6:.2f} MPa  "
      f"(lim = fc = {fc_mu/1e6:.2f} MPa)")
print("=" * 62)

# ══════════════════════════════════════════════════════════════════════════
# 2.  MONTE CARLO SIMULACIJA
# ══════════════════════════════════════════════════════════════════════════
N   = 100_000        # broj MC simulacija
rng = np.random.default_rng(2024)

def ln_params(mu, cov):
    """Parametri log-normalne distribucije iz (μ, CoV)."""
    sigma_ln = np.sqrt(np.log(1.0 + cov**2))
    mu_ln    = np.log(mu) - 0.5 * sigma_ln**2
    return mu_ln, sigma_ln

def sample_lognormal(mu, cov, n, rng):
    """Uzorkovanje iz log-normalne distribucije."""
    mu_ln, sig_ln = ln_params(mu, cov)
    return rng.lognormal(mu_ln, sig_ln, n)

# ─── Uzorci slučajnih varijabli ───────────────────────────────────────
L_s  = sample_lognormal(L_mu,  CoV_L,  N, rng)
b_s  = sample_lognormal(b_mu,  CoV_b,  N, rng)
h_s  = sample_lognormal(h_mu,  CoV_h,  N, rng)
E_s  = sample_lognormal(E_mu,  CoV_E,  N, rng)
q_s  = sample_lognormal(q_mu,  CoV_q,  N, rng)
fc_s = sample_lognormal(fc_mu, CoV_fc, N, rng)

# ─── Odzivi ───────────────────────────────────────────────────────────
I_s     = moment_inercije(b_s, h_s)
delta_s = progib_max(q_s, L_s, E_s, I_s)          # [m]
theta_s = rotacija_max(q_s, L_s, E_s, I_s)        # [rad]
sigma_s = napon_max(q_s, L_s, b_s, h_s)           # [Pa]

# ─── Funkcije graničnih stanja  g(X) ≥ 0 → sigurno ──────────────────
g1 = L_s / 250.0 - delta_s    # GS-1: progib
g2 = theta_lim   - theta_s    # GS-2: rotacija
g3 = fc_s        - sigma_s    # GS-3: naprezanje

fail1 = g1 < 0.0
fail2 = g2 < 0.0
fail3 = g3 < 0.0
fail_any = fail1 | fail2 | fail3

pf1 = np.mean(fail1)
pf2 = np.mean(fail2)
pf3 = np.mean(fail3)
pf_any = np.mean(fail_any)

print(f"\n  MONTE CARLO REZULTATI  (N = {N:,})")
print("-" * 62)
print(f"  P_f  GS-1 (progib)       = {pf1:.4e}  "
      f"  ({int(pf1*N):,} od {N:,} otkazivanja)")
print(f"  P_f  GS-2 (rotacija)     = {pf2:.4e}  "
      f"  ({int(pf2*N):,} od {N:,} otkazivanja)")
print(f"  P_f  GS-3 (naprezanje)   = {pf3:.4e}  "
      f"  ({int(pf3*N):,} od {N:,} otkazivanja)")
print(f"  P_f  Ukupno (union)      = {pf_any:.4e}  "
      f"  ({int(pf_any*N):,} od {N:,} otkazivanja)")
print("=" * 62)

# ─── Konvergencija (kumulativna pf) ──────────────────────────────────
idx     = np.arange(1, N + 1)
conv1   = np.cumsum(fail1.astype(float)) / idx
conv2   = np.cumsum(fail2.astype(float)) / idx
conv3   = np.cumsum(fail3.astype(float)) / idx

# Podskup za scatter prikaz (N_sc točaka radi preglednosti)
N_sc = 8_000
sc_idx = rng.choice(N, size=N_sc, replace=False)

# ══════════════════════════════════════════════════════════════════════════
# 3.  VIZUALIZACIJA
# ══════════════════════════════════════════════════════════════════════════

# ─── FIGURA 1 – Deterministički model: progibna linija ───────────────
fig1, axes1 = plt.subplots(1, 2, figsize=(12, 4.5),
                            gridspec_kw={"width_ratios": [2, 1]})
fig1.suptitle("Slobodnooslonjenja betonska greda – deterministički model",
              fontweight="bold", fontsize=11)

# --- lijevao: progibna linija ---
ax = axes1[0]
x_det, y_det = progibna_linija(q_mu, L_mu, E_mu, I_det)
ax.plot(x_det, -y_det * 1e3, color=C_DET, lw=2.5, label="Elastična progibna linija")
ax.axhline(-delta_lim_det * 1e3, color=C_LIM, ls="--", lw=1.5,
           label=f"Limit L/250 = {delta_lim_det*1e3:.1f} mm")
ax.fill_between(x_det, 0, -y_det * 1e3, alpha=0.08, color=C_DET)

# Kotiranje maksimalnog progiba
ax.annotate(f"δ_max = {delta_det*1e3:.2f} mm",
            xy=(L_mu/2, -delta_det*1e3),
            xytext=(L_mu*0.6, -delta_det*1e3 - 0.8),
            arrowprops=dict(arrowstyle="->", color="black", lw=1),
            fontsize=8.5)
ax.set_xlabel("Položaj duž grede x [m]")
ax.set_ylabel("Progib δ [mm]  (prema dolje = pozitivno)")
ax.set_title("Elastična progibna linija")
ax.legend(loc="lower center")
# ax.invert_yaxis()

# --- desno: presjek + opterećenje (shema) ---
ax2 = axes1[1]
ax2.set_xlim(-0.5, 1.5)
ax2.set_ylim(-0.5, 1.5)
ax2.set_aspect("equal")
ax2.axis("off")
ax2.set_title("Poprečni presjek b×h")

# Crtanje presjeka
rect = plt.Rectangle((0.25, 0.1), 1.0, b_mu/h_mu * 1.0,
                       fc="#d5e8f7", ec=C_DET, lw=2)
ax2.add_patch(rect)
ax2.text(0.75, 0.1 + b_mu/h_mu*0.5,
         f"b = {b_mu*100:.0f} cm\nh = {h_mu*100:.0f} cm\n"
         f"I = {I_det*1e4:.1f} cm⁴\nE = {E_mu/1e9:.0f} GPa",
         ha="center", va="center", fontsize=8.5, color=C_DET)

fig1.tight_layout()
fig1.savefig("fig1_deterministicki_model.png",
             dpi=150, bbox_inches="tight")

# ─── FIGURA 2 – Monte Carlo scatter plot (3 GS) ──────────────────────
fig2 = plt.figure(figsize=(15, 5.5))
fig2.suptitle("Monte Carlo analiza – rasipanje odziva i granična stanja"
              f"  (N = {N:,} simulacija, prikazano {N_sc:,})",
              fontweight="bold", fontsize=11)
gs2 = gridspec.GridSpec(1, 3, figure=fig2, wspace=0.38)

# ┌─ GS-1: δ_max vs. L/250 ─────────────────────────────────────────┐
ax_gs1 = fig2.add_subplot(gs2[0])
x_sc = delta_s[sc_idx] * 1e3                 # progib uzorka [mm]
y_sc = (L_s[sc_idx] / 250.0) * 1e3          # limitna vrijednost [mm]

safe_mask = ~fail1[sc_idx]
ax_gs1.scatter(x_sc[safe_mask],  y_sc[safe_mask],  s=2, alpha=0.20,
               color=C_PASS, rasterized=True, label="Zadovoljava GS-1")
ax_gs1.scatter(x_sc[~safe_mask], y_sc[~safe_mask], s=3, alpha=0.40,
               color=C_FAIL, rasterized=True, label="Ne zadovoljava GS-1")
# Dijagonalna linija granične ravnoteže: δ = L/250
lim_range = np.array([min(x_sc.min(), y_sc.min()),
                       max(x_sc.max(), y_sc.max())])
ax_gs1.plot(lim_range, lim_range, color=C_LIM, lw=1.8, ls="--",
            label="Granica otkazivanja\n(δ = L/250)")
ax_gs1.axvline(delta_det*1e3, color=C_DET, lw=1.2, ls=":")
ax_gs1.axhline(delta_lim_det*1e3, color=C_DET, lw=1.2, ls=":")
ax_gs1.set_xlabel("δ_max  [mm]")
ax_gs1.set_ylabel("L / 250  [mm]")
ax_gs1.set_title(f"GS-1: Progib\n$P_f$ = {pf1:.3e}",
                 color=C_FAIL if pf1 > 0.05 else C_DET)
ax_gs1.legend(loc="upper left", markerscale=3)

# ┌─ GS-2: q vs. θ_max ─────────────────────────────────────────────┐
ax_gs2 = fig2.add_subplot(gs2[1])
x_sc2 = theta_s[sc_idx] * 1e3          # rotacija uzorka [mrad]
y_sc2 = q_s[sc_idx] / 1e3              # opterećenje [kN/m]

safe2 = ~fail2[sc_idx]
ax_gs2.scatter(x_sc2[safe2],  y_sc2[safe2],  s=2, alpha=0.20,
               color=C_PASS, rasterized=True, label="Zadovoljava GS-2")
ax_gs2.scatter(x_sc2[~safe2], y_sc2[~safe2], s=3, alpha=0.40,
               color=C_FAIL, rasterized=True, label="Ne zadovoljava GS-2")
ax_gs2.axvline(theta_lim * 1e3, color=C_LIM, lw=2, ls="--",
               label=f"θ_lim = {theta_lim*1e3:.0f} mrad")
ax_gs2.axvline(theta_det * 1e3, color=C_DET, lw=1.2, ls=":")
ax_gs2.set_xlabel("θ_max  [mrad]")
ax_gs2.set_ylabel("Opterećenje q  [kN/m]")
ax_gs2.set_title(f"GS-2: Rotacija\n$P_f$ = {pf2:.3e}",
                 color=C_FAIL if pf2 > 0.05 else C_DET)
ax_gs2.legend(loc="upper right", markerscale=3)

# ┌─ GS-3: σ_max vs. f_c ─────────────────────────────────────────────┐
ax_gs3 = fig2.add_subplot(gs2[2])
x_sc3 = sigma_s[sc_idx] / 1e6          # naprezanje uzorka [MPa]
y_sc3 = fc_s[sc_idx] / 1e6            # čvrstoća uzorka [MPa]

safe3 = ~fail3[sc_idx]
ax_gs3.scatter(x_sc3[safe3],  y_sc3[safe3],  s=2, alpha=0.20,
               color=C_PASS, rasterized=True, label="Zadovoljava GS-3")
ax_gs3.scatter(x_sc3[~safe3], y_sc3[~safe3], s=3, alpha=0.40,
               color=C_FAIL, rasterized=True, label="Ne zadovoljava GS-3")
lim_r3 = np.array([min(x_sc3.min(), y_sc3.min()),
                    max(x_sc3.max(), y_sc3.max())])
ax_gs3.plot(lim_r3, lim_r3, color=C_LIM, lw=1.8, ls="--",
            label="Granica otkazivanja\n(σ = f_c)")
ax_gs3.axvline(sigma_det/1e6, color=C_DET, lw=1.2, ls=":")
ax_gs3.set_xlabel("σ_max  [MPa]")
ax_gs3.set_ylabel("Projektna čvrstoća f_c  [MPa]")
ax_gs3.set_title(f"GS-3: Naprezanje\n$P_f$ = {pf3:.3e}",
                 color=C_FAIL if pf3 > 0.05 else C_DET)
ax_gs3.legend(loc="upper left", markerscale=3)

fig2.tight_layout()
fig2.savefig("fig2_mc_scatter_gs.png",
             dpi=150, bbox_inches="tight")

# ─── FIGURA 3 – Histogrami slučajnih varijabli ───────────────────────
fig3, axs3 = plt.subplots(2, 3, figsize=(14, 7))
fig3.suptitle("Histogrami uzorkovanih slučajnih varijabli"
              f"  (log-normalna distribucija, N = {N:,})",
              fontweight="bold", fontsize=11)
axs3 = axs3.flatten()

vars_info = [
    (L_s,   L_mu,   CoV_L,  "L [m]",     "Raspon grede"),
    (b_s,   b_mu,   CoV_b,  "b [m]",     "Širina presjeka"),
    (h_s,   h_mu,   CoV_h,  "h [m]",     "Visina presjeka"),
    (E_s/1e9, E_mu/1e9, CoV_E, "E [GPa]", "Modul elastičnosti"),
    (q_s/1e3, q_mu/1e3, CoV_q, "q [kN/m]","UDL opterećenje"),
    (fc_s/1e6, fc_mu/1e6, CoV_fc, "f_ck [MPa]", "Čvrstoća betona"),
]

from scipy.stats import lognorm

for i, (data_i, mu_i, cov_i, xlabel_i, title_i) in enumerate(vars_info):
    ax = axs3[i]
    n_bins = 60
    counts, bins, patches = ax.hist(data_i, bins=n_bins, density=True,
                                    color=C_DIST[i], alpha=0.70,
                                    edgecolor="none")
    # Overlay teoretska PDF
    x_pdf = np.linspace(data_i.min(), data_i.max(), 500)
    sigma_ln = np.sqrt(np.log(1 + cov_i**2))
    mu_ln    = np.log(mu_i) - 0.5 * sigma_ln**2
    pdf_vals = lognorm.pdf(x_pdf, s=sigma_ln, scale=np.exp(mu_ln))
    ax.plot(x_pdf, pdf_vals, color="black", lw=1.8, label="Teorijska PDF")
    ax.axvline(mu_i, color=C_LIM, lw=2, ls="--", label=f"μ = {mu_i:.3g}")
    ax.axvline(np.mean(data_i), color=C_DET, lw=1.5, ls=":",
               label=f"x̄ = {np.mean(data_i):.3g}")
    ax.set_xlabel(xlabel_i)
    ax.set_ylabel("Gustoća vjerojatnosti")
    ax.set_title(f"{title_i}  |  CoV = {cov_i:.0%}  |  σ = {np.std(data_i):.3g}")
    ax.legend(fontsize=7.5)

fig3.tight_layout()
fig3.savefig("fig3_histogrami_varijabli.png",
             dpi=150, bbox_inches="tight")

# ─── FIGURA 4 – Konvergencija P_f ────────────────────────────────────
fig4, axes4 = plt.subplots(1, 3, figsize=(15, 5))
fig4.suptitle("Konvergencija vjerojatnosti otkazivanja s brojem MC simulacija",
              fontweight="bold", fontsize=11)

n_plot  = np.arange(1, N + 1)
CI_mult = 1.96     # 95% CI: ±1.96 * std(p̂)

for j, (conv_j, pf_j, gs_label, gs_color) in enumerate([
        (conv1, pf1, "GS-1: Progib  (δ ≤ L/250)", "#3498db"),
        (conv2, pf2, "GS-2: Rotacija  (θ ≤ θ_lim)", "#9b59b6"),
        (conv3, pf3, "GS-3: Naprezanje  (σ ≤ f_c)", "#e74c3c"),
]):
    ax = axes4[j]
    # Standardna greška Monte Carlo procjene
    se = np.sqrt(np.maximum(conv_j * (1 - conv_j) / n_plot, 1e-30))
    ci_lo = np.maximum(conv_j - CI_mult * se, 0.0)
    ci_hi = conv_j + CI_mult * se

    ax.semilogx(n_plot, conv_j, color=gs_color, lw=1.5, zorder=3)
    ax.fill_between(n_plot, ci_lo, ci_hi, alpha=0.20, color=gs_color,
                    label="95% CI")
    ax.axhline(pf_j, color="black", ls="--", lw=1.2,
               label=f"$P_f$ = {pf_j:.3e}")
    ax.set_xlabel("Broj MC simulacija N")
    ax.set_ylabel("Procjena $P_f$")
    ax.set_title(gs_label)
    ax.legend(fontsize=8)

    # Oznake korisnih N vrijednosti
    for N_mark in [100, 1_000, 10_000, 100_000]:
        if N_mark <= N:
            ax.axvline(N_mark, color="gray", lw=0.6, ls=":", alpha=0.5)

fig4.tight_layout()
fig4.savefig("fig4_konvergencija_pf.png",
             dpi=150, bbox_inches="tight")

# ─── FIGURA 5 – Sažetak: PDF odzivnih varijabli s granicama ──────────
fig5, axs5 = plt.subplots(1, 3, figsize=(14, 5))
fig5.suptitle("Razdiobe odzivnih varijabli i granična stanja",
              fontweight="bold", fontsize=11)

response_info = [
    (delta_s * 1e3,     delta_det * 1e3,   L_s / 250.0 * 1e3,
     "δ_max [mm]", "GS-1: Progib  ($P_f$ = {:.3e})".format(pf1),
     "#3498db", "$L/250$"),
    (theta_s * 1e3,     theta_det * 1e3,   np.full(N, theta_lim * 1e3),
     "θ_max [mrad]", "GS-2: Rotacija  ($P_f$ = {:.3e})".format(pf2),
     "#9b59b6", "$θ_{lim}$"),
    (sigma_s / 1e6,     sigma_det / 1e6,   fc_s / 1e6,
     "σ_max [MPa]", "GS-3: Naprezanje  ($P_f$ = {:.3e})".format(pf3),
     "#e74c3c", "$f_c$"),
]

for k, (resp_k, det_k, lim_k, xlabel_k, title_k, col_k, lim_label) in \
        enumerate(response_info):
    ax = axs5[k]
    lim_mean = np.mean(lim_k)

    ax.hist(resp_k, bins=80, density=True, color=col_k,
            alpha=0.55, label="Odziv (uzorci)", edgecolor="none")
    if np.std(lim_k) > 1e-9:   # limitna vrijednost je i sama slučajna (GS-3)
        ax.hist(lim_k, bins=80, density=True, color=C_LIM,
                alpha=0.40, label=f"Otpornost {lim_label}", edgecolor="none",
                histtype="stepfilled")
    else:
        ax.axvline(lim_mean, color=C_LIM, lw=2.5, ls="--",
                   label=f"Lim. vrijednost {lim_label} = {lim_mean:.2f}")

    ax.axvline(det_k, color=C_DET, lw=2, ls=":",
               label=f"Determ. vrijednost = {det_k:.2f}")
    ax.set_xlabel(xlabel_k)
    ax.set_ylabel("Gustoća vjerojatnosti")
    ax.set_title(title_k)
    ax.legend(fontsize=7.8)

    # Nijansiranje zone otkazivanja
    xlim_ax = ax.get_xlim()
    if np.std(lim_k) < 1e-9:
        ax.axvspan(lim_mean, xlim_ax[1], alpha=0.07, color=C_FAIL)
    ax.set_xlim(xlim_ax)

fig5.tight_layout()
fig5.savefig("fig5_pdf_odzivnih_varijabli.png",
             dpi=150, bbox_inches="tight")

plt.show()
print("\n  Sve slike zapisane u ")
print("  fig1 – deterministički model + progibna linija")
print("  fig2 – MC scatter plotovi za sva 3 GS")
print("  fig3 – histogrami uzorkovanih slučajnih varijabli")
print("  fig4 – konvergencija P_f po GS")
print("  fig5 – PDF odzivnih varijabli s granicama")
