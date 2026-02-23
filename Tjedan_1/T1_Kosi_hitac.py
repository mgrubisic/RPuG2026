# =============================================================================
# KOSI HITAC U PYTHONU - Postupno proširivanje koda
# Predmet: Računalno programiranje u građevinskom inženjerstvu
# =============================================================================
#
# Ovaj skript prikazuje kako od jednostavnih jednadžbi u Pythonu možemo
# postupno graditi sve složeniji kod:
#
#   FAZA 1 – Osnovna fizika (jednadžbe, jedan slučaj, ispis u konzoli)
#   FAZA 2 – Crtanje putanje za jedan kut
#   FAZA 3 – Više kutova pomoću petlje, sve putanje na istom grafu
#
# =============================================================================

# -----------------------------------------------------------------------------
# POTREBNE BIBLIOTEKE
# -----------------------------------------------------------------------------

import numpy as np          # NumPy: matematika, vektori, trigonometrija
import matplotlib.pyplot as plt  # Matplotlib: crtanje grafova


# =============================================================================
# FAZA 1 – OSNOVNA FIZIKA: Jednadžbe kosog hitca
# =============================================================================
#
# Fizikalni model:
#   x(t) = v0 * cos(θ) * t
#   y(t) = v0 * sin(θ) * t - (1/2) * g * t²
#
# Izvedene veličine:
#   Dolet (maksimalna vodoravna udaljenost): R = v0² * sin(2θ) / g
#   Maksimalna visina:                       H = v0² * sin²(θ) / (2g)
#   Ukupno vrijeme leta:                     T = 2 * v0 * sin(θ) / g
#
# =============================================================================

print("=" * 60)
print("FAZA 1 – Jednadžbe kosog hitca (jedan slučaj)")
print("=" * 60)

# --- Ulazni parametri ---
v0    = 50.0   # početna brzina [m/s]
kut   = 45.0   # kut izbačaja [°]
g     = 9.81   # ubrzanje slobodnog pada [m/s²]

# --- Pretvorba kuta iz stupnjeva u radijane ---
# Python trigonometrijske funkcije primaju radijane, ne stupnjeve!
theta = np.radians(kut)   # θ [rad]

# --- Izračun izvedenih veličina ---
T = 2 * v0 * np.sin(theta) / g          # ukupno vrijeme leta [s]
R = v0**2 * np.sin(2 * theta) / g       # dolet [m]
H = v0**2 * np.sin(theta)**2 / (2 * g) # maksimalna visina [m]

# --- Ispis rezultata ---
print(f"\nUlazni podaci:")
print(f"  Početna brzina : v0  = {v0} m/s")
print(f"  Kut izbačaja   : θ   = {kut}°")

print(f"\nIzlazni rezultati:")
print(f"  Vrijeme leta   : T   = {T:.2f} s")
print(f"  Dolet          : R   = {R:.2f} m")
print(f"  Maks. visina   : H   = {H:.2f} m")


# %% Faza 2
# =============================================================================
# FAZA 2 – CRTANJE PUTANJE za jedan kut
# =============================================================================
#
# Sada iste jednadžbe koristimo za izračun (x, y) u svakom trenutku t,
# te rezultat prikazujemo na grafu.
#
# =============================================================================

print("\n" + "=" * 60)
print("FAZA 2 – Crtanje putanje (jedan kut)")
print("=" * 60)

# --- Isti ulazni parametri kao u Fazi 1 ---
v0  = 50.0   # početna brzina [m/s]
kut = 45.0   # kut izbačaja [°]
g   = 9.81   # ubrzanje slobodnog pada [m/s²]

# Pretvorba kuta u radijane
theta = np.radians(kut)

# --- Vektor vremena od 0 do T ---
# np.linspace(start, stop, broj_točaka) – generira ravnomjerno raspoređene točke
T = 2 * v0 * np.sin(theta) / g   # ukupno vrijeme leta [s]
t = np.linspace(0, T, 300)        # 300 točaka od t=0 do t=T

# --- Izračun x i y koordinate u svakom trenutku t ---
# Numpy automatski primjenjuje formulu na svaki element vektora t (vektorizacija)
x = v0 * np.cos(theta) * t                   # vodoravna koordinata [m]
y = v0 * np.sin(theta) * t - 0.5 * g * t**2  # vertikalna koordinata [m]

# --- Crtanje grafa ---
fig, ax = plt.subplots(figsize=(9, 5))  # stvaramo novu figuru i osi

