// Funciones comunes utilizadas por ambas páginas

// Función auxiliar para obtener elementos por ID
function documento(id) {
    return document.getElementById(id);
}

// Función para mostrar errores (usada en ambas páginas)
function mostrarError(mensaje) {
    const div = document.getElementById('mensajeError');
    if (div) {
        div.textContent = '⚠️ ' + mensaje;
        div.classList.add('mostrado');
    }
}

// Función para mostrar mensajes de éxito (usada en ambas páginas)
function mostrarExito(mensaje) {
    const div = document.getElementById('mensajeExito');
    if (div) {
        div.textContent = '✓ ' + mensaje;
        div.classList.add('mostrado');
    }
}

// Función para limpiar mensajes (usada en ambas páginas)
function limpiarMensajes() {
    const mensajeErrorEl = document.getElementById('mensajeError');
    const mensajeExitoEl = document.getElementById('mensajeExito');
    
    if (mensajeErrorEl) mensajeErrorEl.classList.remove('mostrado');
    if (mensajeExitoEl) mensajeExitoEl.classList.remove('mostrado');
}