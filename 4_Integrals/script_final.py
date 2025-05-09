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

# wzór Simpsona dla złożonej kwadratury Newtona-Cotesa opartej na 3 węzłach
def simpson(function_id, a, b, eps) :
    num_range = b - a # długość przedziału
    subrange = 1 # początkowa liczba podprzedziałów
    integral = 0 # zmienna przechowująca wartość całki

    while True :
        subrange *= 2
        s_len = num_range / subrange # długość jednego podprzedziału
        prev_integral = integral # zapis poprzedniej wartości całki żeby później porównać ją z nową
        integral = wxfx(a, function_id) + wxfx(b, function_id) # nowa wartość całki jako suma wartości funkcji w(x)f(x)
                                                               # w punktach granicznych a i b

        for i in range(1, subrange // 2) :
            integral += 4 * wxfx(a + (2 * i - 1) * s_len, function_id)
            integral += 2 * wxfx(a + (2 * i) * s_len, function_id)

        integral *= s_len / 3
        if abs(prev_integral - integral) < eps and subrange > 1 :
            break

    return integral

# wzór Simpsona na mniejszych podprzedziałach
def simpson_lim(function_id, eps) :
    result = 0

    # prawa część przedziału
    a = 0
    b = 0.5

    while True :
        integral = simpson(function_id, a, b, eps)
        result += integral
        a = b
        b += ((1 - b) / 2)
        if abs(integral) < eps :
            break

    # lewa część przedziału
    a = -0.5
    b = 0

    while True :
        integral = simpson(function_id, a, b, eps)
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
        w = PI / nodes_num
        node = -np.cos((2 * i - 1) * PI / (2 * nodes_num))
        integral += w * fx(node, function_id)
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

    print("\nMETODA NEWTONA-COTESA\n---------------------")
    print("Wynik:", simpson_lim(function_id, eps))

    print("\nMETODA GAUSSA-CZEBYSZEWA\n------------------------")
    for nodes in range(2, 6):
        print(f"Liczba węzłów: {nodes}")
        print(f"Wynik: {gauss_chebyshev(function_id, nodes)}\n")

main()