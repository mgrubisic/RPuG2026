"""
============================================================
  JEDNOOSNI MODEL BETONA  –  Stress-Strain dijagram
  Laboratorijski podatci (neovijeni beton)  |  Manderov model
============================================================
  Struktura skripte:
    1.  Import iz Excela
    2.  Normalizacija na zajednički x-raspon
    3.  Glađenje (Savitzky-Golay)
    4.  Statistika: medijan, 16% i 84% fraktila
    5.  Funkcija: naprezanje za proizvoljnu deformaciju
    6.  Osnovna statistika za zadanu deformaciju
    7.  Vizualizacija
============================================================
"""

# ── Biblioteke ────────────────────────────────────────────────
import numpy as np                        # numerički izračuni
import pandas as pd                       # čitanje Excela
import matplotlib.pyplot as plt           # crtanje grafova
from scipy.interpolate import interp1d    # interpolacija krivulja
from scipy.signal import savgol_filter    # glađenje krivulja


# ==============================================================
#  1.  IMPORT IZ EXCELA
# ==============================================================
def import_from_excel(filename, n):
    """
    Čita n krivulja iz Excel datoteke.
    Svaka krivulja je u zasebnom sheetu koji se zove 'Curve_01',
    'Curve_02' itd. i ima stupce  'strain [-]'  i  'stress [MPa]'.

    Rezultat je lista parova:  [ (ec1, fc1), (ec2, fc2), ... ]
      ec  –  array deformacija  [-]
      fc  –  array naprezanja   [MPa]
    """

    # Otvori Excel datoteku
    excel_datoteka = pd.ExcelFile(filename)

    # Prazna lista u kojoj ćemo čuvati sve krivulje
    curves = []

    # Prođi kroz sve krivulje redom (i = 1, 2, ..., n)
    for i in range(1, n + 1):

        # Naziv sheeta, npr. "Curve_01", "Curve_02" ...
        naziv_sheeta = "Curve_" + str(i).zfill(2)

        # Provjeri postoji li taj sheet u datoteci
        if naziv_sheeta in excel_datoteka.sheet_names:

            # Učitaj sheet kao tablicu (DataFrame)
            tablica = pd.read_excel(filename, sheet_name=naziv_sheeta)

            # Izvadi stupce kao numpy array-e
            ec = tablica["strain [-]"].values
            fc = tablica["stress [MPa]"].values

            # Dodaj par (ec, fc) na kraj liste
            curves.append((ec, fc))

    print("  Importirano", len(curves), "krivulja iz:", filename)
    return curves


# ==============================================================
#  2.  NORMALIZACIJA NA ZAJEDNIČKI X-RASPON
# ==============================================================
def normalize_curves(curves, n_pts):
    """
    Sve krivulje imaju različite maksimalne deformacije (x-os).
    Cilj: sve svesti na isti raspon  [0,  eps_common]
    gdje je  eps_common  =  minimum svih maksimalnih deformacija.

    Postupak:
      a) pronađi najmanji 'eps_cu' od svih krivulja
      b) definiraj zajednički grid od 0 do eps_common
      c) svaku krivulju lineano interpoliraj na taj grid
    """

    # ── a) Pronađi zajednički (najmanji) maksimalni x ─────────
    eps_common = curves[0][0][-1]          # start: max. def. prve krivulje

    print("\n  Granične deformacije po krivuljama:")

    for i in range(len(curves)):
        ec = curves[i][0]                  # array deformacija krivulje i
        eps_cu_i = ec[-1]                  # zadnji element = maksimalna def.

        print("    Krivulja", i + 1, ":  eps_cu =", round(eps_cu_i, 4))

        if eps_cu_i < eps_common:
            eps_common = eps_cu_i          # ažuriraj minimum

    print("\n  Zajednički x-raspon: [0,", round(eps_common, 4), "]")

    # ── b) Zajednički grid: n_pts jednako raspoređenih točaka ─
    ec_common = np.linspace(0.0, eps_common, n_pts)

    # ── c) Interpoliraj svaku krivulju na zajednički grid ─────
    normalized = []                        # lista normaliziranih krivulja

    for i in range(len(curves)):
        ec = curves[i][0]
        fc = curves[i][1]

        # Kreiraj interpolacijsku funkciju za ovu krivulju
        # 'linear' = linearna interpolacija između točaka
        f_interp = interp1d(ec, fc,
                            kind="linear",
                            bounds_error=False,
                            fill_value="extrapolate")

        # Evaluiraj interpoliranu funkciju na zajedničkom gridu
        fc_interp = f_interp(ec_common)

        # Osiguraj nenegativna naprezanja (fizikalni uvjet)
        for j in range(len(fc_interp)):
            if fc_interp[j] < 0.0:
                fc_interp[j] = 0.0

        # Napiši 0 na početku (pri nultoj deformaciji)
        fc_interp[0] = 0.0

        # Pohrani normaliziranu krivulju
        normalized.append((ec_common.copy(), fc_interp))

    return normalized, ec_common, eps_common


