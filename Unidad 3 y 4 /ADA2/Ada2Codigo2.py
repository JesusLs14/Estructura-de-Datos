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
        
    def tamano(self):
        return len(self.items)

class SistemaSeguros:
    def __init__(self):
        self.colas_por_servicio = {}
        self.contadores_tickets = {}

    def registrar_llegada(self, servicio):
        if servicio not in self.colas_por_servicio:
            self.colas_por_servicio[servicio] = Cola()
            self.contadores_tickets[servicio] = 1

        numero_ticket = self.contadores_tickets[servicio]
        self.colas_por_servicio[servicio].encolar(numero_ticket)
        
        print(f"\n[+] Cliente registrado. Servicio: {servicio} | Su número de atención es: {numero_ticket}")
        self.contadores_tickets[servicio] += 1

    def atender_cliente(self, servicio):
        if servicio in self.colas_por_servicio and not self.colas_por_servicio[servicio].esta_vacia():
            ticket_llamado = self.colas_por_servicio[servicio].desencolar()
            print(f"\n[!] ATENCIÓN: Llamando al ticket {ticket_llamado} del Servicio {servicio}")
        else:
            print(f"\n[-] No hay clientes en espera para el Servicio {servicio}.")

    def mostrar_estado(self):
        print("\n=== ESTADO ACTUAL DE LAS COLAS ===")
        if not self.colas_por_servicio:
            print("Aún no se han registrado servicios ni clientes.")
        else:
            for servicio, cola in self.colas_por_servicio.items():
                cantidad = cola.tamano()
                if cantidad > 0:
                    print(f" - Servicio {servicio}: {cantidad} cliente(s) en espera. (Tickets en fila: {cola.items})")
                else:
                    print(f" - Servicio {servicio}: Sin clientes en espera.")
        print("==================================")


def ejecutar_sistema():
    sistema = SistemaSeguros()
    print("=== SISTEMA DE ATENCIÓN - COMPAÑÍA DE SEGUROS ===")
    print("Instrucciones:")
    print(" - 'C' + número de servicio para llegada (Ej: C1, C2)")
    print(" - 'A' + número de servicio para atender (Ej: A1, A2)")
    print(" - 'E' para ver el estado de todas las colas")
    print(" - 'S' para salir del sistema")
    print("=================================================")

    while True:
        comando = input("\nIngrese comando (C#, A#, E, S): ").strip().upper()

        if comando == 'S':
            print("\nSaliendo del sistema... ¡Hasta luego!")
            break
            

        if comando == 'E':
            sistema.mostrar_estado()
            continue
        
        if len(comando) < 2:
            print("\n[x] Comando inválido. Recuerde el formato (Ej: C1, A2).")
            continue

        accion = comando[0]
        servicio = comando[1:] 

        if accion == 'C':
            sistema.registrar_llegada(servicio)
        elif accion == 'A':
            sistema.atender_cliente(servicio)
        else:
            print("\n[x] Acción no reconocida. Use 'C', 'A', 'E' o 'S'.")

if __name__ == "__main__":
    ejecutar_sistema()