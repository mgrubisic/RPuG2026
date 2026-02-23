# %% 1. Prvi program: Hello, World!
# Ovaj primjer demonstrira osnovnu upotrebu print() funkcije za ispis teksta u konzolu.
print("Hello, World!")
print("Pozdrav iz Pythona!")
print("Računalno programiranje u građevinarstvu")

# %% 2. Brojevi: cijeli i decimalni
# Primjer definiranja cjelobrojnih (int) i decimalnih (float) varijabli te provjera njihovog tipa.
broj_katova = 5
broj_stupova = 12

## Decimalni brojevi (float)
fck = 30.0          # [MPa] karakteristična čvrstoća betona
L = 6.5             # [m] raspon grede
E = 210000.0        # [MPa] modul elastičnosti čelika

## Provjera tipa
print(type(broj_katova))  # <class 'int'>
print(type(fck))          # <class 'float'>

# %% 3. Tekst (stringovi)
# Prikaz rada sa stringovima, uključujući spajanje (konkatenaciju) i određivanje duljine.
# Stringovi se pišu u navodnicima
ime_projekta = "Poslovna zgrada Osijek"
klasa_betona = 'C30/37'
opis = "Proračun AB grede prema EC2"

# Spajanje stringova
puni_naziv = ime_projekta + " - " + klasa_betona
print(puni_naziv)
# Ispisuje: Poslovna zgrada Osijek - C30/37

# Duljina stringa
print(len(klasa_betona))  # Ispisuje: 6

# %% 4. Logičke vrijednosti (Boolean)
# Uvod u logičke vrijednosti (True/False) i relacijske operatore za usporedbu.
# Logičke vrijednosti
je_armiran = True
potrebna_revizija = False

# Rezultat usporedbe je boolean
fck = 30.0
print(fck > 25)    # True (je li fck veći od 25?)
print(fck == 40)   # False (je li fck jednak 40?)
print(fck != 40)   # True (je li fck različit od 40?)

# Provjera tipa
print(type(je_armiran))  # <class 'bool'>

# %% 5. Varijable i dodjela vrijednosti
# Primjeri kreiranja varijabli, promjene njihovih vrijednosti te višestruke dodjele.
# Dodjela vrijednosti varijabli (znak =)
b = 0.30       # [m] širina presjeka
h = 0.50       # [m] visina presjeka
d = 0.45       # [m] statička visina

# Varijabla može promijeniti vrijednost
h = 0.60       # nova visina
d = h - 0.05   # d ovisi o h

# Višestruka dodjela
x, y, z = 1.0, 2.0, 3.0

a = 1; b = 2;
# Zamjena vrijednosti
a, b = b, a    # Python omogućuje elegantnu zamjenu

# %% 6. Pravila imenovanja varijabli
# Prikaz dobrih i loših praksi pri imenovanju. 
# Napomena: Neispravna imena su zakomentirana kako ne bi prekinula izvođenje skripte.
# Dobra imena (opisna, jasna)
sirina_grede = 0.30
broj_sipki = 4
fcd = 20.0

# Loša imena (nejasna, nečitljiva)
x1 = 0.30
a = 4
temp = 20.0

# Neispravna imena (greška!)
# 2nd_moment = 100   # počinje brojkom
# class = "C30/37"   # rezervirana riječ

# %% 7. Osnovne matematičke operacije
# Prikaz svih ugrađenih aritmetičkih operatora.
a = 15
b = 4

