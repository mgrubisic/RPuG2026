# %% ============================================================
# PRIMJER 4: Oblak točaka, filtriranje i osnovna statistika
# ===============================================================
#
# Kontekst:
#   Kontrola kvalitete betona na gradilištu armiranobetonskog
#   objekta (temelji, stupovi, međukatne ploče).
#   Mjeri se tlačna čvrstoća betona fc [MPa] na uzorcima valjaka
#   (promjer 150 mm, visina 300 mm) prema HRN EN 12390-3.
#
# Razred betona: C30/37
#   fck = 30 MPa  (karakteristična tlačna čvrstoća, 5. percentil)
#   fcm = fck + 8 = 38 MPa  (srednja čvrstoća prema EC2)
#
# Kriteriji conformity prema EN 206-1:
#   Kriterij 1 (C1): fc,i ≥ fck – 4 MPa  za pojedinačni uzorak
#   Kriterij 2 (C2): srednja vrijednost ≥ fck + 1.48·s
#
# Zadatak:
#   1. Generiraj oblak točaka mjerenja po lokacijama objekta
#   2. Filtriraj uzorke koji su ISPOD fck (neprihvatljivi)
#   3. Filtriraj uzorke koji su IZNAD gornje kontrolne granice
#   4. Osnovna deskriptivna statistika za svaku skupinu
#   5. Provjera normalnosti raspodjele (vizualna + KS test)
# ===============================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# ---------------------------------------------------------------
# PARAMETRI BETONA I RAZRED ČVRSTOĆE
# ---------------------------------------------------------------
fck            = 30.0   # [MPa] karakteristična čvrstoća (razred C30/37)
fcm_teorija    = 38.0   # [MPa] srednja čvrstoća prema EC2
granica_donja  = fck    # [MPa] ispod ove granice → neprihvatljivo (kriterij conformity)
granica_gornja = fck + 14.0  # [MPa] iznad → visoka rezerva (gornja kontrolna granica)

# ---------------------------------------------------------------
# GENERIRANJE OBLAKA TOČAKA — simulacija mjerenja s terena
# ---------------------------------------------------------------
np.random.seed(42)   # seed za reproducibilnost

# Broj uzoraka po lokaciji (realističan broj za srednji objekt)
n_temelji = 80
n_stupovi  = 60
n_ploce    = 70

# Mjerenja fc ~ N(μ, σ) po lokaciji — svaka lokacija ima malo
# različite uvjete ugradnje (razlika u vibriranju, vlagi, temperaturi)
#   Temelji: dobro vibriran beton, relativno mali CoV
#   Stupovi:  optimalni uvjeti, visoka čvrstoća
#   Ploče:    veće rasipanje (tanka oplata, poteškoće ugradnje)
fc_temelji  = np.random.normal(loc=37.5, scale=4.0, size=n_temelji)  # [MPa]
fc_stupovi  = np.random.normal(loc=41.0, scale=3.5, size=n_stupovi)  # [MPa]
fc_ploce    = np.random.normal(loc=34.5, scale=6.0, size=n_ploce)    # [MPa]

# Dodajemo nekoliko "loših" uzoraka u pločama (pogreška ugradnje)
# — realističan scenarij na gradilištu
fc_ploce[:6] = np.random.uniform(20.0, 27.5, 6)

# Sve lokacije u jednom nizu s oznakom lokacije
fc_svi   = np.concatenate([fc_temelji, fc_stupovi, fc_ploce])
n_ukupno = len(fc_svi)
lokacije = (
    ['Temelji'] * n_temelji +
    ['Stupovi'] * n_stupovi +
    ['Ploče']   * n_ploce
)
lokacije = np.array(lokacije)
indeksi  = np.arange(n_ukupno)    # redni broj uzorka (za x-os scatter)

