import tkinter as tk
from tkinter import simpledialog, messagebox


root = tk.Tk()
root.withdraw() 

calificaciones = [0] * 5

for i in range(5):
    valor = simpledialog.askinteger("Entrada", f"Capture la calificación {i + 1}:")
        
        
    if valor is not None:
        calificaciones[i] = valor
    else:
        break 

 
messagebox.showinfo("Resultados", f"Calificaciones: {calificaciones}")