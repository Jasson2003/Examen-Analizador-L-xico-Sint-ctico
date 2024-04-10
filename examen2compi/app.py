from flask import Flask, render_template,request

app = Flask(__name__)

# Función para analizar los tokens
def analizar_codigo(codigo):
    palabras_clave = {'include', 'using', 'namespace', 'std', 'int', 'main'}
    operadores = {'<', '>', ';', '}', '{'}
    
    tokens = []

    # Separar el código en palabras separadas
    palabras = codigo.split()

    # Analizar cada palabra
    for palabra in palabras:
        if palabra in palabras_clave:
            tokens.append((palabra, 'Palabra clave'))
        elif palabra in operadores:
            tokens.append((palabra, 'Operador'))
        elif palabra.startswith('"') and palabra.endswith('"'):
            tokens.append((palabra, 'Literal de cadena'))
        else:
            tokens.append((palabra, 'Identificador'))

    return tokens

# Función para analizar la sintaxis del código
def analizar_sintaxis(codigo):
    errores_sintacticos = []
    lineas = codigo.split('\n')

    # Verificar errores sintácticos globales
    if '#include <iostream>' not in codigo:
        errores_sintacticos.append("Falta '#include <iostream>'")
    if 'using namespace std;' not in codigo:
        errores_sintacticos.append("Falta 'using namespace std;'")
    if 'int main()' not in codigo:
        errores_sintacticos.append("Falta 'int main()'")
    if 'cout << "Hello, World!";' not in codigo:
        errores_sintacticos.append('Falta la línea de salida "cout << "Hello, World!";"')
    
    # Identificar la posición de los errores en el código
    for num_linea, linea in enumerate(lineas, start=1):
        # Verificar errores sintácticos específicos por línea
        if '#include <iostream>' not in linea:
            errores_sintacticos.append(f"Error sintáctico: Falta '#include <iostream>' en la línea {num_linea}")
            break
        if 'using namespace std;' not in linea:
            errores_sintacticos.append(f"Error sintáctico: Falta 'using namespace std;' en la línea {num_linea}")
            break
        if 'int main()' not in linea:
            errores_sintacticos.append(f"Error sintáctico: Falta 'int main()' en la línea {num_linea}")
            break
        if 'cout << "Hello, World!";' not in linea:
            errores_sintacticos.append(f'Error sintáctico: Falta la línea de salida "cout << "Hello, World!";" en la línea {num_linea}')
            break

    return errores_sintacticos

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        codigo = request.form['codigo']
        tokens = analizar_codigo(codigo)
        errores_sintacticos = analizar_sintaxis(codigo)
        
        if not errores_sintacticos:
            return render_template('sin_errores.html', codigo=codigo, tokens=tokens)
        else:
            return render_template('resultado.html', codigo=codigo, tokens=tokens, errores_sintacticos=errores_sintacticos)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
