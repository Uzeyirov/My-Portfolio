function toggleMessage(reqId, btn) {
    const msgElement = document.getElementById('msg-' + reqId);
    
    if (msgElement.classList.contains('text-truncate-custom')) {
        // Mətni açırıq
        msgElement.classList.remove('text-truncate-custom');
        msgElement.classList.add('ms-msg-expanded');
        btn.innerText = "QISALT";
        btn.style.color = "#ff4b2b";
    } else {
        // Mətni bağlayırıq
        msgElement.classList.add('text-truncate-custom');
        msgElement.classList.remove('ms-msg-expanded');
        btn.innerText = "TAM OXU";
        btn.style.color = "#00d1ff";
    }
}