# Aplicación Quiz en Python con Flask
from flask import Flask, render_template, request, jsonify, session
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from pdf_processor import process_pdf_with_ollama

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# Directorio para archivos cargados
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'} 

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB máximo

# Base de datos de preguntas por defecto
PREGUNTAS_DEFECTO = [
    {
        "id": 1,
        "pregunta": "¿Qué es Python?",
        "opciones": [
            "Un lenguaje de programación interpretado y de alto nivel",
            "Un tipo de serpiente venenosa",
            "Un sistema operativo de código abierto",
            "Un framework de desarrollo web"
        ],
        "respuesta_correcta": 0,
        "explicacion": "Python es un lenguaje de programación interpretado, de alto nivel y de propósito general. Fue creado por Guido van Rossum y se caracteriza por su sintaxis clara y legible."
    },
    {
        "id": 2,
        "pregunta": "¿Cuál es la diferencia principal entre una lista y una tupla en Python?",
        "opciones": [
            "Las listas son más rápidas que las tuplas",
            "Las tuplas son inmutables, las listas son mutables",
            "Las tuplas solo pueden contener números",
            "No hay diferencia, son sinónimos"
        ],
        "respuesta_correcta": 1,
        "explicacion": "La diferencia fundamental es que las tuplas son inmutables (no se pueden modificar después de su creación), mientras que las listas son mutables (se pueden agregar, eliminar o modificar elementos)."
    },
    {
        "id": 3,
        "pregunta": "¿Qué significa HTML?",
        "opciones": [
            "High Tech Modern Language",
            "Hyperlinks and Text Markup Language",
            "HyperText Markup Language",
            "Home Tool Markup Language"
        ],
        "respuesta_correcta": 2,
        "explicacion": "HTML significa HyperText Markup Language (Lenguaje de Marcado de HiperTexto). Es el lenguaje estándar utilizado para crear y estructurar páginas web."
    },
    {
        "id": 4,
        "pregunta": "¿Cuál es el propósito principal de Docker?",
        "opciones": [
            "Crear aplicaciones web",
            "Gestionar bases de datos",
            "Contenedorizar aplicaciones para facilitar su despliegue",
            "Desarrollar aplicaciones móviles"
        ],
        "respuesta_correcta": 2,
        "explicacion": "Docker es una plataforma de contenedorización que permite empaquetar aplicaciones y sus dependencias en contenedores portátiles, facilitando el despliegue consistente en diferentes entornos."
    },
    {
        "id": 5,
        "pregunta": "¿Qué es un API REST?",
        "opciones": [
            "Un protocolo de seguridad web",
            "Una interfaz de programación que usa HTTP para comunicación entre sistemas",
            "Un lenguaje de programación para backend",
            "Una base de datos en la nube"
        ],
        "respuesta_correcta": 1,
        "explicacion": "REST (Representational State Transfer) es un estilo arquitectónico para APIs que utiliza métodos HTTP (GET, POST, PUT, DELETE) para permitir la comunicación entre sistemas de manera estandarizada y escalable."
    },
    {
        "id": 6,
        "pregunta": "¿Qué es Kubernetes?",
        "opciones": [
            "Un lenguaje de programación",
            "Una plataforma de orquestación de contenedores",
            "Un sistema de control de versiones",
            "Un framework de testing"
        ],
        "respuesta_correcta": 1,
        "explicacion": "Kubernetes es una plataforma de código abierto para automatizar el despliegue, escalado y gestión de aplicaciones contenedorizadas. Orquesta contenedores Docker en clusters de servidores."
    },
    {
        "id": 7,
        "pregunta": "¿Cuál es la función principal de Git?",
        "opciones": [
            "Crear páginas web",
            "Control de versiones de código fuente",
            "Compilar programas",
            "Gestionar bases de datos"
        ],
        "respuesta_correcta": 1,
        "explicacion": "Git es un sistema de control de versiones distribuido que permite a los desarrolladores rastrear cambios en el código fuente, colaborar en proyectos y mantener un historial completo de modificaciones."
    },
    {
        "id": 8,
        "pregunta": "¿Qué es una base de datos relacional?",
        "opciones": [
            "Una base de datos que solo funciona en la nube",
            "Una base de datos que organiza datos en tablas relacionadas entre sí",
            "Una base de datos temporal",
            "Una base de datos sin estructura"
        ],
        "respuesta_correcta": 1,
        "explicacion": "Una base de datos relacional organiza la información en tablas (relaciones) que pueden estar conectadas entre sí mediante claves. Ejemplos incluyen MySQL, PostgreSQL y Oracle."
    }
]

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
       
def validar_preguntas(preguntas):
    """Valida que las preguntas tengan el formato correcto"""
    if not isinstance(preguntas, list) or len(preguntas) == 0:
        return False, "El archivo debe contener una lista de preguntas"
    
    for idx, pregunta in enumerate(preguntas):
        if not isinstance(pregunta, dict):
            return False, f"Pregunta {idx + 1}: debe ser un objeto"
        
        campos_requeridos = ['pregunta', 'opciones', 'respuesta_correcta', 'explicacion']
        for campo in campos_requeridos:
            if campo not in pregunta:
                return False, f"Pregunta {idx + 1}: falta el campo '{campo}'"
        
        if not isinstance(pregunta['opciones'], list) or len(pregunta['opciones']) != 4:
            return False, f"Pregunta {idx + 1}: debe tener exactamente 4 opciones"
        
        if not isinstance(pregunta['respuesta_correcta'], int) or pregunta['respuesta_correcta'] not in [0, 1, 2, 3]:
            return False, f"Pregunta {idx + 1}: respuesta_correcta debe ser 0, 1, 2 o 3"
    
    return True, "Preguntas válidas"

