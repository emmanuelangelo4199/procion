// Simple textarea auto-resize
const textarea = document.querySelector('textarea');
if(textarea){
    textarea.addEventListener('input', function() {
    
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
}

// for mobile sidebar for hover interact
const sidebar = document.getElementById("sidebar");
const mobileMenuBtn = document.getElementById("mobileMenuBtn");
const mobileOverlay = document.getElementById("mobileOverlay");

function toggleMenu() {
    sidebar.classList.toggle("-translate-x-full");
    mobileOverlay.classList.toggle("hidden");
}

mobileMenuBtn.addEventListener("click", toggleMenu);
mobileOverlay.addEventListener("click", toggleMenu);

// Sidebar hover interactions for desktop
const navItems = document.querySelectorAll("nav > a");
navItems.forEach((item) => {
    item.addEventListener("mouseenter", () => {
    if (!item.classList.contains("text-primary")) {
        item.style.transform = "translateX(4px)";
    }
    });
    item.addEventListener("mouseleave", () => {
    item.style.transform = "translateX(0px)";
    });
});

// Chat feed scroll to bottom on load
window.onload = () => {
    const feed = document.querySelector(".overflow-y-auto");
    feed.scrollTop = feed.scrollHeight;
};


// WebSocket chat
(function () {
    const circleData = document.getElementById('circle-data');
    if (!circleData) return;

    const circleId = circleData.dataset.circleId;
    const currentUserName = circleData.dataset.userName;

    const chatFeed = document.getElementById('chat-feed');
    const messageInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');

    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const socket = new WebSocket(`${protocol}://${window.location.host}/ws/circle/${circleId}/`);

    socket.onopen = function () {
        console.log('Circle chat connected.');
    };

    socket.onclose = function (e) {
        console.warn('Circle chat disconnected.', e.code);
    };

    socket.onerror = function (e) {
        console.error('WebSocket error:', e);
    };

    socket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log('Message received:', data); 
        appendMessage(data.sender_name, data.message, data.created_at);
    };

    sendBtn.addEventListener('click', sendMessage);

    messageInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    function sendMessage() {
        const text = messageInput.value.trim();
        if (!text || socket.readyState !== WebSocket.OPEN) return;
        socket.send(JSON.stringify({ message: text }));
        messageInput.value = '';
    }

    function appendMessage(senderName, text, time) {
        console.log('appendMessage called:', senderName, text, time);
        const isSelf = senderName === currentUserName;

        const wrapper = document.createElement('div');
        wrapper.className = `flex flex-col ${isSelf ? 'items-end' : 'items-start'} gap-2 mb-8`;

        const meta = document.createElement('div');
        meta.className = `flex items-center gap-2 ${isSelf ? 'mr-2' : 'ml-2'}`;
        meta.innerHTML = `<span class="font-label-sm text-outline uppercase tracking-wider">
            ${isSelf ? 'You' : senderName} • ${time}
        </span>`;

        const bubble = document.createElement('div');
        bubble.className = isSelf
            ? 'max-w-[80%] bg-primary-container text-on-primary-container rounded-2xl rounded-tr-none p-4'
            : 'max-w-[80%] bg-surface-container-low rounded-2xl rounded-tl-none p-4';
        bubble.innerHTML = `<p class="font-body-md">${escapeHtml(text)}</p>`;

        wrapper.appendChild(meta);
        wrapper.appendChild(bubble);
        chatFeed.appendChild(wrapper);

        chatFeed.scrollTop = chatFeed.scrollHeight;
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.appendChild(document.createTextNode(text));
        return div.innerHTML;
    }
})
();