# ==============================================================
#  3.  GLAĐENJE KRIVULJA  (Savitzky-Golay filter)
# ==============================================================
def smooth_curves(normalized, window, polyorder):
    """
    Zaglade krivulje Savitzky-Golay filterom.

    Savitzky-Golay filter lokalno fitira polinom stupnja 'polyorder'
    na prozor od 'window' točaka i zamjenjuje centralnu točku
    vrijednošću polinoma  –  čuva oblik krivulje bolje od avg filtera.

    window    : broj točaka u prozoru (mora biti neparan, npr. 31)
    polyorder : stupanj polinoma (npr. 3 = kubični)
    """

    smoothed = []                          # lista zaglađenih krivulja

    for i in range(len(normalized)):
        ec = normalized[i][0]
        fc = normalized[i][1]

        # Primijeni filter
        fc_smooth = savgol_filter(fc,
                                  window_length=window,
                                  polyorder=polyorder)

        # Osiguraj nenegativna naprezanja
        for j in range(len(fc_smooth)):
            if fc_smooth[j] < 0.0:
                fc_smooth[j] = 0.0

        fc_smooth[0] = 0.0

        smoothed.append((ec, fc_smooth))

    return smoothed


# ==============================================================
#  4.  STATISTIKA  –  medijan, 16% i 84% fraktila
# ==============================================================
def compute_statistics(smoothed, ec_common):
    """
    Za svaku točku x-osi (svaki iznos deformacije) računa:
      •  medijan        –  srednja vrijednost po rangu
      •  16% fraktila   –  aproksimativno  srednja - 1*std
      •  84% fraktila   –  aproksimativno  srednja + 1*std
      •  srednja vr.    –  aritmetička sredina
      •  std            –  standardna devijacija

    Ideja: skupi naprezanja svih krivulja u matricu
      fc_matrica  ima dimenzije  (n_pts  ×  n_krivulja)
      Svaki redak = vrijednosti svih krivulja za jedan x
      Svaki stupac = jedna krivulja
    """

    n_pts      = len(ec_common)
    n_krivulja = len(smoothed)

    # ── Popuni matricu naprezanja ──────────────────────────────
    # Kreiraj praznu matricu punu nula
    fc_matrica = np.zeros((n_pts, n_krivulja))

    for j in range(n_krivulja):
        fc_matrica[:, j] = smoothed[j][1]   # j-ti stupac = j-ta krivulja

    # ── Izračunaj statistiku za svaki redak (svaki x) ─────────
    # axis=1 znači: računaj po stupcima (po krivuljama) za svaki redak
    median_fc = np.median    (fc_matrica, axis=1)
    p16_fc    = np.percentile(fc_matrica, 16, axis=1)
    p84_fc    = np.percentile(fc_matrica, 84, axis=1)
    mean_fc   = np.mean      (fc_matrica, axis=1)
    std_fc    = np.std       (fc_matrica, axis=1)

    # Pohrani sve u rječnik (dictionary) – zgododan način za
    # grupirati više varijabli pod jednim imenom
    stats = {
        "ec":     ec_common,
        "matrix": fc_matrica,
        "median": median_fc,
        "p16":    p16_fc,
        "p84":    p84_fc,
        "mean":   mean_fc,
        "std":    std_fc,
    }

    return stats


