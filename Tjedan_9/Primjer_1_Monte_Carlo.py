import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from anastruct.fem.system import SystemElements

# ==========================================
# 1. PARAMETRI MONTE CARLO SIMULACIJE
# ==========================================
broj_simulacija = 10_000
limit_pomaka    = 0.02   # m  (granično stanje uporabivosti)
np.random.seed(42)

b = 0.3   # m  — fiksna širina presjeka

# ── Slučajne varijable (normalna razdioba, CoV = 10 %) ──────────────────────
mean_h = 0.30        ; cov = 0.10
mean_E = 3.0e7       # kPa
mean_q = 10.0        # kN/m  (apsolutna vrijednost; smjer definiran predznakom u modelu)

std_h = mean_h * cov
std_E = mean_E * cov
std_q = mean_q * cov

sim_h = np.random.normal(mean_h, std_h, broj_simulacija)   # m
sim_E = np.random.normal(mean_E, std_E, broj_simulacija)   # kPa
sim_q = np.random.normal(mean_q, std_q, broj_simulacija)   # kN/m

# Izvedene veličine po simulaciji
sim_A  = b * sim_h
sim_I  = (b * sim_h**3) / 12.0
sim_EA = sim_E * sim_A
sim_EI = sim_E * sim_I

# ==========================================
# 2. PETLJA SIMULACIJE
# ==========================================
rezultati_pomaka = []
print(f"Pokretanje {broj_simulacija} simulacija strukture...")

for i in range(broj_simulacija):
    ss = SystemElements(EA=sim_EA[i], EI=sim_EI[i])

    ss.add_element(location=[[0, 0], [0, 5]])
    ss.add_element(location=[[0, 5], [5, 5]])
    ss.add_element(location=[[5, 5], [5, 0]])

    ss.add_support_fixed(node_id=1)
    ss.add_support_spring(node_id=4, translation=3, k=4000)

    ss.point_load(Fx=30, node_id=2)
    ss.q_load(q=-sim_q[i], element_id=2)   # predznak zadržan iz originala

    ss.solve()

    pomaci = ss.get_node_displacements()
    if isinstance(pomaci, list):
        ux_2 = next(n["ux"] for n in pomaci if n["id"] == 2)
    else:
        ux_2 = pomaci[2]["ux"]

    rezultati_pomaka.append(ux_2)

pomaci_arr = np.array(rezultati_pomaka)
pomaci_aps = np.abs(pomaci_arr)

# ==========================================
# 3. PRORAČUN VJEROJATNOSTI PREKORAČENJA
# ==========================================
mask_otkaz   = pomaci_aps > limit_pomaka
mask_sigurno = ~mask_otkaz

broj_otkaza         = int(np.sum(mask_otkaz))
vjerojatnost_otkaza = broj_otkaza / broj_simulacija * 100

# ==========================================
# 4. STATISTIČKI IZVJEŠTAJ
# ==========================================
print("\n─── STATISTIČKI IZVJEŠTAJ ───────────────────────────────")
print(f"  Prosječni pomak čvora 2 :  {np.mean(pomaci_arr):+.5f} m")
print(f"  Std. dev. pomaka        :   {np.std(pomaci_arr):.5f} m")
print(f"  95 % raspon (5.–95. pc) :  [{np.percentile(pomaci_arr, 5):.5f}, "
      f"{np.percentile(pomaci_arr, 95):.5f}] m")
print(f"  Broj prekoračenja       :   {broj_otkaza} / {broj_simulacija}")
print(f"  Vjerojatnost prekoračenja (Pf) :  {vjerojatnost_otkaza:.2f} %")
print("─────────────────────────────────────────────────────────")

# ==========================================
# 5. VIZUALIZACIJA
# ==========================================
BLUE   = "#2980b9"
GREEN  = "#27ae60"
RED    = "#c0392b"
ORANGE = "#e67e22"
GRAY   = "#7f8c8d"

fig = plt.figure(figsize=(14, 10))
fig.suptitle("Monte Carlo analiza pouzdanosti konstrukcije  (N = 1 000)",
             fontsize=14, fontweight="bold", y=0.98)

gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.38)

