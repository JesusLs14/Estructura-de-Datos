# Estructura-de-Datos/ordenamiento_externo/controlador.py

import time
from .interfaz_grafica import iniciar_visualizador
from .manejador_archivos import abrir_dialogo_archivo
from .algoritmos_mezcla import generar_pasadas_mezcla_directa, generar_pasadas_mezcla_equilibrada

def ejecutar_app(limite_grafico=30):
    """
    Punto de entrada principal. Abre un archivo, evalúa la cantidad de números
    y decide si usar la interfaz gráfica o resolverlo en la terminal.
    """
    print("Selecciona tu archivo de datos numéricos...")
    datos, nombre = abrir_dialogo_archivo()

    if not datos:
        print("Operación cancelada o archivo vacío.")
        return

    if len(datos) > limite_grafico:
        _ordenar_en_terminal(datos, nombre)
    else:
        print(f"\n[🎨 MODO VISUAL ACTIVO] Cargando {len(datos)} números en la interfaz gráfica...")
        # Le pasamos el límite y la función de terminal como 'callback'
        iniciar_visualizador(
            datos_iniciales=datos, 
            limite_grafico=limite_grafico, 
            funcion_terminal=_ordenar_en_terminal
        )


def _ordenar_en_terminal(datos, nombre):
    """Método interno para procesar archivos masivos silenciosamente."""
    print(f"\n[⚡ MODO TERMINAL ACTIVO]")
    print(f"Archivos procesados: {nombre}")
    print(f"Total de datos detectados: {len(datos)} (Supera el límite gráfico de visualización)\n")
    print("Ordenando en segundo plano...")

    import time
    from .algoritmos_mezcla import (
        ordenar_intercalacion,
        generar_pasadas_mezcla_directa, 
        generar_pasadas_mezcla_equilibrada
    )

    # 1. Prueba de Intercalación
    tiempo_inicio = time.time()
    lista_a, lista_b, pasos_intercalacion = ordenar_intercalacion(datos)
    tiempo_fin = time.time()
    tiempo_inter = tiempo_fin - tiempo_inicio

    # 2. Prueba de Mezcla Directa
    tiempo_inicio = time.time()
    estados_mezcla_directa = generar_pasadas_mezcla_directa(datos)
    tiempo_fin = time.time()
    tiempo_md = tiempo_fin - tiempo_inicio
    
    # 3. Prueba de Mezcla Equilibrada
    tiempo_inicio = time.time()
    secuencias, pasadas_mezcla_equilibrada = generar_pasadas_mezcla_equilibrada(datos)
    tiempo_fin = time.time()
    tiempo_me = tiempo_fin - tiempo_inicio

    # El resultado final ordenado es el mismo para todos
    resultado_final = estados_mezcla_directa[-1]

    print("-" * 55)
    print("📊 RESULTADOS DE RENDIMIENTO (Big O):")
    print(f"✔ Intercalación completada en:      {tiempo_inter:.5f} segundos ({len(pasos_intercalacion)} pasos de fusión)")
    print(f"✔ Mezcla Directa completada en:     {tiempo_md:.5f} segundos ({len(estados_mezcla_directa)-1} pasadas)")
    print(f"✔ Mezcla Equilibrada completada en: {tiempo_me:.5f} segundos ({len(pasadas_mezcla_equilibrada)-1} pasadas)")
    print("-" * 55)
    
    print("\n[🔎 ARREGLO ORDENADO]")
    
    LIMITE_IMPRESION = 1000
    
    if len(resultado_final) <= LIMITE_IMPRESION:
        for i in range(0, len(resultado_final), 10):
            fila = resultado_final[i : i + 10]
            texto_fila = "".join(f"{num:>8}" for num in fila)
            print(texto_fila)
        print(f"\n[✔] Se mostraron los {len(resultado_final)} elementos correctamente.\n")
    else:
        print(f"El arreglo es muy grande ({len(resultado_final)} elementos).")
        print("Mostrando los extremos para proteger la memoria de la consola:\n")
        
        print(f"Primeros 15: {resultado_final[:15]}")
        print(f"             ... [ {len(resultado_final) - 30} números ocultos ] ...")
        print(f"Últimos 15:  {resultado_final[-15:]}\n")