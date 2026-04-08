const chatBox = document.getElementById("chatBox");

// Adiciona mensagem no chat
function addMessage(text, type) {
  const msg = document.createElement("div");
  msg.classList.add("message", type);

  msg.innerHTML = text.replace(/\n/g, "<br>");

  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// ==========================
// TEXTO
// ==========================
async function sendText() {
  const input = document.getElementById("textInput");
  const text = input.value.trim();

  if (!text) return;

  addMessage(text, "user");
  input.value = "";

  const loading = document.createElement("div");
  loading.classList.add("message", "bot");
  loading.innerText = "⏳ Analisando texto...";
  chatBox.appendChild(loading);

  try {
    const res = await fetch("http://localhost:8000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text })
    });

    if (!res.ok) {
      throw new Error("Erro na API");
    }

    const data = await res.json();

    if (data.label !== 0 && data.label !== 1) {
      throw new Error("Resposta inválida");
    }

    loading.remove();

    const isAI = data.label === 1;
    const confidence = Math.max(data.prob_ai, data.prob_human);

    const resultado = `
<strong>${isAI ? "🤖 IA detectada" : "👤 Texto humano"}</strong>

Confiança: ${(confidence * 100).toFixed(2)}%

Probabilidade IA: ${(data.prob_ai * 100).toFixed(2)}%
Probabilidade Humano: ${(data.prob_human * 100).toFixed(2)}%
`;

    addMessage(resultado, "bot");

  } catch (err) {
    loading.innerText = "❌ Erro ao conectar com o servidor.";
    console.error(err);
  }
}

// ==========================
// IMAGEM
// ==========================
document.getElementById("imageInput").addEventListener("change", async function() {
  const file = this.files[0];
  if (!file) return;

  // Preview da imagem no chat
  const reader = new FileReader();
  reader.onload = function(e) {
    addMessage(`<img src="${e.target.result}" style="max-width:200px; border-radius:10px;">`, "user");
  };
  reader.readAsDataURL(file);

  const loading = document.createElement("div");
  loading.classList.add("message", "bot");
  loading.innerText = "⏳ Analisando imagem...";
  chatBox.appendChild(loading);

  try {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:8000/predict-image", {
      method: "POST",
      body: formData
    });

    if (!res.ok) {
      throw new Error("Erro na API");
    }

    const data = await res.json();

    if (data.label !== 0 && data.label !== 1) {
      throw new Error("Resposta inválida");
    }

    loading.remove();

    const isAI = data.label === 1;
    const confidence = Math.max(data.prob_ai, data.prob_human);

    const resultado = `
<strong>${isAI ? "🤖 Imagem gerada por IA" : "📸 Imagem real"}</strong>

Confiança: ${(confidence * 100).toFixed(2)}%

Probabilidade IA: ${(data.prob_ai * 100).toFixed(2)}%
Probabilidade Real: ${(data.prob_human * 100).toFixed(2)}%
`;

    addMessage(resultado, "bot");

  } catch (err) {
    loading.innerText = "❌ Erro ao analisar imagem.";
    console.error(err);
  }
});

// ==========================
// ENTER PARA ENVIAR TEXTO
// ==========================
document.getElementById("textInput").addEventListener("keydown", function(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendText();
  }
});