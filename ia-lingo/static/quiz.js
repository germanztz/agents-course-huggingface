// Variables globales específicas para la página del quiz
let preguntas = [];
let indicePreguntaActual = 0;
let puntuacionActual = 0;
let respuestaSeleccionada = false;

// Inicializar cuando el DOM esté cargado
document.addEventListener('DOMContentLoaded', function() {
    // Verificar si estamos en la página del quiz
    if (document.getElementById('pantalla-quiz')) {
        inicializarQuiz();
    }
});

async function inicializarQuiz() {
    try {
        await cargarPreguntas();
        
        // Log the loaded questions for debugging
        console.log('Preguntas cargadas:', preguntas);
        
        // If we have questions, show the first one
        if (preguntas && preguntas.length > 0) {
            console.log('Mostrando primera pregunta');
            // Add a small delay to ensure the DOM is fully loaded
            setTimeout(() => {
                mostrarPregunta();
            }, 100);
        } else {
            console.log('No hay preguntas disponibles');
            mostrarError('No hay preguntas disponibles');
        }
    } catch (error) {
        console.error('Error al cargar preguntas:', error);
        mostrarError('Error al cargar las preguntas. Por favor, intente de nuevo.');
    }
}

async function cargarPreguntas() {
    try {
        const respuesta = await fetch('/api/preguntas');
        if (!respuesta.ok) {
            throw new Error(`HTTP error! status: ${respuesta.status}`);
        }
        const data = await respuesta.json();
        preguntas = data;
        console.log('Preguntas cargadas desde API:', preguntas);
        return preguntas;
    } catch (error) {
        console.error('Error al cargar preguntas:', error);
        preguntas = [];
        return [];
    }
}

function mostrarPregunta() {
    console.log('Entrando en mostrarPregunta, índice actual:', indicePreguntaActual);
    console.log('Total de preguntas:', preguntas.length);
    
    if (indicePreguntaActual >= preguntas.length) {
        console.log('No hay más preguntas, mostrando resultados');
        mostrarResultados();
        return;
    }

    respuestaSeleccionada = false;
    const pregunta = preguntas[indicePreguntaActual];
    
    console.log('Pregunta actual:', pregunta);

    // Verificar que la pregunta existe y tiene los campos necesarios
    if (!pregunta || !pregunta.pregunta || !pregunta.opciones) {
        console.error('Pregunta inválida:', pregunta);
        mostrarError('Error: Pregunta inválida');
        return;
    }

    // Debug: Check if elements exist
    const numeroPreguntaEl = documento('numero-pregunta');
    const preguntaTextoEl = documento('pregunta-texto');
    const opcionesEl = documento('opciones');
    
    console.log('Elementos disponibles:', {
        numeroPregunta: numeroPreguntaEl ? 'Existe' : 'No existe',
        preguntaTexto: preguntaTextoEl ? 'Existe' : 'No existe',
        opciones: opcionesEl ? 'Existe' : 'No existe'
    });

    if (numeroPreguntaEl) numeroPreguntaEl.textContent = indicePreguntaActual + 1;
    if (preguntaTextoEl) preguntaTextoEl.textContent = pregunta.pregunta;

    const contenedorOpciones = documento('opciones');
    if (contenedorOpciones) {
        contenedorOpciones.innerHTML = '';

        pregunta.opciones.forEach((opcion, indice) => {
            const boton = document.createElement('button');
            boton.className = 'opcion';
            boton.textContent = opcion;
            boton.onclick = () => seleccionarRespuesta(indice);
            contenedorOpciones.appendChild(boton);
        });
    }

    const explicacionEl = documento('explicacion');
    const btnSiguienteEl = documento('btn-siguiente');
    
    if (explicacionEl) explicacionEl.classList.add('hidden');
    if (btnSiguienteEl) btnSiguienteEl.classList.add('hidden');

    actualizarBarraProgreso();
}

async function seleccionarRespuesta(indice) {
    if (respuestaSeleccionada) return;

    respuestaSeleccionada = true;
    const pregunta = preguntas[indicePreguntaActual];

    try {
        const respuesta = await fetch('/api/verificar-respuesta', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                pregunta_id: indicePreguntaActual + 1,
                respuesta_usuario: indice
            })
        });

        const resultado = await respuesta.json();
        mostrarFeedback(indice, resultado);
    } catch (error) {
        console.error('Error al verificar respuesta:', error);
        mostrarFeedbackLocal(indice);
    }
}

function mostrarFeedback(indiceSeleccionado, resultado) {
    const opciones = documento('opciones').children;
    const respuestaCorrecta = resultado.respuesta_correcta;

    for (let i = 0; i < opciones.length; i++) {
        opciones[i].classList.add('deshabilitada');
        if (i === respuestaCorrecta) {
            opciones[i].classList.add('correcta');
        } else if (i === indiceSeleccionado && !resultado.es_correcta) {
            opciones[i].classList.add('incorrecta');
        }
    }

    if (resultado.es_correcta) {
        puntuacionActual++;
        const puntuacionEl = documento('puntuacion');
        if (puntuacionEl) puntuacionEl.textContent = puntuacionActual;
    }

    const textoExplicacionEl = documento('texto-explicacion');
    const explicacionEl = documento('explicacion');
    const btnSiguienteEl = documento('btn-siguiente');
    
    if (textoExplicacionEl) textoExplicacionEl.textContent = resultado.explicacion;
    if (explicacionEl) explicacionEl.classList.remove('hidden');
    if (btnSiguienteEl) btnSiguienteEl.classList.remove('hidden');
}

