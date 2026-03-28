function handleSend() {
    const messageInput = document.getElementById('message');
    const responseContainer = document.getElementById('response-container');
    const helloText = document.getElementById('hello');
    const query = messageInput.value.trim();

    // 1. Validation: Don't send empty queries
    if (!query) return;

    // 2. UI Reset: Hide "Hello" and prepare the response box
    if (helloText) helloText.style.display = 'none';
    
    responseContainer.style.display = 'block';
    responseContainer.innerHTML = '<p class="loading">Searching PDF memory...</p>';

    // 3. Fetch data from your Python backend
    fetch(`/get_dimension?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // SUCCESS: Type the answer onto the surface
                typeEffect(responseContainer, data.formula);
            } else {
                // FAILURE: Show error message on the surface
                responseContainer.innerHTML = `<p style="color: #ff4b4b;">${data.formula}</p>`;
            }
        })
        .catch(error => {
            responseContainer.innerHTML = '<p style="color: #ff4b4b;">Connection error. Is the server running?</p>';
            console.error('Error:', error);
        });

    // Clear input for next question
    messageInput.value = '';
}

// Optional: GPT-style typing effect
function typeEffect(element, text) {
    element.innerHTML = "";
    let i = 0;
    const speed = 20; // milliseconds per character

    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    type();
}

// Allow pressing "Enter" to search
document.getElementById('message').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        handleSend();
    }
});
