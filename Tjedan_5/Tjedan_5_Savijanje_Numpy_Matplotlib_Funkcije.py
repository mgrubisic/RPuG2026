# -*- coding: utf-8 -*-
# =============================================================================
#  Računalno programiranje u građevinarstvu (254810) | Tjedan 4/15
#  Radionica: NumPy nizovi i Matplotlib --- višestruke krivulje petljom
#  Izv. prof. dr. sc. Marin Grubišić | marin.grubisic@gfos.hr | GrAFOS
#  -----------------------------------------------------------------------
#  VERZIJA 2 --- Predložak za nastavu (vlastite funkcije)
# =============================================================================
#
#  UPUTA ZA STUDENTE:
#  ------------------
#  Svaka faza (%% blok) izvršava se ZASEBNO u Spyderu:
#    - Označite blok i pritisnite  Ctrl + Enter
#    - ili kliknite gumb "Run cell" u alatnoj traci
#  Izvršavajte faze REDOM. Ne preskačite!
#
#  CILJ RADIONICE:
#  ---------------
#  Isti fizikalni problem kao u Verziji 1, ali organiziran kroz
#  VLASTITE FUNKCIJE. Svaka funkcija ima JEDNU jasnu zadaću.
#  Prednosti:
#    - kod je čitljiviji i kraći u glavnom programu
#    - svaka funkcija može se testirati zasebno
#    - funkcije se mogu ponovo koristiti u drugim zadacima
#
#  TEORIJSKA PODLOGA:
#  ------------------
#  Progib proste grede pod jednolikim opterećenjem q [kN/m]:
#
#       w(x) = q * x * (L³ - 2L·x² + x³) / (24·E·I)
#
#  Maksimalni progib (na sredini raspona, x = L/2):
#
#       w_max = 5 * q * L⁴ / (384 * E * I)
#
#  Granični uvjet uporabivosti (GSU) prema EC2/EC3:
#
#       w_max ≤ L / 250
#
# =============================================================================


# %%  [FAZA 0]  Uvoz biblioteka
# -----------------------------------------------------------------------
#  Uvijek uvozite na vrhu datoteke. Pokrenite ovaj blok JEDNOM na početku.
# -----------------------------------------------------------------------



print("Biblioteke uspješno uvezene.")
print(f"  NumPy verzija:      {np.__version__}")
print(f"  Matplotlib verzija: {plt.matplotlib.__version__}")


# %%  [FAZA 1]  Definicija vlastitih funkcija
# -----------------------------------------------------------------------
#  SVE funkcije definiramo OVDJE, na jednom mjestu --- prije glavnog koda.
#  Svaka funkcija:
#    - ima jasan naziv koji opisuje što radi
#    - prima ulazne parametre (argumenti)
#    - vraća rezultat pomoću  return
#    - dokumentirana je docstringom (""" ... """)
#
#  Anatomija funkcije u Pythonu:
#
#    def naziv_funkcije(arg1, arg2, ...):
#        """Kratki opis što funkcija radi."""
#        # tijelo funkcije
#        rezultat = ...
#        return rezultat
#
# -----------------------------------------------------------------------

# ------------------------------------------------------------------
# FUNKCIJA 1: Geometrija pravokutnog presjeka
# ------------------------------------------------------------------
def presjek_pravokutni(b, h):
    """
    Izračunava karakteristike pravokutnog presjeka.

    Parametri
    ----------
    b : float   širina presjeka [m]
    h : float   visina presjeka [m]

    Vraća
    -----
    A : float   površina presjeka [m²]
    I : float   moment tromosti oko neutralne osi [m⁴]
    """
    # površina presjeka [m²]

    # moment tromosti oko neutralne osi [m⁴]

    # vraćamo oba rezultata (tuple)


# ------------------------------------------------------------------
# FUNKCIJA 2: Progibna linija w(x)
# ------------------------------------------------------------------
def progib_linija(x, q, L, E, I):
    """
    Izračunava progib proste grede pod jednolikim opterećenjem.

    Parametri
    ----------
    x : np.ndarray  niz položaja duž grede [m]
    q : float       jednoliko opterećenje [kN/m]
    L : float       raspon grede [m]
    E : float       modul elastičnosti [kN/m²]
    I : float       moment tromosti [m⁴]

    Vraća
    -----
    w : np.ndarray  progib u svakoj točki x [m]
    """
    # w(x) = q * x * (L³ - 2L·x² + x³) / (24·E·I)  [vektorski!]



