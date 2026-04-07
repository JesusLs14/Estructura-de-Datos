class UnionFind:
    def __init__(self, nodos):
        self.padre = {nodo: nodo for nodo in nodos}
        self.rango = {nodo: 0 for nodo in nodos}

    def buscar(self, i):
        if self.padre[i] == i:
            return i
        self.padre[i] = self.buscar(self.padre[i])
        return self.padre[i]

    def unir(self, i, j):
        raiz_i = self.buscar(i)
        raiz_j = self.buscar(j)
        if raiz_i != raiz_j:
            if self.rango[raiz_i] < self.rango[raiz_j]:
                self.padre[raiz_i] = raiz_j
            elif self.rango[raiz_i] > self.rango[raiz_j]:
                self.padre[raiz_j] = raiz_i
            else:
                self.padre[raiz_j] = raiz_i
                self.rango[raiz_i] += 1

def kruskal(nodos, aristas):
    aristas.sort() 
    uf = UnionFind(nodos)
    mst = [] 

    for peso, u, v in aristas:
        if uf.buscar(u) != uf.buscar(v):
            uf.unir(u, v)
            mst.append((u, v, peso))

    return mst

# ==========================================
# EJECUCIÓN Y PRUEBA
# ==========================================
nodos_grafo = ['A', 'B', 'C', 'D']
# Formato: (peso, nodo_origen, nodo_destino)
aristas_grafo = [
    (1, 'A', 'B'),
    (4, 'A', 'C'),
    (2, 'B', 'C'),
    (5, 'B', 'D'),
    (1, 'C', 'D')
]

arbol_minimo = kruskal(nodos_grafo, aristas_grafo)

print("--- Árbol de Expansión Mínima (Kruskal) ---")
costo_total = 0
for u, v, peso in arbol_minimo:
    print(f"Arista: {u} - {v} | Costo: {peso}")
    costo_total += peso
print(f"Costo Total del MST: {costo_total}")