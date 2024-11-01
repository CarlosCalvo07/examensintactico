from flask import Flask, render_template, request

app = Flask(__name__)

# Función auxiliar para verificar si un año es bisiesto
def es_bisiesto(anio):
    anio = int(anio)
    return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)

# Función para analizar CURP y generar tokens
def analizar_curp(curp):
    if len(curp) != 18:
        return None, None, "La CURP debe tener exactamente 18 caracteres."

    tokens = []
    tipos = []

    # Definición de tokens con sus respectivas reglas
    tokens.append(curp[0])  # Primera letra del primer apellido
    tipos.append("Primera letra del primer apellido")

    tokens.append(curp[1])  # Primera vocal interna del primer apellido
    tipos.append("Primera vocal interna del primer apellido")

    tokens.append(curp[2])  # Primera letra del segundo apellido
    tipos.append("Primera letra del segundo apellido")

    tokens.append(curp[3])  # Primera letra del primer nombre
    tipos.append("Primera letra del primer nombre")

    tokens.append(curp[4:6])  # Últimos dos dígitos del año de nacimiento
    tipos.append("Últimos dos dígitos del año de nacimiento")

    tokens.append(curp[6:8])  # Mes de nacimiento
    tipos.append("Mes de nacimiento")

    tokens.append(curp[8:10])  # Día de nacimiento
    tipos.append("Día de nacimiento")

    tokens.append(curp[10])  # Sexo
    tipos.append("Sexo")

    tokens.append(curp[11:13])  # Estado de nacimiento
    tipos.append("Estado de nacimiento")

    tokens.append(curp[13])  # Primera consonante interna del primer apellido
    tipos.append("Primera consonante interna del primer apellido")

    tokens.append(curp[14])  # Primera consonante interna del segundo apellido
    tipos.append("Primera consonante interna del segundo apellido")

    tokens.append(curp[15])  # Primera consonante interna del primer nombre
    tipos.append("Primera consonante interna del primer nombre")

    tokens.append(curp[16:18])  # Dígitos para evitar duplicidades y RENAPO
    tipos.append("RENAPO")  # Este es el tipo correcto para los últimos dos dígitos

    # Año, mes y día de nacimiento
    anio = int(curp[4:6])
    mes = int(curp[6:8])
    dia = int(curp[8:10])

    # Determinar si el año corresponde al siglo 1900 o 2000
    if anio <= 23:  # Asume que CURP usa años desde 2000 en adelante
        anio += 2000
    else:
        anio += 1900

    # Validación de mes
    if mes < 1 or mes > 12:
        return None, None, "Fecha inválida: el mes debe estar entre 01 y 12."

    # Diccionario para los días máximos de cada mes
    dias_por_mes = {
        1: 31, 2: 29 if es_bisiesto(anio) else 28, 3: 31,
        4: 30, 5: 31, 6: 30, 7: 31,
        8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }

    # Validación de días para el mes
    if dia < 1 or dia > dias_por_mes[mes]:
        return None, None, f"Fecha inválida: el día para el mes {mes:02} debe estar entre 01 y {dias_por_mes[mes]:02}."

    total_tokens = len(tokens)

    return tokens, tipos, None  # Retornamos None en el tercer parámetro si no hay errores

# Ruta para mostrar el formulario y los resultados
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        curp = request.form['curp']
        
        tokens, tipos, error = analizar_curp(curp)
        
        if error:
            return render_template('vistacurp.html', error=error)
        
        token_data = zip(tokens, tipos)  # Combinamos tokens y tipos aquí en Python
        total_tokens = len(tokens)
        return render_template('vistacurp.html', curp=curp, token_data=token_data, total_tokens=total_tokens)
    
    return render_template('vistacurp.html')

if __name__ == '__main__':
    app.run(debug=True)