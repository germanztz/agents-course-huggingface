# Interactive Quiz App in Python

A web application for questions and answers developed with **Python and Flask**. The app presents questions with 4 options, validates answers in real time, provides immediate feedback, and offers detailed explanations.

## Features

✅ 8 example questions on programming and technology  
✅ 4 options per question  
✅ Server-side answer validation (Python/Flask)  
✅ Visual immediate feedback (correct turns green / incorrect selected answer turnd red)  
✅ Detailed explanations for each question
✅ Real-time scoring system
✅ Final results screen
✅ Responsive design (mobile-friendly)  
✅ Modern interface with gradients and animations

### 3. Use the quiz

1. Go to the welcome screen  
3. On the welcome screen, click "Start" to go to the first question  
4. Read each question and select an option  
5. Provide feedback to the user, The correct answer is marked in green, if the answer is incorrect, the selected option turns red  
7. The explanation justifying the answer appears along with the "Next" button  
8. Click "Next" to continue to the next question  
9. During the questions, the game statistics are always displayed on the screen: example Question 5 of 10, Score: 5

## Project Structure

```
quiz-app/
├── src/
│   ├── app.py                 # Flask backend with REST API
│   ├── questions-controller.py  # Controller for handling requests to generate and retrieve questions, functions: generate_questions, get_questions, load_questions, verify_response
│   └── models/                 # directory for data models
|       └── question.py                 # class that describes a question
├── test/                 # unit tests
│   └── test_question.py         # unit tests for question.py
├── static/
│   ├── styles.css         # CSS styles for the web interface
|   └── script.js         # JavaScript
├── templates/
│   ├── welcome.html      # HTML for the welcome screen
|   └── quiz.html         # HTML for the quiz
├── data/                 # directory for store app data files
│   └── example_questions.json         # example questions
├── requirements.txt      # Python dependencies
├── DockerFile            # to run the app in Docker
└── README.md             # README with the description of the structure, installation
```

## Question model

```
Question:
  id: int # unique id 
  question: str # the given question
  answer: str # the correct answer
  source: str # explanation 
```

## Requisitos

- Python 3.7+
- pip (gestor de paquetes de Python)

## Instalación

### 1. Crear un entorno virtual (recomendado)

```bash
# En macOS/Linux
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Uso

### 1. Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en: **http://localhost:5000**

### 2. Acceder a la aplicación

Abre tu navegador web y ve a `http://localhost:5000`

### 3. Usar el quiz

1. Haz clic en "Comenzar Quiz"
2. Lee cada pregunta y selecciona una opción
3. Recibe retroalimentación inmediata
4. Lee la explicación de la respuesta correcta
5. Haz clic en "Siguiente Pregunta" para continuar
6. Al terminar, verás tu puntuación final

## Endpoints API

### `GET /`
Retorna la página principal del quiz.

### `GET /api/preguntas`
Retorna todas las preguntas (sin revelar respuestas correctas).

**Respuesta:**
```json
[
  {
    "id": 1,
    "pregunta": "¿Qué es Python?",
    "opciones": ["...", "...", "...", "..."]
  }
]
```

### `POST /api/verificar-respuesta`
Verifica si la respuesta del usuario es correcta.

**Solicitud:**
```json
{
  "pregunta_id": 1,
  "respuesta_usuario": 0
}
```

**Respuesta:**
```json
{
  "es_correcta": true,
  "respuesta_correcta": 0,
  "explicacion": "Texto de explicación...",
  "opciones": ["...", "...", "...", "..."]
}
```

### `POST /api/estadisticas`
Guarda las estadísticas finales del quiz.

**Solicitud:**
```json
{
  "puntuacion": 7,
  "total": 8
}
```

**Respuesta:**
```json
{
  "puntuacion": 7,
  "total": 8,
  "porcentaje": 87.5,
  "fecha": "2025-11-02 19:30:00"
}
```

## Personalización

### Agregar nuevas preguntas

Edita el archivo `app.py` y agrega nuevos objetos al array `PREGUNTAS`:

```python
{
    "id": 9,
    "pregunta": "Tu pregunta aquí",
    "opciones": [
        "Opción 1",
        "Opción 2",
        "Opción 3",
        "Opción 4"
    ],
    "respuesta_correcta": 0,  # Índice de la respuesta correcta (0-3)
    "explicacion": "Explicación detallada de la respuesta..."
}
```

### Cambiar estilos

Los estilos CSS están en la sección `<style>` del archivo `templates/index.html`. Puedes personalizar:

- Colores (gradientes principales en `background` y `.btn-siguiente`)
- Tamaños de fuente
- Espaciado y márgenes
- Animaciones y transiciones

### Cambiar la clave secreta

En `app.py`, cambia la línea:
```python
app.secret_key = 'your-secret-key-here-change-in-production'
```

Por una clave segura para producción.

## Persistencia de Datos

Actualmente, las estadísticas se calculan pero no se persisten. Para guardar en una base de datos:

1. Instala un driver de base de datos (ejemplo: `pip install mysql-connector-python`)
2. Modifica la función `guardar_estadisticas()` en `app.py`
3. Implementa la conexión a tu base de datos preferida (MySQL, PostgreSQL, SQLite, etc.)

## Despliegue en Producción

Para desplegar en producción:

1. Cambia `debug=True` a `debug=False` en `app.py`
2. Usa un servidor WSGI como [Gunicorn](https://gunicorn.org/):
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```
3. Configura un proxy inverso (Nginx, Apache)
4. Usa HTTPS
5. Cambia la clave secreta
6. Considera usar variables de entorno para configuración sensible

## Tecnologías

- **Backend:** Python 3, Flask
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Servidor:** WSGI (Flask development, Gunicorn para producción)
- **Base de datos:** Opcional (actualmente en memoria)

## Licencia

Este proyecto es de código abierto y libre para usar y modificar.

## Autor

Desarrollado como aplicación educativa de quiz interactivo.

## Soporte

Si encuentras problemas:

1. Verifica que Python esté instalado: `python --version`
2. Confirma que Flask esté instalado: `pip list | grep Flask`
3. Revisa los logs en la consola para errores
4. Asegúrate de que el puerto 5000 no esté en uso