# ==============================================================
#  5.  FUNKCIJA:  naprezanje za zadanu deformaciju
# ==============================================================
def make_stress_function(stats):
    """
    Gradi interpolacijske funkcije (kubični spline) temeljem
    izračunate statistike.

    Vraća funkciju  'stress_at_strain'  koja prima deformaciju
    i vraća naprezanje za sve statistike (medijan, fraktile ...).

    Primjer korištenja:
        get_stress = make_stress_function(stats)
        rezultat   = get_stress(0.0020)
        print(rezultat['median'])    # medijansko naprezanje [MPa]
    """

    # Za svaku statistiku napravi zasebnu interp. funkciju
    f_median = interp1d(stats["ec"], stats["median"],
                        kind="cubic",
                        bounds_error=False,
                        fill_value=(0.0, 0.0))

    f_p16    = interp1d(stats["ec"], stats["p16"],
                        kind="cubic",
                        bounds_error=False,
                        fill_value=(0.0, 0.0))

    f_p84    = interp1d(stats["ec"], stats["p84"],
                        kind="cubic",
                        bounds_error=False,
                        fill_value=(0.0, 0.0))

    f_mean   = interp1d(stats["ec"], stats["mean"],
                        kind="cubic",
                        bounds_error=False,
                        fill_value=(0.0, 0.0))

    f_std    = interp1d(stats["ec"], stats["std"],
                        kind="cubic",
                        bounds_error=False,
                        fill_value=(0.0, 0.0))

    # ── Definicija funkcije koja se vraća korisniku ────────────
    def stress_at_strain(eps):
        """
        Za zadanu deformaciju eps vraća rječnik s naprezanjima [MPa].

        Parametar:
            eps  : float ili ndarray  –  deformacija [-]

        Vraća:
            dict s ključevima:  'median', 'p16', 'p84', 'mean', 'std'
        """
        eps_array = np.atleast_1d(np.asarray(eps, dtype=float))

        # Evaluiraj svaku interpolacijsku funkciju
        val_median = f_median(eps_array)
        val_p16    = f_p16   (eps_array)
        val_p84    = f_p84   (eps_array)
        val_mean   = f_mean  (eps_array)
        val_std    = f_std   (eps_array)

        # Ako je input bio skalar – vrati skalar (float), ne array
        if eps_array.size == 1:
            val_median = float(np.squeeze(val_median))
            val_p16    = float(np.squeeze(val_p16))
            val_p84    = float(np.squeeze(val_p84))
            val_mean   = float(np.squeeze(val_mean))
            val_std    = float(np.squeeze(val_std))

        # Složi rezultate u rječnik
        rezultat = {
            "eps":    eps,
            "median": val_median,
            "p16":    val_p16,
            "p84":    val_p84,
            "mean":   val_mean,
            "std":    val_std,
        }
        return rezultat

    return stress_at_strain


