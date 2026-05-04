# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 10:25:12 2026

@author: mgrubisic
"""

import numpy as np
import matplotlib.pyplot as plt

# 1. Definiranje podataka opterećenja, greda 10 metara
x_mjereno = np.linspace(0, 10, 10)
y_mjereno = np.array([0, 2, 5, 7, 8, 8, 6, 4, 2, 0])
# q(x) [kN/m] opterećenje

# 2. Linearna interpolacija (povećana gustoća podataka za točniji priračun)
x_gusto = np.linspace(0, 10, 50)
y_interpolirano = np.interp(x_gusto, x_mjereno, y_mjereno)

# 3. Integracija (Izračun ukupne sile)
# Trapezno pravilo
ukupna_sila = np.trapz(y_interpolirano, x_gusto)
print(f"Ukupna sila: {ukupna_sila:.3f} kN\n")

ukupna_sila_izvorna = np.trapz(y_mjereno, x_mjereno)
print(f"Ukupna sila IZVORNA: {ukupna_sila_izvorna:.3f} kN\n")

# 4. Derivacija (Promjena opterećenja duž grede)
nagib_opterecenja = np.gradient(y_interpolirano,
                                x_gusto)
nagib_opterecenja_izvorno = np.gradient(y_mjereno,
                                x_mjereno)



# Plotanje
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6,6
                                              ))
# Gornji graf
ax1.plot(x_mjereno, y_mjereno,
         'b-o',
         lw=5,
         ms=15, 
         label="Mjereno")
ax1.plot(x_gusto, y_interpolirano, 
         'r--s', 
         lw=3,
         ms=8,
         label="Interpolirano")

ax1.fill_between(x_gusto, y_interpolirano,
                 alpha=0.3, color="red")

ax1.set_xlabel("Duljina grede [m]")
ax1.set_ylabel("Opterećenje [kN/m]")
ax1.grid(True, linestyle="--")

ax1.legend()

# Donji graf
ax2.plot(x_gusto, nagib_opterecenja, 'm-',
         lw=5,
         label="Derivacija opterećenja (nagib)")

ax2.plot(x_mjereno, nagib_opterecenja_izvorno, 'b-',
         lw=4,
         label="Derivacija opterećenja (nagib)")

ax2.set_xlabel("Duljina grede [m]")
ax2.set_ylabel("Derivacija opterećenja")
ax2.grid(True, linestyle="--")

ax2.legend()

# plt.savefig("Primjer_20_4_2026_v1.pdf")
# plt.savefig("Primjer_20_4_2026_v1.png", dpi=100)

plt.show()



