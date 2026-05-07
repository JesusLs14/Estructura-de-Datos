"""
╔══════════════════════════════════════════════════════════════════════════╗
║   VISUALIZACIÓN DE ALGORITMOS DE ORDENAMIENTO EXTERNO  v3.0             ║
║   1. Intercalación   2. Mezcla Directa   3. Mezcla Equilibrada          ║
║   ── SOPORTE MULTIDATO: NÚMEROS, LETRAS, FECHAS, SÍMBOLOS Y MIXTOS ──   ║
╚══════════════════════════════════════════════════════════════════════════╝

Formatos de archivo soportados para carga de datos:
  • .txt   → Elementos separados por comas, tabulaciones o saltos de línea
  • .csv   → Lee todas las celdas disponibles
  • .json  → Array plano o array de objetos (extrae valores primitivos)
  • .xml   → Etiquetas <value>, <item>, <data>, etc.
  • .yaml  → Lista plana o bajo una clave
  • .xlsx / .xls → Muestra un menú para seleccionar qué hojas leer (detecta fechas)
  • .npy   → Array NumPy unidimensional
"""

import csv, json, os, re, datetime
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np
from matplotlib.patches import FancyBboxPatch
from matplotlib.widgets import RadioButtons, Button, CheckButtons
from tkinter import Tk, filedialog, messagebox

# ─── Paleta de colores ────────────────────────────────────────────────────────
BG      = "#0d1117"
PANEL   = "#161b22"
BORDER  = "#30363d"
ACCENT1 = "#58a6ff"   # azul  – Intercalación
ACCENT2 = "#3fb950"   # verde – Mezcla Directa
ACCENT3 = "#f78166"   # coral – Mezcla Equilibrada
GOLD    = "#e3b341"
TEXT    = "#c9d1d9"
SUBTEXT = "#8b949e"
COMPARE = "#ff7b72"
MERGE_C = "#d2a8ff"
WARN    = "#ffa657"

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor":   PANEL,
    "axes.edgecolor":   BORDER,
    "text.color":       TEXT,
    "axes.labelcolor":  TEXT,
    "xtick.color":      SUBTEXT,
    "ytick.color":      SUBTEXT,
    "font.family":      "monospace",
})


# ══════════════════════════════════════════════════════════════════════════════
#  UTILIDADES DE PARSEO Y TIPOS DE DATOS
# ══════════════════════════════════════════════════════════════════════════════

def parsear_valor(val):
    """Intenta convertir un valor bruto a su tipo ideal (int, float, date o str)."""
    if val is None or str(val).strip() == "":
        return None
    
    if isinstance(val, (int, float)):
        return val
        
    # Si es fecha de Excel/Python
    if isinstance(val, datetime.datetime):
        return val.strftime("%Y-%m-%d %H:%M")
    if isinstance(val, datetime.date):
        return val.strftime("%Y-%m-%d")
        
    if isinstance(val, str):
        val = val.strip()
        # Intentar numérico
        try:
            if '.' in val:
                return float(val)
            return int(val)
        except ValueError:
            return val # Se queda como string (letras, símbolos)
            
    return str(val)

def unificar_tipos_para_ordenar(datos: list) -> list:
    """
    Python 3 prohíbe comparar (ej. 1 < "A"). 
    Si todos los datos son números, se dejan como números.
    Si hay una mezcla de letras, símbolos y números, se convierte TODO a string.
    """
    if not datos:
        return []
        
    todo_numero = all(isinstance(x, (int, float)) for x in datos)
    if todo_numero:
        return datos
    
    # Si hay mezcla, convertimos todo a string para orden lexicográfico
    return [str(x) for x in datos]


# ══════════════════════════════════════════════════════════════════════════════
#  CARGADOR DE ARCHIVOS Y PARÁMETROS
# ══════════════════════════════════════════════════════════════════════════════

