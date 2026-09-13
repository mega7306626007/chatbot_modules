const form = document.querySelector('#chat-form');
const input = document.querySelector('#message-input');
const conversation = document.querySelector('#conversation');
const welcome = document.querySelector('.welcome-block');
const suggestions = document.querySelector('.suggestions');
const typingIndicator = document.querySelector('#typing-indicator');
const quickReplies = document.querySelector('#quick-replies');
const searchToggle = document.querySelector('#search-toggle');
const searchInput = document.querySelector('#search-input');
const themeToggle = document.querySelector('#theme-toggle');
const clearChat = document.querySelector('#clear-chat');

const STORAGE_KEY = 'mwesh_conversation';
const THEME_KEY = 'mwesh_theme';

let messages = [];
let searchActive = false;

function formatTime(date) {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function saveConversation() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
  } catch {}
}

function loadConversation() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      messages = JSON.parse(stored);
      messages.forEach(m => renderMessage(m.text, m.role, m.imageUrl, m.time, false));
      if (messages.length) {
        welcome?.remove();
        suggestions?.remove();
      }
    }
  } catch {}
}

function setTheme(dark) {
  document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
  themeToggle.setAttribute('aria-pressed', dark);
  themeToggle.textContent = dark ? '&#9790;' : '&#9728;';
  try { localStorage.setItem(THEME_KEY, dark ? 'dark' : 'light'); } catch {}
}

function initTheme() {
  const stored = localStorage.getItem(THEME_KEY);
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  setTheme(stored ? stored === 'dark' : prefersDark);
}

