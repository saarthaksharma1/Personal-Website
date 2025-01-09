// Handles for Navbar View Toggle
const menu = document.querySelector('#mobile-menu');
const menuLinks = document.querySelector('.navbar__menu');

// Ensure elements exist before adding event listeners
if (menu && menuLinks) {
    menu.addEventListener('click', function() {
        menu.classList.toggle('is-active');
        menuLinks.classList.toggle('active');
    });
}

// Toggle Feedback Form Visibility 
document.addEventListener("DOMContentLoaded", () => {
    const feedbackToggle = document.getElementById("feedback-toggle");
    const feedbackFormContainer = document.getElementById("feedback-form-container");

    // Sets initialfeedback form to 'none'
    if (feedbackFormContainer) {
        feedbackFormContainer.style.display = "none";
    }

    // Toggles feedback form between 'block' and 'none'
    if (feedbackToggle && feedbackFormContainer) {
        feedbackToggle.addEventListener("click", () => {
            feedbackFormContainer.style.display =
                feedbackFormContainer.style.display === "block" ? "none" : "block";
        });
    }
});

// Function to handle chat functionality/requirments (chat.js essentially implemented here)
function initializeChat() {
    console.log("Initializing chat...");

    // This protocol checks whether http or https should be used. Use https when deployed
    const protocol = window.location.protocol === 'https:' ? 'https://' : 'http://';
    const socket = io.connect(protocol + document.domain + ':' + location.port + '/chat');

    // Successfully esablishes log connection
    socket.on('connect', function () {
        console.log("Connected to Socket.IO server");
        socket.emit('joined', {});
    });

    // Handles the status on message updates
    socket.on('status', function (data) {
        console.log("Status update received:", data);
        appendMessage(data.msg, data.style);
    });

    // Handles chat messages
    socket.on('message', function (data) {
        console.log("Message received:", data);
        appendMessage(data.msg, data.style);
    });

    // this will attach the messages to the chat box
    function appendMessage(message, style) {
        const chatBox = document.getElementById("chat");
        if (chatBox) {
            const tag = document.createElement("p");
            tag.textContent = message;
            tag.style.cssText = style;
            chatBox.appendChild(tag);
            chatBox.scrollTop = chatBox.scrollHeight; 
        }
    }

    // Handles the "Send" button click and will senf message to chat box
    const sendButton = document.getElementById("send-button");
    const messageInput = document.getElementById("message-input");
    if (sendButton && messageInput) {
        sendButton.addEventListener("click", function () {
            const message = messageInput.value;
            console.log("Send button clicked. Message to send:", message);
            if (message) {
                socket.emit('text', { text: message });
                messageInput.value = ""; // Clear the input field
            }
        });
    }

    // Handles the "Leave Chat" button click and will redirect to home page after clicked
    const leaveButton = document.getElementById("leave-chat-btn");
    if (leaveButton) {
        leaveButton.addEventListener("click", function () {
            console.log("Leave Chat button clicked");
            socket.emit('left', {});
            window.location.href = "/home";
        });
    }
}

// Initializes the chat functionality only on the /chat page
document.addEventListener("DOMContentLoaded", () => {
    if (window.location.pathname === "/chat") {
        initializeChat();
    }
});