def ventana_seleccion_hojas(hojas: list[str]) -> list[str]:
    import tkinter as tk
    from tkinter import messagebox
    
    root = tk.Tk()
    root.title("Parámetros: Hojas de Excel")
    root.attributes("-topmost", True)
    
    tk.Label(root, text="El archivo Excel tiene múltiples hojas.\nSelecciona cuáles deseas procesar:", 
             font=("Helvetica", 10, "bold"), padx=15, pady=10).pack()
    
    frame = tk.Frame(root, padx=20)
    frame.pack(anchor="w")
    
    vars_check = []
    for h in hojas:
        var = tk.IntVar(value=1)
        vars_check.append(var)
        tk.Checkbutton(frame, text=h, variable=var, font=("Helvetica", 10)).pack(anchor="w")
        
    seleccion = []
    def confirmar():
        for i, v in enumerate(vars_check):
            if v.get() == 1:
                seleccion.append(hojas[i])
        if not seleccion:
            messagebox.showwarning("Atención", "Debes seleccionar al menos una hoja.")
            return
        root.quit()
        
    tk.Button(root, text="✔ Cargar Seleccionadas", command=confirmar, bg="#3fb950", fg="white", 
              font=("Helvetica", 10, "bold"), pady=5, padx=10).pack(pady=10)
    
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
    root.destroy()
    return seleccion


