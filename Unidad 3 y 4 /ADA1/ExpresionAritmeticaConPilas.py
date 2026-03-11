def evaluar_expresion(expresion, tipo='posfija'):
    pila = []
    tokens = expresion.split()
    
    if tipo == 'prefija':
        tokens = reversed(tokens)

    try:
        for t in tokens:

            if t.replace('.', '', 1).isdigit() or (t.startswith('-') and t[1:].replace('.', '', 1).isdigit()):
                pila.append(float(t))
            else:

                if tipo == 'posfija':
                    op2 = pila.pop()
                    op1 = pila.pop()
                else:
                    op1 = pila.pop()
                    op2 = pila.pop()

                if t == '+': pila.append(op1 + op2)
                elif t == '-': pila.append(op1 - op2)
                elif t == '*': pila.append(op1 * op2)
                elif t == '/': pila.append(op1 / op2)
                elif t == '^': pila.append(op1 ** op2)
                else:
                    raise ValueError(f"Operador desconocido: {t}")
        
        if len(pila) != 1:
            raise ValueError("La expresión está mal formateada (sobran operandos).")
            
        return pila[0]

    except IndexError:
        return "Error: Faltan operandos para realizar la operación."
    except ZeroDivisionError:
        return "Error: División por cero."
    except Exception as e:
        return f"Error: {e}"

print("--- Evaluador de Expresiones con Pilas ---")


posfija = "5 3 + 2 *"
print(f"Posfija '{posfija}': {evaluar_expresion(posfija, 'posfija')}")

prefija = "* + 5 3 2"
print(f"Prefija '{prefija}': {evaluar_expresion(prefija, 'prefija')}")