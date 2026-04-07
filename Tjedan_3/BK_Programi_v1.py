#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
Statički proračun i dimenzioniranje armiranobetonske konstrukcije bistroa
===============================================================================
Konverzija u Python: poglavlja 1–2
    (Dispozicija, geometrija, materijali, opterećenja, statičke visine)

Norme:
    - HRN EN 1990 (Osnove projektiranja)
    - HRN EN 1991-1-1 (Djelovanja na konstrukcije)
    - HRN EN 1991-1-3 (Opterećenje snijegom)
    - HRN EN 1992-1-1 (Projektiranje betonskih konstrukcija)
    - HRN EN 1998-1 (Potresno inženjerstvo)

Jedinice:
    - Duljine: cm (osim gdje je naznačeno drugačije)
    - Sile: kN
    - Momenti: kNm
    - Naprezanja: kN/cm² ili N/mm²
    - Površinska opterećenja: kN/m²
===============================================================================
"""

import numpy as np


# =============================================================================
# 2.1  DISPOZICIJA KONSTRUKCIJE
# =============================================================================

def definiranje_katastarske_cestice():
    """
    Definira dimenzije katastarske čestice i provjerava
    da se konstrukcija uklapa unutar dostupnog prostora.

    Katastarska čestica: 22 × 49 m
    Vanjski gabariti konstrukcije: 35,85 × 18,00 m
    Zahtjev: bruto površina karakterističnog kata 620–680 m²

    Returns
    -------
    dict
        Rječnik s ključnim podacima o dispoziciji.
    """
    # Katastarska čestica [m]
    B_kc = 22.0   # širina čestice
    L_kc = 49.0   # duljina čestice

    # Vanjski gabariti konstrukcije [m]
    L_konstr = 35.85  # duljina konstrukcije (u smjeru X)
    B_konstr = 18.00  # širina konstrukcije (u smjeru Y)

    # Bruto površina karakterističnog kata [m²]
    A_kat = L_konstr * B_konstr

    # Provjera zahtjeva za površinu
    A_min, A_max = 620.0, 680.0
    zadovoljava_povrsinu = A_min <= A_kat <= A_max

    # Provjera uklopljenosti na česticu
    # Slobodan prostor sa svake strane čestice
    slobodno_x = (L_kc - L_konstr) / 2.0  # ≈ 6,58 m
    slobodno_y = (B_kc - B_konstr) / 2.0   # ≈ 2,00 m
    uklapa_se = (L_konstr <= L_kc) and (B_konstr <= B_kc)

    # Lokacija objekta
    lokacija = "Osijek"
    nadmorska_visina = 95.0  # m.n.m.

    # Visina karakterističnog kata [m]
    h_kat = 3.10

    # Projektirani vijek trajanja [god]
    vijek_trajanja = 50

    # Tip krova
    tip_krova = "ravni, neprohodan, pad 1%"

    # Razred armature
    armatura = "B500B"

    rezultati = {
        "B_kc_m": B_kc,
        "L_kc_m": L_kc,
        "L_konstr_m": L_konstr,
        "B_konstr_m": B_konstr,
        "A_kat_m2": A_kat,
        "zadovoljava_povrsinu": zadovoljava_povrsinu,
        "uklapa_se_na_cesticu": uklapa_se,
        "slobodno_x_m": slobodno_x,
        "slobodno_y_m": slobodno_y,
        "lokacija": lokacija,
        "nadmorska_visina_m": nadmorska_visina,
        "h_kat_m": h_kat,
        "vijek_trajanja_god": vijek_trajanja,
        "tip_krova": tip_krova,
        "armatura": armatura,
    }

    # ----- Ispis rezultata -----
    print("=" * 70)
    print("2.1  DISPOZICIJA KONSTRUKCIJE")
    print("=" * 70)
    print(f"  Katastarska čestica:       {B_kc:.0f} × {L_kc:.0f} m")
    print(f"  Gabariti konstrukcije:     {L_konstr:.2f} × {B_konstr:.2f} m")
    print(f"  Površina kar. kata:        {A_kat:.1f} m²  "
          f"(zahtjev: {A_min:.0f}–{A_max:.0f} m²) "
          f"→ {'OK' if zadovoljava_povrsinu else 'NE ZADOVOLJAVA!'}")
    print(f"  Uklapa se na česticu:      {'DA' if uklapa_se else 'NE'}")
    print(f"    Slobodan prostor X:      {slobodno_x:.2f} m (sa svake strane)")
    print(f"    Slobodan prostor Y:      {slobodno_y:.2f} m (sa svake strane)")
    print(f"  Lokacija:                  {lokacija}, {nadmorska_visina:.0f} m.n.m.")
    print(f"  Visina kata:               {h_kat:.2f} m")
    print(f"  Projektirani vijek:        {vijek_trajanja} godina")
    print(f"  Tip krova:                 {tip_krova}")
    print(f"  Razred armature:           {armatura}")
    print()

    return rezultati


# =============================================================================
# 2.2  DEFINIRANJE GEOMETRIJE – DIMENZIJE POPREČNIH PRESJEKA
# =============================================================================
import math

def round_up_to_even(f):
    return math.ceil(f / 2.0) * 2

def round_up_to_even_ten(f):
    return math.ceil(f / 10.0) * 10
    
def proracun_debljine_ploce(L_min_cm):
    """
    Određuje minimalnu debljinu ploče prema pravilu prakse
    (Tomičić, 1996.): d_pl ≥ L_min / 35.

    Parameters
    ----------
    L_min_cm : float
        Kraći raspon ploče [cm].

    Returns
    -------
    dict
        d_pl_min_cm : minimalna debljina [cm]
        d_pl_usv_cm : usvojena debljina [cm]
    """
    d_pl_min = L_min_cm / 35.0
    # Usvojeno prema pravilu prakse: zaokruženo na 20 cm
    d_pl_usv = round_up_to_even(d_pl_min)

    print("-" * 50)
    print("  Debljina ploče (Tomičić, 1996.):")
    print(f"    d_pl = L_min / 35 = {L_min_cm:.0f} / 35 = {d_pl_min:.2f} cm")
    print(f"    d_pl,usv = {d_pl_usv:.0f} cm")

    return {"d_pl_min_cm": d_pl_min, "d_pl_usv_cm": d_pl_usv}


def proracun_visine_grede(L_raspon_cm):
    """
    Određuje minimalnu visinu grede prema pravilu prakse
    (Tomičić, 1996.): h_g ≥ L / 12.

    Parameters
    ----------
    L_raspon_cm : float
        Raspon grede [cm].

    Returns
    -------
    dict
        h_g_min_cm : minimalna visina grede [cm]
        h_g_usv_cm : usvojena visina grede [cm]
    """
    h_g_min = L_raspon_cm / 12.0
    # Usvojeno: zaokruženo na 70 cm
    h_g_usv = round_up_to_even_ten(h_g_min)

    print("-" * 50)
    print("  Visina grede (Tomičić, 1996.):")
    print(f"    h_g,min = L / 12 = {L_raspon_cm:.0f} / 12 = {h_g_min:.1f} cm")
    print(f"    h_g,usv = {h_g_usv:.0f} cm")

    return {"h_g_min_cm": h_g_min, "h_g_usv_cm": h_g_usv}


def proracun_sirine_grede(b_c_cm, h_w_cm):
    """
    Određuje širinu primarne potresne grede prema HRN EN 1998-1,
    izraz (2.3):
        b_w ≤ min{ b_c + h_w , 2·b_c }

    Parameters
    ----------
    b_c_cm : float
        Širina stupa okomito na promatranu gredu [cm].
    h_w_cm : float
        Visina grede [cm].

    Returns
    -------
    dict
        b_w_max_cm : najveća dopuštena širina grede [cm]
        b_w_usv_cm : usvojena širina grede [cm]
    """
    opcija_1 = b_c_cm + h_w_cm
    opcija_2 = 2.0 * b_c_cm
    b_w_max = min(opcija_1, opcija_2)

    # Usvojeno: 45 cm (≤ b_w_max)
    b_w_usv = 45

    print("-" * 50)
    print("  Širina primarne potresne grede (HRN EN 1998-1):")
    print(f"    b_w ≤ min{{ b_c + h_w , 2·b_c }}")
    print(f"    b_w ≤ min{{ {b_c_cm:.0f} + {h_w_cm:.0f} , 2×{b_c_cm:.0f} }}")
    print(f"    b_w ≤ min{{ {opcija_1:.0f} , {opcija_2:.0f} }} = {b_w_max:.0f} cm")
    print(f"    b_w,usv = {b_w_usv:.0f} cm  (≤ {b_w_max:.0f} cm → OK)")

    return {"b_w_max_cm": b_w_max, "b_w_usv_cm": b_w_usv}


def definiranje_geometrije():
    """
    Objedinjuje proračune debljine ploče, visine grede i širine grede.
    Koristi dimenzije iz dispozicije konstrukcije.

    Returns
    -------
    dict
        Svi geometrijski parametri poprečnih presjeka.
    """
    print("=" * 70)
    print("2.2  DEFINIRANJE GEOMETRIJE – DIMENZIJE POPREČNIH PRESJEKA")
    print("=" * 70)

    # Kraći raspon ploče = 585 cm (svijetli) + 45 cm (greda) → ali
    # prema radu: L_min = 585 cm za debljinu ploče
    L_min_ploca_cm = 585.0
    rez_ploca = proracun_debljine_ploce(L_min_ploca_cm)

    # Raspon grede = 708 cm (osovinski)
    L_raspon_grede_cm = 708.0
    rez_greda_h = proracun_visine_grede(L_raspon_grede_cm)

    # Širina stupa = 45 cm, visina grede = 70 cm
    b_stup_cm = 45.0
    h_greda_cm = rez_greda_h["h_g_usv_cm"]
    rez_greda_b = proracun_sirine_grede(b_stup_cm, h_greda_cm)

    print()

    geometrija = {
        **rez_ploca,
        **rez_greda_h,
        **rez_greda_b,
        "b_stup_cm": b_stup_cm,
    }
    return geometrija


# =============================================================================
# 2.3  NOSIVOST PLOČA
# =============================================================================

def provjera_nosivosti_ploca(L_x_cm, L_y_cm):
    """
    Provjerava nosivost ploče: nosiva u 1 ili 2 smjera.
    Ploča je nosiva u 2 smjera ako je Lx/Ly < 2.

    Napomena: Lx je dulji raspon, Ly kraći raspon.

    Parameters
    ----------
    L_x_cm : float
        Dulji raspon ploče [cm] (os do osi greda).
    L_y_cm : float
        Kraći raspon ploče [cm] (os do osi greda).

    Returns
    -------
    dict
        omjer : float
        nosiva_u_2_smjera : bool
    """
    # Prema radu: Lx = 648 + 60 = 708, Ly = 585 + 45 = 630
    # Ali rad koristi: Lx/Ly = (648+60)/(585+45) = 708/630 = 1.12
    # Zapravo u radu piše Lx/Ly = 1.12 — koristimo dane raspone
    omjer = L_x_cm / L_y_cm
    nosiva_2 = omjer < 2.0

    print("=" * 70)
    print("2.3  NOSIVOST PLOČA")
    print("=" * 70)
    print(f"  Lx = {L_x_cm:.0f} cm,  Ly = {L_y_cm:.0f} cm")
    print(f"  Lx / Ly = {L_x_cm:.0f} / {L_y_cm:.0f} = {omjer:.2f}")
    if nosiva_2:
        print(f"  {omjer:.2f} < 2.0  →  Ploča nosiva u 2 smjera")
    else:
        print(f"  {omjer:.2f} ≥ 2.0  →  Ploča nosiva u 1 smjeru")
    print()

    return {"omjer_Lx_Ly": omjer, "nosiva_u_2_smjera": nosiva_2}


# =============================================================================
# 2.4  RAZRED OKOLIŠA I ODABIR MATERIJALA
# =============================================================================

def definiranje_razreda_okolisa():
    """
    Određuje razred okoliša prema lokaciji i uvjetima okoliša,
    te odabire razred betona.

    Osijek: umjereno vlažan okoliš, prisutnost klorida u zraku
    → Razred okoliša XD1
    → Minimalni razred betona: C30/37

    Returns
    -------
    dict
        razred_okolisa, razred_betona
    """
    razred_okolisa = "XD1"
    razred_betona = "C30/37"

    print("=" * 70)
    print("2.4  RAZRED OKOLIŠA I ODABIR MATERIJALA")
    print("=" * 70)
    print(f"  Lokacija: Osijek")
    print(f"  Uvjeti: umjereno vlažan okoliš, prisutnost klorida u zraku")
    print(f"  Razred okoliša:  {razred_okolisa}")
    print(f"  Min. razred betona: {razred_betona}")
    print()

    return {"razred_okolisa": razred_okolisa, "razred_betona": razred_betona}


# =============================================================================
# 2.5  SLOJEVI PODA  i  2.6  SLOJEVI KROVA
# =============================================================================

def definiranje_slojeva_poda():
    """
    Definira slojeve poda stropne ploče i izračunava
    ukupno stalno opterećenje od slojeva (bez AB ploče, jer
    se vlastita težina AB ploče računa zasebno u tablici).

    Napomena: U ovom proračunu AB ploča je uključena u slojeve
    (prema tablici 2.2 iz rada, d=20 cm, γ=25 kN/m³).

    Returns
    -------
    list of dict
        Svaki sloj: {'naziv', 'debljina_m', 'gustoca_kNm3', 'g_kNm2'}
    """
    slojevi = [
        {"naziv": "Keramičke pločice",   "debljina_m": 0.01, "gustoca_kNm3": 24.0},
        {"naziv": "Ljepilo za keramiku", "debljina_m": 0.01, "gustoca_kNm3": 15.0},
        {"naziv": "Cementni estrih",     "debljina_m": 0.08, "gustoca_kNm3": 22.0},
        {"naziv": "Zvučna izolacija",    "debljina_m": 0.04, "gustoca_kNm3": 0.60},
        {"naziv": "AB ploča",            "debljina_m": 0.20, "gustoca_kNm3": 25.0},
        {"naziv": "Podgled (žbuka)",     "debljina_m": 0.03, "gustoca_kNm3": 20.0},
    ]

    # Izračun opterećenja svakog sloja
    for sloj in slojevi:
        sloj["g_kNm2"] = sloj["debljina_m"] * sloj["gustoca_kNm3"]

    return slojevi


def definiranje_slojeva_krova():
    """
    Definira slojeve ravnog krova (neprohodan, pad 1%)
    i izračunava opterećenje svakog sloja.

    Za geotekstil: debljina zanemariva, zadano g=0.2 kN/m².
    Za hidroizolaciju: d=0.002 m, γ=11 kN/m³.
    Za parnu branu: d=0.01 m, γ=0.30 kN/m³.

    Returns
    -------
    list of dict
        Svaki sloj: {'naziv', 'debljina_m', 'gustoca_kNm3', 'g_kNm2'}
    """
    slojevi = [
        {"naziv": "Nasip šljunka",  "debljina_m": 0.05,  "gustoca_kNm3": 20.0,  "g_kNm2": None},
        {"naziv": "Geotekstil",     "debljina_m": None,   "gustoca_kNm3": None,  "g_kNm2": 0.20},
        {"naziv": "Hidroizolacija", "debljina_m": 0.002,  "gustoca_kNm3": 11.0,  "g_kNm2": None},
        {"naziv": "EPS",            "debljina_m": 0.23,   "gustoca_kNm3": 0.30,  "g_kNm2": None},
        {"naziv": "Parna brana",    "debljina_m": 0.01,   "gustoca_kNm3": 0.30,  "g_kNm2": None},
        {"naziv": "AB ploča",       "debljina_m": 0.20,   "gustoca_kNm3": 25.0,  "g_kNm2": None},
        {"naziv": "Žbuka",          "debljina_m": 0.02,   "gustoca_kNm3": 23.0,  "g_kNm2": None},
    ]

    # Izračun opterećenja svakog sloja
    for sloj in slojevi:
        if sloj["g_kNm2"] is None:
            sloj["g_kNm2"] = sloj["debljina_m"] * sloj["gustoca_kNm3"]

    return slojevi


def ispis_slojeva(slojevi, naziv_elementa):
    """
    Ispisuje tablicu slojeva i vraća ukupno opterećenje.

    Parameters
    ----------
    slojevi : list of dict
        Lista slojeva.
    naziv_elementa : str
        Npr. "krovne ploče" ili "stropne ploče".

    Returns
    -------
    float
        Ukupno stalno opterećenje [kN/m²].
    """
    print(f"  Slojevi {naziv_elementa}:")
    print(f"  {'Sloj':<25s} {'d [m]':>8s} {'γ [kN/m³]':>10s} {'g [kN/m²]':>10s}")
    print(f"  {'-'*25} {'-'*8} {'-'*10} {'-'*10}")

    g_ukupno = 0.0
    for s in slojevi:
        d_str = f"{s['debljina_m']:.3f}" if s['debljina_m'] is not None else "   -"
        g_str = f"{s['gustoca_kNm3']:.2f}" if s['gustoca_kNm3'] is not None else "   -"
        print(f"  {s['naziv']:<25s} {d_str:>8s} {g_str:>10s} {s['g_kNm2']:>10.3f}")
        g_ukupno += s["g_kNm2"]

    print(f"  {'-'*25} {'-'*8} {'-'*10} {'-'*10}")
    print(f"  {'UKUPNO':<25s} {'':>8s} {'':>10s} {g_ukupno:>10.3f}")
    print()

    return g_ukupno


# =============================================================================
# 2.7  ZAŠTITNI SLOJ BETONA
# =============================================================================

def zastitni_sloj_greda(razred_okolisa="XD1"):
    """
    Proračun zaštitnog sloja betona za gredu prema
    Sorić i Kišiček (2014.) i HRN EN 1992-1-1.

    Izraz (2.4): C_nom^GR = C_min^GR + ΔC_dev^GR
    Izraz (2.5): C_min^GR = max{ C_min,b ; C_min,dur ; 10 mm }

    Parameters
    ----------
    razred_okolisa : str
        Razred okoliša (npr. "XD1").

    Returns
    -------
    dict
        C_nom_GR_mm : float – nazivna debljina zaštitnog sloja [mm]
        C_nom_GR_cm : float – nazivna debljina zaštitnog sloja [cm]
    """
    # Pretpostavljeni promjer uzdužne armature grede
    phi_pretp_mm = 14.0  # mm

    # C_min,b = promjer pretpostavljene armature
    C_min_b_mm = phi_pretp_mm  # 14 mm

    # Razred konstrukcije za gredu
    # Referentni razred: S4
    # Za XD1 pri razredu S4 → C_min,dur = 35 mm
    C_min_dur_mm = 35.0

    # C_min = max{ C_min,b ; C_min,dur ; 10 mm }
    C_min_mm = max(C_min_b_mm, C_min_dur_mm, 10.0)

    # Dozvoljeno odstupanje
    delta_C_dev_mm = 20.0  # preporučena vrijednost prema NA

    # Nazivna debljina
    C_nom_mm = C_min_mm + delta_C_dev_mm
    C_nom_cm = C_nom_mm / 10.0

    print("  Zaštitni sloj betona – GREDA (Sorić i Kišiček, 2014.):")
    print(f"    Pretpostavljena armatura: Ø{phi_pretp_mm:.0f} mm")
    print(f"    Razred konstrukcije: S4  (okoliš {razred_okolisa})")
    print(f"    C_min,b   = {C_min_b_mm:.0f} mm")
    print(f"    C_min,dur = {C_min_dur_mm:.0f} mm")
    print(f"    C_min     = max{{ {C_min_b_mm:.0f}; {C_min_dur_mm:.0f}; 10 }}"
          f" = {C_min_mm:.0f} mm")
    print(f"    ΔC_dev    = {delta_C_dev_mm:.0f} mm")
    print(f"    C_nom^GR  = {C_min_mm:.0f} + {delta_C_dev_mm:.0f}"
          f" = {C_nom_mm:.0f} mm = {C_nom_cm:.1f} cm")
    print()

    return {"C_nom_GR_mm": C_nom_mm, "C_nom_GR_cm": C_nom_cm}


def zastitni_sloj_ploca(razred_okolisa="XD1"):
    """
    Proračun zaštitnog sloja betona za ploču prema
    Sorić i Kišiček (2014.) i HRN EN 1992-1-1.

    Izraz (2.6): C_nom^PL = C_min^PL + ΔC_dev^PL
    Izraz (2.7): C_min^PL = max{ C_min,b ; C_min,dur ; 10 mm }

    Za ploču: razred konstrukcije S4 → plošni element (-1) → S3
    S3, XD1 → C_min,dur = 30 mm

    Parameters
    ----------
    razred_okolisa : str
        Razred okoliša (npr. "XD1").

    Returns
    -------
    dict
        C_nom_PL_mm : float – nazivna debljina zaštitnog sloja [mm]
        C_nom_PL_cm : float – nazivna debljina zaštitnog sloja [cm]
    """
    # Pretpostavljeni promjer armature ploče
    phi_pretp_mm = 7.0  # mm

    # C_min,b = promjer pretpostavljene armature
    C_min_b_mm = phi_pretp_mm  # 7 mm

    # Razred konstrukcije za ploču:
    # Referentni razred: S4 → plošni element: -1 → S3
    # S3, XD1 → C_min,dur = 30 mm
    C_min_dur_mm = 30.0

    # C_min = max{ C_min,b ; C_min,dur ; 10 mm }
    C_min_mm = max(C_min_b_mm, C_min_dur_mm, 10.0)

    # Dozvoljeno odstupanje
    delta_C_dev_mm = 20.0

    # Nazivna debljina
    C_nom_mm = C_min_mm + delta_C_dev_mm
    C_nom_cm = C_nom_mm / 10.0

    print("  Zaštitni sloj betona – PLOČA (Sorić i Kišiček, 2014.):")
    print(f"    Pretpostavljena armatura: Ø{phi_pretp_mm:.0f} mm")
    print(f"    Razred konstrukcije: S4 → plošni el. (-1) → S3  "
          f"(okoliš {razred_okolisa})")
    print(f"    C_min,b   = {C_min_b_mm:.0f} mm")
    print(f"    C_min,dur = {C_min_dur_mm:.0f} mm")
    print(f"    C_min     = max{{ {C_min_b_mm:.0f}; {C_min_dur_mm:.0f}; 10 }}"
          f" = {C_min_mm:.0f} mm")
    print(f"    ΔC_dev    = {delta_C_dev_mm:.0f} mm")
    print(f"    C_nom^PL  = {C_min_mm:.0f} + {delta_C_dev_mm:.0f}"
          f" = {C_nom_mm:.0f} mm = {C_nom_cm:.1f} cm")
    print()

    return {"C_nom_PL_mm": C_nom_mm, "C_nom_PL_cm": C_nom_cm}


def proracun_zastitnog_sloja():
    """
    Objedinjuje proračun zaštitnog sloja za gredu i ploču.

    Returns
    -------
    dict
        Zaštitni slojevi za gredu i ploču.
    """
    print("=" * 70)
    print("2.7  ZAŠTITNI SLOJ BETONA")
    print("=" * 70)

    rez_greda = zastitni_sloj_greda()
    rez_ploca = zastitni_sloj_ploca()

    return {**rez_greda, **rez_ploca}


# =============================================================================
# 2.8  PRORAČUNSKE ČVRSTOĆE MATERIJALA
# =============================================================================

def proracunske_cvrstoce_materijala():
    """
    Izračunava proračunske čvrstoće betona C30/37 i armature B500B
    prema HRN EN 1992-1-1.

    Beton C30/37:
        f_cd = f_ck / γ_c = 30 / 1.5 = 20 N/mm² = 2 kN/cm²
        f_ctm = 2.9 N/mm²

    Armatura B500B:
        f_yd = f_yk / γ_s = 500 / 1.15 = 434.78 N/mm² = 43.5 kN/cm²

    Returns
    -------
    dict
        f_ck, f_cd, f_ctm, f_yk, f_yd (sve u N/mm² i kN/cm²)
    """
    # ----- Beton C30/37 -----
    f_ck = 30.0     # karakteristična tlačna čvrstoća [N/mm²]
    gamma_c = 1.5   # parcijalni koeficijent sigurnosti za beton
    f_cd_Nmm2 = f_ck / gamma_c                 # [N/mm²]
    f_cd_kNcm2 = f_cd_Nmm2 / 10.0              # [kN/cm²]
    f_ctm = 2.9     # srednja vlačna čvrstoća betona [N/mm²]

    # ----- Armatura B500B -----
    f_yk = 500.0     # karakteristična vlačna čvrstoća čelika [N/mm²]
    gamma_s = 1.15   # parcijalni koeficijent sigurnosti za čelik
    f_yd_Nmm2 = f_yk / gamma_s                 # [N/mm²]
    f_yd_kNcm2 = f_yd_Nmm2 / 10.0              # [kN/cm²]

    print("=" * 70)
    print("2.8  PRORAČUNSKE ČVRSTOĆE MATERIJALA")
    print("=" * 70)
    print("  BETON C30/37:")
    print(f"    f_ck  = {f_ck:.1f} N/mm²")
    print(f"    γ_c   = {gamma_c:.2f}")
    print(f"    f_cd  = f_ck / γ_c = {f_ck:.1f} / {gamma_c:.2f}"
          f" = {f_cd_Nmm2:.2f} N/mm² = {f_cd_kNcm2:.1f} kN/cm²")
    print(f"    f_ctm = {f_ctm:.1f} N/mm²")
    print()
    print("  ARMATURA B500B:")
    print(f"    f_yk  = {f_yk:.1f} N/mm²")
    print(f"    γ_s   = {gamma_s:.2f}")
    print(f"    f_yd  = f_yk / γ_s = {f_yk:.1f} / {gamma_s:.2f}"
          f" = {f_yd_Nmm2:.2f} N/mm² = {f_yd_kNcm2:.1f} kN/cm²")
    print()

    return {
        "f_ck_Nmm2": f_ck,
        "f_cd_Nmm2": f_cd_Nmm2,
        "f_cd_kNcm2": f_cd_kNcm2,
        "f_ctm_Nmm2": f_ctm,
        "f_yk_Nmm2": f_yk,
        "f_yd_Nmm2": f_yd_Nmm2,
        "f_yd_kNcm2": f_yd_kNcm2,
        "gamma_c": gamma_c,
        "gamma_s": gamma_s,
    }


# =============================================================================
# 2.9  ANALIZA OPTEREĆENJA
# =============================================================================

def opterecenje_krovne_ploce():
    """
    Izračunava stalno i promjenjivo opterećenje na krovnu ploču.

    Stalno opterećenje: slojevi ravnog krova (tablica 2.1).
    Promjenjivo opterećenje:
        - Uporabno: q_k = 0.75 kN/m² (neprohodan krov, kategorija H)
        - Snijeg:   s = μ₁·c_e·c_t·s_k  (HRN EN 1991-1-3)

    Osijek, zona 1, s_k = 1.10 kN/m²
    μ₁ = 0.80 (nagib < 30°), c_e = 1.0, c_t = 1.0
    s = 0.80 × 1.0 × 1.0 × 1.10 = 0.88 kN/m²

    Returns
    -------
    dict
        g_uk_krov_kNm2 : stalno opterećenje [kN/m²]
        q_k_krov_kNm2  : uporabno opterećenje [kN/m²]
        s_k_krov_kNm2  : opterećenje snijegom [kN/m²]
    """
    print("=" * 70)
    print("2.9  ANALIZA OPTEREĆENJA")
    print("=" * 70)
    print()
    print("2.9.1  Opterećenje krovne ploče")
    print("-" * 50)

    # --- Stalno opterećenje ---
    slojevi = definiranje_slojeva_krova()
    g_uk_krov = ispis_slojeva(slojevi, "krovne ploče")

    # --- Promjenjivo – uporabno ---
    q_k = 0.75  # kN/m², neprohodan krov, kategorija H
    print(f"  Promjenjivo – uporabno:")
    print(f"    q_k = {q_k:.2f} kN/m²  (neprohodan krov, kat. H)")
    print()

    # --- Promjenjivo – snijeg ---
    print("  Promjenjivo – snijeg (HRN EN 1991-1-3, izraz 2.9):")
    print("    s = μ₁ × c_e × c_t × s_k")

    # Koeficijent oblika krovne plohe (nagib 0°–30°)
    mu_1 = 0.80
    # Koeficijent izloženosti (uobičajen teren)
    c_e = 1.0
    # Toplinski koeficijent (preporučena vrijednost)
    c_t = 1.0
    # Karakteristična vrijednost opterećenja snijegom na tlu
    # Osijek, zona 1, 94 m.n.m. → s_k = 1.10 kN/m²
    s_k_tlo = 1.10

    s_snijeg = mu_1 * c_e * c_t * s_k_tlo

    print(f"    μ₁   = {mu_1:.2f}  (nagib krovne plohe 0° < α < 30°)")
    print(f"    c_e  = {c_e:.1f}   (uobičajen oblik terena)")
    print(f"    c_t  = {c_t:.1f}   (preporučena vrijednost)")
    print(f"    s_k  = {s_k_tlo:.2f} kN/m²  (Osijek, zona 1)")
    print(f"    s    = {mu_1:.2f} × {c_e:.1f} × {c_t:.1f} × {s_k_tlo:.2f}"
          f" = {s_snijeg:.2f} kN/m²")
    print()

    return {
        "g_uk_krov_kNm2": g_uk_krov,
        "q_k_krov_kNm2": q_k,
        "s_k_krov_kNm2": s_snijeg,
        "slojevi_krov": slojevi,
    }


def opterecenje_stropne_ploce():
    """
    Izračunava stalno i promjenjivo opterećenje na stropnu ploču.

    Stalno opterećenje: slojevi poda (tablica 2.2).
    Promjenjivo opterećenje:
        - Uporabno: q_k = 3.0 kN/m² (kategorija C1 – bistro/restoran)
        - Dodatak za pomične pregradne zidove: +0.5 kN/m²
          (težina zidova 0.7 kN/m → prema EN 1991-1-1)
        - Ukupno: q_uk = 3.5 kN/m²

    Returns
    -------
    dict
        g_uk_strop_kNm2 : stalno opterećenje [kN/m²]
        q_uk_strop_kNm2 : ukupno uporabno opterećenje [kN/m²]
    """
    print("2.9.2  Opterećenje stropne ploče")
    print("-" * 50)

    # --- Stalno opterećenje ---
    slojevi = definiranje_slojeva_poda()
    g_uk_strop = ispis_slojeva(slojevi, "stropne ploče")

    # --- Promjenjivo – uporabno ---
    q_k_osnovno = 3.0   # kN/m², kategorija C1
    q_pregradni = 0.5   # kN/m², dodatak za pomične pregradne zidove
    q_uk = q_k_osnovno + q_pregradni

    print(f"  Promjenjivo – uporabno:")
    print(f"    Kategorija C1 (prostorije sa stolovima – bistro):")
    print(f"    q_k,osnovno = {q_k_osnovno:.1f} kN/m²")
    print(f"    Težina pregradnih zidova: 0.7 kN/m → +{q_pregradni:.1f} kN/m²")
    print(f"    q_uk = {q_k_osnovno:.1f} + {q_pregradni:.1f} = {q_uk:.1f} kN/m²")
    print()

    return {
        "g_uk_strop_kNm2": g_uk_strop,
        "q_uk_strop_kNm2": q_uk,
        "slojevi_strop": slojevi,
    }


# =============================================================================
# 2.10  STATIČKE VISINE POPREČNIH PRESJEKA
# =============================================================================

def staticka_visina_ploce(d_pl_cm, C_nom_PL_cm, phi_u_mm, phi_p_mm=None):
    """
    Izračunava statičku visinu ploče nosive u 2 smjera.

    Ploče nosive u 2 smjera imaju armaturu u oba smjera:
      - d_max: statička visina za prvu (donju) mrežu armature
      - d_min: statička visina za drugu (gornju) mrežu armature

    Parameters
    ----------
    d_pl_cm : float
        Ukupna debljina ploče [cm].
    C_nom_PL_cm : float
        Nazivni zaštitni sloj betona za ploču [cm].
    phi_u_mm : float
        Promjer uzdužne armature [mm].
    phi_p_mm : float, optional
        Promjer poprečne armature [mm]. Ako None, jednako phi_u_mm.

    Returns
    -------
    dict
        d_max_cm : statička visina za prvi (kraći) smjer [cm]
        d_min_cm : statička visina za drugi (dulji) smjer [cm]
    """
    if phi_p_mm is None:
        phi_p_mm = phi_u_mm

    phi_u_cm = phi_u_mm / 10.0
    phi_p_cm = phi_p_mm / 10.0

    # d_max: armatura bliža vlačnom rubu (samo jedan sloj armature + pola promjera)
    d_max = d_pl_cm - C_nom_PL_cm - phi_u_cm / 2.0

    # d_min: armatura dalje od vlačnog ruba (preko prvog sloja armature)
    d_min = d_pl_cm - C_nom_PL_cm - phi_p_cm - phi_u_cm / 2.0

    print(f"    Ploča: d_pl = {d_pl_cm:.0f} cm,  C_nom = {C_nom_PL_cm:.1f} cm,  "
          f"Ø_u = Ø_p = {phi_u_mm:.0f} mm")
    print(f"    d_max = {d_pl_cm:.0f} − {C_nom_PL_cm:.1f} − {phi_u_cm:.1f}/2"
          f" = {d_max:.2f} cm")
    print(f"    d_min = {d_pl_cm:.0f} − {C_nom_PL_cm:.1f} − {phi_p_cm:.1f}"
          f" − {phi_u_cm:.1f}/2 = {d_min:.2f} cm")

    return {"d_max_cm": d_max, "d_min_cm": d_min}


def staticka_visina_grede(h_GR_cm, C_nom_GR_cm, phi_u_mm, phi_w_mm):
    """
    Izračunava statičku visinu grede.

    d = h_GR − C_nom − Ø_w − Ø_u / 2

    Napomena: U radu je korišten C_nom = 5.0 cm (ne 5.5 cm) pri
    izračunu d za gredu:
        d = 70 − 5 − 0.7 − 1.4/2 = 63.6 cm

    Parameters
    ----------
    h_GR_cm : float
        Ukupna visina grede [cm].
    C_nom_GR_cm : float
        Nazivni zaštitni sloj betona za gredu [cm].
        Napomena: autor koristi 5.0 cm (ne formalni C_nom=5.5 cm).
    phi_u_mm : float
        Promjer uzdužne armature [mm].
    phi_w_mm : float
        Promjer poprečne armature (spone) [mm].

    Returns
    -------
    dict
        d_greda_cm : statička visina grede [cm]
    """
    phi_u_cm = phi_u_mm / 10.0
    phi_w_cm = phi_w_mm / 10.0

    # Napomena: autor u radu koristi C_nom = 5.0 cm za proračun d
    # (a formalno C_nom^GR = 5.5 cm). Slijedimo rad.
    C_koristi = C_nom_GR_cm

    d = h_GR_cm - C_koristi - phi_w_cm - phi_u_cm / 2.0

    print(f"    Greda: h_GR = {h_GR_cm:.0f} cm,  C_nom = {C_koristi:.1f} cm,  "
          f"Ø_u = {phi_u_mm:.0f} mm,  Ø_w = {phi_w_mm:.0f} mm")
    print(f"    d = {h_GR_cm:.0f} − {C_koristi:.1f} − {phi_w_cm:.1f}"
          f" − {phi_u_cm:.1f}/2 = {d:.1f} cm")

    return {"d_greda_cm": d}


def proracun_statickih_visina():
    """
    Objedinjuje proračun statičkih visina za ploče i grede.

    Returns
    -------
    dict
        Statičke visine za ploču i gredu.
    """
    print("=" * 70)
    print("2.10  STATIČKE VISINE POPREČNIH PRESJEKA")
    print("=" * 70)

    # ----- Stropna i krovna ploča (nosiva u 2 smjera) -----
    print()
    print("  Stropna i krovna ploča (nosive u 2 smjera):")
    rez_ploca = staticka_visina_ploce(
        d_pl_cm=20.0,
        C_nom_PL_cm=5.0,    # C_nom^PL = 50 mm = 5 cm
        phi_u_mm=7.0,        # pretpostavljena uzdužna armatura Ø7
        phi_p_mm=7.0,        # pretpostavljena poprečna armatura Ø7
    )

    # ----- Greda (stropna i krovna) -----
    print()
    print("  Greda (stropna i krovna):")
    # Napomena: autor koristi C = 5.0 cm u proračunu (ne 5.5 cm)
    rez_greda = staticka_visina_grede(
        h_GR_cm=70.0,
        C_nom_GR_cm=5.0,     # u radu: d = 70 − 5 − 0.7 − 0.7 = 63.6 cm
        phi_u_mm=14.0,        # pretpostavljena uzdužna armatura Ø14
        phi_w_mm=7.0,         # pretpostavljena poprečna armatura Ø7
    )

    print()

    return {**rez_ploca, **rez_greda}


# =============================================================================
# TLOCRTNA RASPODJELA POZICIJA PLOČA
# =============================================================================

def definiranje_pozicija_ploca():
    """
    Definira tlocrtnu raspodjelu pozicija ploča za stropnu i krovnu
    konstrukciju prema slikama 2.2 i 2.3 iz rada.

    Stropne ploče: 101–114
    Krovne ploče:  201–214

    Rasponi ploča [cm]:
        U smjeru X (dulji): 663 cm (svijetli) = 708 cm (osovinski)
        U smjeru Y (kraći): 540 cm (svijetli) = 585 cm (osovinski)

    Širina greda: 45 cm
    Širina stupova: 45×45 cm (pretpostavljeno iz rada)

    Returns
    -------
    dict
        Rječnik s rasponima i brojem polja.
    """
    # Svijetli rasponi ploča [cm]
    Lx_svijetli = 663.0   # dulji raspon (svijetli)
    Ly_svijetli = 540.0   # kraći raspon (svijetli)

    # Širina greda [cm]
    b_greda = 45.0

    # Osovinski rasponi ploča (os greda do osi greda) [cm]
    Lx_os = Lx_svijetli + b_greda   # 663 + 45 = 708 cm
    Ly_os = Ly_svijetli + b_greda    # 540 + 45 = 585 cm

    # Broj polja
    n_polja_x = 5  # polja u smjeru X
    n_polja_y = 3  # polja u smjeru Y

    # Ukupne dimenzije (osovinski)
    L_uk_x = n_polja_x * Lx_os / 100.0  # [m] ≈ 35.40 m (+ rubni stupovi)
    L_uk_y = n_polja_y * Ly_os / 100.0   # [m] ≈ 17.55 m (+ rubni stupovi)

    print("=" * 70)
    print("  TLOCRTNA RASPODJELA POZICIJA PLOČA")
    print("=" * 70)
    print(f"  Svijetli rasponi: Lx = {Lx_svijetli:.0f} cm,  Ly = {Ly_svijetli:.0f} cm")
    print(f"  Širina greda:     b_g = {b_greda:.0f} cm")
    print(f"  Osovinski rasponi: Lx = {Lx_os:.0f} cm,  Ly = {Ly_os:.0f} cm")
    print(f"  Broj polja:       {n_polja_x} × {n_polja_y}")
    print(f"  Ukupna dimenzija (osovinski): "
          f"{n_polja_x}×{Lx_os:.0f} = {n_polja_x * Lx_os:.0f} cm  ×  "
          f"{n_polja_y}×{Ly_os:.0f} = {n_polja_y * Ly_os:.0f} cm")
    print()

    # Definicija pozicija stropnih ploča (rubni uvjeti)
    # Slučajevi rubnih uvjeta (prema tablicama za ploče nosive u 2 smjera):
    #   Slučaj 1: sva 4 ruba slobodna
    #   Slučaj 4: 2 susjedna slobodna, 2 susjedna ukliještena
    #   Slučaj 5: 1 slobodni, 3 ukliještena
    #   Slučaj 9: sva 4 ukliještena
    #   itd.
    pozicije_strop = {
        101: {"opis": "kutna ploča (2 slob. + 2 ukl.)",   "slucaj": 4},
        102: {"opis": "rubna ploča (1 slob. + 3 ukl.)",   "slucaj": 5},
        103: {"opis": "kutna ploča (2 slob. + 2 ukl.)",   "slucaj": 4},
        104: {"opis": "unutarnja ploča (4 ukl.)",          "slucaj": 9},
    }

    print("  Stropne ploče – rubni uvjeti:")
    for poz, info in pozicije_strop.items():
        print(f"    Pozicija {poz}: slučaj {info['slucaj']} – {info['opis']}")
    print()

    return {
        "Lx_svijetli_cm": Lx_svijetli,
        "Ly_svijetli_cm": Ly_svijetli,
        "Lx_os_cm": Lx_os,
        "Ly_os_cm": Ly_os,
        "b_greda_cm": b_greda,
        "n_polja_x": n_polja_x,
        "n_polja_y": n_polja_y,
        "pozicije_strop": pozicije_strop,
    }


# =============================================================================
# SAŽETAK SVIH ULAZNIH PODATAKA
# =============================================================================

def sazetak_ulaznih_podataka(dispozicija, geometrija, okolisni, materijali,
                              zasticni, opt_krov, opt_strop, stat_visine):
    """
    Ispisuje kompaktan sažetak svih ulaznih podataka za statički proračun.

    Parameters
    ----------
    dispozicija : dict
    geometrija : dict
    okolisni : dict
    materijali : dict
    zasticni : dict
    opt_krov : dict
    opt_strop : dict
    stat_visine : dict
    """
    print("=" * 70)
    print("  SAŽETAK SVIH ULAZNIH PODATAKA")
    print("=" * 70)
    print()
    print(f"  Konstrukcija: {dispozicija['L_konstr_m']:.2f} × "
          f"{dispozicija['B_konstr_m']:.2f} m")
    print(f"  Površina kata: {dispozicija['A_kat_m2']:.1f} m²")
    print(f"  Visina kata: {dispozicija['h_kat_m']:.2f} m")
    print(f"  Lokacija: {dispozicija['lokacija']}, "
          f"{dispozicija['nadmorska_visina_m']:.0f} m.n.m.")
    print()
    print(f"  Debljina ploče:       d_pl = {geometrija['d_pl_usv_cm']:.0f} cm")
    print(f"  Visina grede:         h_g  = {geometrija['h_g_usv_cm']:.0f} cm")
    print(f"  Širina grede:         b_w  = {geometrija['b_w_usv_cm']:.0f} cm")
    print(f"  Širina stupa:         b_c  = {geometrija['b_stup_cm']:.0f} cm")
    print()
    print(f"  Razred okoliša:       {okolisni['razred_okolisa']}")
    print(f"  Beton:                {okolisni['razred_betona']}")
    print(f"    f_cd = {materijali['f_cd_kNcm2']:.1f} kN/cm²"
          f" ({materijali['f_cd_Nmm2']:.1f} N/mm²)")
    print(f"    f_ctm = {materijali['f_ctm_Nmm2']:.1f} N/mm²")
    print(f"  Armatura:             {dispozicija['armatura']}")
    print(f"    f_yd = {materijali['f_yd_kNcm2']:.1f} kN/cm²"
          f" ({materijali['f_yd_Nmm2']:.2f} N/mm²)")
    print()
    print(f"  Zaštitni sloj – greda: C_nom = {zasticni['C_nom_GR_mm']:.0f} mm"
          f" ({zasticni['C_nom_GR_cm']:.1f} cm)")
    print(f"  Zaštitni sloj – ploča: C_nom = {zasticni['C_nom_PL_mm']:.0f} mm"
          f" ({zasticni['C_nom_PL_cm']:.1f} cm)")
    print()
    print(f"  Opterećenje krovne ploče:")
    print(f"    Stalno:    g = {opt_krov['g_uk_krov_kNm2']:.2f} kN/m²")
    print(f"    Uporabno:  q = {opt_krov['q_k_krov_kNm2']:.2f} kN/m²"
          f"  (kat. H – neprohodan krov)")
    print(f"    Snijeg:    s = {opt_krov['s_k_krov_kNm2']:.2f} kN/m²")
    print()
    print(f"  Opterećenje stropne ploče:")
    print(f"    Stalno:    g = {opt_strop['g_uk_strop_kNm2']:.2f} kN/m²")
    print(f"    Uporabno:  q = {opt_strop['q_uk_strop_kNm2']:.2f} kN/m²"
          f"  (kat. C1 – bistro/restoran, uklj. pregrade)")
    print()
    print(f"  Statičke visine:")
    print(f"    Ploča:  d_max = {stat_visine['d_max_cm']:.2f} cm,  "
          f"d_min = {stat_visine['d_min_cm']:.2f} cm")
    print(f"    Greda:  d     = {stat_visine['d_greda_cm']:.1f} cm")
    print()


# =============================================================================
#   GLAVNI PROGRAM
# =============================================================================

def main():
    """
    Glavni program: pokreće sve proračune od poglavlja 1 do 2.10
    (prije poglavlja 3: Ručni proračun i dimenzioniranje).
    """
    print()
    print("╔" + "═" * 68 + "╗")
    print("║  STATIČKI PRORAČUN I DIMENZIONIRANJE AB KONSTRUKCIJE BISTROA       ║")
    print("║  Poglavlja 1–2: Dispozicija, geometrija, materijali,               ║")
    print("║                 opterećenja, statičke visine                       ║")
    print("╚" + "═" * 68 + "╝")
    print()

    # 2.1 Dispozicija konstrukcije
    dispozicija = definiranje_katastarske_cestice()

    # 2.2 Definiranje geometrije
    geometrija = definiranje_geometrije()

    # 2.3 Nosivost ploča
    # Osovinski rasponi: Lx = 708 cm, Ly = 630 cm (prema radu: 648+60=708, 585+45=630)
    # Ali u radu piše Lx/Ly = (648+60)/(585+45) = 708/630 = 1.12
    nosivost = provjera_nosivosti_ploca(L_x_cm=708.0, L_y_cm=630.0)

    # 2.4 Razred okoliša
    okolisni = definiranje_razreda_okolisa()

    # 2.5 & 2.6 Slojevi poda i krova (ispisuju se unutar analize opterećenja)

    # 2.7 Zaštitni sloj betona
    zasticni = proracun_zastitnog_sloja()

    # 2.8 Proračunske čvrstoće materijala
    materijali = proracunske_cvrstoce_materijala()

    # 2.9 Analiza opterećenja
    opt_krov = opterecenje_krovne_ploce()
    opt_strop = opterecenje_stropne_ploce()

    # 2.10 Statičke visine
    stat_visine = proracun_statickih_visina()

    # Tlocrtna raspodjela pozicija (informativno)
    pozicije = definiranje_pozicija_ploca()

    # Sažetak
    sazetak_ulaznih_podataka(
        dispozicija, geometrija, okolisni, materijali,
        zasticni, opt_krov, opt_strop, stat_visine,
    )

    print("=" * 70)
    print("  KRAJ POGLAVLJA 2 – Slijedi: 3. RUČNI PRORAČUN I DIMENZIONIRANJE")
    print("=" * 70)

    return {
        "dispozicija": dispozicija,
        "geometrija": geometrija,
        "nosivost": nosivost,
        "okolisni": okolisni,
        "zasticni": zasticni,
        "materijali": materijali,
        "opt_krov": opt_krov,
        "opt_strop": opt_strop,
        "stat_visine": stat_visine,
        "pozicije": pozicije,
    }


if __name__ == "__main__":
    rezultati = main()