# ==============================================================
#  6.  OSNOVNA STATISTIKA ZA ZADANU DEFORMACIJU
# ==============================================================
def statistics_at_strain(eps_query, stats):
    """
    Za zadanu deformaciju eps_query:
      •  pronađe odgovarajući indeks u zajedničkom gridu
      •  izvuče naprezanja svih krivulja u toj točki
      •  ispiše tablicu osnovnih statističkih mjera
      •  vrati array s vrijednostima svih krivulja
    """

    # Pronađi indeks točke najbliže eps_query
    razlike = np.abs(stats["ec"] - eps_query)  # apsolutne razlike
    idx     = int(np.argmin(razlike))           # indeks najmanje razlike
    eps_act = stats["ec"][idx]                  # stvarna x-vrijednost

    # Izvuci naprezanja svih krivulja za taj indeks
    fc_vals = stats["matrix"][idx, :]           # redak idx, svi stupci

    # Izračunaj statistike
    n        = len(fc_vals)
    fc_min   = np.min(fc_vals)
    fc_max   = np.max(fc_vals)
    fc_mean  = np.mean(fc_vals)
    fc_med   = np.median(fc_vals)
    fc_std   = np.std(fc_vals)
    fc_p5    = np.percentile(fc_vals,  5)
    fc_p16   = np.percentile(fc_vals, 16)
    fc_p84   = np.percentile(fc_vals, 84)
    fc_p95   = np.percentile(fc_vals, 95)

    if fc_mean != 0:
        CoV = fc_std / fc_mean * 100
    else:
        CoV = 0.0

    # Ispis rezultata
    sep = "─" * 56
    print()
    print(sep)
    print("  Statistika naprezanja za  eps =", round(eps_act, 5), "[-]")
    print(sep)

    for i in range(n):
        print("    Krivulja", str(i + 1).rjust(2), ":  ",
              round(fc_vals[i], 3), "MPa")

    print("  " + "─" * 46)
    print("    N              =", n)
    print("    Min            =", round(fc_min,  3), "MPa")
    print("    Max            =", round(fc_max,  3), "MPa")
    print("    Srednja vr.    =", round(fc_mean, 3), "MPa")
    print("    Medijan        =", round(fc_med,  3), "MPa")
    print("    Std devijacija =", round(fc_std,  3), "MPa")
    print("    CoV            =", round(CoV,     2), "%")
    print("    5%  fraktila   =", round(fc_p5,   3), "MPa")
    print("    16% fraktila   =", round(fc_p16,  3), "MPa")
    print("    84% fraktila   =", round(fc_p84,  3), "MPa")
    print("    95% fraktila   =", round(fc_p95,  3), "MPa")
    print(sep)

    return fc_vals


