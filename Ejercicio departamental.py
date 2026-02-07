class VentasDepartamentos:
    def __init__(self):

        self.departamentos = ["Ropa", "Deportes", "Juguetería"]
        
        self.meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        
        self.ventas = [[0 for _ in self.departamentos] for _ in self.meses]

    def insertar_venta(self, mes, departamento, monto):
        if mes in self.meses and departamento in self.departamentos:
            fila = self.meses.index(mes)
            columna = self.departamentos.index(departamento)
            self.ventas[fila][columna] = monto
            print(f"Venta insertada: {mes} - {departamento} = ${monto}")
        else:
            print("Mes o departamento inválido")


    def buscar_venta(self, mes, departamento):
        if mes in self.meses and departamento in self.departamentos:
            fila = self.meses.index(mes)
            columna = self.departamentos.index(departamento)
            monto = self.ventas[fila][columna]
            print(f"Venta encontrada: {mes} - {departamento} = ${monto}")
            return monto
        else:
            print("Mes o departamento inválido")
            return None

    def eliminar_venta(self, mes, departamento):
        if mes in self.meses and departamento in self.departamentos:
            fila = self.meses.index(mes)
            columna = self.departamentos.index(departamento)
            self.ventas[fila][columna] = 0
            print(f"Venta eliminada: {mes} - {departamento}")
        else:
            print("Mes o departamento inválido")

    def mostrar_tabla(self):
        print("\nTabla de Ventas Mensuales")
        print("Mes".ljust(12), end="")
        for d in self.departamentos:
            print(d.ljust(15), end="")
        print()

        for i, mes in enumerate(self.meses):
            print(mes.ljust(12), end="")
            for venta in self.ventas[i]:
                print(str(venta).ljust(15), end="")
            print()


ventas = VentasDepartamentos()

ventas.insertar_venta("Enero", "Ropa", 15000)
ventas.insertar_venta("Enero", "Deportes", 8000)
ventas.insertar_venta("Febrero", "Juguetería", 12000)

ventas.buscar_venta("Enero", "Ropa")

ventas.eliminar_venta("Enero", "Deportes")

ventas.mostrar_tabla()