# ------------------------------------------------------------------
# FUNKCIJA 3: Analitički maksimalni progib
# ------------------------------------------------------------------
def w_max_analiticki(q, L, E, I):
    """
    Izračunava analitički maksimalni progib proste grede
    pod jednolikim opterećenjem (na sredini raspona).

    Parametri
    ----------
    q : float   jednoliko opterećenje [kN/m]
    L : float   raspon grede [m]
    E : float   modul elastičnosti [kN/m²]
    I : float   moment tromosti [m⁴]

    Vraća
    -----
    w_max : float   maksimalni progib [m]
    """
    # w_max = 5 * q * L⁴ / (384 * E * I)



# ------------------------------------------------------------------
# FUNKCIJA 4: Provjera graničnog uvjeta uporabivosti (GSU)
# ------------------------------------------------------------------
def provjera_gsu(w_max, L, limit=250):
    """
    Provjerava zadovoljava li progib granični uvjet uporabivosti.

    Parametri
    ----------
    w_max : float   maksimalni progib [m]
    L     : float   raspon grede [m]
    limit : int     nazivnik granice (default: 250 → L/250)

    Vraća
    -----
    zadovoljeno : bool    True ako je w_max ≤ L/limit
    w_lim       : float   granični progib L/limit [m]
    """
    # granični progib [m]

    # booleova provjera (True / False)

    # vraćamo oba rezultata (tuple)


# ------------------------------------------------------------------
# FUNKCIJA 5: Ispis usporedne tablice raspona
# ------------------------------------------------------------------
def ispisi_tablicu_raspona(L_arr, q, E, I, limit=250):
    """
    Ispisuje usporednu tablicu progiba i provjere GSU
    za niz raspona L_arr pri konstantnom opterećenju q.

    Parametri
    ----------
    L_arr : np.ndarray  niz raspona [m]
    q     : float       jednoliko opterećenje [kN/m]
    E     : float       modul elastičnosti [kN/m²]
    I     : float       moment tromosti [m⁴]
    limit : int         nazivnik GSU granice (default: 250)
    """
    print(f"--- Provjera GSU (q = {q:.0f} kN/m, granica L/{limit}) ---")
    print(f"{'L [m]':>7} | {'w_max [mm]':>10} | "
          f"{'L/{:d} [mm]'.format(limit):>10} | {'Ocjena':>9}")
    print("-" * 46)
    for L_p in L_arr:
        # pozivamo funkcije 3 i 4 unutar petlje

        # "OK!" ako je zadovoljeno, inače "NOK!"

        print(f"{L_p:>7.1f} | {w_max*1000:>10.2f} | "
              f"{w_lim*1000:>10.1f} | {ocjena:>9}")


# ------------------------------------------------------------------
# FUNKCIJA 6: Graf višestrukih raspona
# ------------------------------------------------------------------
def crtaj_vise_raspona(L_arr, q, E, I, ax=None, paleta='viridis'):
    """
    Crta progibne linije za niz raspona na jednom grafu.

    Parametri
    ----------
    L_arr  : np.ndarray  niz raspona [m]
    q      : float       jednoliko opterećenje [kN/m]
    E      : float       modul elastičnosti [kN/m²]
    I      : float       moment tromosti [m⁴]
    ax     : Axes        matplotlib os (ako je None, kreira novu)
    paleta : str         naziv matplotlib palete boja

    Vraća
    -----
    ax : Axes   matplotlib os s ucrtanim krivuljama
    """
    # ako ax nije proslijeđen, kreiramo novi graf
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 5))

    # paleta boja: N diskretnih boja iz odabrane palete

    for k, L_p in enumerate(L_arr):
        # diskretizacija osi x za ovaj raspon

        # poziv funkcije 2: progibna linija

        # poziv funkcije 4: GSU granica za ovaj raspon

        # crtamo krivulju s bojom cmap(k)

        # isprekidana crta GSU granice (ista boja, alpha=0.5)

    # formatiranje grafa
    ax.invert_yaxis()
    ax.set_xlabel('x  [m]', fontsize=12)
    ax.set_ylabel('w  [mm]', fontsize=12)
    ax.legend(fontsize=10, loc='lower center')
    ax.grid(True, linestyle='--', alpha=0.4)
    return ax


