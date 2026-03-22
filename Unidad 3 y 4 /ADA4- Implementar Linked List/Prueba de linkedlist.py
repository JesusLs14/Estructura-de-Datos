from MyLinkedList import LinkedList

def main():
    print("--- Probando MyLinkedList ---")
    mi_lista = LinkedList()
    
    mi_lista.agregar_al_final("Manzana")
    mi_lista.agregar_al_final("Pera")
    mi_lista.insertar_al_inicio("Fresa")
    
    print("Lista original:")
    mi_lista.mostrar()  # Resultado esperado: Fresa -> Manzana -> Pera -> None
    
    print("\nEliminando 'Manzana':")
    mi_lista.eliminar_nodo("Manzana")
    mi_lista.mostrar()  # Resultado esperado: Fresa -> Pera -> None

if __name__ == "__main__":
    main()