function renderMarkdown(text) {
  const escapeHtml = (s) => s.replace(/&/g,'&').replace(/</g,'<').replace(/>/g,'>');
  let html = escapeHtml(text);

  html = html.replace(/^### (.*$)/gm, '<h3>$1</h3>');
  html = html.replace(/^## (.*$)/gm, '<h2>$1</h2>');
  html = html.replace(/^# (.*$)/gm, '<h1>$1</h1>');

  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
  html = html.replace(/`(.+?)`/g, '<code>$1</code>');

  html = html.replace(/^```(\w*)\n([\s\S]*?)\n```/gm, (_, lang, code) => `<pre><code class="language-${lang}">${code}</code></pre>`);

  html = html.replace(/^\|(.+)\|\n\|[\s\-:]+\|\n((?:\|.+\|\n?)*)/gm, (_, header, rows) => {
    const th = header.split('|').slice(1, -1).map(h => `<th>${h.trim()}</th>`).join('');
    const tr = rows.trim().split('\n').map(r => {
      const td = r.split('|').slice(1, -1).map(c => `<td>${c.trim()}</td>`).join('');
      return `<tr>${td}</tr>`;
    }).join('');
    return `<table><thead><tr>${th}</tr></thead><tbody>${tr}</tbody></table>`;
  });

  html = html.replace(/^> (.*$)/gm, '<blockquote>$1</blockquote>');
  html = html.replace(/^\- (.*$)/gm, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');
  html = html.replace(/^\d+\. (.*$)/gm, '<li>$1</li>');

  html = html.replace(/^\-\-\-$/gm, '<hr>');

  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');

  html = html.replace(/\n/g, '<br>');

  return html;
}

function renderMessage(text, role, imageUrl = null, time = null, save = true) {
  const message = document.createElement('div');
  message.className = `message ${role}`;

  const bubble = document.createElement('div');
  bubble.className = 'message-bubble';
  bubble.innerHTML = renderMarkdown(text);

  const copyBtn = document.createElement('button');
  copyBtn.className = 'copy-btn';
  copyBtn.textContent = '📋';
  copyBtn.title = 'Copy';
  copyBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    navigator.clipboard.writeText(text).then(() => {
      copyBtn.textContent = '✓';
      setTimeout(() => copyBtn.textContent = '📋', 1200);
    });
  });
  bubble.appendChild(copyBtn);

  const timestamp = document.createElement('div');
  timestamp.className = 'message-time';
  timestamp.textContent = time || formatTime(new Date());
  bubble.appendChild(timestamp);

  if (imageUrl) {
    const image = document.createElement('img');
    image.className = 'chat-image';
    image.src = imageUrl;
    image.alt = 'Generated image';
    bubble.appendChild(image);
    const download = document.createElement('a');
    download.className = 'image-download';
    download.href = imageUrl;
    download.download = 'mwesh-image.png';
    download.textContent = 'Download image';
    bubble.appendChild(download);
  }

  message.appendChild(bubble);
  conversation.appendChild(message);

  if (save) {
    messages.push({ text, role, imageUrl, time: timestamp.textContent });
    saveConversation();
  }

  conversation.scrollTop = conversation.scrollHeight;
}

function showTyping(show) {
  typingIndicator.hidden = !show;
  typingIndicator.setAttribute('aria-hidden', !show);
}

function showQuickReplies(replies) {
  quickReplies.innerHTML = '';
  if (!replies?.length) return;
  replies.forEach(r => {
    const btn = document.createElement('button');
    btn.className = 'quick-reply';
    btn.type = 'button';
    btn.textContent = r;
    btn.addEventListener('click', () => sendMessage(r));
    quickReplies.appendChild(btn);
  });
}

function getQuickRepliesFor(text) {
  const t = text.toLowerCase();
  if (t.includes('joke')) return ['Another one', 'Tell me a riddle', 'Give me a quote'];
  if (t.includes('story')) return ['Another story', 'Different genre', 'Make it longer'];
  if (t.includes('poem') || t.includes('haiku')) return ['Another poem', 'Different style', 'Make it rhyme'];
  if (t.includes('image') || t.includes('generate')) return ['Different scene', 'Online photo instead', 'Change style'];
  if (t.includes('news')) return ['Tech news', 'Science news', 'More headlines'];
  if (t.includes('weather')) return ['Forecast', 'Different city', 'Hourly'];
  if (t.includes('help') || t.includes('capabilit')) return ['Show memory', 'What can you do?', 'System status'];
  return ['Tell me more', 'Explain differently', 'Another example'];
}

async function sendMessage(text) {
  const cleanText = text.trim();
  if (!cleanText) return;
  welcome?.remove();
  suggestions?.remove();
  showQuickReplies([]);
  renderMessage(cleanText, 'user');
  input.value = '';
  input.focus();
  showTyping(true);

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
    showTyping(false);
    renderMessage(payload.reply, 'bot', payload.image_url);
    const replies = getQuickRepliesFor(payload.reply);
    showQuickReplies(replies);
  } catch (error) {
    showTyping(false);
    renderMessage(`I could not reach the Python chatbot. Start it with "python main.py --web" and try again. (${error.message})`, 'bot');
  }
}

function clearConversation() {
  messages = [];
  localStorage.removeItem(STORAGE_KEY);
  conversation.innerHTML = '';
  quickReplies.innerHTML = '';
  conversation.appendChild(welcome);
  conversation.appendChild(suggestions);
  welcome.style.display = '';
  suggestions.style.display = '';
}

function exportConversation() {
  if (!messages.length) return;
  const lines = messages.map(m => `[${m.time}] ${m.role === 'user' ? 'You' : 'Mwesh'}: ${m.text}`);
  const blob = new Blob([lines.join('\n\n')], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `mwesh-chat-${new Date().toISOString().slice(0,10)}.txt`;
  a.click();
  URL.revokeObjectURL(url);
}

function filterMessages(query) {
  const q = query.toLowerCase();
  document.querySelectorAll('.message').forEach(msg => {
    const text = msg.textContent.toLowerCase();
    msg.style.display = text.includes(q) ? '' : 'none';
  });
}

searchToggle.addEventListener('click', () => {
  searchActive = !searchActive;
  searchInput.classList.toggle('hidden', !searchActive);
  searchToggle.setAttribute('aria-expanded', searchActive);
  if (searchActive) searchInput.focus();
});

searchInput.addEventListener('input', (e) => filterMessages(e.target.value));

themeToggle.addEventListener('click', () => {
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  setTheme(!isDark);
});

clearChat.addEventListener('click', clearConversation);

document.querySelector('#new-chat').addEventListener('click', clearConversation);

document.querySelectorAll('[data-command]').forEach((button) => {
  button.addEventListener('click', () => sendMessage(button.dataset.command));
});

document.querySelectorAll('[data-fill]').forEach((button) => {
  button.addEventListener('click', () => {
    input.value = button.dataset.fill;
    input.focus();
    input.setSelectionRange(input.value.length, input.value.length);
  });
});

document.querySelector('.menu-toggle').addEventListener('click', () => document.querySelector('.sidebar').classList.add('open'));
document.querySelector('.mobile-close').addEventListener('click', () => document.querySelector('.sidebar').classList.remove('open'));

document.querySelectorAll('.nav-section-header').forEach((header) => {
  header.addEventListener('click', () => header.parentElement.classList.toggle('open'));
});

const scrollUp = document.querySelector('#scroll-up');
const scrollDown = document.querySelector('#scroll-down');
function goToTop() {
  try { conversation?.scrollTo({ top: 0, behavior: 'smooth' }); } catch { if (conversation) conversation.scrollTop = 0; }
}
function goToBottom() {
  const top = conversation ? conversation.scrollHeight : document.documentElement.scrollHeight;
  try { conversation?.scrollTo({ top, behavior: 'smooth' }); } catch { if (conversation) conversation.scrollTop = top; }
}
scrollUp?.addEventListener('click', goToTop);
scrollDown?.addEventListener('click', goToBottom);
function updateScrollButtons() {
  if (!conversation || !scrollUp || !scrollDown) return;
  const atTop = conversation.scrollTop <= 10 && window.scrollY <= 10;
  const atBottom = conversation.scrollTop + conversation.clientHeight >= conversation.scrollHeight - 10;
  scrollUp.style.opacity = atTop ? '0.55' : '0.92';
  scrollDown.style.opacity = atBottom ? '0.55' : '0.92';
}
conversation?.addEventListener('scroll', updateScrollButtons);
window.addEventListener('scroll', updateScrollButtons);
updateScrollButtons();

form.addEventListener('submit', (event) => {
  event.preventDefault();
  sendMessage(input.value);
});

let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  showInstallBanner();
});

