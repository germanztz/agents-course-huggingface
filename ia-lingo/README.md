# Aplicación Quiz Interactivo en Python

Una aplicación web de preguntas y respuestas desarrollada con **Python y Flask**. La aplicación presenta preguntas con 4 opciones, valida respuestas en tiempo real, muestra retroalimentación inmediata y proporciona explicaciones detalladas.

## Características

✅ 8 preguntas de ejemplo sobre programación y tecnología  
✅ 4 opciones por pregunta  
✅ Validación de respuestas en el servidor (Python/Flask)  
✅ Feedback visual inmediato (respuestas correctas/incorrectas)  
✅ Desaparición animada de respuestas incorrectas 
✅ Explicaciones detalladas para cada pregunta  
✅ Sistema de puntuación en tiempo real  
✅ Pantalla de resultados finales  
✅ Diseño responsivo (mobile-friendly)  
✅ Interfaz moderna con gradientes y animaciones  

### 3. Usar el quiz

1. entra a la pantalla welcome
2. en la pantalla welcome Haz clic en "cargar pdf comenzar" selecciona un pdf, se sube el pdf al servidor i comienza la primera pregunta
3. en la pantalla welcome Haz clic en "Comenzar" para ir a la primera pregunta
4. Lee cada pregunta y selecciona una opción
5. retroalimentacion al usuario si la respuesta es correcta o incorrecta
6. la respuesta correcta se marca en verde y se ocultan el resto de respuestas
7. aparece la explicacion justificando la respuesta junto con el boton siguiente
8. Haz clic en "Siguiente" para continuar con la siguiente pregunta
9. Durante las preguntas siempre aparece en pantalla estadisticas del juego: pregunta 5 de 10 puntutación: 5


## Estructura del Proyecto

```
quiz-app/
├── src/
│   ├── app.py                 # Backend Flask con API REST
│   ├── questions.py           # Backend generate_questions, get_questions, load_questions, verify_response
│   └── models/                 # directorio de modelo de datos
|       └── question.py                 # class que describe una question
├── test/                 # tests unitarios
│   └── test_question.py         # tests unitarios para question.py
├── static/
│   ├── styles.css         # Estilos CSS para la interfaz web
│   ├── preguntas-ejemplo.json         # Preguntas de ejemplo 
|   └── script.js         # JavaScript
├── templates/
│   ├── welcome.html      # HTML para la pantalla de inicio
|   └── quiz.html         # HTML para el quiz
├── uploads/              # Directorio para subir archivos pdf
├── requirements.txt      # Dependencias Python
├── DockerFile            # para ejecutar la app en docker
└── README.md             # README con la descripcion de la estructura, instalacion
```

## Question model

```
Question:
  id: int
  question: str #the given question
  answers: list[Answer] # list of possible answers
  hint: str # clue about the question
  why: str # explanation why is correct

Answer:
  answer: str #the given answer
  is_correct: bool # True si es la respuesta correcta, False si no
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