# ---------------------------------------------------------------
# FILTRIRANJE — tri kategorije uzoraka
# ---------------------------------------------------------------
# Kategorija A: NEPRIHVATLJIVI — ispod karakteristične čvrstoće fck
mask_nep  = fc_svi < granica_donja

# Kategorija B: PRIHVATLJIVI — unutar dopuštenog raspona
mask_prih = (fc_svi >= granica_donja) & (fc_svi <= granica_gornja)

# Kategorija C: VISOKA REZERVA — iznad gornje kontrolne granice
mask_vis  = fc_svi > granica_gornja

# Provjera: zbroj svih maski mora biti n_ukupno
assert np.sum(mask_nep) + np.sum(mask_prih) + np.sum(mask_vis) == n_ukupno

# ---------------------------------------------------------------
# DESKRIPTIVNA STATISTIKA — pomoćna funkcija
# ---------------------------------------------------------------
def statistika(naziv, podaci):
    """
    Izračunava i ispisuje osnovnu deskriptivnu statistiku.
    Parametri:
        naziv  : string — naziv grupe (za ispis)
        podaci : 1D ndarray — vrijednosti fc [MPa]
    """
    n       = len(podaci)
    mu      = np.mean(podaci)
    sigma   = np.std(podaci, ddof=1)    # neupravljeni estimator (N-1)
    cov     = sigma / mu * 100           # koeficijent varijacije [%]
    med     = np.median(podaci)
    q25     = np.percentile(podaci, 25)
    q75     = np.percentile(podaci, 75)
    fck_5   = np.percentile(podaci, 5)  # empirijska karakteristična vrijednost
    iqr     = q75 - q25                 # interkvartilni raspon

    print(f"\n  ┌─ {naziv.upper()} (n = {n}) {'─'*(40-len(naziv))}")
    print(f"  │ Srednja vrijednost (μ):         {mu:>8.3f} MPa")
    print(f"  │ Std. devijacija (σ):            {sigma:>8.3f} MPa")
    print(f"  │ Koef. varijacije (CoV):         {cov:>8.2f} %")
    print(f"  │ Medijan:                        {med:>8.3f} MPa")
    print(f"  │ Min / Maks:                     {np.min(podaci):>6.2f} / {np.max(podaci):>6.2f} MPa")
    print(f"  │ Q25 / Q75:                      {q25:>6.2f} / {q75:>6.2f} MPa")
    print(f"  │ IQR (interkvartilni raspon):    {iqr:>8.3f} MPa")
    print(f"  └ Kar. čvrstoća (5. percentil):  {fck_5:>8.3f} MPa")

    return {'n': n, 'mu': mu, 'sigma': sigma, 'cov': cov, 'fck_5': fck_5}

print("=" * 65)
print("PRIMJER 4: Kontrola kvalitete betona C30/37")
print(f"           fck = {fck} MPa,  Gornja granica = {granica_gornja} MPa")
print("=" * 65)

# Ispis statistike za sve skupne
stat_svi  = statistika("Svi uzorci",         fc_svi)
stat_prih = statistika("Prihvatljivi",        fc_svi[mask_prih])
stat_nep  = statistika("Neprihvatljivi (< fck)", fc_svi[mask_nep])
if np.sum(mask_vis) > 0:
    stat_vis = statistika("Visoka rezerva (> gornje granice)", fc_svi[mask_vis])

# Statistika po lokaciji
print("\n" + "─" * 65)
print("  STATISTIKA PO LOKACIJI:")
for lok in ['Temelji', 'Stupovi', 'Ploče']:
    statistika(lok, fc_svi[lokacije == lok])

# EN 206 conformity provjera
mu_svi   = stat_svi['mu']
sigma_svi = stat_svi['sigma']
konf_krit2 = fck + 1.48 * sigma_svi   # prag za kriterij 2
print(f"\n  EN 206 Kriterij 2: fcm,n ≥ fck + 1.48·s = {konf_krit2:.2f} MPa")
print(f"  Izmjerena srednja: fcm = {mu_svi:.2f} MPa → ",
      end="")
