# =============================================================================
# Računalno programiranje u građevinarstvu (254810)
# Domaća zadaća #1 — Karakteristike kružnog presjeka
# =============================================================================
# Opis   : Program računa geometrijske karakteristike kružnog poprečnog
#          presjeka (površinu, opseg, moment tromosti i moment otpora)
#          za zadani promjer D.
# =============================================================================

import math  # učitavanje standardnog matematičkog modula (sadrži math.pi)

# -----------------------------------------------------------------------------
# 1. ULAZNI PODATAK
# -----------------------------------------------------------------------------

D = 0.40  # [m] promjer kružnog presjeka

# -----------------------------------------------------------------------------
# 2. PRORAČUN GEOMETRIJSKIH KARAKTERISTIKA
# -----------------------------------------------------------------------------

# Površina poprečnog presjeka
# Formula: A = π * D² / 4
A = (math.pi * D**2) / 4          # [m²]

# Opseg (obod) kružnog presjeka
# Formula: O = π * D
O = math.pi * D                    # [m]

# Moment tromosti oko težišne osi (aksijalni)
# Formula: I = π * D⁴ / 64
I = (math.pi * D**4) / 64         # [m⁴]

# Moment otpora (za savijanje) — odnos momenta tromosti i udaljenosti ruba
# od težišne osi (= D/2)
# Formula: W = π * D³ / 32   (ekvivalentno: W = I / (D/2))
W = (math.pi * D**3) / 32         # [m³]

# -----------------------------------------------------------------------------
# 3. ISPIS REZULTATA
# -----------------------------------------------------------------------------

print("=" * 55)
print("  GEOMETRIJSKE KARAKTERISTIKE KRUŽNOG PRESJEKA")
print("=" * 55)

# Ispis ulaznog podatka
print(f"  Promjer presjeka      D  = {D:.4f} m")
print("-" * 55)

# Površina — ispisujemo u m² i u cm² (1 m² = 10 000 cm²)
print(f"  Površina              A  = {A:.6f} m²")
print(f"                           = {A * 1e4:.4f} cm²")

# Opseg — ispisujemo u m i u cm
print(f"  Opseg                 O  = {O:.6f} m")
print(f"                           = {O * 1e2:.4f} cm")

# Moment tromosti — ispisujemo u m⁴ i u cm⁴ (1 m⁴ = 1×10⁸ cm⁴)
print(f"  Moment tromosti       I  = {I:.8f} m⁴")
print(f"                           = {I * 1e8:.4f} cm⁴")

# Moment otpora — ispisujemo u m³ i u cm³ (1 m³ = 1×10⁶ cm³)
print(f"  Moment otpora         W  = {W:.8f} m³")
print(f"                           = {W * 1e6:.4f} cm³")

print("=" * 55)

# -----------------------------------------------------------------------------
# 4. PROVJERA: W = I / (D/2)  →  mora biti jednako gornjem rezultatu
# -----------------------------------------------------------------------------

W_provjera = I / (D / 2)          # alternativni izračun momenta otpora

print(f"\n  PROVJERA: W = I/(D/2) = {W_provjera * 1e6:.4f} cm³  ✓")
print("=" * 55)
