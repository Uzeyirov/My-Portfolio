document.addEventListener('DOMContentLoaded', function() {
    const chatLog = document.getElementById('chat-log');
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('chat-message-input');
    const imageInput = document.getElementById('image-input');
    const fileInput = document.getElementById('file-input');
    const preview = document.getElementById('attachment-preview');
    const fileName = document.getElementById('file-name');

    // Çatı aşağı sürüşdürən funksiya
    function scrollToBottom() {
        chatLog.scrollTop = chatLog.scrollHeight;
    }
    scrollToBottom();

    // Fayl seçiləndə önbaxış
    [imageInput, fileInput].forEach(input => {
        input.addEventListener('change', () => {
            if (input.files.length > 0) {
                preview.style.display = 'block';
                fileName.textContent = input.files[0].name;
            }
        });
    });

    // Mesaj göndərmə (Real-time AJAX)
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(chatForm);
        
        if (!messageInput.value.trim() && !imageInput.files[0] && !fileInput.files[0]) {
            return;
        }

        fetch(chatForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        })
        .then(response => response.json()) // Cavabı JSON kimi alırıq
        .then(data => {
            if (data.status === 'success') {
                // HTML-ə yeni mesajı əlavə edirik
                let mediaHtml = '';
                if (data.image_url) {
                    mediaHtml += `<img src="${data.image_url}" class="chat-img">`;
                }
                if (data.file_url) {
                    mediaHtml += `<a href="${data.file_url}" class="chat-file" target="_blank">📂 ${data.file_name}</a>`;
                }

                const newMessage = `
                    <div class="message-item mine">
                        <span class="username">@${data.user}</span>
                        <div class="bubble-wrapper">
                            <div class="bubble">
                                ${data.content ? data.content : ''}
                                ${mediaHtml}
                            </div>
                            <span class="time">${data.timestamp}</span>
                        </div>
                    </div>
                `;

                chatLog.insertAdjacentHTML('beforeend', newMessage);
                
                // Formu təmizləyirik
                chatForm.reset();
                preview.style.display = 'none';
                
                // Aşağı sürüşdürürük
                scrollToBottom();
            } else {
                alert("Xəta baş verdi.");
            }
        })
        .catch(error => console.error('Error:', error));
    });
});





