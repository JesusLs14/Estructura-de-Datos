import heapq

def dijkstra(grafo, inicio):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    cola_prioridad = [(0, inicio)]

    while cola_prioridad:
        dist_actual, nodo_actual = heapq.heappop(cola_prioridad)

        if dist_actual > distancias[nodo_actual]:
            continue

        for vecino, peso in grafo[nodo_actual].items():
            distancia = dist_actual + peso
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                heapq.heappush(cola_prioridad, (distancia, vecino))

    return distancias

grafo_prueba = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

nodo_inicio = 'A'
resultados = dijkstra(grafo_prueba, nodo_inicio)

print(f"--- Distancias más cortas desde '{nodo_inicio}' ---")
for destino, costo in resultados.items():
    print(f"Hacia {destino}: {costo}")