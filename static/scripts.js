// scripts.js

// Function to scroll chat messages container to the bottom
function scrollToBottom() {
    var chatMessages = document.getElementById('chat-messages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Scroll to the bottom when the page loads
window.onload = function() {
    scrollToBottom();
}

// Scroll to the bottom when a new message is added
var chatForm = document.getElementById('chat-form');
chatForm.addEventListener('submit', function() {
    setTimeout(scrollToBottom, 100); // Delay to ensure the message is rendered
});
