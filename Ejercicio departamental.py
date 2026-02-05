# Departamentos (columnas)
departamentos = ["Ropa", "Deportes", "Juguetería"]

# Meses (filas)
meses = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

# Arreglo bidimensional
ventas = []

# -----------------------------
# Captura inicial de datos
# -----------------------------
for mes in meses:
    fila = []
    print(f"\nIngresando ventas para {mes}:")
    for depto in departamentos:
        monto = float(input(f"  Venta en {depto}: "))
        fila.append(monto)
    ventas.append(fila)

# -----------------------------
# Mostrar tabla completa
# -----------------------------
def mostrar_tabla():
    print("\nMes\t\tRopa\tDeportes\tJuguetería")
    for i in range(len(meses)):
        print(f"{meses[i]:<10}\t{ventas[i][0]}\t{ventas[i][1]}\t\t{ventas[i][2]}")

mostrar_tabla()

# -----------------------------
# Modificar un valor
# -----------------------------
print("\n--- MODIFICAR UNA VENTA ---")
mes_mod = int(input("Ingresa el número de mes (1 a 12): "))
dep_mod = int(input("Departamento (1=Ropa, 2=Deportes, 3=Juguetería): "))

if 1 <= mes_mod <= 12 and 1 <= dep_mod <= 3:
    nuevo_valor = float(input("Ingresa el nuevo monto: "))
    ventas[mes_mod - 1][dep_mod - 1] = nuevo_valor
    print("✅ Venta modificada correctamente.")
else:
    print("❌ Mes o departamento inválido.")

# -----------------------------
# Buscar un mes en particular
# -----------------------------
print("\n--- BUSCAR UN MES ---")
buscar_mes = input("Ingresa el nombre del mes (ej. Marzo): ").capitalize()

if buscar_mes in meses:
    indice = meses.index(buscar_mes)
    print(f"\nVentas de {buscar_mes}:")
    for i in range(len(departamentos)):
        print(f"{departamentos[i]}: {ventas[indice][i]}")
else:
    print("❌ Mes no encontrado.")

def eliminar_venta():
    print("\n--- ELIMINAR UNA VENTA ---")
    
    mes = int(input("Ingresa el número de mes (1 a 12): "))
    depto = int(input("Departamento (1=Ropa, 2=Deportes, 3=Juguetería): "))
    
    if 1 <= mes <= 12 and 1 <= depto <= 3:
        print(f"Venta actual: {ventas[mes-1][depto-1]}")
        ventas[mes-1][depto-1] = 0
        print("✅ Venta eliminada correctamente (valor = 0).")
    else:
        print("❌ Mes o departamento inválido.")


# -----------------------------
# Mostrar tabla final
# -----------------------------
mostrar_tabla()

