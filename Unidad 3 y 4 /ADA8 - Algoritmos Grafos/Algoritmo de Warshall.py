def warshall(matriz_adyacencia):
    n = len(matriz_adyacencia)
    alcance = [[bool(val) for val in fila] for fila in matriz_adyacencia]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                alcance[i][j] = alcance[i][j] or (alcance[i][k] and alcance[k][j])
                
    return alcance

matriz_booleana = [
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 0],
    [1, 0, 1, 0]
]

resultado_warshall = warshall(matriz_booleana)

print("--- Matriz de Clausura Transitiva (Warshall) ---")
for fila in resultado_warshall:
    # Convertimos los True/False a 1 y 0 para que la captura se vea más limpia
    print([1 if val else 0 for val in fila])