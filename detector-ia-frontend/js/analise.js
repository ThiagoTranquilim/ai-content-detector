// ==================== CONTADOR DE CARACTERES ====================
const textoInput = document.getElementById('texto-input');
if (textoInput) {
    textoInput.addEventListener('input', (e) => {
        const count = e.target.value.length;
        const charCount = document.getElementById('char-count');
        if (charCount) charCount.innerText = `${count} / 5000 caracteres`;
    });
}

// ==================== ANÁLISE DE TEXTO ====================
const btnAnalisarTexto = document.getElementById('btn-analisar-texto');
if (btnAnalisarTexto) {
    btnAnalisarTexto.addEventListener('click', async () => {
        const texto = document.getElementById('texto-input').value;
        
        if (!texto.trim()) {
            alert('Por favor, insira um texto para análise');
            return;
        }
        
        mostrarLoading();
        
        setTimeout(() => {
            const resultado = {
                classe: 'IA',
                score: 0.87,
                nivel: 'alta'
            };
            exibirResultado(resultado);
            esconderLoading();
        }, 2000);
    });
}

// ==================== ELEMENTOS DO UPLOAD ====================
const uploadArea = document.getElementById('upload-area');
const arquivoInput = document.getElementById('arquivo-input');
const previewContainer = document.getElementById('preview-container');
const previewImagem = document.getElementById('preview-imagem');
const previewArquivo = document.getElementById('preview-arquivo');
const nomeArquivo = document.getElementById('nome-arquivo');
const btnAnalisarArquivo = document.getElementById('btn-analisar-arquivo');
const btnRemover = document.getElementById('remover-arquivo');

// Variável de controle para evitar duplicidade
let uploadTriggered = false;

// ==================== FUNÇÃO PARA ABRIR EXPLORADOR DE ARQUIVOS (APENAS UMA VEZ) ====================
function abrirExploradorArquivos(event) {
    if (event) {
        event.stopPropagation();
        event.preventDefault();
    }
    
    // Evita múltiplas aberturas
    if (uploadTriggered) return;
    uploadTriggered = true;
    
    if (arquivoInput) {
        arquivoInput.click();
    }
    
    // Reset após 500ms
    setTimeout(() => {
        uploadTriggered = false;
    }, 500);
}

// ==================== CLICK NA ÁREA DE UPLOAD ====================
if (uploadArea) {
    const uploadBox = uploadArea.querySelector('.upload-box');
    
    if (uploadBox) {
        // Remove qualquer listener anterior e adiciona um novo
        uploadBox.removeEventListener('click', abrirExploradorArquivos);
        uploadBox.addEventListener('click', abrirExploradorArquivos);
    }
}

// ==================== BOTÃO DE UPLOAD (LABEL) - Impede propagação ====================
const btnUpload = document.querySelector('.btn-upload');
if (btnUpload) {
    btnUpload.addEventListener('click', (e) => {
        e.stopPropagation(); // Impede que o clique chegue no upload-box
        // Não chama o click aqui, deixa o label fazer seu trabalho naturalmente
    });
}

// ==================== INPUT FILE - Impede propagação ====================
if (arquivoInput) {
    arquivoInput.addEventListener('click', (e) => {
        e.stopPropagation();
    });
    
    arquivoInput.addEventListener('change', (e) => {
        e.stopPropagation();
        if (e.target.files && e.target.files[0]) {
            processarArquivo(e.target.files[0]);
        }
    });
}

// ==================== PROCESSAR ARQUIVO SELECIONADO ====================
function processarArquivo(file) {
    const fileType = file.type;
    
    const uploadBox = uploadArea ? uploadArea.querySelector('.upload-box') : null;
    if (uploadBox) uploadBox.style.display = 'none';
    if (previewContainer) previewContainer.style.display = 'block';
    if (btnAnalisarArquivo) btnAnalisarArquivo.style.display = 'block';
    
    if (fileType.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
            if (previewImagem) {
                previewImagem.src = e.target.result;
                previewImagem.style.display = 'block';
            }
            if (previewArquivo) previewArquivo.style.display = 'none';
        };
        reader.readAsDataURL(file);
    } else {
        if (previewImagem) previewImagem.style.display = 'none';
        if (previewArquivo) {
            if (nomeArquivo) nomeArquivo.innerText = file.name;
            previewArquivo.style.display = 'block';
        }
    }
}

