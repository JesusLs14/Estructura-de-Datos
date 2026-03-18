class NodoIngrediente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.siguiente = None

class Postre:
    def __init__(self, nombre):
        self.nombre = nombre
        self.lista_ingredientes = None

class GestionPostres:
    def __init__(self):
        self.arreglo_postres = []
        self._cargar_datos_iniciales()

    def _cargar_datos_iniciales(self):
        self.alta_postre("Arroz con Leche")
        self.insertar_ingrediente("Arroz con Leche", "Arroz")
        self.insertar_ingrediente("Arroz con Leche", "Leche")
        
        self.alta_postre("Pastel Chocolate")
        self.insertar_ingrediente("Pastel Chocolate", "Harina")

    def _buscar_indice(self, nombre):
        for i, p in enumerate(self.arreglo_postres):
            if p.nombre.lower() == nombre.lower():
                return i
        return None

    def alta_postre(self, nombre):
        nuevo = Postre(nombre)
        self.arreglo_postres.append(nuevo)
        self.arreglo_postres.sort(key=lambda x: x.nombre.lower())
        print(f"¡Éxito! El postre '{nombre}' se ha guardado en el arreglo.")

    def insertar_ingrediente(self, nombre_postre, ingrediente):
        idx = self._buscar_indice(nombre_postre)
        if idx is not None:
            nuevo = NodoIngrediente(ingrediente)
            nuevo.siguiente = self.arreglo_postres[idx].lista_ingredientes
            self.arreglo_postres[idx].lista_ingredientes = nuevo
            print(f"Ingrediente '{ingrediente}' agregado a {nombre_postre}.")
        else:
            print(f"Error: No se encontró el postre '{nombre_postre}'.")

    def mostrar_todo(self):
        print("\n" + "="*40)
        print("ESTRUCTURA ACTUAL (ARREGLO DE LISTAS)")
        print("="*40)
        if not self.arreglo_postres:
            print("El arreglo está vacío.")
        for i, p in enumerate(self.arreglo_postres):
            print(f"Índice [{i}] -> Postre: {p.nombre.upper()}")
            actual = p.lista_ingredientes
            print("   Lista de Ingredientes:", end=" ")
            if not actual: 
                print("NIL")
            else:
                while actual:
                    print(f"[{actual.nombre}]", end=" -> ")
                    actual = actual.siguiente
                print("NIL")
        print("="*40)

    def eliminar_ingrediente(self, nom_p, ing):
        idx = self._buscar_indice(nom_p)
        if idx is None: return
        p = self.arreglo_postres[idx]
        act, ant = p.lista_ingredientes, None
        while act:
            if act.nombre.lower() == ing.lower():
                if not ant: p.lista_ingredientes = act.siguiente
                else: ant.siguiente = act.siguiente
                print(f"'{ing}' eliminado de la lista.")
                return
            ant, act = act, act.siguiente
        print("El ingrediente no existe en este postre.")

    def baja_postre(self, nombre):
        idx = self._buscar_indice(nombre)
        if idx is not None:
            self.arreglo_postres.pop(idx)
            print(f"Postre '{nombre}' eliminado del arreglo.")
        else:
            print("El postre no existe.")

def menu():
    sys = GestionPostres()
    while True:
        print("\n--- MENÚ DE GESTIÓN ---")
        print("1. Alta Postre")
        print("2. Agregar Ingrediente")
        print("3. VER ESTRUCTURA COMPLETA")
        print("4. Eliminar un Ingrediente")
        print("5. Dar de Baja un Postre")
        print("6. Salir")
        
        op = input("\nSeleccione una opción: ")
        
        if op == "1": sys.alta_postre(input("Nombre del postre: "))
        elif op == "2": sys.insertar_ingrediente(input("¿A qué postre?: "), input("Ingrediente: "))
        elif op == "3": sys.mostrar_todo()
        elif op == "4": sys.eliminar_ingrediente(input("Postre: "), input("Ingrediente a borrar: "))
        elif op == "5": sys.baja_postre(input("Postre a borrar: "))
        elif op == "6": break
        else: print("Opción no válida.")

if __name__ == "__main__":
    menu()