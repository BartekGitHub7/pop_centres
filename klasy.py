
            # PRZYKLADOWE KLASY na 5-minutowke: trening


    # napisz klase ktora bedzie obliczala predkosc pojazdu na podstawie czasu w jakim pokonał on określony odcinek
class KalkulatorPredkosciPojazdu:
    def __init__(self, dystans, czas):
        self.dystans = dystans
        self.czas = czas

    def oblicz_predkosc(self):
        if self.czas == 0:
             return "Czas nie może być równy zero."
        predkosc = self.dystans / self.czas
        return predkosc
def wprowadz_dane():
    dystans = float(input("Wprowadz dystans: "))
    czas = float(input("Wprowadz czas: "))
    return dystans, czas

    # Przykładowe użycie
dystans, czas = wprowadz_dane()
dystans_obliczony = KalkulatorPredkosciPojazdu(dystans, czas)
print(f"Prędkość pojazdu: {dystans_obliczony.oblicz_predkosc()} km/h")



    # napisz klasę Drzewo która przechowuje wysokość i szerokość drzewa, przyjmij ze drzewo jest walcem i oblicz jego objetosc
class Drzewo:
    def __init__(self, wysokosc, srednica):
        self.wysokosc = wysokosc
        self.srednica = srednica

    def oblicz_objetosc(self):
        promien = self.srednica / 2
        objetosc = 3.14 * (promien ** 2) * self.wysokosc  # ** oznacza do kwadratu
        return objetosc
    # Przykładowe użycie
drzewo1 = Drzewo(10, 1)
print(f"Objętość drzewa: {drzewo1.oblicz_objetosc()} m^3")


    # bardziej zaawansowane:
class Drzewo:
    def __init__(self, wysokosc, srednica):
        self.wysokosc = wysokosc
        self.srednica = srednica

    def oblicz_objetosc(self):
        promien = self.srednica / 2
        objetosc = 3.14 * (promien ** 2) * self.wysokosc  # ** oznacza do kwadratu
        return objetosc

    # Funkcja do wprowadzania danych przez użytkownika
def wprowadz_dane():
    wysokosc = float(input("Podaj wysokość drzewa (w metrach): "))
    srednica = float(input("Podaj średnicę drzewa (w metrach): "))
    return wysokosc, srednica

    # Główna część programu
wysokosc, srednica = wprowadz_dane()
drzewo = Drzewo(wysokosc, srednica)
print(f"Objętość drzewa: {drzewo.oblicz_objetosc()} m^3")


    # napisz klase ktora bedzie sumowala wartosci od 1 do 10

class Suma:
    def __init__(self, wartosc):
        self.wartosc = wartosc
    def oblicz_sume(self):
        suma = 0
        for i in range(0, self.wartosc+1):
            suma += i
        return suma
suma = Suma(10)
print(suma.oblicz_sume())


class Parzyste:
    def __init__(self):
        self.liczba = 0
    def wypisz(self):
        for liczba in range(self.liczba, 101):
            if liczba %2 == 0:
                print(liczba)
Parzyste().wypisz()

 # napisz klase ktora bedzie odejmowala wartosci od 10 do 1
class OdejmowanieOdDziesieciu:
    def __init__(self):
        self.liczba = 10

    def odejmij(self):
        while self.liczba >= 1:
            print(self.liczba)
            self.liczba -= 1


    # Użycie klasy:
odejmowanie = OdejmowanieOdDziesieciu()
odejmowanie.odejmij()

            # przykładowa pętle
        # napisz pętle, która bedzie odliczała od 1000 do 0 z krokiem 50 i wyświetlała przy tym odliczana wartości

i = 1000
while i >= 0:
    print(i)
    i = i - 50
        # napisz pętle, która bedzie odliczała od 0 do 10000 z krokiem 25 i wyświetlała przy tym odliczana wartości

i = 0
while i <= 1000:
    print(i)
    i = i + 25