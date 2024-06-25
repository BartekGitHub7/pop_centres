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
    dystans = float(input("Wprowadzy dystans czas: "))
    czas = float(input("Wprowadzy czas czas: "))
    return dystans, czas

    # Przykładowe użycie
dystans, czas = wprowadz_dane()
dystans1 = KalkulatorPredkosciPojazdu(dystans, czas)
print(f"Prędkość pojazdu: {dystans1.oblicz_predkosc()} km/h")



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



