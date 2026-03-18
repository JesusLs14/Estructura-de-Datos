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
        self.insertar_ingrediente("Arroz con Leche", "Canela")
        
        self.alta_postre("Pastel Chocolate")
        self.insertar_ingrediente("Pastel Chocolate", "Harina")
        self.insertar_ingrediente("Pastel Chocolate", "Cacao")

    def _buscar_indice(self, nombre):
        for i, p in enumerate(self.arreglo_postres):
            if p.nombre.lower() == nombre.lower():
                return i
        return None

    def alta_postre(self, nombre):
        if self._buscar_indice(nombre) is not None:
            return False
        nuevo = Postre(nombre)
        self.arreglo_postres.append(nuevo)
        self.arreglo_postres.sort(key=lambda x: x.nombre.lower())
        return True

    def insertar_ingrediente(self, nombre_postre, ingrediente):
        idx = self._buscar_indice(nombre_postre)
        if idx is not None:
            nuevo = NodoIngrediente(ingrediente)
            nuevo.siguiente = self.arreglo_postres[idx].lista_ingredientes
            self.arreglo_postres[idx].lista_ingredientes = nuevo

    def mostrar_todo(self):
        print("\n--- LISTA TOTAL DE POSTRES Y CLASES ---")
        if not self.arreglo_postres:
            print("Arreglo vacío.")
        for p in self.arreglo_postres:
            print(f"Postre: {p.nombre.upper()}")
            actual = p.lista_ingredientes
            print("  Ingredientes:", end=" ")
            if not actual: print("NIL")
            while actual:
                print(f"[{actual.nombre}]", end=" -> ")
                actual = actual.siguiente
                if not actual: print("NIL")
        print("---------------------------------------")


    def eliminar_ingrediente(self, nom_p, ing):
        idx = self._buscar_indice(nom_p)
        if idx is None: return
        p = self.arreglo_postres[idx]
        act, ant = p.lista_ingredientes, None
        while act:
            if act.nombre.lower() == ing.lower():
                if not ant: p.lista_ingredientes = act.siguiente
                else: ant.siguiente = act.siguiente
                return
            ant, act = act, act.siguiente

    def baja_postre(self, nombre):
        idx = self._buscar_indice(nombre)
        if idx is not None: self.arreglo_postres.pop(idx)


def menu():
    sys = GestionPostres()
    while True:
        print("\n1. Alta Postre | 2. Alta Ingrediente | 3. VER TODO | 4. Baja Ingrediente")
        print("5. Baja Postre | 6. Salir")
        op = input("Selección: ")
        
        if op == "1": sys.alta_postre(input("Nombre postre: "))
        elif op == "2": sys.insertar_ingrediente(input("Postre: "), input("Ingrediente: "))
        elif op == "3": sys.mostrar_todo()
        elif op == "4": sys.eliminar_ingrediente(input("Postre: "), input("Ingrediente: "))
        elif op == "5": sys.baja_postre(input("Postre: "))
        elif op == "6": break
menu()