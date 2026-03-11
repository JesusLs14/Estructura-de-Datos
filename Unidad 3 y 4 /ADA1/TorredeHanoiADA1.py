class PilaHanoi:
    def __init__(self, nombre):
        self.items = []
        self.nombre = nombre

    def push(self, disco):
        if not self.is_empty() and disco > self.peek():
            raise ValueError(f"¡Movimiento inválido! No puedes poner el disco {disco} sobre el {self.peek()}")
        
        self.items.append(disco)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def __str__(self):
        return f"{self.nombre}: {self.items}"


def mover_disco(origen, destino):
    disco = origen.pop()
    try:
        destino.push(disco)
        print(f"Mover disco {disco}: {origen.nombre} -> {destino.nombre}")
    except ValueError as e:
        print(f"Error: {e}")
        origen.push(disco)

def hanoi_recursivo(n, origen, destino, auxiliar):
    if n == 1:
        mover_disco(origen, destino)
    else:
        hanoi_recursivo(n - 1, origen, auxiliar, destino)
        mover_disco(origen, destino)
        hanoi_recursivo(n - 1, auxiliar, destino, origen)


A = PilaHanoi("Torre A")
B = PilaHanoi("Torre B")
C = PilaHanoi("Torre C")

for d in range(3, 0, -1):
    A.push(d)

print("Estado inicial:")
print(f"{A}\n{B}\n{C}\n" + "-"*20)

hanoi_recursivo(3, A, C, B)

print("-"*20 + "\nEstado final:")
print(f"{A}\n{B}\n{C}")