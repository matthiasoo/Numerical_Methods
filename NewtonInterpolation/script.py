import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class InterpolationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interpolacja Newtona")

        # Domyślne ustawienia
        self.function_var = StringVar(value="liniowa")
        self.interval_start_var = DoubleVar(value=-5.0)
        self.interval_end_var = DoubleVar(value=5.0)
        self.nodes_count_var = IntVar(value=5)
        self.custom_nodes = []

        # Tworzenie interfejsu
        self.create_widgets()

    def create_widgets(self):
        # Ramka dla ustawień
        settings_frame = LabelFrame(self.root, text="Ustawienia interpolacji", padx=10, pady=10)
        settings_frame.pack(padx=10, pady=10, fill="x")

        # Wybór funkcji
        Label(settings_frame, text="Funkcja:").grid(row=0, column=0, sticky="w")
        functions = ["liniowa", "|x|", "wielomian", "trygonometryczna", "złożenie1", "złożenie2"]
        OptionMenu(settings_frame, self.function_var, *functions).grid(row=0, column=1, sticky="ew")

        # Przedział interpolacji
        Label(settings_frame, text="Przedział interpolacji:").grid(row=1, column=0, sticky="w")
        Entry(settings_frame, textvariable=self.interval_start_var, width=10).grid(row=1, column=1)
        Label(settings_frame, text="do").grid(row=1, column=2)
        Entry(settings_frame, textvariable=self.interval_end_var, width=10).grid(row=1, column=3)

        # Liczba węzłów
        Label(settings_frame, text="Liczba węzłów:").grid(row=2, column=0, sticky="w")
        self.entry = Entry(settings_frame, textvariable=self.nodes_count_var, width=10)
        self.entry.grid(row=2, column=1)

        # Przycisk do wczytywania niestandardowych węzłów
        Button(settings_frame, text="Wczytaj węzły z pliku", command=self.load_custom_nodes).grid(row=3, column=0,
                                                                                        columnspan=4, pady=5)
        Button(settings_frame, text="Resetuj węzły", command=self.reset_custom_nodes).grid(row=3, column=3,
                                                                                        columnspan=4, pady=5)
        # Przycisk obliczania
        Button(self.root, text="Oblicz i rysuj", command=self.calculate_and_plot).pack(pady=10)

        # Miejsce na wykres
        self.figure, self.ax = plt.subplots(figsize=(8, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # Funkcja do ładowania węzłów z pliku
    def load_custom_nodes(self):
        filepath = filedialog.askopenfilename(filetypes=[("Pliki tekstowe", "*.txt")])
        if filepath:
            try:
                with open(filepath, 'r') as file:
                    lines = file.readlines()
                    self.custom_nodes = [float(line.strip()) for line in lines if line.strip()]
                messagebox.showinfo("Sukces", f"Wczytano {len(self.custom_nodes)} węzłów.")
                self.nodes_count_var.set(len(self.custom_nodes))
                self.entry.config(state="disabled")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się wczytać węzłów: {e}")

    def reset_custom_nodes(self):
        self.custom_nodes.clear()
        self.entry.config(state="normal")

    def linear_function(self, x):
        # Funkcja liniowa: f(x) = 2x + 1
        return 2 * x + 1

    def abs_function(self, x):
        # Funkcja g(x) = |x|
        return np.abs(x)

    def polynomial_function(self, x):
        # Funkcja wielomianowa: h(x) = x^3 - 2x + 5
        return x**3 - 2 * x + 5

    def trigonometric_function(self, x):
        # Funkcja trygonometryczna: i(x) = sin(x) + cos(2x)
        return np.sin(x)

    def composite_function1(self, x):
        # Złożenie |x| i wielomianu - j(x) = g(h(x))
        return self.abs_function(self.polynomial_function(x));

    def composite_function2(self, x):
        # Złożenie wielomianu i f. trygonometrycznej - k(x) = h(i(x))
        return self.polynomial_function(self.trigonometric_function(x));

    def calculate_function(self, x):
        # Wybiera odpowiednią funkcję na podstawie wyboru użytkownika.
        function_type = self.function_var.get()
        function_map = {
            "liniowa": self.linear_function,
            "|x|": self.abs_function,
            "wielomian": self.polynomial_function,
            "trygonometryczna": self.trigonometric_function,
            "złożenie1": self.composite_function1,
            "złożenie2": self.composite_function2
        }
        if function_type not in function_map:
            raise ValueError("Nieznana funkcja.")
        return function_map[function_type](x)

    def newton_interpolation(self, x_nodes, y_nodes):
        # Oblicza współczynniki wielomianu interpolacyjnego Newtona
        n = len(x_nodes)
        # Kopia y_nodes, ponieważ będziemy modyfikować wartości
        divided_diff = np.copy(y_nodes).astype(float)
        coeffs = np.zeros(n)
        coeffs[0] = divided_diff[0]

        # Obliczanie ilorazów różnicowych n-tego rzędu
        for j in range(1, n):
            for i in range(n - 1, j - 1, -1):
                divided_diff[i] = (divided_diff[i] - divided_diff[i - 1]) / (x_nodes[i] - x_nodes[i - j])
            coeffs[j] = divided_diff[j]

        return coeffs

    def eval_newton_poly(self, x, x_nodes, coeffs):
        # Oblicza wartość wielomianu interpolacyjnego Newtona w punktach x.
        n = len(coeffs)
        result = np.zeros_like(x, dtype=float)

        for i in range(n):
            term = coeffs[i]
            for j in range(i):
                term *= (x - x_nodes[j])
            result += term

        return result

    def horner_eval(self, x, coeffs, x_nodes):
        return self.eval_newton_poly(x, x_nodes, coeffs)

    def calculate_and_plot(self):
        try:
            a = self.interval_start_var.get()
            b = self.interval_end_var.get()
            n = self.nodes_count_var.get()

            if a >= b:
                raise ValueError("Początek przedziału musi być mniejszy niż koniec.")
            if n < 1:
                raise ValueError("Liczba węzłów musi być dodatnia.")

            # Wybór węzłów interpolacji
            if self.custom_nodes:
                x_nodes = np.array(sorted(self.custom_nodes))
                if len(x_nodes) < 2:
                    raise ValueError("Za mało węzłów interpolacji (minimum 2).")
                n = len(x_nodes)
            else:
                x_nodes = np.linspace(a, b, n)

            # Sprawdzanie unikalności węzłów
            if len(np.unique(x_nodes)) != len(x_nodes):
                raise ValueError("Węzły interpolacji muszą być unikalne.")

            # Obliczanie wartości funkcji w węzłach
            y_nodes = self.calculate_function(x_nodes)

            # Obliczanie współczynników wielomianu interpolacyjnego Newtona
            coeffs = self.newton_interpolation(x_nodes, y_nodes)

            # Punkty do rysowania wykresu
            x_plot = np.linspace(a, b, 500)
            y_original = self.calculate_function(x_plot)
            y_interp = self.eval_newton_poly(x_plot, x_nodes, coeffs)

            # Rysowanie wykresu
            self.ax.clear()
            self.ax.plot(x_plot, y_original, label="Funkcja interpolowana", linewidth=2)
            self.ax.plot(x_plot, y_interp, label="Wielomian interpolacyjny", linestyle='--', linewidth=2)
            self.ax.scatter(x_nodes, y_nodes, color='red', label="Węzły interpolacji", zorder=5)
            self.ax.legend()
            self.ax.grid(True)
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("y")
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Błąd", str(e))


if __name__ == "__main__":
    root = Tk()
    app = InterpolationApp(root)
    root.mainloop()