ax.plot(x, y, color='steelblue', linewidth=2.5,
        label=f'θ = {kut}°')          # crtamo putanju

# Oznaka maksimalne visine (najniži indeks najbliži maksimumu y)
idx_max = np.argmax(y)                 # indeks elementa s najvećom y vrijednošću
ax.annotate(f'H = {y[idx_max]:.1f} m',
            xy=(x[idx_max], y[idx_max]),         # točka na grafu
            xytext=(x[idx_max] + 20, y[idx_max] - 10), # pozicija teksta
            arrowprops=dict(arrowstyle='->', color='gray'),
            fontsize=10)

# Estetika grafa
ax.set_xlabel('Vodoravna udaljenost  x [m]', fontsize=12)
ax.set_ylabel('Visina  y [m]', fontsize=12)
ax.set_title(f'Putanja kosog hitca  (v₀ = {v0} m/s, θ = {kut}°)', fontsize=13)
ax.legend(fontsize=11)
ax.grid(True, linestyle='--', alpha=0.6)  # mreža za lakše čitanje
ax.set_ylim(bottom=0)                      # y-os počinje od 0 (tlo)

plt.tight_layout()                 # automatsko podešavanje margina
plt.savefig('faza2_jedan_kut.png', dpi=150)
plt.show()
print("Graf spremljen: faza2_jedan_kut.png")


# %% Faza 3
# =============================================================================
# FAZA 3 – VIŠE KUTOVA POMOĆU PETLJE
# =============================================================================
#
# Sada isti kod "omotamo" u for petlju i ponavljamo izračun za više kutova.
# Svaki prolaz petlje = jedan kut = jedan graf na istoj slici.
#
# Novi koncepti koje studenti vide:
#   - lista (list) za pohranu kutova
#   - for petlja za ponavljanje bloka koda
#   - automatsko upravljanje bojama (plt.cm colormap)
#   - pohrana doleta R za svaki kut → drugi graf (dolet vs kut)
#
# =============================================================================

print("\n" + "=" * 60)
print("FAZA 3 – Više kutova pomoću petlje")
print("=" * 60)

# --- Ulazni parametri ---
v0 = 50.0    # početna brzina [m/s] – ostaje ista za sve kutove
g  = 9.81    # ubrzanje slobodnog pada [m/s²]

# Lista kutova koje želimo analizirati [°]
# Ovaj jedan redak zamjenjuje višekratno kopiranje koda!
kutovi = [15, 30, 45, 60, 75]

# Prazne liste za pohranu rezultata svake iteracije petlje
doleti  = []   # dolet R za svaki kut
visine  = []   # maksimalna visina H za svaki kut

# --- Boje za svaku putanju (automatski iz colormap palete) ---
boje = plt.cm.tab10.colors  # 10 unaprijed definiranih boja

# --- Priprema grafa ---
fig, axes = plt.subplots(1, 2, figsize=(14, 5))  # 2 grafa jedan pored drugog
ax1 = axes[0]   # lijevi graf  – putanje
ax2 = axes[1]   # desni graf  – dolet vs kut

# =============================================================================
# PETLJA – prolazimo kroz svaki kut u listi
# =============================================================================
for i, kut in enumerate(kutovi):
    # enumerate() daje i = redni broj (0,1,2,...) i kut = vrijednost kuta

    # Pretvorba kuta u radijane
    theta = np.radians(kut)

    # Izračun vremena leta i vektora vremena
    T = 2 * v0 * np.sin(theta) / g
    t = np.linspace(0, T, 300)

    # Izračun koordinata putanje
    x = v0 * np.cos(theta) * t
    y = v0 * np.sin(theta) * t - 0.5 * g * t**2

    # Izvedene veličine (dolet i maksimalna visina)
    R = v0**2 * np.sin(2 * theta) / g
    H = v0**2 * np.sin(theta)**2 / (2 * g)

    # Pohrana u liste (koristit ćemo ih za drugi graf)
    doleti.append(R)    # dodajemo R na kraj liste doleti
    visine.append(H)    # dodajemo H na kraj liste visine

    # Ispis rezultata u konzoli za svaki kut
    print(f"  θ = {kut:2d}°  →  T = {T:.2f} s,  R = {R:.1f} m,  H = {H:.1f} m")

    # Crtanje putanje na lijevom grafu (ax1)
    ax1.plot(x, y,
             color=boje[i],          # svaki kut ima svoju boju
             linewidth=2.2,
             label=f'θ = {kut}°')   # legenda automatski preuzima label

