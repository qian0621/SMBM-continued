
        const chatContainer = document.getElementById('chat-container');
        const chatOutput = document.getElementById('chat-output');
        const chatForm = document.getElementById('chat-form');
        const chatInput = document.getElementById('chat-input');

        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = chatInput.value;
            chatInput.value = '';

            const response = await fetch('/send-message', {
                method: 'POST',
                body: JSON.stringify({ message }),
                headers: { 'Content-Type': 'application/json' },
            });

            if (!response.ok) {
                console.error('Error sending message');
                return;
            }

            const { message: receivedMessage } = await response.json();
            chatOutput.innerHTML += `<p>${receivedMessage}</p>`;
        });