# ------------------------------------------------------------------
# FUNKCIJA 7: Graf višestrukih opterećenja
# ------------------------------------------------------------------
def crtaj_vise_opterecenja(q_arr, L_fix, E, I, ax=None, paleta='plasma'):
    """
    Crta progibne linije za niz opterećenja pri fiksnom rasponu.

    Parametri
    ----------
    q_arr  : np.ndarray  niz opterećenja [kN/m]
    L_fix  : float       fiksni raspon grede [m]
    E      : float       modul elastičnosti [kN/m²]
    I      : float       moment tromosti [m⁴]
    ax     : Axes        matplotlib os (ako je None, kreira novu)
    paleta : str         naziv matplotlib palete boja

    Vraća
    -----
    ax : Axes   matplotlib os s ucrtanim krivuljama
    """
    # ako ax nije proslijeđen, kreiramo novi graf
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 5))

    # paleta boja: N diskretnih boja iz odabrane palete

    for k, q_i in enumerate(q_arr):
        # diskretizacija osi x (raspon je fiksiran!)

        # poziv funkcije 2: progibna linija

        # crtamo krivulju s bojom cmap(k)

    # GSU granica --- samo jedanput (isti L_fix za sve!)
    # poziv funkcije 4: dobivamo samo w_lim (zadovoljeno ignoriramo s _)

    # ax.axhline(...)   GSU crta

    # formatiranje grafa
    ax.invert_yaxis()
    ax.set_xlabel('x  [m]', fontsize=12)
    ax.set_ylabel('w  [mm]', fontsize=12)
    ax.legend(fontsize=9, loc='lower center')
    ax.grid(True, linestyle=':', alpha=0.5)
    return ax


print("Sve funkcije uspješno definirane.")
print("  Dostupne funkcije:")
print("    presjek_pravokutni(b, h)")
print("    progib_linija(x, q, L, E, I)")
print("    w_max_analiticki(q, L, E, I)")
print("    provjera_gsu(w_max, L, limit=250)")
print("    ispisi_tablicu_raspona(L_arr, q, E, I, limit=250)")
print("    crtaj_vise_raspona(L_arr, q, E, I, ax, paleta)")
print("    crtaj_vise_opterecenja(q_arr, L_fix, E, I, ax, paleta)")


# %%  [FAZA 2]  Parametri presjeka i materijala
# -----------------------------------------------------------------------
#  Pozivamo funkciju presjek_pravokutni() --- umjesto pisanja
#  formule direktno u kod, koristimo definiranu funkciju.
# -----------------------------------------------------------------------

# Materijal: beton C30/37
      # modul elastičnosti [kN/m²]

# Presjek: pravokutni AB presjek
        # širina presjeka [m]
        # visina presjeka [m]

# Poziv funkcije --- vraća dva rezultata odjednom (tuple raspakiravanje)


print("--- Parametri presjeka ---")
print(f"  b = {b*100:.0f} cm,  h = {h*100:.0f} cm")
print(f"  A = {A*1e4:.1f} cm²")
print(f"  I = {I*1e8:.2f} cm⁴")
print(f"  E = {E/1e6:.0f} GPa   -->   EI = {E*I:.2f} kNm²")


# %%  [FAZA 3]  Provjera funkcija za JEDAN slučaj
# -----------------------------------------------------------------------
#  Testiramo svaku funkciju zasebno --- ovo je "unit test" u malom.
#  Uspoređujemo analitički maksimum s np.max() numeričkim rezultatom.
# -----------------------------------------------------------------------

      # kN/m
       # m

# Diskretizacija osi grede
    # 300 točaka od 0 do L

# Poziv funkcija (svaku posebno --- redoslijed je bitan!)
            # F2: numpy array [m]
             # F3: skalar [m]
                              # numerički max [m]
                                   # F4: GSU provjera

