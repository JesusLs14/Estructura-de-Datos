# MyLinkedList/core.py

class Nodo:
    """Clase que representa un eslabón individual de la lista."""
    def __init__(self, datos):
        self.datos = datos
        self.siguiente = None

class LinkedList:
    """Clase principal que gestiona la lista enlazada."""
    def __init__(self):
        self.head = None

    def agregar_al_final(self, datos):
        """Añade un nodo al final de la lista."""
        nuevo_nodo = Nodo(datos)
        if self.head is None:
            self.head = nuevo_nodo
            return
        nodo_actual = self.head
        while nodo_actual.siguiente is not None:
            nodo_actual = nodo_actual.siguiente
        nodo_actual.siguiente = nuevo_nodo

    def insertar_al_inicio(self, datos):
        """Añade un nodo al principio de la lista (¡muy rápido!)."""
        nuevo_nodo = Nodo(datos)
        nuevo_nodo.siguiente = self.head  
        self.head = nuevo_nodo            

    def eliminar_nodo(self, valor_a_eliminar):
        """Busca un valor y elimina el primer nodo que lo contenga."""
        nodo_actual = self.head
        
        if nodo_actual is None:
            return

        if nodo_actual.datos == valor_a_eliminar:
            self.head = nodo_actual.siguiente 
            nodo_actual = None             
            return

        previo = None
        while nodo_actual is not None and nodo_actual.datos != valor_a_eliminar:
            previo = nodo_actual
            nodo_actual = nodo_actual.siguiente

        if nodo_actual is None:
            print(f"Valor {valor_a_eliminar} no encontrado en la lista.")
            return

        previo.siguiente = nodo_actual.siguiente
        nodo_actual = None

    def mostrar(self):
        """Imprime la lista de forma visual."""
        elementos = []
        nodo_actual = self.head
        while nodo_actual is not None:
            elementos.append(str(nodo_actual.datos))
            nodo_actual = nodo_actual.siguiente
        print(" -> ".join(elementos) + " -> None")