print(a + b)    # 19    (zbrajanje)
print(a - b)    # 11    (oduzimanje)
print(a * b)    # 60    (množenje)
print(a / b)    # 3.75  (dijeljenje - uvijek float!)
print(a // b)   # 3     (cjelobrojno dijeljenje)
print(a % b)    # 3     (ostatak dijeljenja - modulo)
print(a ** b)   # 50625 (potenciranje: 15^4)

# %% 8. Redoslijed operacija
# Važnost korištenja zagrada pri proračunima na primjeru momenta tromosti.
# Primjer: formula za moment tromosti pravokutnika
b = 0.30  # [m]
h = 0.50  # [m]

# I = b * h^3 / 12
I = b * h**3 / 12
print(I)  # 0.003125 m^4

# S zagradama za jasnoću
I = (b * h**3) / 12

# %% 9. Matematičke funkcije (modul math)
# Korištenje ugrađenog 'math' modula za trigonometriju, logaritme i konstante.
import math  # učitavanje modula

# Konstante
print(math.pi)     # 3.141592653589793
print(math.e)      # 2.718281828459045

# Funkcije
print(math.sqrt(16))      # 4.0 (korijen)
print(math.sin(math.pi/2))  # 1.0 (sinus, argument u radijanima!)
print(math.cos(0))        # 1.0 (kosinus)
print(math.log(10))       # 2.302... (prirodni logaritam)
print(math.log10(100))    # 2.0 (logaritam baze 10)
print(math.exp(1))        # 2.718... (e^1)
print(math.degrees(math.pi))  # 180.0 (radijani u stupnjeve)
print(math.radians(90))   # 1.5707... (stupnjevi u radijane)

# %% 10. Primjer 1: Površina i opseg pravokutnika
# Rješavanje jednostavnog geometrijskog zadatka uz ispis rezultata s jedinicama.
# Proračun površine i opsega pravokutnog presjeka

# Ulazni podaci
b = 0.30   # [m] širina
h = 0.50   # [m] visina

# Proračun
A = b * h           # površina
O = 2 * (b + h)     # opseg

# Ispis rezultata
print("Širina b =", b, "m")
print("Visina h =", h, "m")
print("Površina A =", A, "m2")
print("Opseg O =", O, "m")

# %% 11. Primjer 2: Moment tromosti i otpora
# Proračun statičkih karakteristika poprečnog presjeka s konverzijom mjernih jedinica.
# Moment tromosti i moment otpora pravokutnog presjeka

# Dimenzije presjeka
b = 0.30   # [m] širina
h = 0.50   # [m] visina

# Moment tromosti oko težišne osi
# Iy = b * h^3 / 12
Iy = (b * h**3) / 12

# Moment otpora (za savijanje)
# Wy = Iy / (h/2) = b * h^2 / 6
Wy = (b * h**2) / 6

# Ispis s formatiranjem
print("Moment tromosti Iy =", Iy, "m4")
print("Moment otpora Wy =", Wy, "m3")

# U praktičnijim jedinicama
print("Moment tromosti Iy =", Iy * 1e8, "cm4")
print("Moment otpora Wy =", Wy * 1e6, "cm3")

# %% 12. Primjer 3: Normalno naprezanje u gredi
# Određivanje maksimalnog normalnog naprezanja od savijanja.
# Proračun normalnog naprezanja od savijanja

# Podaci
M = 150.0    # [kNm] moment savijanja
b = 0.30     # [m] širina presjeka  
h = 0.50     # [m] visina presjeka

# Moment otpora
Wy = (b * h**2) / 6   # [m3]

# Maksimalno naprezanje na rubu presjeka
# sigma = M / Wy
sigma = M / Wy        # [kN/m2] = [kPa]

# Pretvorba u MPa (1 MPa = 1000 kPa)
sigma_MPa = sigma / 1000

print("Moment savijanja M =", M, "kNm")
print("Moment otpora Wy =", Wy * 1e6, "cm3")
print("Naprezanje sigma =", sigma, "kPa")
print("Naprezanje sigma =", sigma_MPa, "MPa")

# %% 13. Primjer 4: Progib proste grede

# Složeniji proračun koji uključuje provjeru maksimalnog progiba na sredini raspona.
# Maksimalni progib proste grede pod jednoliko 
# raspoređenim opterećenjem: w_max = 5*q*L^4 / (384*E*I)

# Podaci
q = 10.0          # [kN/m] opterećenje
L = 6.0           # [m] raspon
E = 30000000.0    # [kN/m2] modul elast. betona (30 GPa)
b = 0.30          # [m] širina
h = 0.50          # [m] visina

# Moment tromosti
I = (b * h**3) / 12

# Maksimalni progib na sredini raspona
w_max = (5 * q * L**4) / (384 * E * I)

# Ispis
print("Progib w_max =", w_max * 1000, "mm")
print("Granični progib L/250 =", L/250 * 1000, "mm")
