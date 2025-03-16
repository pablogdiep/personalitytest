import sqlite3
from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# Crear la base de datos y la tabla si no existen
def init_db():
    conn = sqlite3.connect("inteligencia_emocional.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS respuestas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT,
                        correo TEXT,
                        respuestas TEXT,
                        puntaje INTEGER
                    )''')
    conn.commit()
    conn.close()

init_db()

# Página principal con el cuestionario en una interfaz visual
@app.route('/')
def index():
    return render_template('index.html')

# Guardar respuestas en la base de datos
@app.route('/guardar_respuestas', methods=['POST'])
def guardar_respuestas():
    data = request.json
    nombre = data['nombre']
    correo = data['correo']
    respuestas = data['respuestas']
    puntaje = sum(respuestas)  # Suma de los puntajes
    
    conn = sqlite3.connect("inteligencia_emocional.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO respuestas (nombre, correo, respuestas, puntaje) VALUES (?, ?, ?, ?)", 
                   (nombre, correo, str(respuestas), puntaje))
    conn.commit()
    conn.close()
    
    return jsonify({"mensaje": "Respuestas guardadas exitosamente", "puntaje": puntaje})

# Obtener todos los resultados
@app.route('/resultados', methods=['GET'])
def obtener_resultados():
    conn = sqlite3.connect("inteligencia_emocional.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM respuestas")
    datos = cursor.fetchall()
    conn.close()
    
    resultados = []
    for fila in datos:
        resultados.append({
            "id": fila[0],
            "nombre": fila[1],
            "correo": fila[2],
            "respuestas": fila[3],
            "puntaje": fila[4]
        })
    
    return jsonify(resultados)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
