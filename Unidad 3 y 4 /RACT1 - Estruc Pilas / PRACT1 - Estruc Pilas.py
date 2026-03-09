import tkinter as tk
from tkinter import messagebox

class LaboratorioPilas:
    def __init__(self, root, capacidad=8):
        self.root = root
        self.root.title("Laboratorio Manual de Pilas (Principal y Auxiliar)")
        self.root.geometry("900x650")
        self.root.configure(bg="#f0f0f0")

        self.pila_principal = []
        self.pila_auxiliar = []
        self.capacidad = capacidad
        self.animando = False  

        self.color_ppal = "#3498db"    
        self.color_aux = "#9b59b6"
        self.color_cima = "#e74c3c"    
        self.color_fondo = "white"     
        self.fuente_ui = ("Arial", 12)
        self.fuente_bloque = ("Arial", 14, "bold")

        self._crear_widgets()
        self._actualizar_vista_grafica()

    def _crear_widgets(self):
        frame_controles = tk.Frame(self.root, bg="#f0f0f0", padx=15, pady=15)
        frame_controles.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(frame_controles, text="Operaciones Manuales", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=(0, 15))

        tk.Label(frame_controles, text="Escribe el valor:", font=self.fuente_ui, bg="#f0f0f0").pack(anchor="w")
        self.entry_valor = tk.Entry(frame_controles, font=self.fuente_ui, width=15)
        self.entry_valor.pack(pady=(0, 15))

        btn_estilo = {"font": self.fuente_ui, "width": 18, "pady": 5}
        
        tk.Button(frame_controles, text="Insertar (Push)", bg="#2ecc71", fg="white", 
                  command=self.btn_push, **btn_estilo).pack(pady=5)
        
        tk.Button(frame_controles, text="Eliminar (Pop)", bg="#e67e22", fg="white", 
                  command=self.btn_pop, **btn_estilo).pack(pady=5)
        
        tk.Frame(frame_controles, height=2, bd=1, relief=tk.SUNKEN, bg="gray").pack(fill=tk.X, pady=20)

        tk.Button(frame_controles, text="Limpiar Todo", bg="#e74c3c", fg="white", 
                  command=self.reiniciar_pilas, **btn_estilo).pack(pady=5)

        # --- ÁREA GRÁFICA ---
        self.frame_grafico = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        self.frame_grafico.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.ancho_canvas = 550
        self.alto_canvas = 480
        self.canvas = tk.Canvas(self.frame_grafico, width=self.ancho_canvas, 
                                height=self.alto_canvas, bg=self.color_fondo, bd=2, relief=tk.SOLID)
        self.canvas.pack()

        self.lbl_info = tk.Label(self.frame_grafico, text="Ingresa un valor y selecciona Insertar o Eliminar.", 
                                 font=("Arial", 13, "bold"), bg="#f0f0f0", fg="#333", wraplength=500)
        self.lbl_info.pack(pady=15)

    def _dibujar_pila(self, pila, x_offset, titulo, color_base):
        ancho_bloque = 180
        alto_bloque = 40
        espaciado = 5
        y_base = self.alto_canvas - 40 

        self.canvas.create_line(x_offset - 10, 80, x_offset - 10, y_base + 5, width=3, fill="#333")
        self.canvas.create_line(x_offset + ancho_bloque + 10, 80, x_offset + ancho_bloque + 10, y_base + 5, width=3, fill="#333")
        self.canvas.create_line(x_offset - 10, y_base + 5, x_offset + ancho_bloque + 10, y_base + 5, width=3, fill="#333")
        
        self.canvas.create_text(x_offset + (ancho_bloque // 2), 35, text=titulo, font=("Arial", 14, "bold"), fill="#333")
        self.canvas.create_text(x_offset + (ancho_bloque // 2), 60, text=f"TOPE = {len(pila)}", font=("Arial", 12, "bold"), fill="blue")

        num_elementos = len(pila)
        for i in range(num_elementos):
            valor = pila[i]
            y_superior = y_base - ((i + 1) * (alto_bloque + espaciado))
            y_inferior = y_superior + alto_bloque

            es_cima = (i == num_elementos - 1)
            color_relleno = self.color_cima if es_cima else color_base

            self.canvas.create_rectangle(x_offset, y_superior, x_offset + ancho_bloque, 
                                          y_inferior, fill=color_relleno, outline="#2c3e50", width=2)
            self.canvas.create_text(x_offset + (ancho_bloque // 2), y_superior + (alto_bloque // 2), 
                                     text=str(valor), fill="white", font=self.fuente_bloque)

    def _actualizar_vista_grafica(self):
        self.canvas.delete("all") 
        self._dibujar_pila(self.pila_principal, 50, "PILA PRINCIPAL", self.color_ppal)
        self._dibujar_pila(self.pila_auxiliar, 320, "PILA AUXILIAR", self.color_aux)

    def _set_mensaje(self, msg, color="#333"):
        self.lbl_info.config(text=msg, fg=color)

    def reiniciar_pilas(self):
        if self.animando: return
        self.pila_principal = []
        self.pila_auxiliar = []
        self.entry_valor.delete(0, tk.END)
        self._actualizar_vista_grafica()
        self._set_mensaje("🔄 Pantalla limpiada.", "#333")

    def btn_push(self):
        if self.animando: return
        valor = self.entry_valor.get().strip()
        if not valor:
            self._set_mensaje("⚠️ Escribe un valor primero.", "#c0392b")
            return
            
        if len(self.pila_principal) >= self.capacidad:
            self._set_mensaje("❌ Error: Stack Overflow. La pila está llena.", "#c0392b")
            return

        self.pila_principal.append(valor)
        self.entry_valor.delete(0, tk.END)
        self._actualizar_vista_grafica()
        self._set_mensaje(f"✅ Se insertó '{valor}'. TOPE={len(self.pila_principal)}", "#27ae60")

    def btn_pop(self):
        if self.animando: return
        valor = self.entry_valor.get().strip()
        if not valor:
            self._set_mensaje("⚠️ Escribe qué valor quieres eliminar.", "#c0392b")
            return

        if not self.pila_principal:
            respuesta = messagebox.askyesno(
                "Stack Underflow", 
                f"La pila está vacía. No se puede eliminar '{valor}'.\n¿Deseas insertarlo y eliminarlo inmediatamente?"
            )
            if respuesta:
                self.animar_push_pop_inmediato(valor)
            return

        if self.pila_principal[-1] == valor:
            extraido = self.pila_principal.pop()
            self.entry_valor.delete(0, tk.END)
            self._actualizar_vista_grafica()
            self._set_mensaje(f"🟠 Se eliminó '{extraido}' de la cima. TOPE={len(self.pila_principal)}", "#e67e22")
            return

        if valor in self.pila_principal:
            respuesta = messagebox.askyesno(
                "Elemento Bloqueado",
                f"El elemento '{valor}' NO está en la cima. Sacarlo directamente rompería la regla LIFO.\n\n"
                f"¿Deseas usar la Pila Auxiliar para extraerlo sin perder los demás datos?"
            )
            if respuesta:
                self.entry_valor.delete(0, tk.END)
                self.animar_extraccion_auxiliar(valor)
            return

        respuesta = messagebox.askyesno(
            "Elemento No Encontrado",
            f"El elemento '{valor}' no existe en la pila.\n¿Deseas insertarlo y eliminarlo inmediatamente?"
        )
        if respuesta:
            self.animar_push_pop_inmediato(valor)

    def animar_push_pop_inmediato(self, valor):
        self.animando = True
        self.entry_valor.delete(0, tk.END)
        
        self.pila_principal.append(valor)
        self._actualizar_vista_grafica()
        self._set_mensaje(f"⚡ Insertando '{valor}' para eliminarlo de inmediato...", "#8e44ad")
        
        def hacer_pop():
            self.pila_principal.pop()
            self._actualizar_vista_grafica()
            self._set_mensaje(f"🟠 Se eliminó '{valor}'. TOPE={len(self.pila_principal)}", "#e67e22")
            self.animando = False
            
        self.root.after(1000, hacer_pop)

    def animar_extraccion_auxiliar(self, objetivo):
        self.animando = True
        secuencia = []
        indice_obj = self.pila_principal.index(objetivo)
        elementos_a_mover = len(self.pila_principal) - 1 - indice_obj
        
        def mover_a_aux():
            v = self.pila_principal.pop()
            self.pila_auxiliar.append(v)
            self._actualizar_vista_grafica()
            self._set_mensaje(f"Moviendo '{v}' a la Pila Auxiliar...", "#9b59b6")

        def extraer_obj():
            self.pila_principal.pop()
            self._actualizar_vista_grafica()
            self._set_mensaje(f"¡Objetivo '{objetivo}' extraído con éxito!", "#c0392b")

        def regresar_ppal():
            v = self.pila_auxiliar.pop()
            self.pila_principal.append(v)
            self._actualizar_vista_grafica()
            self._set_mensaje(f"Regresando '{v}' a la Principal...", "#3498db")
            
        def fin_animacion():
            self._set_mensaje(f"✅ Proceso terminado. '{objetivo}' fue eliminado usando la pila auxiliar.", "#27ae60")
            self.animando = False

        for _ in range(elementos_a_mover):
            secuencia.append(mover_a_aux)
            
        secuencia.append(extraer_obj)
        
        for _ in range(elementos_a_mover):
            secuencia.append(regresar_ppal)
            
        secuencia.append(fin_animacion)

        tiempo_base = 1200
        for i, accion in enumerate(secuencia):
            self.root.after(tiempo_base * (i + 1), accion)

if __name__ == "__main__":
    root = tk.Tk()
    app = LaboratorioPilas(root, capacidad=8)
    root.mainloop()