print("ZADOVOLJENO ✓" if mu_svi >= konf_krit2 else "NIJE ZADOVOLJENO ✗")

# ---------------------------------------------------------------
# KOLMOGOROV-SMIRNOV TEST NORMALNOSTI
# ---------------------------------------------------------------
ks_stat, ks_p = stats.kstest(fc_svi, 'norm',
                              args=(mu_svi, sigma_svi))
print(f"\n  Kolmogorov-Smirnov test normalnosti:")
print(f"    KS statistika = {ks_stat:.5f}")
print(f"    p-vrijednost  = {ks_p:.5f}")
if ks_p > 0.05:
    print("    Zaključak: Ne možemo odbaciti H₀ normalnosti (p > 0.05)")
else:
    print("    Zaključak: Odbacujemo H₀ normalnosti (p ≤ 0.05)")
print("=" * 65)

# ---------------------------------------------------------------
# GRAFIČKI PRIKAZ — 2 × 2 raspored
# ---------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle(
    f'Primjer 4 — Kontrola kvalitete betona C30/37\n'
    f'fck = {fck} MPa | Gornja kontrolna granica = {granica_gornja} MPa | '
    f'n = {n_ukupno} uzoraka',
    fontsize=13, fontweight='bold'
)

# Boje po lokaciji i kategoriji
boje_lok = {'Temelji': '#2980b9', 'Stupovi': '#8e44ad', 'Ploče': '#27ae60'}
boja_nep = '#e74c3c'     # neprihvatljivi → crvena
boja_vis = '#f39c12'     # visoka rezerva → narančasta

# ── GRAF 1: Oblak točaka — sva mjerenja po redoslijedu ────────
ax = axes[0, 0]
offset = 0
for lok in ['Temelji', 'Stupovi', 'Ploče']:
    maska_lok = lokacije == lok
    idx_lok   = indeksi[maska_lok]
    ax.scatter(idx_lok, fc_svi[maska_lok],
               color=boje_lok[lok], s=22, alpha=0.65,
               label=f'{lok} (n={np.sum(maska_lok)})', zorder=3)
    offset += np.sum(maska_lok)

# Posebno označi neprihvatljive uzorke crvenim prstenovima
idx_nep = indeksi[mask_nep]
ax.scatter(idx_nep, fc_svi[mask_nep],
           facecolors='none', edgecolors=boja_nep, s=90,
           linewidth=1.8, zorder=5,
           label=f'Ispod fck — neprihvatljivi (n={np.sum(mask_nep)})')

# Označi visoku rezervu narančastim trokutima
idx_vis = indeksi[mask_vis]
ax.scatter(idx_vis, fc_svi[mask_vis],
           marker='^', color=boja_vis, s=40, alpha=0.8, zorder=5,
           label=f'Visoka rezerva (n={np.sum(mask_vis)})')

# Kontrolne granice
ax.axhline(granica_donja, color=boja_nep, linestyle='--', linewidth=2.0,
           label=f'fck = {fck:.0f} MPa (donja granica)')
ax.axhline(granica_gornja, color=boja_vis, linestyle='--', linewidth=2.0,
           label=f'Gornja granica = {granica_gornja:.0f} MPa')
ax.axhline(mu_svi, color='black', linestyle=':', linewidth=1.5,
           label=f'Srednja vrijednost = {mu_svi:.1f} MPa')

# Obojeni pojasevi
ax.axhspan(0, granica_donja, alpha=0.06, color=boja_nep)
ax.axhspan(granica_gornja, fc_svi.max() + 5, alpha=0.06, color=boja_vis)

ax.set_title('Oblak točaka — sva mjerenja po redoslijedu uzorkovanja',
             fontweight='bold')
ax.set_xlabel('Redni broj uzorka')
ax.set_ylabel('fc [MPa]')
ax.legend(fontsize=7.5, loc='upper left', ncol=1)
ax.grid(True, alpha=0.3)
ax.set_ylim(bottom=0)

