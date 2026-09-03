const form = document.querySelector('#chat-form');
const input = document.querySelector('#message-input');
const conversation = document.querySelector('#conversation');
const welcome = document.querySelector('.welcome-block');
const suggestions = document.querySelector('.suggestions');

function addMessage(text, role) {
  const message = document.createElement('div');
  message.className = `message ${role}`;
  const bubble = document.createElement('div');
  bubble.className = 'message-bubble';
  bubble.textContent = text;
  message.appendChild(bubble);
  conversation.appendChild(message);
  conversation.scrollTop = conversation.scrollHeight;
}

async function sendMessage(text) {
  const cleanText = text.trim();
  if (!cleanText) return;
  welcome?.remove();
  suggestions?.remove();
  addMessage(cleanText, 'user');
  try {
    const apiUrl = window.location.protocol === 'file:'
      ? 'http://127.0.0.1:8765/api/chat'
      : '/api/chat';
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: cleanText })
    });
    const responseText = await response.text();
    let payload;
    try {
      payload = JSON.parse(responseText);
    } catch {
      throw new Error(responseText || `The server returned an empty response (HTTP ${response.status}).`);
    }
    if (!response.ok) throw new Error(payload.error || 'Request failed');
    addMessage(payload.reply, 'bot');
  } catch (error) {
    addMessage(`I could not reach the Python chatbot. Start it with "python main.py --web" and try again. (${error.message})`, 'bot');
  }
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  sendMessage(input.value);
  input.value = '';
  input.focus();
});

document.querySelectorAll('[data-command]').forEach((button) => {
  button.addEventListener('click', () => sendMessage(button.dataset.command));
});

document.querySelector('#new-chat').addEventListener('click', () => window.location.reload());
document.querySelector('#clear-chat').addEventListener('click', () => window.location.reload());
document.querySelector('.menu-toggle').addEventListener('click', () => document.querySelector('.sidebar').classList.add('open'));
document.querySelector('.mobile-close').addEventListener('click', () => document.querySelector('.sidebar').classList.remove('open'));