# =============================================================================
# KRAJ PETLJE – sve putanje su nacrtane
# =============================================================================

# --- Estetika lijevog grafa (putanje) ---
ax1.set_xlabel('Vodoravna udaljenost  x [m]', fontsize=12)
ax1.set_ylabel('Visina  y [m]', fontsize=12)
ax1.set_title(f'Putanje kosog hitca  (v₀ = {v0} m/s)', fontsize=13)
ax1.legend(fontsize=10, loc='upper right')
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.set_ylim(bottom=0)

# --- Desni graf: Dolet R u ovisnosti o kutu θ ---
# Koristimo listu kutovi (x-os) i listu doleti (y-os) koje smo punili u petlji
ax2.bar(kutovi, doleti,                    # stupčasti dijagram
        color=boje[:len(kutovi)],          # iste boje kao putanje
        width=8, edgecolor='black', linewidth=0.8)

# Ispis vrijednosti iznad svakog stupca
for kut, R in zip(kutovi, doleti):
    ax2.text(kut, R + 5, f'{R:.0f} m',    # tekst iznad stupca
             ha='center', va='bottom', fontsize=9, fontweight='bold')

ax2.set_xlabel('Kut izbačaja  θ [°]', fontsize=12)
ax2.set_ylabel('Dolet  R [m]', fontsize=12)
ax2.set_title('Dolet u ovisnosti o kutu izbačaja', fontsize=13)
ax2.set_xticks(kutovi)                     # oznake na x-osi samo za naše kutove
ax2.grid(True, axis='y', linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig('faza3_vise_kutova.png', dpi=150)
plt.show()
print("\nGraf spremljen: faza3_vise_kutova.png")

# %% Faza 4
# =============================================================================
# BONUS FAZA – Parametarska studija: promjena v0, fiksni kut
# =============================================================================
#
# Sada mijenjamo početnu brzinu v0 dok kut ostaje konstantan.
# Ovim primjerom pokazujemo da je promjena ulaznih parametara trivijalna
# – mijenjamo samo jednu listu, a ostatak koda ostaje identičan.
#
# =============================================================================

print("\n" + "=" * 60)
print("BONUS – Parametarska studija: dolet vs. početna brzina")
print("=" * 60)

kut      = 45.0                        # fiksni kut [°]
theta    = np.radians(kut)
brzine   = [20, 30, 40, 50, 60, 70]   # lista početnih brzina [m/s]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
ax1 = axes[0]
ax2 = axes[1]

doleti_v0 = []   # pohrana doleta za svaku brzinu

for i, v0 in enumerate(brzine):
    T = 2 * v0 * np.sin(theta) / g
    t = np.linspace(0, T, 300)
    x = v0 * np.cos(theta) * t
    y = v0 * np.sin(theta) * t - 0.5 * g * t**2
    R = v0**2 * np.sin(2 * theta) / g

    doleti_v0.append(R)
    print(f"  v0 = {v0:2d} m/s  →  R = {R:.1f} m")

    ax1.plot(x, y, color=boje[i], linewidth=2.2, label=f'v₀ = {v0} m/s')

ax1.set_xlabel('Vodoravna udaljenost  x [m]', fontsize=12)
ax1.set_ylabel('Visina  y [m]', fontsize=12)
ax1.set_title(f'Putanje kosog hitca  (θ = {kut}°)', fontsize=13)
ax1.legend(fontsize=10)
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.set_ylim(bottom=0)

# Dolet vs. v0 – linijski dijagram (kvadratna ovisnost R ∝ v0²)
ax2.plot(brzine, doleti_v0, 'o-', color='steelblue',
         linewidth=2.5, markersize=8, markerfacecolor='white',
         markeredgewidth=2)
ax2.set_xlabel('Početna brzina  v₀ [m/s]', fontsize=12)
ax2.set_ylabel('Dolet  R [m]', fontsize=12)
ax2.set_title(f'Dolet u ovisnosti o početnoj brzini  (θ = {kut}°)', fontsize=13)
ax2.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig('bonus_parametarska_studija.png', dpi=150)
plt.show()
print("\nGraf spremljen: bonus_parametarska_studija.png")

print("\n" + "=" * 60)
print("Svi primjeri završeni!")
print("=" * 60)