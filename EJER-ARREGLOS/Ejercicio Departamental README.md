Usé una matriz donde las filas representan los meses y las columnas los departamentos.
Implementé métodos para insertar, buscar y eliminar ventas accediendo a las posiciones por índice, lo que hace el programa eficiente y fácil de mantener. El método para insertar ventas recibe como parámetros el mes, el departamento y el monto de la venta. Primero valida que el mes y el departamento existan dentro de la estructura. Después, obtiene la posición exacta dentro de la matriz usando los índices correspondientes y almacena el monto en esa celda. 

El método de búsqueda permite consultar una venta específica indicando el mes y el departamento. Al igual que en el método para insertar, se utilizan los índices de fila y columna para acceder directamente al valor almacenado en la matriz, lo que hace la búsqueda rápida y eficiente.

El método para eliminar una venta no modifica el tamaño de la matriz, sino que restablece el valor de la venta a cero en la posición indicada. Esto simula la eliminación de una venta manteniendo la estructura del arreglo intacta.

Finalmente, el método para mostrar la tabla recorre la matriz y presenta los datos de forma ordenada, mostrando los meses como filas y los departamentos como columnas.