# ==============================================================
#  7.  VIZUALIZACIJA
# ==============================================================
def plot_results(curves_raw, smoothed, stats, eps_query, save_path):
    """
    Crta četiri subplota:
      (a)  Sirove (uvezene) krivulje
      (b)  Zaglađene krivulje
      (c)  Zaglađene krivulje + statistika (medijan, fraktile, pojas)
      (d)  Histogram naprezanja za eps_query
    """

    # Paleta boja za 10 krivulja
    cmap   = plt.cm.tab10
    colors = []
    for i in range(10):
        colors.append(cmap(i / 10))

    # x-os: deformacije u promilima [‰] radi preglednosti
    ec_promili = stats["ec"] * 1000

    # Kreiraj figuru s 4 subplota (2 reda, 2 stupca)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    naslov = ("Jednoosni model betona  –  Neovijeni beton  "
              r"($f_{cm}$ = 53 MPa,  C45/55)")
    fig.suptitle(naslov, fontsize=13, fontweight="bold")


    # ──────────────────────────────────────────────────────────
    # SUBPLOT (a)  –  Sirove uvezene krivulje
    # ──────────────────────────────────────────────────────────
    ax = axes[0, 0]

    for i in range(len(curves_raw)):
        ec_i = curves_raw[i][0] * 1000     # konverzija u ‰
        fc_i = curves_raw[i][1]
        ax.plot(ec_i, fc_i,
                color=colors[i],
                alpha=1,
                linewidth=1.5,
                label="K" + str(i + 1))

    ax.set_xlabel(r"$\varepsilon_c$ [‰]")
    ax.set_ylabel(r"$\sigma_c$ [MPa]")
    ax.set_title("(a) Sirove krivulje")
    ax.legend(fontsize=7, ncol=5, loc="upper right")
    ax.grid(True, alpha=0.25)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)


    # ──────────────────────────────────────────────────────────
    # SUBPLOT (b)  –  Zaglađene krivulje
    # ──────────────────────────────────────────────────────────
    ax = axes[0, 1]

    for i in range(len(smoothed)):
        ec_i = smoothed[i][0] * 1000       # konverzija u ‰
        fc_i = smoothed[i][1]
        ax.plot(ec_i, fc_i,
                color=colors[i],
                alpha=1,
                linewidth=1.5,
                label="K" + str(i + 1))

    ax.set_xlabel(r"$\varepsilon_c$ [‰]")
    ax.set_ylabel(r"$\sigma_c$ [MPa]")
    ax.set_title("(b) Zaglađene krivulje (Savitzky-Golay)")
    ax.legend(fontsize=7, ncol=5, loc="upper right")
    ax.grid(True, alpha=0.25)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)


    # ──────────────────────────────────────────────────────────
    # SUBPLOT (c)  –  Statistika
    # ──────────────────────────────────────────────────────────
    ax = axes[1, 0]

    # Nacrtaj pojedinačne krivulje u pozadini (blijede)
    for i in range(len(smoothed)):
        ec_i = smoothed[i][0] * 1000
        fc_i = smoothed[i][1]
        ax.plot(ec_i, fc_i,
                color=colors[i],
                alpha=0.30,
                linewidth=1)

    # Pojas između 16% i 84% fraktile (fill_between)
    ax.fill_between(ec_promili,
                    stats["p16"],
                    stats["p84"],
                    alpha=0.20,
                    color="steelblue",
                    label="16–84% pojas")

    # Fraktile i statistike
    ax.plot(ec_promili, stats["p16"],
            color="blue", linestyle="--", linewidth=2,
            label="16% fraktila")

    ax.plot(ec_promili, stats["p84"],
            color="red", linestyle="--", linewidth=2,
            label="84% fraktila")

    ax.plot(ec_promili, stats["mean"],
            color="green", linestyle="-", linewidth=2,
            label="Srednja vr.")

    ax.plot(ec_promili, stats["median"],
            color="black", linestyle="-", linewidth=2.5,
            label="Medijan")

    # Vertikalna linija za eps_query
    ax.axvline(x=eps_query * 1000,
               color="darkorange",
               linestyle=":",
               linewidth=2.5,
               label=r"$\varepsilon$ = " + str(round(eps_query * 1000, 1)) + "‰")

    ax.set_xlabel(r"$\varepsilon_c$ [‰]")
    ax.set_ylabel(r"$\sigma_c$ [MPa]")
    ax.set_title("(c) Statistička obrada – medijan, 16% i 84% fraktila")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.25)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)


    # ──────────────────────────────────────────────────────────
    # SUBPLOT (d)  –  Histogram za eps_query
    # ──────────────────────────────────────────────────────────
    ax = axes[1, 1]

    # Pronađi indeks za eps_query
    razlike = np.abs(stats["ec"] - eps_query)
    idx_q   = int(np.argmin(razlike))
    fc_q    = stats["matrix"][idx_q, :]    # naprezanja svih 10 krivulja

    mu_q = np.mean(fc_q)
    s_q  = np.std(fc_q)

    # Histogram
    ax.hist(fc_q,
            bins=6,
            color="steelblue",
            edgecolor="black",
            alpha=0.65,
            zorder=2)

    # Vertikalne linije za statistike
    ax.axvline(x=mu_q,
               color="green", linestyle="-", linewidth=2.2,
               label="Srednja = " + str(round(mu_q, 2)) + " MPa")

    ax.axvline(x=np.median(fc_q),
               color="black", linestyle="--", linewidth=2.2,
               label="Medijan = " + str(round(float(np.median(fc_q)), 2)) + " MPa")

    ax.axvline(x=np.percentile(fc_q, 16),
               color="blue", linestyle=":", linewidth=2.0,
               label="16% = " + str(round(float(np.percentile(fc_q, 16)), 2)) + " MPa")

    ax.axvline(x=np.percentile(fc_q, 84),
               color="red", linestyle=":", linewidth=2.0,
               label="84% = " + str(round(float(np.percentile(fc_q, 84)), 2)) + " MPa")

    # Sjenčani pojas ±1σ
    ax.axvspan(mu_q - s_q, mu_q + s_q,
               alpha=0.10,
               color="gray",
               label="±1σ  (σ = " + str(round(s_q, 2)) + " MPa)")

    ax.set_xlabel(r"$\sigma_c$ [MPa]")
    ax.set_ylabel("Frekvencija")
    ax.set_title(r"(d) Distribucija $\sigma_c$  za  $\varepsilon$ = "
                 + str(round(eps_query * 1000, 1)) + "‰")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.25)

    # Uredi razmak između subplotova i spremi
    plt.tight_layout()
    fig.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close(fig)
    print("  Slika spremljena:", save_path)


