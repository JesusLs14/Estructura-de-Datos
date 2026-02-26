import time

def fibonacci_iterativo(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def fibonacci_recursivo(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    
    return fibonacci_recursivo(n - 1) + fibonacci_recursivo(n - 2)

def main():
    print("--- Comparación de Algoritmos: Fibonacci ---")
    try:
        n = int(input("Ingresa la posición en la serie de Fibonacci a calcular (ej. 35): "))
        if n < 0:
            print("Por favor, ingresa un número entero positivo.")
            return

        inicio_iter = time.perf_counter()
        resultado_iter = fibonacci_iterativo(n)
        fin_iter = time.perf_counter()
        tiempo_iter = fin_iter - inicio_iter

        inicio_rec = time.perf_counter()
        resultado_rec = fibonacci_recursivo(n)
        fin_rec = time.perf_counter()
        tiempo_rec = fin_rec - inicio_rec

        print("\nResultados:")
        print(f"Fibonacci({n}) = {resultado_iter}")
        print("-" * 30)
        print(f"Tiempo Iterativo: {tiempo_iter:.8f} segundos")
        print(f"Tiempo Recursivo: {tiempo_rec:.8f} segundos")
        
        if tiempo_rec > 0:
            diferencia = tiempo_rec / (tiempo_iter if tiempo_iter > 0 else 1e-9)
            print(f"\nLa versión iterativa fue aproximadamente {diferencia:,.0f} veces más rápida.")

    except ValueError:
        print("Entrada no válida. Debes ingresar un número entero.")

if __name__ == "__main__":
    main()