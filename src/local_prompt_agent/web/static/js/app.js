// Local Prompt Agent - Web UI JavaScript
// UTF-8 encoding for Chinese characters

// State
let currentTheme = localStorage.getItem('theme') || 'light';
let language = localStorage.getItem('language') || 'en';
let ragEnabled = false;
let ws = null;

// Elements
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const messages = document.getElementById('messages');
const emptyState = document.getElementById('emptyState');
const themeToggle = document.getElementById('themeToggle');
const languageSelector = document.getElementById('languageSelector');
const menuButton = document.getElementById('menuButton');
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('overlay');
const newChatButton = document.getElementById('newChatButton');
const charCount = document.getElementById('charCount');
const pdfUpload = document.getElementById('pdfUpload');
const ragToggle = document.getElementById('ragToggle');
const docsList = document.getElementById('docsList');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Load theme
    document.documentElement.setAttribute('data-theme', currentTheme);
    themeToggle.textContent = currentTheme === 'dark' ? '🌞' : '🌓';
    
    // Load language
    languageSelector.value = language;
    
    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keydown', handleKeyPress);
    messageInput.addEventListener('input', handleInput);
    themeToggle.addEventListener('click', toggleTheme);
    languageSelector.addEventListener('change', changeLanguage);
    menuButton.addEventListener('click', toggleSidebar);
    overlay.addEventListener('click', toggleSidebar);
    newChatButton.addEventListener('click', newChat);
    pdfUpload.addEventListener('change', handlePDFUpload);
    ragToggle.addEventListener('change', toggleRAG);
    
    // Load indexed documents
    loadIndexedDocuments();
});

// Handle input
function handleInput() {
    // Auto-resize textarea
    messageInput.style.height = 'auto';
    const newHeight = Math.min(messageInput.scrollHeight, 200);
    messageInput.style.height = newHeight + 'px';
    
    // Update character count
    const count = messageInput.value.length;
    charCount.textContent = `${count} / 4000`;
    
    // Enable/disable send button
    sendButton.disabled = messageInput.value.trim().length === 0;
}

// Handle Enter key
function handleKeyPress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

// Send message
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;
    
    // Hide empty state
    if (emptyState) {
        emptyState.style.display = 'none';
    }
    
    // Add user message
    addMessage('user', message);
    
    // Clear input
    messageInput.value = '';
    messageInput.style.height = 'auto';
    charCount.textContent = '0 / 4000';
    sendButton.disabled = true;
    
    // Send to backend (WebSocket streaming)
    await streamResponse(message);
}

// Send suggested prompt
function sendSuggested(message) {
    messageInput.value = message;
    sendMessage();
}