print("--- Provjera za jedan slučaj ---")
print(f"  q = {q} kN/m,  L = {L} m")
print(f"  w_max (analitički) = {w_max_an*1000:.3f} mm")
print(f"  w_max (np.max)     = {w_max_np*1000:.3f} mm")
print(f"  Relativna razlika  = {abs(w_max_an - w_max_np)/w_max_an*100:.4f} %")
print(f"  Granični progib    = {w_lim*1000:.1f} mm  (L/250)")
print(f"  GSU zadovoljeno:     {'DA ✓' if zadovoljeno else 'NE ✗'}")


# %%  [FAZA 4]  Graf jedne krivulje
# -----------------------------------------------------------------------
#  Vizualiziramo progibnu liniju iz Faze 3.
# -----------------------------------------------------------------------

# fig, ax = plt.subplots(...)

# ax.plot(...)          progibna linija (w u mm!)

# ax.axhline(...)       GSU granica

# ax.invert_yaxis()
# ax.set_xlabel(...)    ax.set_ylabel(...)    ax.set_title(...)
# ax.legend(...)        ax.grid(...)
# plt.tight_layout()    plt.show()

print("Graf jedne krivulje iscrtan.")


# %%  [FAZA 5]  Tablica i graf višestrukih raspona
# -----------------------------------------------------------------------
#  Koristimo ispisi_tablicu_raspona() i crtaj_vise_raspona() ---
#  glavni program sada je SAMO poziv funkcija!
# -----------------------------------------------------------------------

      # kN/m
    # rasponi [m]

# Tablica --- jedan poziv funkcije (F5)


# Graf --- jedan poziv funkcije (F6)
# fig, ax = plt.subplots(...)
# crtaj_vise_raspona(...)
# ax.set_title(...)
# plt.tight_layout()    plt.savefig(...)    plt.show()

print("Graf s višestrukim rasponima iscrtan i pohranjen.")


# %%  [FAZA 6]  Graf višestrukih opterećenja
# -----------------------------------------------------------------------
#  Fiksiramo raspon L = 6 m, mijenjamo q.
#  Glavni program: samo poziv funkcije crtaj_vise_opterecenja().
# -----------------------------------------------------------------------

         # fiksni raspon [m]
                                                   # kN/m

# fig, ax = plt.subplots(...)
# crtaj_vise_opterecenja(...)
# ax.set_title(...)
# plt.tight_layout()    plt.savefig(...)    plt.show()

print("Graf višestrukih opterećenja iscrtan i pohranjen.")


# %%  [FAZA 7]  Sažetak naučenih naredbi
# -----------------------------------------------------------------------
#  Ispisujemo pregled svih ključnih naredbi korištenih u radionici.
# -----------------------------------------------------------------------

sazetak = """
╔══════════════════════════════════════════════════════════════════════╗
║     SAŽETAK: Vlastite funkcije + NumPy + Matplotlib (Tjedan 4/15)   ║
╠══════════════════════════════════════════════════════════════════════╣
║  Anatomija funkcije:                                                 ║
║    def naziv(arg1, arg2):   — definicija s parametrima              ║
║        \'\'\'Docstring.\'\'\'                                            ║
║        return rezultat      — vraća jedan ili više rezultata         ║
║                                                                      ║
║  Poziv i raspakiravanje višestrukih rezultata:                       ║
║    A, I = presjek_pravokutni(b, h)   — tuple raspakiravanje          ║
║    ok, w_lim = provjera_gsu(w, L)   — dva return vrijednosti        ║
║                                                                      ║
║  Parametar s default vrijednošću:                                    ║
║    def provjera_gsu(w, L, limit=250)  — limit je opcionalan         ║
║    provjera_gsu(w, L)         — poziv bez limit → koristi 250       ║
║    provjera_gsu(w, L, 300)    — poziv s limit=300                   ║
║                                                                      ║
║  Prednosti vlastitih funkcija:                                       ║
║    ✓  Glavna skripta čitljivija (samo pozivi funkcija)               ║
║    ✓  Lako testiranje svake funkcije zasebno                         ║
║    ✓  Ponovna upotreba (copy-paste funkcije u novu skriptu)          ║
║    ✓  Smanjuje ponavljanje koda (DRY princip)                        ║
╚══════════════════════════════════════════════════════════════════════╝
"""
print(sazetak)
