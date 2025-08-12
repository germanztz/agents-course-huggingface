const intervalId = setInterval(() => {
  const comboCanales = document.getElementById('comboCanales');
  const span = document.querySelector("#info-franja-disponible > span:nth-child(1)");

  if (span && span.textContent.includes('En estos momentos no podemos ofrecerle citas en la oficina seleccionada.')) {
    comboCanales.value = '1'
    console.log(`Interval ID: ${intervalId} | Script ha cambiado el valor a: ${comboCanales.value}`);
    comboCanales.dispatchEvent(new Event('change'));
  } else {
    console.log(`Texto de error no detectado. omitiendo interval ID: ${intervalId}`);
    return;
  }

}, Math.floor(Math.random() * (5000 - 3000 + 1)) + 3000);