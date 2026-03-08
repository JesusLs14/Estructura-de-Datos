import time

torres = {
    'A': [],
    'B': [],
    'C': []
}

def mostrar_estado(paso):
    """Muestra el contenido actual de las tres torres."""
    print(f"--- Paso {paso} ---")
    print(f"Torre A: {torres['A']}")
    print(f"Torre B: {torres['B']}")
    print(f"Torre C: {torres['C']}")
    print("-" * 20)

def mover_disco(origen, destino):
    """Saca un disco de la pila origen y lo pone en la pila destino."""
    disco = torres[origen].pop()
    torres[destino].append(disco)
    print(f" > Moviendo el disco {disco} de la Torre {origen} a la Torre {destino}")

def hanoi_recursivo(n, origen, destino, auxiliar, contador_pasos):
    """Algoritmo recursivo que resuelve el problema y actualiza las pilas."""
    if n == 1:
        contador_pasos[0] += 1
        mover_disco(origen, destino)
        mostrar_estado(contador_pasos[0])
        return
    
    hanoi_recursivo(n - 1, origen, auxiliar, destino, contador_pasos)
    
    contador_pasos[0] += 1
    mover_disco(origen, destino)
    mostrar_estado(contador_pasos[0])
    
    hanoi_recursivo(n - 1, auxiliar, destino, origen, contador_pasos)

NUM_DISCOS = 30
torres['A'] = list(range(NUM_DISCOS, 0, -1)) 

print("ESTADO INICIAL:")
mostrar_estado(0)

pasos = [0] 

tiempo_inicio = time.perf_counter()

hanoi_recursivo(NUM_DISCOS, 'A', 'C', 'B', pasos)

tiempo_fin = time.perf_counter()

tiempo_total = tiempo_fin - tiempo_inicio

print("==========================================")
print(f"¡Problema resuelto con éxito en {pasos[0]} movimientos!")
print(f"⏳ Tiempo de ejecución: {tiempo_total:.6f} segundos")
print("==========================================")