# ── GRAF 2: Histogram s normalnom raspodjelom ─────────────────
ax = axes[0, 1]
# Obojeni histogrami po kategorijama (slojeviti prikaz)
rozmaci = np.linspace(fc_svi.min() - 2, fc_svi.max() + 2, 28)
for fc_podaci, boja, lab in [
    (fc_svi[mask_nep],  boja_nep,    f'Ispod fck (n={np.sum(mask_nep)})'),
    (fc_svi[mask_prih], '#2ecc71',   f'Prihvatljivi (n={np.sum(mask_prih)})'),
    (fc_svi[mask_vis],  boja_vis,    f'Visoka rezerva (n={np.sum(mask_vis)})')
]:
    if len(fc_podaci) > 0:
        ax.hist(fc_podaci, bins=rozmaci, alpha=0.60, color=boja,
                edgecolor='white', linewidth=0.4, label=lab, density=True)

# Fit normalne raspodjele na UKUPNIM podacima (za usporedbu)
x_norm = np.linspace(fc_svi.min() - 5, fc_svi.max() + 5, 400)
ax.plot(x_norm, stats.norm.pdf(x_norm, mu_svi, sigma_svi),
        'k-', linewidth=2.5,
        label=f'N(μ={mu_svi:.1f}, σ={sigma_svi:.1f}) MPa')

# Kontrolne granice na histogramu
ax.axvline(granica_donja, color=boja_nep, linestyle='--', linewidth=2.0)
ax.axvline(granica_gornja, color=boja_vis, linestyle='--', linewidth=2.0)
# 5. percentil
fck_5perc = np.percentile(fc_svi, 5)
ax.axvline(fck_5perc, color='#9b59b6', linestyle=':', linewidth=1.8,
           label=f'5. percentil = {fck_5perc:.1f} MPa')

ax.set_title('Histogram tlačnih čvrstoća\n'
             'po kategorijama prihvatljivosti', fontweight='bold')
ax.set_xlabel('fc [MPa]')
ax.set_ylabel('Gustoća vjerojatnosti')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# ── GRAF 3: Box plot po lokacijama s ovjerhom granica ─────────
ax = axes[1, 0]
podaci_box  = [fc_svi[lokacije == lok] for lok in ['Temelji', 'Stupovi', 'Ploče']]
etikete_box = ['Temelji', 'Stupovi', 'Ploče']

bp = ax.boxplot(
    podaci_box,
    labels=etikete_box,
    patch_artist=True,              # popuni kutije bojom
    notch=True,                     # zarezani box (vizualizacija CI medijana)
    medianprops=dict(color='black', linewidth=2.5),
    whiskerprops=dict(linewidth=1.5),
    capprops=dict(linewidth=1.5),
    flierprops=dict(marker='o', markersize=5, linestyle='none', alpha=0.5)
)
for patch, lok in zip(bp['boxes'], etikete_box):
    patch.set_facecolor(boje_lok[lok])
    patch.set_alpha(0.65)

# Kontrolne granice
ax.axhline(granica_donja, color=boja_nep, linestyle='--', linewidth=2.0,
           label=f'fck = {fck:.0f} MPa')
ax.axhline(granica_gornja, color=boja_vis, linestyle='--', linewidth=2.0,
           label=f'Gornja granica = {granica_gornja:.0f} MPa')
ax.axhline(fcm_teorija, color='#2c3e50', linestyle=':', linewidth=1.8,
           label=f'fcm,teor = {fcm_teorija:.0f} MPa (EC2)')

