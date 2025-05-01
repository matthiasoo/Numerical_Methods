import numpy as np

PI = np.pi

def horner(x, coefficients):
    result = 0
    for coeff in coefficients:
        result = result * x + coeff
    return result

def linear(x):
    return 2 * x + 1

def poly(x):
    # 3x^3 + 2x^2 + 5x + 7
    return horner(x, [3, 2, 5, 7])

def trigonometric(x):
    return np.sin(x)

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

def wx(x) :
    # w(x) = 1/sqrt(1-x^2) - funkcja wagowa
    return np.sqrt(1 - x * x)

# Funkcja obliczająca w(x) * f(x)
def evaluate_wxfx(x, function_id):
    try:
        return fx(x, function_id) / wx(x)
    except ZeroDivisionError:
        return 0

# Kwadratura Gaussa-Czebyszewa
def gauss_chebyshev(function_id, num_nodes):
    result = 0
    for i in range(1, num_nodes + 1):
        weight = PI / num_nodes
        node = -np.cos((2 * i - 1) * PI / (2 * num_nodes))
        result += weight * fx(node, function_id)
    return result

# Całkowanie metodą Simpsona
def simpson_integral(function_id, a, b, eps):
    n = 1
    result = 0
    while True:
        n *= 2
        h = (b - a) / n
        prev_result = result
        result = evaluate_wxfx(a, function_id) + evaluate_wxfx(b, function_id)

        for i in range(1, n // 2):
            result += 4 * evaluate_wxfx(a + (2 * i - 1) * h, function_id)
            result += 2 * evaluate_wxfx(a + (2 * i) * h, function_id)

        result *= h / 3
        if abs(prev_result - result) < eps and n > 1:
            break

    return result


# Obliczanie granicy dla kwadratury Newtona-Cotesa
def simpson_lim(function_id, eps):
    result = 0

    # Całkowanie od 0 do 1
    a = 0
    b = 0.5
    while True:
        temp = simpson_integral(function_id, a, b, eps)
        result += temp
        a = b
        b = b + (1 - b) / 2
        if abs(temp) < eps:
            break

    # Całkowanie od -1 do 0
    b = 0
    a = -0.5
    while True:
        temp = simpson_integral(function_id, a, b, eps)
        result += temp
        b = a
        a = a - (1 - abs(b)) / 2
        if abs(temp) < eps:
            break

    return result

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