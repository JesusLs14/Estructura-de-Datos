import random
import time

MATERIAS = 50000
ALUMNOS = 1000000

print("Creando matriz de 500 materias x 10,000 alumnos...\n")
calificaciones = [
    [random.randint(0, 100) for _ in range(ALUMNOS)]
    for _ in range(MATERIAS)
]

print("IMPRIMIENDO TODOS LOS DATOS:\n")

print("Materia/Alumno", end="\t")
for a in range(ALUMNOS):
    print(f"A{a+1}", end="\t")
print()

for m in range(MATERIAS):
    print(f"Materia {m+1}", end="\t")
    for a in range(ALUMNOS):
        print(calificaciones[m][a], end="\t")
    print()

print("\n--- BÚSQUEDA DE CALIFICACIÓN ---")

materia = int(input("Ingresa la materia (1 a 50000): "))
alumno = int(input("Ingresa el alumno (1 a 1000000): "))

if 1 <= materia <= MATERIAS and 1 <= alumno <= ALUMNOS:
    inicio = time.perf_counter()
    valor = calificaciones[materia - 1][alumno - 1]
    fin = time.perf_counter()

    print(f"\nResultado:")
    print(f"Materia {materia}, Alumno {alumno} → {valor}")
    print(f"Tiempo de acceso: {(fin - inicio):.10f} segundos")
else:
    print("\n❌ Posición fuera de rango.")
