import numpy as np

PI = np.pi

# horner
def horner(x, coefficients):
    result = 0
    for coeff in coefficients:
        result = result * x + coeff
    return result

# f. liniowa
def linear(x):
    return 2 * x + 1

# wielomian
def poly(x):
    # 3x^3 + 2x^2 + 5x + 7
    return horner(x, [3, 2, 5, 7])

# f. trygonometryczna
def trigonometric(x):
    return np.sin(x)

# złożenie f. trygonometrycznej i liniowej
def composite(x):
    return trigonometric(linear(x))

def fx(x, function_choice):
    if function_choice == 1:
        return linear(x)
    elif function_choice == 2:
        return poly(x)
    elif function_choice == 3:
        return trigonometric(x)
    elif function_choice == 4:
        return composite(x)
    else:
        raise ValueError("Nieprawidłowy wybór funkcji!")

# funkcja wagowa
def wx(x) :
    # w(x) = 1/sqrt(1-x^2)
    return 1 / np.sqrt(1 - x * x)

# funkcja obliczająca w(x) * f(x)
def wxfx(x, function_id):
    try:
        return fx(x, function_id) * wx(x)
    except ZeroDivisionError:
        return 0

# version = 0 - wersja bez wagi (używa fx)
# version = 1 - wersja z wagą (używa wxfx)
def function_type(x, function_id, version) :
    if version == 0 :
        return fx(x, function_id)
    elif version == 1 :
        return wxfx(x, function_id)
    else:
        raise ValueError("Nieprawidłowy wybór wersji!")

# wzór Simpsona dla złożonej kwadratury Newtona-Cotesa opartej na 3 węzłach
# version = 0 - wersja bez wagi (używa fx)
# version = 1 - wersja z wagą (używa wxfx)
def simpson(function_id, a, b, eps, version) :
    num_range = b - a # długość przedziału
    subrange = 1 # początkowa liczba podprzedziałów
    integral = 0 # zmienna przechowująca wartość całki

    while True :
        subrange *= 2
        s_len = num_range / subrange # długość jednego podprzedziału
        prev_integral = integral # zapis poprzedniej wartości całki żeby później porównać ją z nową
        integral = function_type(a, function_id, version) + function_type(b, function_id, version) # nowa wartość całki jako suma wartości funkcji f(x)
                                                           # w punktach granicznych a i b
        # przechodzimy przez punkty wewn. przedziałów
        for i in range(1, subrange // 2) :
            integral += 4 * function_type(a + (2 * i - 1) * s_len, function_id, version) # wartości w środku każdego podprzedziału
                                                                       # 4 to waga dla punktów środkowych
            integral += 2 * function_type(a + (2 * i) * s_len, function_id, version) # wartości na granicach między podpredziałami
                                                                   # 2 to waga dla punktów pośrednich

        integral *= s_len / 3 # zgodnie z wzorem Simpsona
        # różnica < eps i wiecej niz 1 podprzedzial
        if abs(prev_integral - integral) < eps and subrange > 1 :
            break

    return integral

# wzór Simpsona na przedziale [-1, 1]
# dzielimy na podprzedziały (szczegolnie blisko koncow)
# i zbliżamy się do +-1,
# ponieważ funkcja wagowa jest nieskończona w +-1
def simpson_lim(function_id, eps) :
    result = 0

    # prawa część przedziału
    a = 0
    b = 0.5

    # zbliżamy się do 1
    while True :
        integral = simpson(function_id, a, b, eps, 1) # używamy wersji Simpsona z wagą
        result += integral
        a = b
        b += ((1 - b) / 2)
        if abs(integral) < eps :
            break

    # lewa część przedziału
    a = -0.5
    b = 0

    # zbliżamy się do -1
    while True :
        integral = simpson(function_id, a, b, eps, 1) # używamy wersji Simpsona z wagą
        result += integral
        b = a
        a -= ((1 - abs(b)) / 2)
        if (abs(integral) < eps) :
            break

    return result

# kwadratura Gaussa-Czebyszewa dla n węzłów
def gauss_chebyshev(function_id, nodes_num) :
    integral = 0
    for i in range(1, nodes_num + 1) :
        w = PI / nodes_num # obliczamy wage
        node = -np.cos((2 * i - 1) * PI / (2 * nodes_num)) #obliczenie węzłów za pomocą cosinusa (literatury)
        integral += w * fx(node, function_id) # mnożenie wartości funkcji przez wagę
    return integral

def main():
    print("Wybierz funkcję:")
    print("---------------")
    print("1. liniowa")
    print("2. wielomian")
    print("3. trygonometryczna")
    print("4. złożenie (liniowa i trygonometryczna)")

    function_id = int(input("\nFunkcja: "))
    eps = float(input("\nPodaj dokładność: "))

    a = float(input("\nPodaj a: "))
    b = float(input("\nPodaj b: "))

    print(f"WZÓR SIMPSONA BEZ WAGI NA PRZEDZIALE [{a};{b}]\n--------------------------")
    print(simpson(function_id, a, b, eps, 0))

    print("\nMETODA NEWTONA-COTESA\n--------------------------")
    print("Wynik:", simpson_lim(function_id, eps))

    print("\nMETODA GAUSSA-CZEBYSZEWA\n--------------------------")
    for nodes in range(2, 6):
        print(f"Liczba węzłów: {nodes}")
        print(f"Wynik: {gauss_chebyshev(function_id, nodes)}\n")



main()