// ==================== REMOVER ARQUIVO ====================
if (btnRemover) {
    btnRemover.addEventListener('click', (e) => {
        e.stopPropagation();
        e.preventDefault();
        
        const uploadBox = uploadArea ? uploadArea.querySelector('.upload-box') : null;
        if (uploadBox) uploadBox.style.display = 'block';
        if (previewContainer) previewContainer.style.display = 'none';
        if (btnAnalisarArquivo) btnAnalisarArquivo.style.display = 'none';
        if (arquivoInput) arquivoInput.value = '';
        if (previewImagem) {
            previewImagem.src = '';
            previewImagem.style.display = 'none';
        }
        if (nomeArquivo) nomeArquivo.innerText = '';
    });
}

// ==================== ANALISAR ARQUIVO ====================
if (btnAnalisarArquivo) {
    btnAnalisarArquivo.addEventListener('click', (e) => {
        e.stopPropagation();
        mostrarLoading();
        setTimeout(() => {
            const resultado = {
                classe: 'Humano',
                score: 0.72,
                nivel: 'media'
            };
            exibirResultado(resultado);
            esconderLoading();
        }, 2000);
    });
}

// ==================== FUNÇÕES DE RESULTADO ====================
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
    if (resultado.nivel === 'alta') {
        nivelClass = 'confianca-alta';
        nivelText = 'Alta confiança';
    } else if (resultado.nivel === 'media') {
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

// ==================== BOTÃO NOVA ANÁLISE ====================
const btnNovaAnalise = document.getElementById('btn-nova-analise');
if (btnNovaAnalise) {
    btnNovaAnalise.addEventListener('click', () => {
        const resultadoArea = document.getElementById('resultado-area');
        const chatInputArea = document.getElementById('chat-input-area');
        const uploadAreaElement = document.getElementById('upload-area');
        const chatOptions = document.getElementById('chat-options');
        const textoInputElement = document.getElementById('texto-input');
        const arquivoInputElement = document.getElementById('arquivo-input');
        
        if (resultadoArea) resultadoArea.style.display = 'none';
        if (chatInputArea) chatInputArea.style.display = 'none';
        if (uploadAreaElement) uploadAreaElement.style.display = 'none';
        if (chatOptions) chatOptions.style.display = 'flex';
        if (textoInputElement) textoInputElement.value = '';
        if (arquivoInputElement) arquivoInputElement.value = '';
        
        if (previewContainer) previewContainer.style.display = 'none';
        
        const uploadBox = uploadAreaElement ? uploadAreaElement.querySelector('.upload-box') : null;
        if (uploadBox) uploadBox.style.display = 'block';
        
        if (btnAnalisarArquivo) btnAnalisarArquivo.style.display = 'none';
        if (previewImagem) previewImagem.style.display = 'none';
        
        const charCount = document.getElementById('char-count');
        if (charCount) charCount.innerText = '0 / 5000 caracteres';
    });
}

// ==================== BOTÕES DAS OPÇÕES (TEXTO, IMAGEM, ARQUIVO) ====================
const chatOptionsDiv = document.getElementById('chat-options');
const chatInputAreaDiv = document.getElementById('chat-input-area');
const uploadAreaDiv = document.getElementById('upload-area');
const chatMessagesDiv = document.getElementById('chat-messages');

optionBtns.forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.stopPropagation();
        
        const opcao = this.getAttribute('data-tipo');
        const textoBotao = this.textContent.trim();
        
        if (chatOptionsDiv) chatOptionsDiv.style.display = 'none';
        
        const userMessage = document.createElement('div');
        userMessage.className = 'message user';
        userMessage.innerHTML = `<div class="message-content">${textoBotao}</div>`;
        if (chatMessagesDiv) chatMessagesDiv.appendChild(userMessage);
        
        setTimeout(() => {
            const botMessage = document.createElement('div');
            botMessage.className = 'message bot';
            
            if (opcao === 'texto') {
                botMessage.innerHTML = `<div class="message-content">Por favor, cole ou digite o texto que deseja analisar:</div>`;
                if (chatMessagesDiv) chatMessagesDiv.appendChild(botMessage);
                if (chatInputAreaDiv) chatInputAreaDiv.style.display = 'block';
                if (uploadAreaDiv) uploadAreaDiv.style.display = 'none';
            } else {
                botMessage.innerHTML = `<div class="message-content">Por favor, faça upload do ${opcao === 'imagem' ? 'imagem' : 'arquivo'} que deseja analisar:</div>`;
                if (chatMessagesDiv) chatMessagesDiv.appendChild(botMessage);
                if (uploadAreaDiv) uploadAreaDiv.style.display = 'block';
                if (chatInputAreaDiv) chatInputAreaDiv.style.display = 'none';
            }
            
            if (chatMessagesDiv) chatMessagesDiv.scrollTop = chatMessagesDiv.scrollHeight;
        }, 500);
        
        if (chatMessagesDiv) chatMessagesDiv.scrollTop = chatMessagesDiv.scrollHeight;
    });
});