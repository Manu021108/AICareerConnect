/**
 * AICareerConnect — Dashboard JavaScript
 * Handles: stats fetching, Chart.js rendering, AI chat, and speech I/O.
 */

// ---- Dashboard Stats & Chart ----
async function loadDashboard() {
    try {
        const res = await fetch('/dashboard/api/stats');
        const data = await res.json();

        document.getElementById('stat-chats').textContent = data.total_chats;
        document.getElementById('stat-assessments').textContent = data.total_assessments;

        if (data.skills.length > 0) {
            const ctx = document.getElementById('skillChart').getContext('2d');
            new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: data.skills.map(s => s.skill),
                    datasets: [{
                        label: 'Skill Score',
                        data: data.skills.map(s => s.score),
                        backgroundColor: 'rgba(108, 99, 255, 0.2)',
                        borderColor: '#6c63ff',
                        pointBackgroundColor: '#00d4aa',
                    }]
                },
                options: {
                    scales: { r: { beginAtZero: true, max: 100 } },
                    plugins: { legend: { labels: { color: '#e4e4e7' } } },
                }
            });
        }
    } catch (err) {
        console.error('Dashboard load error:', err);
    }
}

// ---- AI Chat ----
async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    if (!message) return;

    appendMessage('user', message);
    input.value = '';

    try {
        const res = await fetch('/api/chat/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message }),
        });
        const data = await res.json();
        appendMessage('assistant', data.reply);

        // Auto-speak the reply
        speakText(data.reply);
    } catch (err) {
        appendMessage('assistant', 'Sorry, something went wrong.');
    }
}

function appendMessage(role, content) {
    const container = document.getElementById('chatMessages');
    const div = document.createElement('div');
    div.className = `chat-bubble chat-${role}`;
    div.textContent = content;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

// Allow Enter key to send
document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.addEventListener('keypress', e => {
            if (e.key === 'Enter') sendMessage();
        });
    }
    loadDashboard();
});

// ---- Speech-to-Text (via MediaRecorder) ----
let mediaRecorder = null;
let audioChunks = [];

async function toggleRecording() {
    const btn = document.getElementById('micBtn');

    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        btn.textContent = '🎤';
        return;
    }

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
    mediaRecorder.onstop = async () => {
        const blob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audio', blob, 'recording.wav');

        try {
            const res = await fetch('/api/speech/transcribe', { method: 'POST', body: formData });
            const data = await res.json();
            document.getElementById('chatInput').value = data.transcription;
        } catch (err) {
            console.error('Transcription error:', err);
        }
    };

    mediaRecorder.start();
    btn.textContent = '⏹️';
}

// ---- Text-to-Speech (via browser SpeechSynthesis) ----
function speakText(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1;
        speechSynthesis.speak(utterance);
    }
}

// ---- Skill Assessment ----
async function runAssessment() {
    try {
        const res = await fetch('/api/career/assess', { method: 'POST' });
        const data = await res.json();
        alert(`Assessment complete! ${data.assessments.length} skills evaluated.`);
        loadDashboard();
    } catch (err) {
        alert('Assessment failed. Please set up your career profile first.');
    }
}
