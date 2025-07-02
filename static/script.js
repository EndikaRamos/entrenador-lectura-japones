const startBtn = document.getElementById("startBtn");
const otraBtn = document.getElementById("otraBtn");
const resultado = document.getElementById("resultado");
const historial = document.getElementById("historial");
const modeloSelect = document.getElementById("modeloSelect");
const datasetSelect = document.getElementById("datasetSelect");
const kanjiEl = document.getElementById("kanji");
const hiraganaEl = document.getElementById("hiragana");

let mediaRecorder;
let chunks = [];

function playBeep() {
  const ctx = new AudioContext();
  const oscillator = ctx.createOscillator();
  const gainNode = ctx.createGain();

  oscillator.type = "sine";
  oscillator.frequency.setValueAtTime(880, ctx.currentTime);
  oscillator.connect(gainNode);
  gainNode.connect(ctx.destination);

  oscillator.start();
  gainNode.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.3);
  oscillator.stop(ctx.currentTime + 0.3);
}

startBtn.onclick = async () => {
  startBtn.disabled = true;
  resultado.textContent = "🕓 Espera unos segundos... prepárate para hablar";

  setTimeout(async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = e => chunks.push(e.data);

    mediaRecorder.onstop = async () => {
      const blob = new Blob(chunks, { type: "audio/webm" });
      const formData = new FormData();

      const kanji = kanjiEl.textContent.trim();
      formData.append("audio", blob, "grabacion.webm");
      formData.append("modelo", modeloSelect.value);
      formData.append("kanji", kanji);
      formData.append("dataset", datasetSelect.value);

      resultado.innerHTML = `<span class="loader"></span> <strong>Procesando...</strong>`;

      const res = await fetch("/transcribe", {
        method: "POST",
        body: formData
      });

      const data = await res.json();
      const textoHiragana = data.hiragana;
      const esperado = data.esperado;
      const errores = data.errores;

      let salida = `<strong>Dijiste:</strong> ${textoHiragana}<br>`;
      salida += `<strong>Esperado:</strong> ${esperado}<br>`;

      if (errores.length === 0) {
        salida += `<span class="has-text-success">✔️ Correcto</span>`;
      } else {
        salida += `<span class="has-text-danger">❌ Errores:</span><ul>`;
        errores.forEach(e => {
          salida += `<li><code>${e.dicho}</code> → <code>${e.esperado}</code> (posición ${e.pos + 1})</li>`;
        });
        salida += `</ul>`;
      }

      resultado.innerHTML = salida;

      const p = document.createElement("p");
      p.innerHTML = `<strong>${textoHiragana}</strong>`;
      historial.prepend(p);

      startBtn.disabled = false;
      chunks = [];
    };

    mediaRecorder.start();
    playBeep();
    resultado.textContent = "🎙️ Grabando ahora... puedes hablar";

    setTimeout(() => {
      mediaRecorder.stop();
    }, 4000);
  }, 1500);
};

// Función para cargar una nueva frase desde el dataset actual
async function cargarNuevaFrase() {
  const res = await fetch(`/frase?dataset=${datasetSelect.value}`);
  const data = await res.json();

  kanjiEl.textContent = data.kanji || "（エラー）";
  hiraganaEl.textContent = data.hiragana || "（データなし）";
  resultado.textContent = "Frase cambiada, lista para grabar.";
}

otraBtn.onclick = cargarNuevaFrase;
datasetSelect.onchange = cargarNuevaFrase;
