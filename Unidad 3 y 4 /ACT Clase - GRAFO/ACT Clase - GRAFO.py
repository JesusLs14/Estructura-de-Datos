import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import networkx as nx

class Vertice:
    def __init__(self, elemento):
        self.elemento = elemento 

    def __str__(self):
        return str(self.elemento)

class Arista:
    def __init__(self, origen, destino, elemento, dirigida=False):
        self.origen = origen
        self.destino = destino
        self.elemento = elemento
        self.dirigida = dirigida

    def __str__(self):
        conector = " -> " if self.dirigida else " -- "
        return f"({self.origen}{conector}{self.destino} : {self.elemento})"

class Grafo:
    def __init__(self):
        self._vertices = []
        self._aristas = []

    def numVertices(self):
        return len(self._vertices)

    def numAristas(self):
        return len(self._aristas)

    def vertices(self):
        return self._vertices

    def aristas(self):
        return self._aristas

    def buscarVerticePorInfo(self, elemento_str):
        for v in self._vertices:
            if str(v.elemento) == str(elemento_str):
                return v
        return None

    def insertaVertice(self, o):
        if self.buscarVerticePorInfo(o):
            raise ValueError("El vértice ya existe.")
        nuevo_vertice = Vertice(o)
        self._vertices.append(nuevo_vertice)
        return nuevo_vertice

    def insertaArista(self, v_info, w_info, o):
        v = self.buscarVerticePorInfo(v_info)
        w = self.buscarVerticePorInfo(w_info)
        if not v or not w:
            raise ValueError("Vértices no existen.")
        nueva_arista = Arista(v, w, o, dirigida=False)
        self._aristas.append(nueva_arista)
        return nueva_arista

    def insertaAristaDirigida(self, v_info, w_info, o):
        v = self.buscarVerticePorInfo(v_info)
        w = self.buscarVerticePorInfo(w_info)
        if not v or not w:
            raise ValueError("Vértices no existen.")
        nueva_arista = Arista(v, w, o, dirigida=True)
        self._aristas.append(nueva_arista)
        return nueva_arista

    def eliminaVertice(self, v_info):
        v = self.buscarVerticePorInfo(v_info)
        if not v:
            raise ValueError("El vértice no existe.")
        self._aristas = [a for a in self._aristas if a.origen != v and a.destino != v]
        self._vertices.remove(v)

class GrafoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TDA Grafo - Visualización Dinámica")
        self.root.geometry("1000x700")
        
        self.grafo = Grafo()

        frame_izq = tk.Frame(root, width=280, bg="#f5f5f5", padx=10, pady=10)
        frame_izq.pack(side=tk.LEFT, fill=tk.Y)

        self.frame_der = tk.Frame(root, padx=5, pady=5)
        self.frame_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        frame_consola = tk.Frame(self.frame_der)
        frame_consola.pack(side=tk.TOP, fill=tk.X)
        self.txt_consola = tk.Text(frame_consola, height=7, bg="black", fg="white", font=("Courier", 10))
        self.txt_consola.pack(fill=tk.BOTH)

        self.frame_visual = tk.Frame(self.frame_der, bg="white")
        self.frame_visual.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        tk.Label(frame_izq, text="OPERACIONES", font=("Arial", 12, "bold"), bg="#f5f5f5").pack(pady=(0,15))

        tk.Label(frame_izq, text="[+] AGREGAR VÉRTICE (o)", font=("Arial", 10, "bold"), bg="#f5f5f5", anchor="w").pack(fill=tk.X)
        self.entry_vertice = tk.Entry(frame_izq)
        self.entry_vertice.pack(fill=tk.X, pady=(0, 5))
        tk.Button(frame_izq, text="insertaVertice(o)", command=self.agregar_vertice).pack(fill=tk.X, pady=(0,15))

        tk.Label(frame_izq, text="[<->] AGREGAR ARISTA", font=("Arial", 10, "bold"), bg="#f5f5f5", anchor="w").pack(fill=tk.X)
        
        tk.Label(frame_izq, text="Origen (v):", bg="#f5f5f5").pack(anchor="w")
        self.combo_origen = ttk.Combobox(frame_izq, state="readonly")
        self.combo_origen.pack(fill=tk.X)

        tk.Label(frame_izq, text="Destino (w):", bg="#f5f5f5").pack(anchor="w")
        self.combo_destino = ttk.Combobox(frame_izq, state="readonly")
        self.combo_destino.pack(fill=tk.X)

        tk.Label(frame_izq, text="Info Arista (o):", bg="#f5f5f5").pack(anchor="w")
        self.entry_arista = tk.Entry(frame_izq)
        self.entry_arista.pack(fill=tk.X, pady=(0, 5))

        self.var_dirigida = tk.BooleanVar()
        tk.Checkbutton(frame_izq, text="Es Dirigida", variable=self.var_dirigida, bg="#f5f5f5").pack(anchor="w")

        tk.Button(frame_izq, text="insertaArista(...) / Dirigida(...)", command=self.agregar_arista).pack(fill=tk.X, pady=(0,15))

        tk.Label(frame_izq, text="[-] ELIMINAR VÉRTICE (v)", font=("Arial", 10, "bold"), bg="#f5f5f5", anchor="w").pack(fill=tk.X)
        tk.Button(frame_izq, text="eliminaVertice(v)", command=self.eliminar_vertice).pack(fill=tk.X, pady=(0,15))

        tk.Label(frame_izq, text="[?] CONSULTAS", font=("Arial", 10, "bold"), bg="#f5f5f5", anchor="w").pack(fill=tk.X)
        
        tk.Button(frame_izq, text="Listar Datos y numVertices()", command=self.listar_todo).pack(fill=tk.X, pady=2)
        tk.Button(frame_izq, text="Limpiar Consola y Gráfico", command=self.limpiar_consola_y_grafico).pack(fill=tk.X, pady=2)

        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.ax.axis('off')

        self.canvas_visual = FigureCanvasTkAgg(self.fig, master=self.frame_visual)
        self.canvas_visual.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas_visual, self.frame_visual)
        self.toolbar.update()
        self.canvas_visual.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.log("Sistema Grafo Visualizado Inicializado. Listo para operaciones.")
        self.actualizar_visualizacion()

    def actualizar_comboboxes(self):
        nombres_vertices = [str(v) for v in self.grafo.vertices()]
        self.combo_origen['values'] = nombres_vertices
        self.combo_destino['values'] = nombres_vertices

    def agregar_vertice(self):
        info = self.entry_vertice.get().strip()
        if not info:
            messagebox.showwarning("Error", "Debe ingresar información para el vértice.")
            return
        try:
            self.grafo.insertaVertice(info)
            self.log(f"-> Vértice insertado: '{info}'")
            self.entry_vertice.delete(0, tk.END)
            self.actualizar_comboboxes()
            self.actualizar_visualizacion()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def agregar_arista(self):
        origen = self.combo_origen.get()
        destino = self.combo_destino.get()
        info = self.entry_arista.get().strip()
        dirigida = self.var_dirigida.get()

        if not origen or not destino or not info:
            messagebox.showwarning("Error", "Faltan datos para la arista (origen, destino o info).")
            return

        try:
            if dirigida:
                self.grafo.insertaAristaDirigida(origen, destino, info)
                self.log(f"-> Arista Dirigida: ({origen} -> {destino} : {info})")
            else:
                self.grafo.insertaArista(origen, destino, info)
                self.log(f"-> Arista No Dirigida: ({origen} -- {destino} : {info})")
            self.entry_arista.delete(0, tk.END)
            self.actualizar_visualizacion()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def eliminar_vertice(self):
         seleccion = self.combo_origen.get()
         if not seleccion:
             messagebox.showwarning("Error", "Seleccione un vértice en 'Origen (v)' para eliminar.")
             return
         if messagebox.askyesno("Confirmar", f"¿Eliminar vértice '{seleccion}' y sus aristas incidentes?"):
            try:
                self.grafo.eliminaVertice(seleccion)
                self.log(f"-> Vértice '{seleccion}' y sus aristas eliminados.")
                self.actualizar_comboboxes()
                self.combo_origen.set('')
                self.combo_destino.set('')
                self.actualizar_visualizacion()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def actualizar_visualizacion(self):
        self.ax.clear()
        self.ax.axis('off')

        G_nx = nx.DiGraph() 

        for v in self.grafo.vertices():
            v_id = str(v.elemento)
            G_nx.add_node(v_id)

        edges_dir = []
        edges_undir = []
        edge_labels = {}

        for a in self.grafo.aristas():
            u_id = str(a.origen.elemento)
            v_id = str(a.destino.elemento)
            label = str(a.elemento)

            G_nx.add_edge(u_id, v_id)
            edge_labels[(u_id, v_id)] = label

            if a.dirigida:
                edges_dir.append((u_id, v_id))
            else:
                edges_undir.append((u_id, v_id))

        if G_nx.number_of_nodes() == 0:
             self.canvas_visual.draw()
             return

        pos = nx.spring_layout(G_nx, seed=42, k=1.0)

        nx.draw_networkx_nodes(G_nx, pos, ax=self.ax, node_color='#b3e5fc', node_size=1500, edgecolors='black')
        nx.draw_networkx_labels(G_nx, pos, ax=self.ax, font_size=10, font_weight='bold')

        nx.draw_networkx_edges(G_nx, pos, ax=self.ax, edgelist=edges_undir, edge_color='#4caf50', width=2, arrows=False)
        nx.draw_networkx_edges(G_nx, pos, ax=self.ax, edgelist=edges_dir, edge_color='#e53935', width=2, arrows=True, arrowsize=20, connectionstyle="arc3,rad=0.1")

        nx.draw_networkx_edge_labels(G_nx, pos, edge_labels=edge_labels, ax=self.ax, font_size=9, label_pos=0.6)

        self.fig.tight_layout()
        self.canvas_visual.draw()

    def listar_todo(self):
        verts = [str(v) for v in self.grafo.vertices()]
        aris = [str(a) for a in self.grafo.aristas()]
        self.log(f"==============================")
        self.log(f"DATOS ACTUALES DEL GRAFO:")
        self.log(f"numVertices(): {self.grafo.numVertices()}")
        self.log(f"Vértices: {verts}")
        self.log(f"numAristas(): {self.grafo.numAristas()}")
        self.log("Aristas:")
        for a in aris:
            self.log("  " + a)
        self.log(f"==============================")

    def log(self, mensaje):
        self.txt_consola.insert(tk.END, mensaje + "\n")
        self.txt_consola.see(tk.END)

    def limpiar_consola_y_grafico(self):
        self.txt_consola.delete(1.0, tk.END)
        self.grafo = Grafo()
        self.actualizar_comboboxes()
        self.actualizar_visualizacion()
        self.log("Sistema Reiniciado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GrafoGUI(root)
    root.mainloop()
    root = tk.Tk()
    app = GrafoGUI(root)
    root.mainloop()