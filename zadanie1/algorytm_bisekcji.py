import math

ex = 1e-8

def wielomian(x) :
    return x**3 + x**2 - 2*x

def trygonometryczna(x) :
    return math.sin(x)

def wykladnicza(x) :
    return 0.5**x - 1

def zlozenie_wiel_tryg(x) :
    return wielomian(trygonometryczna(x))

def zlozenie_wykl_wiel(x) :
    return wykladnicza(wielomian(x))

funkcje = {
    "1": wielomian,
    "2": trygonometryczna,
    "3": wykladnicza,
    "4": zlozenie_wiel_tryg,
    "5": zlozenie_wykl_wiel
}

print("Funkcje:")
print("1 - wielomian")
print("2 - f. trygonometryczna")
print("3 - f. wykładnicza")
print("4 - zlozenie: wielomian od f. wykładniczej")
print("5 - zlozenie: f. wykładnicza od wielomianu")
wybor_f = input("Wybierz funkcję: ")

if wybor_f not in funkcje:
    print("Niepoprawny wybór funkcji")
    exit()

funkcja = funkcje[wybor_f]

print("Kryteria stopu:")
print("1 - |x - x_prev| < epsilon")
print("2 - liczba iteracji")
wybor_k = input("Wybierz kryterium stopu: ")

if wybor_k not in ["1", "2"] :
    print("Niepoprawny wybór kryterium stopu")
    exit()

if wybor_k == "1" :
    ex = float(input("Podaj epsilon: "))
else :
    iter = int(input("Podaj liczbę iteracji: "))

a = float(input("Podaj a: "))
b = float(input("Podaj b: "))

if b < a :
    print("b jest mniejsze od a")
    exit()

fa = funkcja(a)
fb = funkcja(b)

if fa * fb >= 0 :
    print("Funkcja musi mieć różne znaki na końcach przedziału [a, b]")
else :
    x0 = (a + b) / 2

    while abs(a - x0) > ex if wybor_k == "1" else iter > 0 :
        fx = funkcja(x0);
        fa = funkcja(a);
        fb = funkcja(b);

        if fx == 0 :
            break

        if fx * fb < 0 :
            a = x0

        if fx * fa < 0 :
            b = x0

        x0 = (a + b) / 2

        if wybor_k == "2" :
            iter -= 1

    print(f"x0 = {x0}")