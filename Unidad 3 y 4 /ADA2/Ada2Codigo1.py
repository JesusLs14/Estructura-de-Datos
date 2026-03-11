class Cola:
    def __init__(self):
        self.items = []

    def esta_vacia(self):
        return len(self.items) == 0

    def encolar(self, item):
        self.items.append(item)

    def desencolar(self):
        if not self.esta_vacia():
            return self.items.pop(0)
        return None
        
    def ver_elementos(self):
        
        return self.items

def sumar_colas(cola_a, cola_b):
    cola_resultado = Cola()
    
    while not cola_a.esta_vacia() and not cola_b.esta_vacia():
        valor_a = cola_a.desencolar()
        valor_b = cola_b.desencolar()
        
        suma = valor_a + valor_b
        cola_resultado.encolar(suma)
        
    return cola_resultado

cola_a = Cola()
cola_b = Cola()

for num in [3, 4, 2, 8, 12]:
    cola_a.encolar(num)

for num in [6, 2, 9, 11, 3]:
    cola_b.encolar(num)

resultado = sumar_colas(cola_a, cola_b)

print("Cola A:       ", [3, 4, 2, 8, 12])
print("Cola B:       ", [6, 2, 9, 11, 3])
print("Cola Resultado:", resultado.ver_elementos())