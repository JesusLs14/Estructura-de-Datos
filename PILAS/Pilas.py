import tkinter as tk
from tkinter import messagebox

class PilaVisual:
    def __init__(self, root, capacidad=8):
        self.root = root
        self.root.title("Visualizador de Estructura de Datos: Pila (Stack)")
        self.root.geometry("700x550")
        self.root.configure(bg="#f0f0f0")

        self.pila = []
        self.capacidad = capacidad

        self.color_pila = "#3498db"    
        self.color_cima = "#e74c3c"    
        self.color_fondo = "white"     
        self.fuente_ui = ("Arial", 12)
        self.fuente_bloque = ("Arial", 14, "bold")

        self._crear_widgets()
        self._actualizar_vista_grafica()

    def _crear_widgets(self):
        """Inicializa los componentes de la interfaz gráfica."""
        
        frame_controles = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        frame_controles.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(frame_controles, text="Operaciones", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=(0, 20))

        tk.Label(frame_controles, text="Valor del elemento:", font=self.fuente_ui, bg="#f0f0f0").pack(anchor="w")
        self.entry_valor = tk.Entry(frame_controles, font=self.fuente_ui, width=15)
        self.entry_valor.pack(pady=(0, 20))
        self.entry_valor.bind('<Return>', lambda event: self.operacion_push()) # Enter key support

        btn_estilo = {"font": self.fuente_ui, "width": 18, "pady": 5}
        
        tk.Button(frame_controles, text="Insertar (Push)", bg="#2ecc71", fg="white", 
                  command=self.operacion_push, **btn_estilo).pack(pady=5)
        
        tk.Button(frame_controles, text="Quitar (Pop)", bg="#e67e22", fg="white", 
                  command=self.operacion_pop, **btn_estilo).pack(pady=5)
        
        tk.Button(frame_controles, text="Ver Cima (Peek)", bg="#9b59b6", fg="white", 
                  command=self.operacion_peek, **btn_estilo).pack(pady=5)

        tk.Frame(frame_controles, height=2, bd=1, relief=tk.SUNKEN, bg="gray").pack(fill=tk.X, pady=20)

        tk.Button(frame_controles, text="¿Está Vacía?", command=self.comprobar_vacia, **btn_estilo).pack(pady=5)
        tk.Button(frame_controles, text="¿Está Llena?", command=self.comprobar_llena, **btn_estilo).pack(pady=5)

        self.frame_grafico = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        self.frame_grafico.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.ancho_canvas = 350
        self.alto_canvas = 480
        self.canvas = tk.Canvas(self.frame_grafico, width=self.ancho_canvas, 
                                height=self.alto_canvas, bg=self.color_fondo, bd=2, relief=tk.SOLID)
        self.canvas.pack()

        self.lbl_info = tk.Label(self.frame_grafico, text="Bienvenido. Inserte un elemento.", 
                                 font=("Arial", 12, "italic"), bg="#f0f0f0", fg="#555", wraplength=300)
        self.lbl_info.pack(pady=10)

    def _actualizar_vista_grafica(self):
        """Dibuja la pila completa en el canvas basándose en el estado de self.pila."""
        self.canvas.delete("all") 

        ancho_bloque = 250
        alto_bloque = 40
        espaciado = 5
        
        x_inicial = (self.ancho_canvas - ancho_bloque) // 2
        y_base = self.alto_canvas - 20 

        self.canvas.create_line(x_inicial - 10, 50, x_inicial - 10, y_base + 5, width=3, fill="#333") # Pared izq
        self.canvas.create_line(x_inicial + ancho_bloque + 10, 50, x_inicial + ancho_bloque + 10, y_base + 5, width=3, fill="#333") # Pared der
        self.canvas.create_line(x_inicial - 10, y_base + 5, x_inicial + ancho_bloque + 10, y_base + 5, width=3, fill="#333") # Suelo

        num_elementos = len(self.pila)
        for i in range(num_elementos):
            valor = self.pila[i]
            
            y_superior = y_base - ((i + 1) * (alto_bloque + espaciado))
            y_inferior = y_superior + alto_bloque

            es_cima = (i == num_elementos - 1)
            color_relleno = self.color_cima if es_cima else self.color_pila

            self.canvas.create_rectangle(x_inicial, y_superior, x_inicial + ancho_bloque, 
                                          y_inferior, fill=color_relleno, outline="#2c3e50", width=2)

            self.canvas.create_text(x_inicial + (ancho_bloque // 2), y_superior + (alto_bloque // 2), 
                                     text=str(valor), fill="white", font=self.fuente_bloque)
            
            if es_cima:
                self.canvas.create_text(x_inicial - 40, y_superior + (alto_bloque // 2), 
                                         text="CIMA ➔", fill=self.color_cima, font=("Arial", 10, "bold"))

    def _set_mensaje(self, msg, tipo="info"):
        """Actualiza la etiqueta de información con color."""
        colores = {"info": "#555", "error": "#c0392b", "exito": "#27ae60", "peek": "#8e44ad"}
        self.lbl_info.config(text=msg, fg=colores.get(tipo, "#555"))


    def operacion_push(self):
        """Método INSERTAR (Push)."""
        valor = self.entry_valor.get().strip()
        
        if not valor:
            self._set_mensaje("⚠️ Por favor, escribe un valor.", "error")
            return

        if len(self.pila) >= self.capacidad:
            self._set_mensaje(f"❌ Error: Stack Overflow. La pila está llena ({self.capacidad}).", "error")
            messagebox.showwarning("Stack Overflow", "No se pueden insertar más elementos.")
            return

        self.pila.append(valor)
        
        self.entry_valor.delete(0, tk.END) 
        self._actualizar_vista_grafica()
        self._set_mensaje(f"✅ Se insertó '{valor}' en la cima.", "exito")

    def operacion_pop(self):
        """Método QUITAR (Pop)."""
        if not self.pila:
            self._set_mensaje("❌ Error: Stack Underflow. La pila está vacía.", "error")
            messagebox.showwarning("Stack Underflow", "No hay nada que quitar.")
            return

        valor_quitado = self.pila.pop()
        
        self._actualizar_vista_grafica()
        self._set_mensaje(f"🟠 Se quitó '{valor_quitado}' de la cima.", "info")

    def operacion_peek(self):
        """Método VER CIMA (Peek)."""
        if not self.pila:
            self._set_mensaje("La pila está vacía, no hay cima.", "error")
            return

        cima = self.pila[-1]
        
        self._set_mensaje(f"👁️ El elemento en la cima es: '{cima}'", "peek")

    def comprobar_vacia(self):
        """Método SABER SI ESTÁ VACÍA."""
        vacia = (len(self.pila) == 0)
        msg = "Sí, la pila está vacía (0 elementos)." if vacia else f"No, tiene {len(self.pila)} elementos."
        tipo = "exito" if vacia else "info"
        self._set_mensaje(f"❓ Vacia: {msg}", tipo)

    def comprobar_llena(self):
        """Método SABER SI ESTÁ LLENA."""
        llena = (len(self.pila) == self.capacidad)
        msg = f"Sí, está llena ({self.capacidad}/{self.capacidad})." if llena else f"No, quedan {self.capacidad - len(self.pila)} espacios."
        tipo = "error" if llena else "info"
        self._set_mensaje(f"❓ Llena: {msg}", tipo)

if __name__ == "__main__":
    root = tk.Tk()
    app = PilaVisual(root, capacidad=8)
    root.mainloop()