// Stream response via WebSocket
async function streamResponse(message) {
    const assistantMsgDiv = addMessage('assistant', '', true);
    const textElement = assistantMsgDiv.querySelector('.message-text');
    
    try {
        // Connect WebSocket
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/chat`;
        ws = new WebSocket(wsUrl);
        
        ws.onopen = () => {
            // Send message with RAG mode
            ws.send(JSON.stringify({
                message: message,
                agent: 'default',
                use_rag: ragEnabled
            }));
        };
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            if (data.type === 'token') {
                // Append token
                textElement.textContent += data.token;
                scrollToBottom();
            } else if (data.type === 'done') {
                // Remove streaming cursor
                assistantMsgDiv.classList.remove('streaming');
                const cursor = textElement.querySelector('.cursor');
                if (cursor) cursor.remove();
                ws.close();
            } else if (data.type === 'error') {
                // Show error
                textElement.textContent = `Error: ${data.error}`;
                assistantMsgDiv.classList.remove('streaming');
                ws.close();
            }
        };
        
        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            textElement.textContent = 'Error: Connection failed. Using fallback...';
            assistantMsgDiv.classList.remove('streaming');
            // Fallback to HTTP
            fallbackToHTTP(message, textElement, assistantMsgDiv);
        };
        
    } catch (error) {
        console.error('Streaming error:', error);
        // Fallback to HTTP
        fallbackToHTTP(message, textElement, assistantMsgDiv);
    }
}

// Fallback to HTTP POST if WebSocket fails
async function fallbackToHTTP(message, textElement, messageDiv) {
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json; charset=utf-8',
                'Accept': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                stream: false
            })
        });
        
        const data = await response.json();
        textElement.textContent = data.response;
        messageDiv.classList.remove('streaming');
        
    } catch (error) {
        textElement.textContent = `Error: ${error.message}`;
        messageDiv.classList.remove('streaming');
    }
}

// Add message to UI
function addMessage(role, text, streaming = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${role}`;
    if (streaming) messageDiv.classList.add('streaming');
    
    const avatar = role === 'user' ? '👤' : '🤖';
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <div class="message-text">${text}${streaming ? '<span class="cursor">▊</span>' : ''}</div>
            <div class="message-meta">${time}</div>
        </div>
    `;
    
    messages.appendChild(messageDiv);
    scrollToBottom();
    
    return messageDiv;
}

// Scroll to bottom
function scrollToBottom() {
    messages.scrollTop = messages.scrollHeight;
}

// Toggle theme
function toggleTheme() {
    currentTheme = currentTheme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);
    localStorage.setItem('theme', currentTheme);
    themeToggle.textContent = currentTheme === 'dark' ? '🌞' : '🌓';
}

// Change language
function changeLanguage() {
    language = languageSelector.value;
    localStorage.setItem('language', language);
    // Update UI text based on language (to be implemented)
}

// Toggle sidebar (mobile)
function toggleSidebar() {
    sidebar.classList.toggle('open');
    overlay.classList.toggle('active');
}

// New chat
function newChat() {
    // Clear messages
    while (messages.firstChild) {
        messages.removeChild(messages.firstChild);
    }
    
    // Show empty state
    const emptyStateHTML = `
        <div class="empty-state" id="emptyState">
            <div class="empty-icon">🤖</div>
            <h2>Hello! How can I help you today?</h2>
            <p>你好！我能為你做什麼？</p>
            
            <div class="suggested-prompts">
                <button class="prompt-card" onclick="sendSuggested('Explain how RAG works')">
                    <span class="prompt-icon">💡</span>
                    <span class="prompt-text">Explain how RAG works</span>
                </button>
                <button class="prompt-card" onclick="sendSuggested('Write Python code for fibonacci')">
                    <span class="prompt-icon">💻</span>
                    <span class="prompt-text">Write Python code</span>
                </button>
                <button class="prompt-card" onclick="sendSuggested('用繁體中文解釋什麼是AI')">
                    <span class="prompt-icon">🌐</span>
                    <span class="prompt-text">用繁體中文解釋AI</span>
                </button>
                <button class="prompt-card" onclick="sendSuggested('Help me understand machine learning')">
                    <span class="prompt-icon">📚</span>
                    <span class="prompt-text">Explain ML concepts</span>
                </button>
            </div>
        </div>
    `;
    messages.innerHTML = emptyStateHTML;
    
    // Clear backend history
    fetch('/api/clear', { method: 'POST' });
}

// Handle PDF upload
async function handlePDFUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    // Show progress
    const progressDiv = document.createElement('div');
    progressDiv.className = 'upload-progress';
    progressDiv.textContent = `📄 Uploading ${file.name}...`;
    docsList.prepend(progressDiv);
    
    try {
        // Upload file
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/api/rag/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            progressDiv.textContent = `✓ Indexed: ${result.file_name} (${result.page_count} pages, ${result.num_chunks} chunks)`;
            progressDiv.style.background = '#00c853';
            
            // Reload documents list
            setTimeout(() => {
                progressDiv.remove();
                loadIndexedDocuments();
            }, 2000);
            
            // Enable RAG mode
            ragToggle.checked = true;
            ragEnabled = true;
        } else {
            progressDiv.textContent = `✗ Error: ${result.message}`;
            progressDiv.style.background = '#ff3d00';
            setTimeout(() => progressDiv.remove(), 3000);
        }
        
    } catch (error) {
        progressDiv.textContent = `✗ Upload failed: ${error.message}`;
        progressDiv.style.background = '#ff3d00';
        setTimeout(() => progressDiv.remove(), 3000);
    }
    
    // Reset file input
    event.target.value = '';
}

// Toggle RAG mode
function toggleRAG() {
    ragEnabled = ragToggle.checked;
    
    // Visual feedback
    if (ragEnabled) {
        console.log('RAG mode enabled');
        // Could add visual indicator to input area
    } else {
        console.log('RAG mode disabled');
    }
}

// Load indexed documents
async function loadIndexedDocuments() {
    try {
        const response = await fetch('/api/rag/documents');
        const result = await response.json();
        
        if (result.success && result.documents.length > 0) {
            // Clear list
            docsList.innerHTML = '';
            
            // Add each document
            result.documents.forEach(doc => {
                const docDiv = document.createElement('div');
                docDiv.className = 'doc-item';
                docDiv.innerHTML = `
                    <span class="doc-icon">📄</span>
                    <span class="doc-name" title="${doc.file_name}">${doc.file_name}</span>
                    <span class="doc-stats">${doc.pages}p</span>
                `;
                docsList.appendChild(docDiv);
            });
        } else {
            docsList.innerHTML = '<div style="font-size: 12px; color: var(--text-secondary); padding: 8px;">No documents yet</div>';
        }
        
    } catch (error) {
        console.error('Error loading documents:', error);
    }
}

// Focus input on load
messageInput.focus();
