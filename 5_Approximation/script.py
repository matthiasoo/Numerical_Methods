import numpy as np
import matplotlib.pyplot as plt

PI = np.pi

def horner(x, coefficients):
    result = 0
    for coeff in coefficients:
        result = result * x + coeff
    return result

def linear(x):
    return 2 * x + 1

def absolute(x):
    return np.abs(x)

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
        return absolute(x)
    elif function_choice == 3:
        return poly(x)
    elif function_choice == 4:
        return trigonometric(x)
    elif function_choice == 5:
        return composite(x)
    else:
        raise ValueError("Nie ma takiej funkcji!")

# Kwadratura Gaussa-Czebyszewa
def gauss_chebyshev(function_id, nodes_num):
    integral = 0
    for i in range(1, nodes_num + 1):
        w = PI / nodes_num
        node = -np.cos((2 * i - 1) * PI / (2 * nodes_num))
        integral += w * fx(node, function_id)
    return integral

# Wielomian Czebyszewa
def chebyshev_poly(x, n):
    if n == 0:
        return 1
    elif n == 1:
        return x
    else:
        T_prev = 1
        T_curr = x
        for _ in range(2, n + 1):
            T_next = 2 * x * T_curr - T_prev
            T_prev = T_curr
            T_curr = T_next
        return T_curr

# Obliczanie współczynników aproksymacji Czebyszewa
def compute_chebyshev_coefficients(function_id, degree, nodes_num):
    coefficients = []
    for n in range(degree + 1):
        def integrand(x):
            try:
                return fx(x, function_id) * chebyshev_poly(x, n)
            except ZeroDivisionError:
                return 0

        integral = gauss_chebyshev(lambda x: fx(x, function_id) * chebyshev_poly(x, n), nodes_num)
        coeff = (1 / PI) * integral if n == 0 else (2 / PI) * integral
        coefficients.append(coeff)
    return coefficients

# Obliczanie wartości aproksymacji Czebyszewa
def chebyshev_approx(x, coefficients):
    result = 0
    for n, coeff in enumerate(coefficients):
        result += coeff * chebyshev_poly(x, n)
    return result

# Obliczanie błędu aproksymacji na przedziale [a, b]
def compute_error(function_id, coefficients, a, b, num_points=1000):
    x = np.linspace(a, b, num_points)
    y_true = fx(x, function_id)
    y_approx = np.array([chebyshev_approx(xi, coefficients) for xi in x])
    # Mean squared error
    mse = np.mean((y_true - y_approx) ** 2)
    return mse

def plot_functions(function_id, coefficients, a, b, title):
    x = np.linspace(a, b, 1000)
    y_true = fx(x, function_id)
    y_approx = np.array([chebyshev_approx(xi, coefficients) for xi in x])

    plt.figure(figsize=(10, 6))
    plt.plot(x, y_true, 'b-', label='Funkcja oryginalna')
    plt.plot(x, y_approx, 'r--', label='Wielomian aproksymacyjny')
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.legend()
    plt.close()

def main():
    print("Wybierz funkcję do aproksymacji:")
    print("-------------------------------")
    print("1. Liniowa: 2x + 1")
    print("2. Moduł: |x|")
    print("3. Wielomian: 3x^3 + 2x^2 + 5x + 7")
    print("4. Trygonometryczna: sin(x)")
    print("5. Złożenie: sin(2x + 1)")

    function_id = int(input("\nFunkcja (1-5): "))
    if function_id not in [1, 2, 3, 4, 5]:
        print("Nie ma takiej funkcji!")
        return

    a = float(input("Podaj lewą stronę przedziału aproksymacji: "))
    b = float(input("Podaj prawą stronę przedziału aproksymacji: "))
    if a >= b or a < -1 or b > 1:
        print("Przedział musi nie może wychodzić poza zakres [-1, 1] oraz a < b!")
        return

    mode = input("Wybierz tryb: (1) Stały stopień, (2) Docelowy błąd: ")
    nodes_num = int(input("Podaj liczbę węzłów Gaussa-Czebyszewa: "))

    if mode == '1':
        degree = int(input("Podaj stopień wielomianu: "))
        coefficients = compute_chebyshev_coefficients(function_id, degree, nodes_num)
        error = compute_error(function_id, coefficients, a, b)
        print(f"\nWspółczynniki aproksymacji Czebyszewa: {coefficients}")
        print(f"Bład aproksymacji: {error}")
        plot_functions(function_id, coefficients, a, b, f"Aproksymacja Czebyszewa (Stopień {degree})")
    elif mode == '2':
        target_error = float(input("Podaj błąd: "))
        degree = 1
        while True:
            coefficients = compute_chebyshev_coefficients(function_id, degree, nodes_num)
            error = compute_error(function_id, coefficients, a, b)
            print(f"Stopień {degree}: Bład = {error}")
            if error < target_error or degree > 50:
                print(f"\nOstateczny stopień: {degree}")
                print(f"Współczynniki aproksymacji Czebyszewa: {coefficients}")
                print(f"Błąd aproksymacji: {error}")
                plot_functions(function_id, coefficients, a, b, f"Aproksymacja Czebyszewa (Stopień {degree})")
                break
            degree += 1
    else:
        print("Nieprawidłowy tryb!")
        return


if __name__ == "__main__":
    main()