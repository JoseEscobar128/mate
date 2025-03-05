import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp

class NumericalMethodsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Métodos Numéricos")

        # Explicación e instrucciones
        self.description_label = ttk.Label(
            self.root,
            text="Esta aplicación resuelve ecuaciones usando los métodos numéricos:\n"
                 "- Euler Mejorado\n- Newton-Raphson\n- Runge-Kutta 4\n\n"
                 "🔹 Instrucciones:\n"
                 "1️⃣ Selecciona el método.\n"
                 "2️⃣ Ingresa los valores requeridos.\n"
                 "3️⃣ Presiona 'Calcular' para obtener los resultados.\n"
                 "4️⃣ Usa 'Limpiar Tabla' para borrar los resultados.\n",
            justify="left"
        )
        self.description_label.pack(pady=10)

        # Selección del método
        self.method_label = ttk.Label(self.root, text="Selecciona el método:")
        self.method_label.pack()

        self.method_combobox = ttk.Combobox(self.root, values=["Euler Mejorado", "Newton-Raphson", "Runge-Kutta 4"])
        self.method_combobox.pack()
        self.method_combobox.bind("<<ComboboxSelected>>", self.show_inputs)

        self.inputs_frame = ttk.Frame(self.root)
        self.inputs_frame.pack()

        # Botones
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=5)

        self.calculate_button = ttk.Button(self.button_frame, text="Calcular", command=self.calculate)
        self.calculate_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(self.button_frame, text="Limpiar Tabla", command=self.clear_results)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Tabla de resultados
        self.result_table = ttk.Treeview(self.root, columns=("Iteración", "x", "y"), show="headings")
        self.result_table.heading("Iteración", text="Iteración")
        self.result_table.heading("x", text="x")
        self.result_table.heading("y", text="y")
        self.result_table.pack()

    def show_inputs(self, event):
        for widget in self.inputs_frame.winfo_children():
            widget.destroy()

        method = self.method_combobox.get()
        if method == "Euler Mejorado":
            self.create_euler_inputs()
        elif method == "Newton-Raphson":
            self.create_newton_inputs()
        elif method == "Runge-Kutta 4":
            self.create_runge_kutta_inputs()

    def create_euler_inputs(self):
        labels = [
            ("x0", "Valor inicial de x", "0"),
            ("y0", "Valor inicial de y", "1"),
            ("h", "Tamaño del paso", "0.1"),
            ("n", "Número de iteraciones", "10"),
            ("Función", "Ecuación en términos de x y y", "y - x**2 + 1")
        ]
        self.create_input_fields(labels)

    def create_newton_inputs(self):
        labels = [
            ("x0", "Valor inicial de x", "1"),
            ("Tolerancia", "Criterio de parada", "0.0001"),
            ("Iteraciones", "Máximo de iteraciones", "10"),
            ("Función", "Función en términos de x", "x**3 - x - 1"),
            ("Derivada", "Derivada de la función", "3*x**2 - 1")
        ]
        self.create_input_fields(labels)

    def create_runge_kutta_inputs(self):
        labels = [
            ("x0", "Valor inicial de x", "0"),
            ("y0", "Valor inicial de y", "1"),
            ("h", "Tamaño del paso", "0.1"),
            ("n", "Número de iteraciones", "10"),
            ("Función", "Ecuación en términos de x y y", "y - x**2 + 1")
        ]
        self.create_input_fields(labels)

    def create_input_fields(self, labels):
        self.entries = {}
        for label, hint, example in labels:
            ttk.Label(self.inputs_frame, text=f"{hint} ({label}):").pack()
            entry = ttk.Entry(self.inputs_frame)
            entry.pack()
            entry.insert(0, example)
            self.entries[label] = entry

    def calculate(self):
        method = self.method_combobox.get()
        self.clear_results()

        if method == "Newton-Raphson":
            self.newton_raphson()
        elif method == "Euler Mejorado":
            self.euler_mejorado()
        elif method == "Runge-Kutta 4":
            self.runge_kutta_4()

    def clear_results(self):
        for item in self.result_table.get_children():
            self.result_table.delete(item)

    def euler_mejorado(self):
        try:
            x0 = float(self.entries["x0"].get())
            y0 = float(self.entries["y0"].get())
            h = float(self.entries["h"].get())
            n = int(self.entries["n"].get())
            func_str = self.entries["Función"].get()
            
            x, y = sp.symbols('x y')
            f = sp.sympify(func_str)
            
            for i in range(n):
                k1 = f.subs([(x, x0), (y, y0)])
                k2 = f.subs([(x, x0 + h), (y, y0 + h * k1)])
                y0 = y0 + (h / 2) * (k1 + k2)
                x0 = x0 + h
                self.result_table.insert("", "end", values=(i, x0, y0))
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {e}")

    def runge_kutta_4(self):
        try:
            x0 = float(self.entries["x0"].get())
            y0 = float(self.entries["y0"].get())
            h = float(self.entries["h"].get())
            n = int(self.entries["n"].get())
            func_str = self.entries["Función"].get()
            
            x, y = sp.symbols('x y')
            f = sp.sympify(func_str)
            
            for i in range(n):
                k1 = f.subs([(x, x0), (y, y0)])
                k2 = f.subs([(x, x0 + h/2), (y, y0 + h/2 * k1)])
                k3 = f.subs([(x, x0 + h/2), (y, y0 + h/2 * k2)])
                k4 = f.subs([(x, x0 + h), (y, y0 + h * k3)])
                y0 = y0 + (h / 6) * (k1 + 2*k2 + 2*k3 + k4)
                x0 = x0 + h
                self.result_table.insert("", "end", values=(i, x0, y0))
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {e}")
    def newton_raphson(self):
        try:
            x0 = float(self.entries["x0"].get())
            tol = float(self.entries["Tolerancia"].get())
            max_iter = int(self.entries["Iteraciones"].get())
            func_str = self.entries["Función"].get()
            deriv_str = self.entries["Derivada"].get()

            x = sp.Symbol('x')
            f = sp.sympify(func_str)
            df = sp.sympify(deriv_str)

            for i in range(max_iter):
                fx0 = f.subs(x, x0)
                dfx0 = df.subs(x, x0)

                # Evitar divisiones por valores demasiado pequeños
                if abs(dfx0) < 1e-10:
                    messagebox.showerror("Error", f"Derivada muy pequeña en x = {x0}, posible división por cero.")
                    return

                x1 = x0 - fx0 / dfx0

                # Mostrar datos en la tabla
                self.result_table.insert("", "end", values=(i, x1, fx0))

                # Criterio de parada usando la diferencia y la función evaluada
                if abs(x1 - x0) < tol and abs(f.subs(x, x1)) < tol:
                    self.result_table.insert("", "end", values=(i+1, x1, "Raíz encontrada"))
                    messagebox.showinfo("Resultado", f"Raíz encontrada: {x1}")
                    return

                x0 = x1

            messagebox.showwarning("Atención", "Se alcanzó el número máximo de iteraciones sin convergencia.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {e}")

            try:
                x0 = float(self.entries["x0"].get())
                tol = float(self.entries["Tolerancia"].get())
                max_iter = int(self.entries["Iteraciones"].get())
                func_str = self.entries["Función"].get()
                deriv_str = self.entries["Derivada"].get()

                x = sp.Symbol('x')
                f = sp.sympify(func_str)
                df = sp.sympify(deriv_str)

                for i in range(max_iter):
                    fx0 = f.subs(x, x0)
                    dfx0 = df.subs(x, x0)
                    if dfx0 == 0:
                        messagebox.showerror("Error", "Derivada cero, no se puede continuar")
                        return
                    x1 = x0 - fx0 / dfx0
                    self.result_table.insert("", "end", values=(i, x1, fx0))
                    if abs(x1 - x0) < tol:
                        messagebox.showinfo("Resultado", f"Raíz encontrada: {x1}")
                        return
                    x0 = x1
            except Exception as e:
                messagebox.showerror("Error", f"Error en el cálculo: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NumericalMethodsApp(root)
    root.mainloop()