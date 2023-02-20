const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const messagesContainer = document.querySelector('.messages-container');

// Send a message when the "Send" button is clicked
sendButton.addEventListener('click', () => {
    const message = messageInput.value;
    if (message) {
        // Add the message to the messages container
        const messageElement = document.createElement('div');
        messageElement.innerText = message;
        messagesContainer.appendChild(messageElement);
        // Clear the message input
        messageInput.value = '';
    }
});
