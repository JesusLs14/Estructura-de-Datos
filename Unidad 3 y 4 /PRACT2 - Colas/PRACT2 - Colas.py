class Pedido:
    def __init__(self, cantidad, cliente):
        self.cliente = cliente
        self.cantidad = cantidad
        
    def imprimir_pedido(self):
        print(f"    Cliente: {self.cliente}")
        print(f"    Cantidad: {self.cantidad}")
        print("    ------------")

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class Cola:
    def __init__(self):
        self.inicio = None
        self.final = None
        self._tamano = 0

    def tamano(self):
        return self._tamano
        
    def esta_vacia(self):
        return self._tamano == 0
        
    def frente(self):
        if self.esta_vacia(): return None
        return self.inicio.dato
        
    def encolar(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.inicio = nuevo_nodo
            self.final = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo
        self._tamano += 1
        
    def desencolar(self):
        if self.esta_vacia(): return None
        dato = self.inicio.dato
        self.inicio = self.inicio.siguiente
        self._tamano -= 1
        if self.esta_vacia(): self.final = None
        return dato

    def obtener_enesimo(self, posicion):
        if posicion < 0 or posicion >= self.tamano(): return None
        nodo_actual = self.inicio
        for _ in range(posicion):
            nodo_actual = nodo_actual.siguiente
        return nodo_actual.dato

    def eliminar_en_posicion(self, posicion):
        """Elimina un nodo en una posición específica (0 es el primero)."""
        if posicion < 0 or posicion >= self.tamano():
            return False 
            
        if posicion == 0:
            self.desencolar()
            return True

        nodo_anterior = self.inicio
        for _ in range(posicion - 1):
            nodo_anterior = nodo_anterior.siguiente
            
        nodo_a_borrar = nodo_anterior.siguiente
        
        nodo_anterior.siguiente = nodo_a_borrar.siguiente
        
        if nodo_a_borrar == self.final:
            self.final = nodo_anterior
            
        self._tamano -= 1
        return True

    def imprimir_info(self):
        print("\n" + "="*30)
        print(f"ESTADO DE LA COLA (Tamaño: {self.tamano()})")
        print("="*30)
        if self.esta_vacia():
            print("  [La cola está vacía]")
        else:
            nodo = self.inicio
            contador = 0
            while nodo is not None:
                print(f"Posición [{contador}]: {nodo.dato.cliente} (Cant: {nodo.dato.cantidad})")
                nodo = nodo.siguiente
                contador += 1
        print("="*30 + "\n")

def main():
    mi_cola = Cola()

    while True:

        mi_cola.imprimir_info()
        
        print("¿Qué deseas hacer?")
        print("1. Encolar (Añadir pedido)")
        print("2. Desencolar (Atender el primer pedido)")
        print("3. Ver quién está al frente")
        print("4. Eliminar pedido por posición")
        print("5. Salir")
        
        opcion = input("\nElige una opción (1-5): ")
        
        if opcion == '1':
            cliente = input("Nombre del cliente: ")
            try:
                cantidad = int(input(f"Cantidad para {cliente}: "))
                mi_cola.encolar(Pedido(cantidad, cliente))
                print(" Pedido añadido con éxito.")
            except ValueError:
                print(" Error: La cantidad debe ser un número.")
                
        elif opcion == '2':
            atendido = mi_cola.desencolar()
            if atendido:
                print(f" Se atendió a {atendido.cliente}.")
            else:
                print(" No hay nadie en la cola.")
                
        elif opcion == '3':
            frente = mi_cola.frente()
            if frente:
                print(f" Al frente está: {frente.cliente} con {frente.cantidad} unidades.")
            else:
                print(" La cola está vacía.")
                
        elif opcion == '4':
            try:
                pos = int(input("¿Qué posición deseas eliminar? (0 es el primero): "))
                exito = mi_cola.eliminar_en_posicion(pos)
                if exito:
                    print(f" Pedido en la posición {pos} eliminado.")
                else:
                    print(" Posición inválida.")
            except ValueError:
                print("Error: Debes ingresar un número válido.")
                
        elif opcion == '5':
            print("¡Hasta luego!")
            break 
            
        else:
            print(" Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()