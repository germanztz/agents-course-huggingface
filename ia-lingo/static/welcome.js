// Variables globales específicas para la página de bienvenida
let archivoSeleccionadoActual = null;

// Inicializar cuando el DOM esté cargado
document.addEventListener('DOMContentLoaded', function() {
    // Verificar si estamos en la página de bienvenida
    const areaCarga = document.getElementById('areaCarga');
    const inputArchivo = document.getElementById('inputArchivo');
    
    // Solo inicializar si los elementos existen (estamos en la página de bienvenida)
    if (areaCarga && inputArchivo) {
        inicializarEventosArrastrarSoltar(areaCarga, inputArchivo);
    }
});

function inicializarEventosArrastrarSoltar(areaCarga, inputArchivo) {
    // Eventos de arrastrar y soltar
    areaCarga.addEventListener('dragover', (e) => {
        e.preventDefault();
        areaCarga.classList.add('sobre');
    });

    areaCarga.addEventListener('dragleave', () => {
        areaCarga.classList.remove('sobre');
    });

    areaCarga.addEventListener('drop', (e) => {
        e.preventDefault();
        areaCarga.classList.remove('sobre');
        const archivos = e.dataTransfer.files;
        if (archivos.length > 0) {
            inputArchivo.files = archivos;
            manejarSeleccionArchivo({ target: inputArchivo });
        }
    });
}

function abrirSelector() {
    const inputArchivo = document.getElementById('inputArchivo');
    if (inputArchivo) {
        inputArchivo.click();
    }
}

function manejarSeleccionArchivo(event) {
    const archivo = event.target.files[0];
    if (!archivo) return;

    if (archivo.type !== 'application/pdf') {
        mostrarError('Por favor, selecciona un archivo PDF válido');
        return;
    }

    archivoSeleccionadoActual = archivo;
    const nombreArchivoEl = document.getElementById('nombreArchivo');
    const archivoSeleccionadoEl = document.getElementById('archivoSeleccionado');
    const botonesArchivoEl = document.getElementById('botonesArchivo');
    
    if (nombreArchivoEl) nombreArchivoEl.textContent = archivo.name;
    if (archivoSeleccionadoEl) archivoSeleccionadoEl.classList.add('mostrado');
    if (botonesArchivoEl) botonesArchivoEl.style.display = 'flex';
    
    limpiarMensajes();
}

function cargarArchivo() {
    if (!archivoSeleccionadoActual) return;

    const formData = new FormData();
    formData.append('archivo', archivoSeleccionadoActual);

    const btn = event.target;
    if (btn) {
        btn.disabled = true;
        btn.textContent = 'Cargando...';
    }

    fetch('/api/cargar-archivo', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            mostrarError(data.error);
            if (btn) {
                btn.disabled = false;
                btn.textContent = 'Cargar y Comenzar';
            }
        } else {
            mostrarExito(`${data.mensaje}`);
            setTimeout(() => iniciarQuiz(), 1500);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarError('Error al cargar el archivo');
        if (btn) {
            btn.disabled = false;
            btn.textContent = 'Cargar y Comenzar';
        }
    });
}

function cancelarArchivo() {
    archivoSeleccionadoActual = null;
    const inputArchivo = document.getElementById('inputArchivo');
    const archivoSeleccionadoEl = document.getElementById('archivoSeleccionado');
    const botonesArchivoEl = document.getElementById('botonesArchivo');
    
    if (inputArchivo) inputArchivo.value = '';
    if (archivoSeleccionadoEl) archivoSeleccionadoEl.classList.remove('mostrado');
    if (botonesArchivoEl) botonesArchivoEl.style.display = 'none';
    
    limpiarMensajes();
}

function mostrarError(mensaje) {
    const div = document.getElementById('mensajeError');
    if (div) {
        div.textContent = '⚠️ ' + mensaje;
        div.classList.add('mostrado');
    }
}

function mostrarExito(mensaje) {
    const div = document.getElementById('mensajeExito');
    if (div) {
        div.textContent = '✓ ' + mensaje;
        div.classList.add('mostrado');
    }
}

function limpiarMensajes() {
    const mensajeErrorEl = document.getElementById('mensajeError');
    const mensajeExitoEl = document.getElementById('mensajeExito');
    
    if (mensajeErrorEl) mensajeErrorEl.classList.remove('mostrado');
    if (mensajeExitoEl) mensajeExitoEl.classList.remove('mostrado');
}

function iniciarQuiz() {
    // Redirect to the quiz page
    window.location.href = '/quiz';
}