@app.route('/')
def index():
    """Página principal del quiz - pantalla de bienvenida"""
    session.clear()
    return render_template('welcome.html')

@app.route('/quiz')
def quiz():
    """Página del quiz - pantalla de preguntas"""
    # Check if there are questions in the session
    if 'preguntas' not in session or len(session.get('preguntas', [])) == 0:
        # If no questions in session, use default questions
        session['preguntas'] = PREGUNTAS_DEFECTO
        session.modified = True
    
    return render_template('quiz.html')

@app.route('/api/preguntas')
def obtener_preguntas():
    """Retorna todas las preguntas sin revelar la respuesta correcta"""
    # Always ensure we have questions in the session
    if 'preguntas' not in session or len(session.get('preguntas', [])) == 0:
        session['preguntas'] = PREGUNTAS_DEFECTO
        session.modified = True
    
    preguntas = session.get('preguntas', PREGUNTAS_DEFECTO)
    preguntas_sin_respuesta = []
    for i, pregunta in enumerate(preguntas):
        # Ensure the question has all required fields
        if isinstance(pregunta, dict) and 'pregunta' in pregunta and 'opciones' in pregunta:
            pregunta_temp = {
                "id": pregunta.get("id", i + 1),
                "pregunta": pregunta["pregunta"],
                "opciones": pregunta["opciones"]
            }
            preguntas_sin_respuesta.append(pregunta_temp)
        else:
            print(f"Pregunta inválida en posición {i}: {pregunta}")
    
    return jsonify(preguntas_sin_respuesta)

    
@app.route('/api/cargar-archivo', methods=['POST'])
def cargar_archivo():
    """Carga un archivo PDF y extrae preguntas usando Ollama"""
    if 'archivo' not in request.files:
        return jsonify({'error': 'No se ha proporcionado archivo'}), 400
    
    archivo = request.files['archivo']
    
    if archivo.filename == '':
        return jsonify({'error': 'No se ha seleccionado archivo'}), 400
    
    if not allowed_file(archivo.filename):
        return jsonify({'error': 'Solo se permiten archivos PDF'}), 400
    
    try:
        # Save PDF file
        filename = secure_filename(archivo.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        archivo.save(pdf_path)
        
        # Process PDF with Ollama
        preguntas, json_path = process_pdf_with_ollama(pdf_path, filename)
        
        if not preguntas:
            return jsonify({'error': 'No se pudieron extraer preguntas del PDF'}), 400
        
        # Validate questions
        es_valido, mensaje = validar_preguntas(preguntas)
        if not es_valido:
            return jsonify({'error': f'Preguntas extraídas no válidas: {mensaje}'}), 400
        
        # Store in session
        session['preguntas'] = preguntas
        session.modified = True
        
        return jsonify({
            'exito': True,
            'mensaje': f'PDF procesado exitosamente. {len(preguntas)} preguntas extraídas y guardadas en {os.path.basename(json_path)}.',
            'cantidad_preguntas': len(preguntas),
            'archivo_json': os.path.basename(json_path)
        })
    
    except Exception as e:
        return jsonify({'error': f'Error al procesar el archivo: {str(e)}'}), 500


@app.route('/api/verificar-respuesta', methods=['POST'])
def verificar_respuesta():
    """Verifica si la respuesta del usuario es correcta"""
    datos = request.json
    pregunta_id = datos.get('pregunta_id')
    respuesta_usuario = datos.get('respuesta_usuario')
    
    preguntas = session.get('preguntas', PREGUNTAS_DEFECTO)
    
    # Buscar la pregunta
    pregunta = None
    for p in preguntas:
        if p.get('id') == pregunta_id or preguntas.index(p) == pregunta_id - 1:
            pregunta = p
            break
    
    if not pregunta:
        return jsonify({'error': 'Pregunta no encontrada'}), 404
    
    es_correcta = respuesta_usuario == pregunta['respuesta_correcta']
    
    return jsonify({
        'es_correcta': es_correcta,
        'respuesta_correcta': pregunta['respuesta_correcta'],
        'explicacion': pregunta['explicacion'],
        'opciones': pregunta['opciones']
    })

@app.route('/api/estadisticas', methods=['POST'])
def guardar_estadisticas():
    """Guarda las estadísticas finales del quiz"""
    datos = request.json
    puntuacion = datos.get('puntuacion')
    total = datos.get('total')
    porcentaje = (puntuacion / total * 100) if total > 0 else 0
    
    estadistica = {
        'puntuacion': puntuacion,
        'total': total,
        'porcentaje': round(porcentaje, 2),
        'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return jsonify(estadistica)

@app.errorhandler(404)
def no_encontrado(error):
    return jsonify({'error': 'Recurso no encontrado'}), 404

@app.errorhandler(500)
def error_servidor(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
@app.errorhandler(500)
def error_servidor(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)