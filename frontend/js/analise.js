// ==================== CONTADOR DE CARACTERES ====================
const textoInput = document.getElementById('texto-input');
if (textoInput) {
    textoInput.addEventListener('input', (e) => {
        const count = e.target.value.length;
        const charCount = document.getElementById('char-count');
        if (charCount) charCount.innerText = `${count} / 5000 caracteres`;
    });
}

// ==================== ANÁLISE DE TEXTO (INTEGRADO COM BACKEND) ====================
const btnAnalisarTexto = document.getElementById('btn-analisar-texto');
if (btnAnalisarTexto) {
    btnAnalisarTexto.addEventListener('click', async () => {
        const texto = document.getElementById('texto-input').value;
        
        if (!texto.trim()) {
            alert('Por favor, insira um texto para análise');
            return;
        }
        
        mostrarLoading();
        
        try {
            // Chamada real para o backend FastAPI
            const response = await fetch("http://localhost:8000/analises/texto", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text: texto })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Erro na API");
            }
            
            const data = await response.json();
            
            // Mapear resposta do backend para o formato que o frontend espera
            // Backend retorna: { predicted_class: "humano" ou "ia", score: 0.87, confidence_level: "alto/médio/baixo" }
            const resultado = {
                classe: data.predicted_class === "ia" ? "IA" : "Humano",
                score: data.score,
                nivel: data.confidence_level
            };
            
            exibirResultado(resultado);
            
        } catch (error) {
            console.error("Erro na requisição:", error);
            alert("Erro ao conectar com o servidor. Verifique se o backend está rodando em http://localhost:8000");
        } finally {
            esconderLoading();
        }
    });
}

// ==================== RESULTADO ====================
function exibirResultado(resultado) {
    const resultadoArea = document.getElementById('resultado-area');
    const classePrevista = document.getElementById('classe-prevista');
    const scoreFill = document.getElementById('score-fill');
    const scoreValue = document.getElementById('score-value');
    const nivelConfianca = document.getElementById('nivel-confianca');
    
    if (!resultadoArea) return;
    
    const classe = resultado.classe;
    const score = resultado.score * 100;
    
    if (classePrevista) {
        classePrevista.innerHTML = `<span class="${classe === 'IA' ? 'classe-ia' : 'classe-humano'}">${classe === 'IA' ? 'Gerado por Inteligência Artificial' : 'Criado por Humano'}</span>`;
    }
    if (scoreFill) scoreFill.style.width = `${score}%`;
    if (scoreValue) scoreValue.innerText = `${Math.round(score)}%`;
    
    let nivelClass = '';
    let nivelText = '';
    
    if (resultado.nivel === 'alto') {
        nivelClass = 'confianca-alta';
        nivelText = 'Alta confiança';
    } else if (resultado.nivel === 'médio') {
        nivelClass = 'confianca-media';
        nivelText = 'Média confiança';
    } else {
        nivelClass = 'confianca-baixa';
        nivelText = 'Baixa confiança';
    }
    
    if (nivelConfianca) {
        nivelConfianca.className = `nivel-confianca ${nivelClass}`;
        nivelConfianca.innerText = nivelText;
    }
    
    resultadoArea.style.display = 'block';
    resultadoArea.scrollIntoView({ behavior: 'smooth' });
}

function mostrarLoading() {
    const loading = document.getElementById('loading');
    const resultadoArea = document.getElementById('resultado-area');
    if (loading) loading.style.display = 'block';
    if (resultadoArea) resultadoArea.style.display = 'none';
}

function esconderLoading() {
    const loading = document.getElementById('loading');
    if (loading) loading.style.display = 'none';
}

// ==================== NOVA ANÁLISE ====================
const btnNovaAnalise = document.getElementById('btn-nova-analise');
if (btnNovaAnalise) {
    btnNovaAnalise.addEventListener('click', () => {
        const resultadoArea = document.getElementById('resultado-area');
        const chatInputArea = document.getElementById('chat-input-area');
        const chatOptions = document.getElementById('chat-options');
        const textoInputElement = document.getElementById('texto-input');
        
        if (resultadoArea) resultadoArea.style.display = 'none';
        if (chatInputArea) chatInputArea.style.display = 'none';
        if (chatOptions) chatOptions.style.display = 'flex';
        if (textoInputElement) textoInputElement.value = '';
        
        const charCount = document.getElementById('char-count');
        if (charCount) charCount.innerText = '0 / 5000 caracteres';
        
        // Limpa as mensagens do chat e volta para a mensagem inicial
        const chatMessages = document.getElementById('chat-messages');
        if (chatMessages) {
            chatMessages.innerHTML = `
                <div class="message bot">
                    <div class="message-content">
                        Olá! Eu sou o assistente de detecção de IA. Para começar, clique em "Iniciar":
                    </div>
                </div>
            `;
        }
    });
}