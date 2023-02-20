
const messagesContainer = document.getElementById("messages");
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");

//Event Listeners
sendButton.addEventListener("click", async () => {
  const message = messageInput.value;
  messageInput.value = "";
  const res = await postData("/new_message", { message });
  const data = await res.json();
  if (data.success) {
    const messageElement = document.createElement("div");
    messageElement.innerText = data.message;
    messagesContainer.appendChild(messageElement);
  }
});

//fetch function
async function postData(url = '', data = {}) {
    const res = await fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return res;
}

//polling for new messages
setInterval(async () => {
  const res = await fetch("/messages");
  const data = await