# ── Pomoćna funkcija za histogram razdiobe ulaznih varijabli ────────────────
def plot_input_dist(ax, samples, mean, std, label, unit, color):
    x = np.linspace(mean - 4*std, mean + 4*std, 300)
    from scipy.stats import norm
    pdf = norm.pdf(x, mean, std)

    ax.hist(samples, bins=30, density=True,
            color=color, alpha=0.55, edgecolor="white", linewidth=0.4)
    ax.plot(x, pdf, color=color, linewidth=2.0)
    ax.axvline(mean, color="black", linestyle="--", linewidth=1.4,
               label=f"μ = {mean:.4g} {unit}")
    ax.axvline(mean - std, color=GRAY, linestyle=":", linewidth=1.1)
    ax.axvline(mean + std, color=GRAY, linestyle=":", linewidth=1.1,
               label=f"σ = {std:.4g} {unit}")
    ax.set_title(label, fontsize=10, fontweight="bold")
    ax.set_xlabel(f"[{unit}]", fontsize=8)
    ax.set_ylabel("Gustoća vjerojatnosti", fontsize=8)
    ax.legend(fontsize=7.5)
    ax.grid(axis="y", alpha=0.25)

# Gornji red — razdiobe ulaznih varijabli
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[0, 2])

plot_input_dist(ax1, sim_h, mean_h, std_h,
                "Visina presjeka  h", "m", BLUE)
plot_input_dist(ax2, sim_E, mean_E, std_E,
                "Modul elastičnosti  E", "kPa", ORANGE)
plot_input_dist(ax3, sim_q, mean_q, std_q,
                "Raspodijeljeno opterećenje  q", "kN/m", GREEN)

# ── Donji lijevi — histogram pomaka (sigurni / prekoračeni) ─────────────────
ax4 = fig.add_subplot(gs[1, 0:2])

bins = np.linspace(pomaci_arr.min() * 0.95, pomaci_arr.max() * 1.05, 35)

ax4.hist(pomaci_arr[mask_sigurno], bins=bins,
         color=GREEN,  alpha=0.70, edgecolor="white", linewidth=0.4,
         label=f"Sigurni uzorci  (N = {np.sum(mask_sigurno)})")
ax4.hist(pomaci_arr[mask_otkaz], bins=bins,
         color=RED, alpha=0.75, edgecolor="white", linewidth=0.4,
         label=f"Prekoračenje GS  (N = {broj_otkaza})")

ax4.axvline(np.mean(pomaci_arr), color=BLUE, linestyle="--", linewidth=1.8,
            label=f"Prosjek: {np.mean(pomaci_arr):+.4f} m")
ax4.axvline(limit_pomaka, color=RED, linestyle="-", linewidth=2.2,
            label=f"Granično stanje: {limit_pomaka} m")

ax4.set_title("Razdioba horizontalnog pomaka čvora 2  (u_x)", fontsize=10, fontweight="bold")
ax4.set_xlabel("Horizontalni pomak  u_x  [m]", fontsize=9)
ax4.set_ylabel("Frekvencija", fontsize=9)
ax4.legend(fontsize=8)
ax4.grid(axis="y", alpha=0.25)

# ── Donji desni — scatter: indeks simulacije vs pomak ───────────────────────
ax5 = fig.add_subplot(gs[1, 2])

idx = np.arange(broj_simulacija)
ax5.scatter(idx[mask_sigurno], pomaci_aps[mask_sigurno],
            s=4, color=GREEN, alpha=0.55, label="Sigurni")
ax5.scatter(idx[mask_otkaz], pomaci_aps[mask_otkaz],
            s=10, color=RED, alpha=0.85, label="Prekoračenje GS",
            zorder=5)
ax5.axhline(limit_pomaka, color=RED, linestyle="-", linewidth=1.8,
            label=f"GS = {limit_pomaka} m")

ax5.set_title("MC uzorci — apsolutni pomak", fontsize=10, fontweight="bold")
ax5.set_xlabel("Indeks simulacije  [ – ]", fontsize=9)
ax5.set_ylabel("|u_x|  [m]", fontsize=9)
ax5.legend(fontsize=8)
ax5.grid(alpha=0.25)

# Tekstualni okvir s rezultatom
textstr = (f"$P_f$ = {vjerojatnost_otkaza:.2f} %\n"
           f"Prekoračenja: {broj_otkaza} / {broj_simulacija}")
ax5.text(0.97, 0.97, textstr, transform=ax5.transAxes,
         fontsize=9, verticalalignment="top", horizontalalignment="right",
         bbox=dict(boxstyle="round,pad=0.4", facecolor="lightyellow",
                   edgecolor=RED, alpha=0.9))

plt.savefig("mc_pouzdanost.pdf", dpi=300, bbox_inches="tight")
plt.show()