# ==============================================================
#  GLAVNI DIO SKRIPTE  (MAIN)
# ==============================================================
print("=" * 60)
print("  JEDNOOSNI MODEL BETONA  –  Analiza laboratorijskih podataka")
print("  fcm = 53 MPa,  eps_c0 = 0.0024,  Ec = 36000 MPa")
print("=" * 60)


# ── KORAK 1: Import ───────────────────────────────────────────
print("\n[1]  Import iz Excela ...")

curves_in = import_from_excel("Beton_Radni_dijagrami.xlsx", n=10)


# ── KORAK 2: Normalizacija ────────────────────────────────────
print("\n[2]  Normalizacija krivulja ...")

normalized, ec_common, eps_min = normalize_curves(curves_in, n_pts=600)


# ── KORAK 3: Glađenje ─────────────────────────────────────────
print("\n[3]  Glađenje krivulja (Savitzky-Golay, w=101, p=3) ...")

smoothed = smooth_curves(normalized, window=101, polyorder=3)
print("  Zaglađeno.")


# ── KORAK 4: Statistika ───────────────────────────────────────
print("\n[4]  Računanje statistike ...")

stats = compute_statistics(smoothed, ec_common)
print("  Statistika izračunata.")


# ── KORAK 5: Funkcija za naprezanje ───────────────────────────
print("\n[5]  Kreiranje interpolacijske funkcije ...")

get_stress = make_stress_function(stats)

# Provjerni upiti – ispis naprezanja za odabrane deformacije
print()
print("  Naprezanje za nekoliko vrijednosti deformacije:")
print()
print("  {:>10}  {:>10}  {:>10}  {:>10}  {:>10}  {:>10}".format(
    "eps [-]", "Medijan", "16%", "84%", "Srednja", "Std"))
print("  " + "-" * 66)

eps_lista = [0.0005, 0.0010, 0.0015, 0.0020, 0.0025, 0.0030]

for eps_t in eps_lista:
    if eps_t > eps_min:
        print("  {:>10.4f}  van raspona  (eps > eps_common = {:.4f})".format(
            eps_t, eps_min))
        continue

    r = get_stress(eps_t)
    print("  {:>10.4f}  {:>10.3f}  {:>10.3f}  {:>10.3f}  {:>10.3f}  {:>10.3f}".format(
        eps_t, r["median"], r["p16"], r["p84"], r["mean"], r["std"]))


# ── KORAK 6: Statistika za zadanu deformaciju ─────────────────
EPS_QUERY = 0.002   # <-- promijenite po potrebi

print("\n[6]  Osnovna statistika za  eps =", EPS_QUERY, "...")
statistics_at_strain(EPS_QUERY, stats)


# ── KORAK 7: Vizualizacija ────────────────────────────────────
print("\n[7]  Vizualizacija ...")

plot_results(curves_raw=curves_in,
             smoothed=smoothed,
             stats=stats,
             eps_query=EPS_QUERY,
             save_path="Beton_Radni_dijagrami.png")


print()
print("=" * 60)
print("  Analiza završena.")
print("=" * 60)