function mostrarFeedbackLocal(indiceSeleccionado) {
    const pregunta = preguntas[indicePreguntaActual];
    const respuestaCorrecta = pregunta.respuesta_correcta;
    const opciones = documento('opciones').children;

    for (let i = 0; i < opciones.length; i++) {
        opciones[i].classList.add('deshabilitada');
        if (i === respuestaCorrecta) {
            opciones[i].classList.add('correcta');
        } else if (i === indiceSeleccionado && indiceSeleccionado !== respuestaCorrecta) {
            opciones[i].classList.add('incorrecta');
        }
    }

    if (indiceSeleccionado === respuestaCorrecta) {
        puntuacionActual++;
        const puntuacionEl = documento('puntuacion');
        if (puntuacionEl) puntuacionEl.textContent = puntuacionActual;
    }

    const textoExplicacionEl = documento('texto-explicacion');
    const explicacionEl = documento('explicacion');
    const btnSiguienteEl = documento('btn-siguiente');
    
    if (textoExplicacionEl) textoExplicacionEl.textContent = pregunta.explicacion;
    if (explicacionEl) explicacionEl.classList.remove('hidden');
    if (btnSiguienteEl) btnSiguienteEl.classList.remove('hidden');
}

function actualizarBarraProgreso() {
    const porcentaje = ((indicePreguntaActual) / preguntas.length) * 100;
    const barraProgresoEl = documento('barra-progreso');
    const numeroPreguntaEl = documento('numero-pregunta');
    
    if (barraProgresoEl) barraProgresoEl.style.width = porcentaje + '%';
    if (numeroPreguntaEl) numeroPreguntaEl.textContent = indicePreguntaActual + 1;
    
    const infoValorEl = document.querySelector('.info-etiqueta:nth-child(2) + .info-valor');
    if (infoValorEl) infoValorEl.textContent = preguntas.length;
}

function siguientePregunta() {
    indicePreguntaActual++;
    mostrarPregunta();
}

function mostrarResultados() {
    const pantallaQuizEl = documento('pantalla-quiz');
    const pantallaResultadosEl = documento('pantalla-resultados');
    
    if (pantallaQuizEl) pantallaQuizEl.classList.add('hidden');
    if (pantallaResultadosEl) pantallaResultadosEl.classList.remove('hidden');

    const porcentaje = Math.round((puntuacionActual / preguntas.length) * 100);
    const mensajes = {
        100: '¡Perfecto! ¡Eres un experto!',
        80: '¡Excelente! Demostraste un gran conocimiento.',
        60: 'Bien hecho. Hay aspectos para mejorar.',
        40: 'Debes estudiar un poco más estos temas.',
        0: 'No te desanimes, intenta de nuevo.'
    };

    let mensaje = mensajes[0];
    if (porcentaje >= 100) mensaje = mensajes[100];
    else if (porcentaje >= 80) mensaje = mensajes[80];
    else if (porcentaje >= 60) mensaje = mensajes[60];
    else if (porcentaje >= 40) mensaje = mensajes[40];

    const resultadoPuntuacionEl = documento('resultado-puntuacion');
    const resultadoPorcentajeEl = documento('resultado-porcentaje');
    const resultadoMensajeEl = documento('resultado-mensaje');
    const resultadoDetallesEl = documento('resultado-detalles');
    
    if (resultadoPuntuacionEl) resultadoPuntuacionEl.textContent = `${puntuacionActual}/${preguntas.length}`;
    if (resultadoPorcentajeEl) resultadoPorcentajeEl.textContent = `${porcentaje}%`;
    if (resultadoMensajeEl) resultadoMensajeEl.textContent = mensaje;
    if (resultadoDetallesEl) resultadoDetallesEl.textContent = `Respondiste correctamente ${puntuacionActual} de ${preguntas.length} preguntas en tu quiz.`;

    guardarEstadisticas();
}

async function guardarEstadisticas() {
    try {
        await fetch('/api/estadisticas', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                puntuacion: puntuacionActual,
                total: preguntas.length
            })
        });
    } catch (error) {
        console.error('Error al guardar estadísticas:', error);
    }
}

function reiniciarQuiz() {
    indicePreguntaActual = 0;
    puntuacionActual = 0;
    respuestaSeleccionada = false;
    
    // Redirect back to the welcome page
    window.location.href = '/';
}

// Función auxiliar para obtener elementos por ID
function documento(id) {
    return document.getElementById(id);
}

// Función para mostrar errores (compartida con welcome.js)
function mostrarError(mensaje) {
    const div = document.getElementById('mensajeError');
    if (div) {
        div.textContent = '⚠️ ' + mensaje;
        div.classList.add('mostrado');
    }
}