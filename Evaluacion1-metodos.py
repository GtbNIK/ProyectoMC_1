import tkinter as tk
from tkinter import ttk
import simpy
import random
from ttkthemes import ThemedStyle

class ModeloRed:
    def __init__(self, nodos, llegadas_por_nodo):
        self.nodos = nodos
        self.llegadas_por_nodo = llegadas_por_nodo
        self.env = simpy.Environment()
        self.nodos_simpy = [simpy.Resource(self.env) for _ in range(len(nodos))]
        self.resultados = {}

    def ejecutar_simulacion(self, tiempo_simulacion):
        for i, llegada in enumerate(self.llegadas_por_nodo):
            for j in range(llegada):
                self.env.process(self.cliente(i, j))
        self.env.run(until=tiempo_simulacion)

    def cliente(self, nodo_actual, cliente_id):
        yield self.env.timeout(random.expovariate(1.0/self.llegadas_por_nodo[nodo_actual]))
        with self.nodos_simpy[nodo_actual].request() as req:
            yield req
            proximo_nodo = random.choice(list(set(range(len(self.nodos))) - {nodo_actual}))
            self.resultados[(nodo_actual, proximo_nodo)] = self.resultados.get((nodo_actual, proximo_nodo), 0) + 1

class InterfazGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Modelo de Red de Colas Interconectadas - Neil Rangel")
        self.style = ThemedStyle(self.root)
        self.style.theme_use('equilux')

        self.frame = ttk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        self.label_nodos = ttk.Label(self.frame, text="Nodos:")
        self.label_nodos.grid(row=0, column=0, sticky="w")

        self.entry_nodos = ttk.Entry(self.frame)
        self.entry_nodos.grid(row=0, column=1, padx=5)

        self.label_llegadas = ttk.Label(self.frame, text="Llegadas por nodo:")
        self.label_llegadas.grid(row=1, column=0, sticky="w")

        self.entry_llegadas = ttk.Entry(self.frame)
        self.entry_llegadas.grid(row=1, column=1, padx=5)

        self.label_tiempo_simulacion = ttk.Label(self.frame, text="Tiempo de simulación:")
        self.label_tiempo_simulacion.grid(row=2, column=0, sticky="w")

        self.entry_tiempo_simulacion = ttk.Entry(self.frame)
        self.entry_tiempo_simulacion.grid(row=2, column=1, padx=5)

        self.button_simular = ttk.Button(self.frame, text="Simular", command=self.simular)
        self.button_simular.grid(row=3, columnspan=2, pady=10)

        self.resultados_text = tk.Text(self.frame, height=10, width=40)
        self.resultados_text.grid(row=4, columnspan=2)

    def simular(self):
        nodos = self.entry_nodos.get().split(',')
        llegadas_por_nodo = [int(x) for x in self.entry_llegadas.get().split(',')]
        tiempo_simulacion = int(self.entry_tiempo_simulacion.get())

        modelo = ModeloRed(nodos, llegadas_por_nodo)
        modelo.ejecutar_simulacion(tiempo_simulacion)

        self.resultados_text.delete(1.0, tk.END)
        for k, v in modelo.resultados.items():
            probabilidad = v / sum(llegadas_por_nodo)
            self.resultados_text.insert(tk.END, f"Probabilidad de cliente en nodo {k[1]} después de estar en nodo {k[0]}: {probabilidad:.4f}\n")

def main():
    root = tk.Tk()
    app = InterfazGrafica(root)
    root.mainloop()

if __name__ == "__main__":
    main()
