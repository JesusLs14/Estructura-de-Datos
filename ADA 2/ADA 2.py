import random
import time

MATERIAS = 500
ALUMNOS = 10000

print("Creando matriz de 500 materias x 10,000 alumnos...")
inicio = time.perf_counter()

calificaciones = [
    [random.randint(0, 100) for _ in range(ALUMNOS)]
    for _ in range(MATERIAS)
]

fin = time.perf_counter()
print(f"Matriz creada en {fin - inicio:.3f} segundos\n")

print("--- BÚSQUEDA DE CALIFICACIÓN ---")

materia = int(input("Ingresa la materia (1 a 500): "))
alumno = int(input("Ingresa el alumno (1 a 10000): "))

if 1 <= materia <= MATERIAS and 1 <= alumno <= ALUMNOS:
    inicio = time.perf_counter()
    valor = calificaciones[materia - 1][alumno - 1]
    fin = time.perf_counter()

    print("\nResultado:")
    print(f"Materia {materia}, Alumno {alumno} → {valor}")
    print(f"Tiempo de acceso: {(fin - inicio):.10f} segundos")
else:
    print("\n Posición fuera de rango.")