# Dodaj anotaciju za broj neprihvatljivih u pločama
n_nep_ploce = np.sum((lokacije == 'Ploče') & mask_nep)
ax.annotate(
    f'{n_nep_ploce} uzoraka\nispod fck!',
    xy=(3, granica_donja - 1),
    xytext=(2.5, granica_donja - 8),
    arrowprops=dict(arrowstyle='->', color=boja_nep, lw=1.5),
    color=boja_nep, fontsize=9,
    bbox=dict(boxstyle='round,pad=0.3', facecolor='#fdecea', alpha=0.8)
)

ax.set_title('Box plot po lokaciji\n'
             '(zarezani box → 95% CI medijana)', fontweight='bold')
ax.set_ylabel('fc [MPa]')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3, axis='y')

# ── GRAF 4: QQ-plot (vizualna provjera normalnosti) ───────────
ax = axes[1, 1]
# Teorijski kvantili vs. uzorkovani kvantili
(th_kvantili, fc_kvantili), (slope, intercept, r) = stats.probplot(fc_svi)
ax.scatter(th_kvantili, fc_kvantili,
           s=20, alpha=0.50, color='#2980b9', label='Svi uzorci', zorder=3)

# Posebno označi neprihvatljive uzorke na QQ-plotu
if np.sum(mask_nep) > 1:
    (q_nep, fc_nep_q), _ = stats.probplot(fc_svi[mask_nep])
    ax.scatter(q_nep, fc_nep_q,
               s=50, color=boja_nep, zorder=5,
               label=f'Ispod fck (n={np.sum(mask_nep)})', edgecolors='black', lw=0.5)

# Teorijska normalna linija
x_qq = np.array([th_kvantili.min(), th_kvantili.max()])
ax.plot(x_qq, slope * x_qq + intercept, 'k--', linewidth=1.8,
        label=f'Teorijska normalna linija (r = {r:.4f})')

ax.set_title(
    'QQ-plot — provjera normalnosti raspodjele\n'
    'Ako točke prate liniju → raspodjela ≈ normalna',
    fontweight='bold'
)
ax.set_xlabel('Teorijski kvantili')
ax.set_ylabel('Uzorkovani kvantili fc [MPa]')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# Anotacija: objašnjenje repova
ax.annotate(
    'Rep → neprihvatljivi\nuzorci (Ploče)',
    xy=(th_kvantili[3], fc_kvantili[3]),
    xytext=(-2.5, 30),
    arrowprops=dict(arrowstyle='->', color=boja_nep, lw=1.5),
    color=boja_nep, fontsize=8.5,
    bbox=dict(boxstyle='round,pad=0.2', facecolor='#fdecea', alpha=0.8)
)

plt.tight_layout()
plt.savefig('primjer_04_statistika.pdf',
            dpi=150, bbox_inches='tight')
plt.show()

# ---------------------------------------------------------------
# SAŽETAK REZULTATA — kontrolne veličine
# ---------------------------------------------------------------
print(f"\n{'='*65}")
print("SAŽETAK — KONTROLA KVALITETE BETONA C30/37")
print(f"{'='*65}")
print(f"  Ukupan broj uzoraka:              {n_ukupno:>6}")
print(f"  Prihvatljivi uzorci:              {np.sum(mask_prih):>6}  "
      f"({np.sum(mask_prih)/n_ukupno*100:.1f} %)")
print(f"  Neprihvatljivi (ispod fck):       {np.sum(mask_nep):>6}  "
      f"({np.sum(mask_nep)/n_ukupno*100:.1f} %)")
print(f"  Visoka rezerva (iznad gor. gr.):  {np.sum(mask_vis):>6}  "
      f"({np.sum(mask_vis)/n_ukupno*100:.1f} %)")
print(f"\n  Izmjerena srednja čvrstoća fcm = {mu_svi:.2f} MPa")
print(f"  Teorijska srednja čvrstoća fcm = {fcm_teorija:.2f} MPa")
print(f"  Karakteristična čvrstoća (5. %) = {fck_5perc:.2f} MPa  "
      f"({'≥' if fck_5perc >= fck else '<'} fck = {fck:.0f} MPa)")
print("=" * 65)
