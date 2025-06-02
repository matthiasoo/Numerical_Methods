import numpy as np
import matplotlib.pyplot as plt

# Wielomian Czebyszewa k-tego stopnia
'''
def chebyshev_polynomial(x,k):
    if abs(x)<=1:
        return np.cos(k*np.acos(x))
    elif x>1:
        return np.cosh(k*np.acosh(x))
    return (-1)**k*np.cosh(k*np.acosh(-x))
'''
# Wielomian Czebyszewa k-tego stopnia
def chebyshev_polynomial(x, n):
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

# Wartość wielomianu aproksymacyjnego
def chebyshev(coeffs,a,b, x):
    x=(2*x-(a+b))/(b-a)
    result = 0
    it = 0
    for c in coeffs:
        result+=c*chebyshev_polynomial(x,it)
        it=it+1
    return result

# Schemat Hornera
def horner(x, coefficients):
    result = 0
    for coeff in coefficients:
        result = result * x + coeff
    return result

# Funkcje do aproksymacji
def linear(x):
    return 2*x+1

def absolute(x):
    return np.abs(x)

def polynomial(x):
    #return horner(x,[1,-2,1-1])
    return x**3 - 2*x**2 + x - 1

def trigonometric(x):
    return np.sin(x)

def composite(x):
	return trigonometric(linear(x))

def fx(function_choice):
    if function_choice == 1:
        return linear
    elif function_choice == 2:
        return absolute
    elif function_choice == 3:
        return polynomial
    elif function_choice == 4:
        return trigonometric
    elif function_choice == 5:
        return composite
    else:
        raise ValueError("Nie ma takiej funkcji!")

# Aproksymacja Czebyszewa - współczynniki
def chebyshev_approximation(f, d, a, b, n):
    x_j = np.cos((np.arange(n) + 0.5) * np.pi / n)  # Węzły Czebyszewa na [-1; 1]
    x_mapped = (b-a)/2 * x_j + (a+b)/2  # Transformacja do przedziału [a; b]
    f_values = f(x_mapped)
    
    coefficients = np.zeros(d+1)
    for i in range(d+1):
        coefficients[i] = (2 / n) * np.sum(f_values * chebyshev_polynomial(x_j, i))
    coefficients[0]/=2
    return coefficients

# kwadratura Gaussa-Czebyszewa dla n węzłów
def integral_gauss_chebyshev(function, a, b, nodes_num) :
    integral = 0
    w = np.pi / nodes_num
    for i in range(1, nodes_num + 1) :
        node = np.cos((2 * i - 1) * np.pi / (2 * nodes_num))
        node = (b-a)/2 * node+(a+b)/2
        integral += w * function(node) * (b-a)/2
    return integral
# Obliczanie błędu aproksymacji
def approximation_error(func, coeffs, a, b, nodes_num):
    error_func = lambda x: abs(func(x) - chebyshev(coeffs,a,b, x))
    error = integral_gauss_chebyshev(error_func, a, b, nodes_num)
    return error

# Tryb iteracyjny: dobór stopnia wielomianu
def iterative_approximation(func, a, b, num_nodes, error_threshold):
    degree = 1
    while True:
        coeffs = chebyshev_approximation(func, degree, a, b, num_nodes)
        error = approximation_error(func, coeffs, a, b, num_nodes)
        if error <= error_threshold:
            return degree, coeffs
        degree += 1

def main():
    print("Wybierz funkcję do aproksymacji:")
    print("-------------------------------")
    print("1. Liniowa: 2x + 1")
    print("2. Moduł: |x|")
    print("3. Wielomian: x^3 - 2x^2 + x - 1")
    print("4. Trygonometryczna: sin(x)")
    print("5. Złożenie: sin(2x + 1)")

    function_id = int(input("\nFunkcja (1-5): "))
    if function_id not in [1, 2, 3, 4, 5]:
        print("Nie ma takiej funkcji!")
        return

    selected_function=fx(function_id)

    a = float(input("Podaj lewą stronę przedziału aproksymacji: "))
    b = float(input("Podaj prawą stronę przedziału aproksymacji: "))
    if a >= b:
        print("Nieprawidłowy przedział")
        exit()

    mode = input("Wybierz tryb: (1) Stały stopień, (2) Docelowy błąd: ")

    if mode == '1':
        degree = int(input("Podaj stopień wielomianu aproksymacyjnego: "))
        num_nodes = int(input("Podaj ilość węzłów dla całkowania numerycznego: "))
        coeffs = chebyshev_approximation(selected_function, degree, a, b, num_nodes)
    elif mode == '2':
        error_threshold = float(input("Podaj maksymalny błąd aproksymacji: "))
        num_nodes = int(input("Podaj ilość węzłów dla całkowania numerycznego: "))
        degree, coeffs = iterative_approximation(selected_function, a, b, num_nodes, error_threshold)
        print(f"Dobrany stopień wielomianu: {degree}")
    else:
        print("Nieprawidłowy tryb!")
        return

    print("Współczynniki aproksymacji Czebyszewa:\n")
    print(coeffs)

    error = approximation_error(selected_function, coeffs, a, b, num_nodes)
    print(f"Błąd aproksymacji: {error}")

    # Rysowanie wykresu
    x_values = np.linspace(a, b, 100)
    y_original = selected_function(x_values)
    y_approx = [chebyshev(coeffs,a,b, x) for x in x_values]

    plt.plot(x_values, y_original, label="Oryginalna funkcja")
    plt.plot(x_values, y_approx, label="Aproksymacja Czebyszewa", linestyle='dashed')
    plt.legend()
    plt.title("Aproksymacja Czebyszewa")
    plt.show()

if __name__ == "__main__":
    main()
