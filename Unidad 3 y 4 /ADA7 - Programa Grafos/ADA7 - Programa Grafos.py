import networkx as nx
import matplotlib.pyplot as plt

def crear_grafo():
    G = nx.Graph()
    estados = ['Yucatán', 'Quintana Roo', 'Campeche', 'Tabasco', 'Chiapas', 'Veracruz', 'Oaxaca']
    G.add_nodes_from(estados)

    conexiones = [
        ('Yucatán', 'Quintana Roo', 320),
        ('Yucatán', 'Campeche', 180),
        ('Quintana Roo', 'Campeche', 380),
        ('Campeche', 'Tabasco', 400),
        ('Tabasco', 'Chiapas', 250),
        ('Tabasco', 'Veracruz', 480),
        ('Veracruz', 'Oaxaca', 360),
        ('Chiapas', 'Oaxaca', 420),
        ('Veracruz', 'Chiapas', 500)
    ]
    
    for origen, destino, costo in conexiones:
        G.add_edge(origen, destino, weight=costo)
        
    return G

def calcular_costo_ruta(G, ruta):
    costo_total = 0
    for i in range(len(ruta) - 1):
        origen = ruta[i]
        destino = ruta[i+1]
        if G.has_edge(origen, destino):
            costo_total += G[origen][destino]['weight']
        else:
            return -1
    return costo_total

def buscar_ruta_sin_repetir(G, nodo_actual, visitados, camino_actual):
    if len(visitados) == len(G.nodes):
        return camino_actual
    
    for vecino in G.neighbors(nodo_actual):
        if vecino not in visitados:
            visitados.add(vecino)
            camino_actual.append(vecino)
            
            resultado = buscar_ruta_sin_repetir(G, vecino, visitados, camino_actual)
            if resultado: return resultado
                
            visitados.remove(vecino)
            camino_actual.pop()
    return None

def visualizar_grafo_y_ruta(G, ruta, titulo, costo):
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G, seed=42)
    
    nx.draw_networkx_nodes(G, pos, node_color='#A0CBE2', node_size=2500, edgecolors='black')
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    nx.draw_networkx_edges(G, pos, edge_color='lightgray', width=2)
    
    etiquetas_pesos = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas_pesos, font_color='gray')

    if ruta and costo != -1:
        aristas_ruta = [(ruta[i], ruta[i+1]) for i in range(len(ruta)-1)]
        G_dirigido = nx.DiGraph()
        G_dirigido.add_edges_from(aristas_ruta)
        
        nx.draw_networkx_edges(
            G_dirigido, pos, 
            edgelist=aristas_ruta, 
            edge_color='red', 
            width=3, 
            arrows=True, 
            arrowstyle='-|>',
            arrowsize=20,
            connectionstyle='arc3, rad=0.1'
        )
        titulo_completo = f"{titulo}\nCosto Total: ${costo} | Ruta: {' -> '.join(ruta)}"
    elif costo == -1:
        titulo_completo = f"{titulo}\n¡Ruta Inválida! Faltan conexiones directas entre algunos estados."
    else:
        titulo_completo = f"{titulo}\n(Grafo Base sin ruta seleccionada)"

    plt.title(titulo_completo, fontsize=12, pad=15)
    plt.axis('off')
    plt.show(block=False)

def ingresar_ruta_manual(G):
    print("\n" + "="*50)
    print("OPCIÓN DE RUTA PERSONALIZADA")
    print("Estados disponibles:", ", ".join(G.nodes))
    
    entrada = input("\nIngresa tu ruta separando los estados por comas (ej. Yucatán, Campeche, Tabasco):\n")
    ruta_usuario = [estado.strip() for estado in entrada.split(',')]
    
    nodos_validos = all(nodo in G.nodes for nodo in ruta_usuario)
    
    if len(ruta_usuario) > 1 and nodos_validos:
        costo = calcular_costo_ruta(G, ruta_usuario)
        if costo != -1:
            print(f"\nRuta válida trazada con éxito. Costo: ${costo}")
        else:
            print("\nError: La ruta incluye saltos entre estados que no están conectados directamente.")
        visualizar_grafo_y_ruta(G, ruta_usuario, "Ruta Personalizada del Usuario", costo)
    else:
        print("\nError: Asegúrate de ingresar al menos dos estados válidos separados por comas, respetando mayúsculas y acentos.")

if __name__ == "__main__":
    grafo = crear_grafo()
    
    visualizar_grafo_y_ruta(grafo, None, "Grafo Base - Estados y Costos", 0)
    
    inicio = 'Quintana Roo'
    ruta_a = buscar_ruta_sin_repetir(grafo, inicio, {inicio}, [inicio])
    if ruta_a:
        costo_a = calcular_costo_ruta(grafo, ruta_a)
        print("\na) Ruta SIN repetir:")
        print(" -> ".join(ruta_a))
        print(f"Costo: ${costo_a}")
        visualizar_grafo_y_ruta(grafo, ruta_a, "Ruta A: Recorrido sin repetir estados", costo_a)

    if ruta_a:
        ruta_b = [ruta_a[0], ruta_a[1], ruta_a[0]] + ruta_a[1:]
        costo_b = calcular_costo_ruta(grafo, ruta_b)
        print("\nb) Ruta CON repetición (Ida y vuelta inicial):")
        print(" -> ".join(ruta_b))
        print(f"Costo: ${costo_b}")
        visualizar_grafo_y_ruta(grafo, ruta_b, "Ruta B: Recorrido repitiendo un estado", costo_b)

    ingresar_ruta_manual(grafo)

    print("\nTodas las ventanas han sido generadas. Cierra las ventanas emergentes para finalizar el programa.")
    plt.show()