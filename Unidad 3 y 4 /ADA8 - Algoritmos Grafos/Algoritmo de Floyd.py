def floyd(matriz_pesos):
    n = len(matriz_pesos)
    dist = [fila[:] for fila in matriz_pesos]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    
    return dist

# ==========================================
# EJECUCIÓN Y PRUEBA
# ==========================================
INF = float('inf')
# Grafo de 4 nodos (0, 1, 2, 3)
matriz_ejemplo = [
    [0,   3, INF,   5],
    [2,   0, INF,   4],
    [INF, 1,   0, INF],
    [INF, INF, 2,   0]
]

resultado_floyd = floyd(matriz_ejemplo)

print("--- Matriz de distancias más cortas (Floyd) ---")
for fila in resultado_floyd:
    # Formateamos para que los infinitos se lean mejor
    print([val if val != float('inf') else "INF" for val in fila])