function showInstallBanner() {
  if (document.querySelector('.install-banner')) return;
  const banner = document.createElement('div');
  banner.className = 'install-banner';
  banner.style.cssText = 'position:fixed;bottom:80px;left:50%;transform:translateX(-50%);background:var(--green);color:white;padding:12px 20px;border-radius:8px;box-shadow:var(--shadow);display:flex;align-items:center;gap:12px;z-index:100;font-size:13px;';
  banner.innerHTML = 'Install Mwesh for offline access&nbsp;<button style="background:white;color:var(--green);border:0;padding:6px 12px;border-radius:6px;font-weight:700;">Install</button><button style="background:transparent;border:1px solid white;color:white;padding:6px 10px;border-radius:6px;">Later</button>';
  const [installBtn, laterBtn] = banner.querySelectorAll('button');
  installBtn.onclick = async () => {
    banner.remove();
    if (deferredPrompt) {
      deferredPrompt.prompt();
      await deferredPrompt.userChoice;
      deferredPrompt = null;
    }
  };
  laterBtn.onclick = () => banner.remove();
  document.body.appendChild(banner);
  setTimeout(() => banner.remove(), 30000);
}

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => navigator.serviceWorker.register('/sw.js').catch(()=>{}));
}

initTheme();
loadConversation();