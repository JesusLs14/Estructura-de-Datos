import os

def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr

def quick_sort(arr):
    if len(arr) <= 1: return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def heapify(arr, n, i):
    largest, l, r = i, 2 * i + 1, 2 * i + 2
    if l < n and arr[i] < arr[l]: largest = l
    if r < n and arr[largest] < arr[r]: largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1): heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr

def counting_sort_for_radix(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1
    for i in range(1, 10): count[i] += count[i - 1]
    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1
    for i in range(n): arr[i] = output[i]

def radix_sort(arr):
    max1 = max(arr)
    exp = 1
    while max1 // exp > 0:
        counting_sort_for_radix(arr, exp)
        exp *= 10
    return arr

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def obtener_datos():
    while True:
        try:
            n = int(input("\n[+] ¿Cuántos números deseas ingresar?: "))
            if n <= 0:
                print("(!) Por favor, ingresa un número mayor a 0.")
                continue
            arr = []
            for i in range(n):
                val = int(input(f"    -> Número {i+1}: "))
                arr.append(val)
            return arr
        except ValueError:
            print("(!) Entrada inválida. Ingresa solo números enteros.")

def menu():
    while True:
        limpiar_pantalla()
        print("=========================================")
        print("      SISTEMA DE ORDENAMIENTO v1.0       ")
        print("=========================================")
        print("  1. [ ShellSort     ]")
        print("  2. [ Quicksort     ]")
        print("  3. [ Heapsort      ]")
        print("  4. [ Radix Sort    ]")
        print("  5. [ Salir         ]")
        print("=========================================")
        
        opcion = input(">> Selecciona una opción: ")
        
        if opcion == '5':
            print("\n¡Hasta luego!")
            break
        
        if opcion in ['1', '2', '3', '4']:
            datos = obtener_datos()
            print(f"\nLista original: {datos}")
            
            # Procesamiento
            if opcion == '1': resultado = shell_sort(datos.copy())
            elif opcion == '2': resultado = quick_sort(datos.copy())
            elif opcion == '3': resultado = heap_sort(datos.copy())
            elif opcion == '4': resultado = radix_sort([abs(x) for x in datos])
            
            print(f"Lista ordenada: {resultado}")
            input("\nPresiona ENTER para volver al menú...")
        else:
            print("\n(!) Opción no válida.")
            input("Presiona ENTER para intentar de nuevo...")

if __name__ == "__main__":
    menu()