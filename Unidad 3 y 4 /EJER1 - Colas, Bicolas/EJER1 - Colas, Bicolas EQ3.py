from collections import deque

class CacheWeb:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.cache = deque()

    def consultar_pagina(self, url):
        print(f"\nConsultando: {url}")
        
        if url in self.cache:
            print(f"-> Encontrado! Moviendo '{url}' al frente.")
            self.cache.remove(url)
            self.cache.appendleft(url)
            
        else:
            print(f"-> No encontrado! Agregando '{url}' a la caché.")
            if len(self.cache) >= self.capacidad:
                eliminada = self.cache.pop()
                print(f"  [!] Caché llena. Eliminando la más antigua: {eliminada}")
            
            self.cache.appendleft(url)
        
        self.mostrar_cache()

    def mostrar_cache(self):
        print(f"Estado actual de la Caché: {list(self.cache)}")

capacidad_max = 3
mi_cache = CacheWeb(capacidad_max)

urls_a_consultar = [
    "google.com", 
    "github.com", 
    "stackoverflow.com", 
    "google.com",      
    "youtube.com",      
    "linkedin.com" 
    "stackoverflow.com", 
]

print(f"--- Iniciando Simulación (Capacidad: {capacidad_max}) ---")
for url in urls_a_consultar:
    mi_cache.consultar_pagina(url)