def cargar_archivo(ruta: str) -> list:
    ext = os.path.splitext(ruta)[1].lower()
    resultados = []

    if ext == ".txt":
        with open(ruta, encoding="utf-8") as f:
            texto = f.read()
        # En TXT separamos por comas, saltos de línea o tabulaciones
        partes = re.split(r'[,\n\t]+', texto)
        for p in partes:
            val = parsear_valor(p)
            if val is not None: resultados.append(val)

    elif ext == ".csv":
        with open(ruta, encoding="utf-8") as f:
            reader = csv.reader(f)
            for fila in reader:
                for celda in fila:
                    val = parsear_valor(celda)
                    if val is not None: resultados.append(val)

    elif ext == ".json":
        with open(ruta, encoding="utf-8") as f:
            data = json.load(f)
        resultados = _extraer_primitivos_json(data)

    elif ext == ".xml":
        import xml.etree.ElementTree as ET
        tree = ET.parse(ruta)
        root = tree.getroot()
        for tag in ("value", "item", "number", "data", "val", "text", "word"):
            for elem in root.iter(tag):
                val = parsear_valor(elem.text)
                if val is not None: resultados.append(val)
        if not resultados:
            for elem in root.iter():
                if elem.text and elem.text.strip():
                    val = parsear_valor(elem.text)
                    if val is not None: resultados.append(val)

    elif ext in (".yaml", ".yml"):
        try: import yaml
        except ImportError: raise ImportError("Instala PyYAML:  pip install pyyaml")
        with open(ruta, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        resultados = _extraer_primitivos_json(data)

    elif ext == ".xlsx":
        try: import openpyxl
        except ImportError: raise ImportError("Instala openpyxl:  pip install openpyxl")
        wb = openpyxl.load_workbook(ruta, read_only=True, data_only=True)
        hojas = wb.sheetnames
        seleccionadas = ventana_seleccion_hojas(hojas) if len(hojas) > 1 else hojas
            
        for h in seleccionadas:
            ws = wb[h]
            for fila in ws.iter_rows(values_only=True):
                for celda in fila:
                    val = parsear_valor(celda)
                    if val is not None: resultados.append(val)
        wb.close()

    elif ext == ".xls":
        try: import xlrd
        except ImportError: raise ImportError("Instala xlrd:  pip install xlrd")
        wb = xlrd.open_workbook(ruta)
        hojas = wb.sheet_names()
        seleccionadas = ventana_seleccion_hojas(hojas) if len(hojas) > 1 else hojas
            
        for h in seleccionadas:
            ws = wb.sheet_by_name(h)
            for r in range(ws.nrows):
                for c in range(ws.ncols):
                    cell_val = ws.cell_value(r, c)
                    val = parsear_valor(cell_val)
                    if val is not None: resultados.append(val)

    elif ext == ".npy":
        arr = np.load(ruta, allow_pickle=True).flatten()
        for x in arr:
            val = parsear_valor(x)
            if val is not None: resultados.append(val)
    else:
        raise ValueError(f"Extensión '{ext}' no soportada.")

    if not resultados:
        raise ValueError("El archivo está vacío o no se reconocieron datos.")
    return resultados


def _extraer_primitivos_json(data) -> list:
    nums = []
    if isinstance(data, list):
        for item in data:
            if isinstance(item, (int, float, str)):
                v = parsear_valor(item)
                if v is not None: nums.append(v)
            elif isinstance(item, (dict, list)):
                nums.extend(_extraer_primitivos_json(item))
    elif isinstance(data, dict):
        for v in data.values(): 
            nums.extend(_extraer_primitivos_json(v))
    return nums


def abrir_dialogo_archivo() -> tuple[list | None, str]:
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    tipos = [
        ("Formatos soportados", "*.txt *.csv *.json *.xml *.yaml *.yml *.xlsx *.xls *.npy"),
        ("Todos los archivos", "*.*"),
    ]
    rutas = filedialog.askopenfilenames(title="Seleccionar archivo(s) de datos", filetypes=tipos)
    root.destroy()

    if not rutas: return None, ""

    datos_totales = []
    nombres = []
    try:
        for ruta in rutas:
            datos = cargar_archivo(ruta)
            datos_totales.extend(datos)
            nombres.append(os.path.basename(ruta))
        return datos_totales, ", ".join(nombres)
    except Exception as e:
        root2 = Tk()
        root2.withdraw()
        messagebox.showerror("Error al leer los archivos", str(e))
        root2.destroy()
        return None, ""


# ══════════════════════════════════════════════════════════════════════════════
#  UTILIDADES DE DIBUJO
# ══════════════════════════════════════════════════════════════════════════════

def format_text_for_box(val, max_len=6):
    """Trunca el texto si es muy largo para que no se salga de la caja visual."""
    s = str(val)
    if len(s) > max_len:
        return s[:max_len-1] + "…"
    return s

def draw_array(ax, data, colors, y=0, cell_h=0.7, label="", title_color=TEXT, cell_w=0.9, fontsize=11):
    n = len(data)
    # Reducir fuente si la caja es muy pequeña
    dynamic_font = fontsize if cell_w >= 0.7 else (fontsize - 3)
    
    for i, (val, col) in enumerate(zip(data, colors)):
        rect = FancyBboxPatch((i * cell_w, y), cell_w - 0.05, cell_h,
                              boxstyle="round,pad=0.05", fc=col, ec=BORDER, lw=1.2)
        ax.add_patch(rect)
        
        texto_mostrar = format_text_for_box(val, max_len=int(cell_w * 10))
        
        ax.text(i * cell_w + (cell_w - 0.05) / 2, y + cell_h / 2, texto_mostrar,
                ha="center", va="center",
                fontsize=dynamic_font, fontweight="bold",
                color=BG if col != PANEL else TEXT)
    if label:
        ax.text(-0.6, y + cell_h / 2, label, ha="right", va="center", fontsize=9, color=title_color, fontweight="bold")
    return n

def section_title(ax, text, color, fontsize=13):
    ax.set_title(text, color=color, fontsize=fontsize, fontweight="bold", pad=10, loc="left",
                 path_effects=[pe.withStroke(linewidth=3, foreground=BG)])

def calcular_cell_w(n: int) -> float:
    if n <= 10: return 0.9
    if n <= 20: return 0.7
    if n <= 40: return 0.5
    return 0.4

def normalizar_datos(datos: list, max_n: int = 40) -> list:
    if len(datos) > max_n:
        datos = datos[:max_n]
    return datos


# ══════════════════════════════════════════════════════════════════════════════
#  ALGORITMOS DE ORDENAMIENTO (CON SOPORTE MULTITIPO)
# ══════════════════════════════════════════════════════════════════════════════

def demo_intercalacion(ax, datos: list):
    n2 = len(datos) // 2
    A = sorted(datos[:n2])
    B = sorted(datos[n2:])
    merged_so_far = []
    steps = []
    ai, bi = 0, 0
    while ai < len(A) and bi < len(B):
        if A[ai] <= B[bi]:
            steps.append(("A", ai, bi, A[ai])); ai += 1
        else:
            steps.append(("B", ai, bi, B[bi])); bi += 1
    while ai < len(A):
        steps.append(("A", ai, bi, A[ai])); ai += 1
    while bi < len(B):
        steps.append(("B", ai, bi, B[bi])); bi += 1

    ptr = {"A": 0, "B": 0}
    cw = calcular_cell_w(max(len(A), len(B)))

    def render(frame):
        ax.cla()
        ax.set_xlim(-1, max(len(A), len(B)) * cw + 1)
        ax.set_ylim(-1, 5.5)
        ax.axis("off")
        section_title(ax, "[1] INTERCALACIÓN  —  Fusión de dos mitades ordenadas", ACCENT1)

        nonlocal merged_so_far
        si = frame % (len(steps) + 4)
        if si < len(steps):
            src, ai2, bi2, _ = steps[si]
            ptr["A"] = ai2; ptr["B"] = bi2
            merged_so_far = [steps[k][3] for k in range(si + 1)]
        elif si >= len(steps):
            merged_so_far = [s[3] for s in steps]

        colA = [SUBTEXT if k < ptr["A"] else ACCENT1 for k in range(len(A))]
        colB = [SUBTEXT if k < ptr["B"] else ACCENT2 for k in range(len(B))]

        draw_array(ax, A, colA, y=3.2, label="Mitad A", title_color=ACCENT1, cell_w=cw)
        draw_array(ax, B, colB, y=2.0, label="Mitad B", title_color=ACCENT2, cell_w=cw)

        if si < len(steps):
            xi = min(ptr["A"], len(A) - 1) * cw + cw / 2
            ax.annotate("", xy=(xi, 3.2), xytext=(xi, 2.0 + 0.7), arrowprops=dict(arrowstyle="<->", color=GOLD, lw=1.5))

        col_res = [MERGE_C] * len(merged_so_far) + [PANEL] * (len(A) + len(B) - len(merged_so_far))
        draw_array(ax, merged_so_far + [""] * (len(A) + len(B) - len(merged_so_far)),
                   col_res, y=0.5, label="Resultado", title_color=MERGE_C, cell_w=cw)
        estado = f"Paso {min(si+1, len(steps))} / {len(steps)}  →  fusionados: {len(merged_so_far)}"
        ax.text(0, -0.5, estado, fontsize=8, color=GOLD)

    return render, len(steps) + 5

def generar_pasadas_mezcla_directa(data):
    estados = [data[:]]
    arr = data[:]
    n = len(arr)
    size = 1
    while size < n:
        nueva = []
        for left in range(0, n, size * 2):
            mid   = min(left + size, n)
            right = min(left + size * 2, n)
            L, R  = arr[left:mid], arr[mid:right]
            merged = []
            i2, j2 = 0, 0
            while i2 < len(L) and j2 < len(R):
                if L[i2] <= R[j2]: merged.append(L[i2]); i2 += 1
                else: merged.append(R[j2]); j2 += 1
            merged += L[i2:] + R[j2:]
            nueva += merged
        arr = nueva
        estados.append(arr[:])
        size *= 2
    return estados

def demo_mezcla_directa(ax, datos: list):
    estados = generar_pasadas_mezcla_directa(datos)
    total_frames = (len(estados) + 1) * 8
    cw = calcular_cell_w(len(datos))
    block_colors = [ACCENT1, ACCENT2, ACCENT3, GOLD, MERGE_C, "#79c0ff", "#56d364", "#ffa657"]

    def render(frame):
        ax.cla()
        ax.set_xlim(-1.2, len(datos) * cw + 0.5)
        ax.set_ylim(-1, len(estados) * 1.5 + 2)
        ax.axis("off")
        section_title(ax, "[2] MEZCLA DIRECTA  —  Runs crecientes por pasada", ACCENT2)

        pasada_actual = min(frame // 8, len(estados) - 1)
        for p, estado in enumerate(estados[:pasada_actual + 1]):
            y_pos = (len(estados) - p - 1) * 1.4 + 0.2
            label_p = f"Pasada {p}" if p > 0 else "Original"
            cols = [block_colors[(k // (2 ** p if p > 0 else 1)) % len(block_colors)] for k in range(len(estado))]
            draw_array(ax, estado, cols, y=y_pos, label=label_p, title_color=ACCENT2, cell_w=cw)

        size = 2 ** pasada_actual if pasada_actual > 0 else 1
        ax.text(0, -0.6, f"Pasada {pasada_actual}: bloques de tamaño {size}  →  {len(estados)-1} pasadas", fontsize=8, color=GOLD)

    return render, total_frames

def demo_mezcla_equilibrada(ax, datos: list):
    k = 2
    run_size = 2
    runs = [sorted(datos[i:i+run_size]) for i in range(0, len(datos), run_size)]
    cintas_in = [[] for _ in range(k)]
    for idx, run in enumerate(runs): cintas_in[idx % k].append(run)

    pasadas = [{"in": [list(c) for c in cintas_in], "out": None, "label": "Distribución inicial"}]
    fuente = cintas_in
    for _ in range(8):
        cintas_out = [[] for _ in range(k)]
        min_len = min(len(c) for c in fuente)
        if min_len == 0: break
        merged_runs = []
        for j in range(min_len):
            combined = []
            for c in fuente: combined += c[j]
            combined.sort()
            merged_runs.append(combined)
        for idx2, mr in enumerate(merged_runs): cintas_out[idx2 % k].append(mr)
        pasadas.append({"in": [list(c) for c in fuente], "out": [list(c) for c in cintas_out], "label": f"Pasada {len(pasadas)}"})
        fuente = cintas_out
        if all(len(c) <= 1 for c in fuente): break

    total_frames = len(pasadas) * 10 + 5
    colors_cinta = [ACCENT1, ACCENT3, ACCENT2, GOLD]

    def render(frame):
        ax.cla()
        ax.set_xlim(-0.5, 14)
        ax.set_ylim(-1, 7)
        ax.axis("off")
        section_title(ax, "[3] MEZCLA EQUILIBRADA  —  k=2 cintas alternas", ACCENT3)

        p_idx = min(frame // 10, len(pasadas) - 1)
        pasada = pasadas[p_idx]

        ax.text(0, 5.6, "CINTAS ENTRADA", fontsize=8, color=SUBTEXT, fontweight="bold")
        for ci, cinta in enumerate(pasada["in"]):
            y_c = 4.5 - ci * 1.3
            ax.text(-0.4, y_c + 0.35, f"C{ci+1}", fontsize=9, color=colors_cinta[ci], fontweight="bold", ha="right")
            x_off = 0
            for run in cinta:
                for val in run:
                    rect = FancyBboxPatch((x_off, y_c), 0.8, 0.65, boxstyle="round,pad=0.04", fc=colors_cinta[ci], ec=BORDER, lw=1)
                    ax.add_patch(rect)
                    
                    texto_mostrar = format_text_for_box(val, max_len=7)
                    ax.text(x_off + 0.4, y_c + 0.325, texto_mostrar, ha="center", va="center", fontsize=8, fontweight="bold", color=BG)
                    x_off += 0.85
                ax.plot([x_off + 0.05, x_off + 0.05], [y_c, y_c + 0.65], color=BORDER, lw=2, ls="--")
                x_off += 0.35

        ax.annotate("", xy=(5.8, 2.6), xytext=(5.8, 3.5), arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=2))
        ax.text(6.0, 3.0, pasada["label"], fontsize=9, color=GOLD, fontweight="bold")

        if pasada.get("out"):
            ax.text(0, 2.4, "CINTAS SALIDA", fontsize=8, color=SUBTEXT, fontweight="bold")
            for ci, cinta in enumerate(pasada["out"]):
                y_c = 1.3 - ci * 1.2
                ax.text(-0.4, y_c + 0.35, f"S{ci+1}", fontsize=9, color=MERGE_C, fontweight="bold", ha="right")
                x_off = 0
                for run in cinta:
                    for val in run:
                        rect = FancyBboxPatch((x_off, y_c), 0.8, 0.65, boxstyle="round,pad=0.04", fc=MERGE_C, ec=BORDER, lw=1)
                        ax.add_patch(rect)
                        texto_mostrar = format_text_for_box(val, max_len=7)
                        ax.text(x_off + 0.4, y_c + 0.325, texto_mostrar, ha="center", va="center", fontsize=8, fontweight="bold", color=BG)
                        x_off += 0.85
                    x_off += 0.35
        else:
            ax.text(2, 1.5, "← Distribuyendo runs...", fontsize=9, color=SUBTEXT)

        ax.text(0, -0.7, f"k={k} cintas  |  Paso {p_idx+1}/{len(pasadas)}  |  Tamaño de runs: {run_size * (2**p_idx)}", fontsize=8, color=GOLD)

    return render, total_frames


# ══════════════════════════════════════════════════════════════════════════════
#  MODO COMPARACIÓN Y MENÚ PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

def vista_comparacion(fig, datos: list, seleccionados: list[bool]):
    fig.clear()
    activos = [i for i, s in enumerate(seleccionados) if s]
    if not activos:
        ax = fig.add_subplot(111, facecolor=PANEL)
        ax.axis("off")
        ax.text(0.5, 0.5, "Selecciona al menos un método", ha="center", va="center", fontsize=14, color=WARN, transform=ax.transAxes)
        fig.canvas.draw_idle()
        return

    n = len(activos)
    axes = [fig.add_subplot(1, n, i + 1, facecolor=PANEL) for i in range(n)]
    for spine in sum([list(a.spines.values()) for a in axes], []): spine.set_edgecolor(BORDER)

    fns = [demo_intercalacion, demo_mezcla_directa, demo_mezcla_equilibrada]
    renders_and_frames = []
    for ax, idx in zip(axes, activos):
        rf = fns[idx](ax, datos[:])
        renders_and_frames.append(rf)

    nombres = ["Intercalación", "Mezcla Directa", "Mezcla Equilibrada"]
    fig.suptitle("COMPARACIÓN:  " + "   vs   ".join(nombres[i] for i in activos),
                 color=GOLD, fontsize=11, fontweight="bold", fontfamily="monospace",
                 path_effects=[pe.withStroke(linewidth=3, foreground=BG)])

    state = {"frame": 0, "playing": True}
    max_frames = max(mf for _, mf in renders_and_frames)

    ax_prev = fig.add_axes([0.01, 0.02, 0.08, 0.06], facecolor=PANEL)
    ax_play = fig.add_axes([0.11, 0.02, 0.10, 0.06], facecolor=PANEL)
    ax_next = fig.add_axes([0.23, 0.02, 0.08, 0.06], facecolor=PANEL)
    ax_rst  = fig.add_axes([0.33, 0.02, 0.12, 0.06], facecolor=PANEL)
    ax_back = fig.add_axes([0.80, 0.02, 0.18, 0.06], facecolor=PANEL)

    btn_prev = Button(ax_prev, "◀ Prev", color=PANEL, hovercolor=BORDER)
    btn_play = Button(ax_play, "⏸ Pausar", color=PANEL, hovercolor=BORDER)
    btn_next = Button(ax_next, "Next ▶", color=PANEL, hovercolor=BORDER)
    btn_rst  = Button(ax_rst, "↺ Reiniciar", color=PANEL, hovercolor=BORDER)
    btn_back = Button(ax_back, "← Volver al menú", color=PANEL, hovercolor=BORDER)

    for btn in (btn_prev, btn_play, btn_next, btn_rst, btn_back):
        btn.label.set_color(TEXT); btn.label.set_fontfamily("monospace"); btn.label.set_fontsize(8); btn.label.set_fontweight("bold")

    def redraw():
        for (rf, _), _ in zip(renders_and_frames, activos): rf(state["frame"])
        fig.canvas.draw_idle()

    def on_prev(_): state["playing"] = False; btn_play.label.set_text("▶ Reanudar"); state["frame"] = max(0, state["frame"] - 1); redraw()
    def on_play(_): state["playing"] = not state["playing"]; btn_play.label.set_text("⏸ Pausar" if state["playing"] else "▶ Reanudar"); fig.canvas.draw_idle()
    def on_next(_): state["playing"] = False; btn_play.label.set_text("▶ Reanudar"); state["frame"] = min(state["frame"] + 1, max_frames - 1); redraw()
    def on_rst(_): state["frame"] = 0; state["playing"] = True; btn_play.label.set_text("⏸ Pausar"); redraw()
    def on_back(_): timer.stop(); main()

    btn_prev.on_clicked(on_prev); btn_play.on_clicked(on_play); btn_next.on_clicked(on_next); btn_rst.on_clicked(on_rst); btn_back.on_clicked(on_back)

    def update(_):
        if state["playing"]:
            if state["frame"] < max_frames - 1: state["frame"] += 1; redraw()
            else: state["playing"] = False; btn_play.label.set_text("▶ Reanudar"); fig.canvas.draw_idle()

    timer = fig.canvas.new_timer(interval=700); timer.add_callback(update, None); timer.start(); redraw()


def main():
    datos_default = ["Zebra", 45, "@", "Auto", 12, "2023-01", "Sol", 5]
    
    datos_archivos = {"1": {"valores": [], "nombre": ""}, "2": {"valores": [], "nombre": ""}}
    datos_actuales = {"valores": unificar_tipos_para_ordenar(datos_default[:]), "nombre": "datos mixtos por defecto"}

    fig = plt.figure(figsize=(15, 9), facecolor=BG)
    fig.canvas.manager.set_window_title("Visualizador de Ordenamiento Externo Multitipo  v3.0")

    ax_radio   = fig.add_axes([0.01, 0.52, 0.17, 0.28], facecolor="#161b22")
    ax_check   = fig.add_axes([0.01, 0.30, 0.17, 0.20], facecolor="#161b22")
    ax_info    = fig.add_axes([0.01, 0.10, 0.17, 0.18], facecolor="#161b22")
    ax_vis     = fig.add_axes([0.21, 0.12, 0.77, 0.83], facecolor=PANEL)

    ax_prev    = fig.add_axes([0.21, 0.02, 0.07, 0.07], facecolor=PANEL)
    ax_play    = fig.add_axes([0.29, 0.02, 0.08, 0.07], facecolor=PANEL)
    ax_next    = fig.add_axes([0.38, 0.02, 0.07, 0.07], facecolor=PANEL)
    ax_rst     = fig.add_axes([0.46, 0.02, 0.08, 0.07], facecolor=PANEL)
    ax_arch1   = fig.add_axes([0.56, 0.02, 0.09, 0.07], facecolor=PANEL)
    ax_arch2   = fig.add_axes([0.66, 0.02, 0.09, 0.07], facecolor=PANEL)
    ax_comp    = fig.add_axes([0.77, 0.02, 0.11, 0.07], facecolor=PANEL)

    for spine in ax_vis.spines.values(): spine.set_edgecolor(BORDER); spine.set_linewidth(1.5)
    for a in (ax_radio, ax_check, ax_info):
        for sp in a.spines.values(): sp.set_edgecolor(BORDER); sp.set_linewidth(1)

    fig.text(0.09, 0.90, "ALGORITMOS\nDE MEZCLA", ha="center", va="top", fontsize=10, fontweight="bold", color=TEXT, fontfamily="monospace", path_effects=[pe.withStroke(linewidth=3, foreground=BG)])

    labels_radio = ["Intercalación", "Mezcla Directa", "Mzcla Equilibrada"]
    colors_btn   = [ACCENT1, ACCENT2, ACCENT3]
    radio = RadioButtons(ax_radio, labels_radio, activecolor=GOLD)
    for lbl, col in zip(radio.labels, colors_btn): lbl.set_color(col); lbl.set_fontfamily("monospace"); lbl.set_fontsize(9); lbl.set_fontweight("bold")

    ax_check.axis("off")
    ax_check.text(0.05, 0.97, "Comparar (marca varios):", transform=ax_check.transAxes, va="top", fontsize=8, color=SUBTEXT, fontfamily="monospace")
    ax_chk2 = fig.add_axes([0.015, 0.30, 0.165, 0.20], facecolor="#161b22")
    check = CheckButtons(ax_chk2, ["Intercalación", "Mezcla Directa", "M. Equilibrada"], [False, False, False])
    for lbl, col in zip(check.labels, colors_btn): lbl.set_color(col); lbl.set_fontfamily("monospace"); lbl.set_fontsize(8); lbl.set_fontweight("bold")

    state = {"selected": 0, "frame": 0, "playing": True, "render_fn": None, "max_frames": 1}
    fns_demo = [demo_intercalacion, demo_mezcla_directa, demo_mezcla_equilibrada]

    def actualizar_info(idx):
        ax_info.cla(); ax_info.axis("off")
        d = datos_actuales["valores"]
        
        texto_fuente = datos_actuales['nombre']
        if len(texto_fuente) > 25: texto_fuente = texto_fuente[:22] + "..."
            
        resumen = f"Datos Totales: {len(d)}\n"
        resumen += f"Fuente: {texto_fuente}\n"
        if len(d) > 0:
            resumen += "Tipo: Mixto (Texto/Núm)" if isinstance(d[0], str) else "Tipo: Solo Numérico"
            
        ax_info.text(0.05, 0.98, resumen + "\n\nSe ordenará " + ("alfabéticamente" if isinstance(d[0], str) else "numéricamente"),
                     transform=ax_info.transAxes, va="top", fontsize=7.5, color=TEXT, fontfamily="monospace")
        fig.canvas.draw_idle()

    def cargar_demo(idx):
        datos = normalizar_datos(datos_actuales["valores"]) 
        if not datos: return
        render_fn, max_f = fns_demo[idx](ax_vis, datos)
        state["render_fn"] = render_fn; state["max_frames"] = max_f; state["frame"] = 0; state["selected"] = idx
        actualizar_info(idx)
        fig.canvas.draw_idle()

    btn_prev  = Button(ax_prev,  "◀ Prev", color=PANEL, hovercolor=BORDER)
    btn_play  = Button(ax_play,  "⏸ Pausar", color=PANEL, hovercolor=BORDER)
    btn_next  = Button(ax_next,  "Next ▶", color=PANEL, hovercolor=BORDER)
    btn_rst   = Button(ax_rst,   "↺ Reiniciar", color=PANEL, hovercolor=BORDER)
    btn_arch1 = Button(ax_arch1, "📂 Arch 1", color="#182b40", hovercolor="#254261")
    btn_arch2 = Button(ax_arch2, "📂 Arch 2", color="#1f3a2b", hovercolor="#2d5a3d")
    btn_comp  = Button(ax_comp,  "⚡ Comparar", color="#3a1f2b", hovercolor="#5a2d40")

    for btn in (btn_prev, btn_play, btn_next, btn_rst, btn_arch1, btn_arch2, btn_comp):
        btn.label.set_color(TEXT); btn.label.set_fontfamily("monospace"); btn.label.set_fontsize(8); btn.label.set_fontweight("bold")
    btn_arch1.label.set_color(ACCENT1); btn_arch2.label.set_color(ACCENT2); btn_comp.label.set_color(ACCENT3)

    def on_prev(_): state["playing"] = False; btn_play.label.set_text("▶ Reanudar"); state["frame"] = max(0, state["frame"] - 1); state["render_fn"](state["frame"]); fig.canvas.draw_idle()
    def on_play(_): state["playing"] = not state["playing"]; btn_play.label.set_text("⏸ Pausar" if state["playing"] else "▶ Reanudar"); fig.canvas.draw_idle()
    def on_next(_): state["playing"] = False; btn_play.label.set_text("▶ Reanudar"); state["frame"] = min(state["frame"] + 1, state["max_frames"] - 1); state["render_fn"](state["frame"]); fig.canvas.draw_idle()
    def on_rst(_): state["frame"] = 0; state["playing"] = True; btn_play.label.set_text("⏸ Pausar"); state["render_fn"](0); fig.canvas.draw_idle()

    def agrupar_datos_globales():
        comb = []
        noms = []
        if datos_archivos["1"]["valores"]: comb.extend(datos_archivos["1"]["valores"]); noms.append("A1:"+datos_archivos["1"]["nombre"])
        if datos_archivos["2"]["valores"]: comb.extend(datos_archivos["2"]["valores"]); noms.append("A2:"+datos_archivos["2"]["nombre"])
            
        if comb:
            datos_actuales["valores"] = unificar_tipos_para_ordenar(comb)
            datos_actuales["nombre"] = " + ".join(noms)
        else:
            datos_actuales["valores"] = unificar_tipos_para_ordenar(datos_default[:])
            datos_actuales["nombre"] = "datos mixtos por defecto"

    def cargar_slot(slot):
        datos, nombre = abrir_dialogo_archivo()
        if datos is None: return
        datos_archivos[slot] = {"valores": datos, "nombre": nombre}
        agrupar_datos_globales()
        cargar_demo(state["selected"])
        ax_vis.text(0.5, 0.02, f"✔ Archivo {slot} cargado exitosamente.", ha="center", va="bottom", fontsize=8, color=ACCENT2, transform=ax_vis.transAxes, fontfamily="monospace")
        fig.canvas.draw_idle()

    def on_arch1(_): cargar_slot("1")
    def on_arch2(_): cargar_slot("2")

    def on_comparar(_):
        seleccionados = check.get_status()
        if not any(seleccionados): seleccionados = [True, True, True]
        datos = normalizar_datos(datos_actuales["valores"])
        timer.stop(); vista_comparacion(fig, datos, list(seleccionados))

    def on_radio(label):
        idx = labels_radio.index(label)
        state["playing"] = True; btn_play.label.set_text("⏸ Pausar"); cargar_demo(idx)

    radio.on_clicked(on_radio); btn_prev.on_clicked(on_prev); btn_play.on_clicked(on_play); btn_next.on_clicked(on_next); btn_rst.on_clicked(on_rst)
    btn_arch1.on_clicked(on_arch1); btn_arch2.on_clicked(on_arch2); btn_comp.on_clicked(on_comparar)

    ax_prog = fig.add_axes([0.21, 0.10, 0.77, 0.02], facecolor=BG); ax_prog.axis("off")
    prog_text = ax_prog.text(0.0, 0.5, "", va="center", fontsize=8, color=SUBTEXT, fontfamily="monospace")

    def update(_):
        if state["playing"] and state["render_fn"]:
            if state["frame"] < state["max_frames"] - 1: state["frame"] += 1; state["render_fn"](state["frame"])
            else: state["playing"] = False; btn_play.label.set_text("▶ Reanudar")
            pct = int(state["frame"] / max(state["max_frames"] - 1, 1) * 100)
            bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
            prog_text.set_text(f"[{bar}] {pct:3d}%  frame {state['frame']}/{state['max_frames']-1}")
            fig.canvas.draw_idle()

    timer = fig.canvas.new_timer(interval=700); timer.add_callback(update, None); timer.start()
    fig.text(0.09, 0.08, "Formatos:\n.txt .csv .json\n.xml .yaml .xlsx\n.xls .npy", ha="center", va="top", fontsize=6.5, color=SUBTEXT, fontfamily="monospace")
    cargar_demo(0)
    plt.show()

if __name__ == "__main__":
    main()