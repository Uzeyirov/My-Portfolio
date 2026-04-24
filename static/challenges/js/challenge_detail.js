function initChallengeTimer(deadlineString) {
    const timerElement = document.getElementById('timer-display');
    const targetDate = new Date(deadlineString).getTime();

    const interval = setInterval(() => {
        const now = new Date().getTime();
        const diff = targetDate - now;

        if (diff < 0) {
            clearInterval(interval);
            timerElement.innerHTML = "VAXT BİTDİ";
            return;
        }

        const d = Math.floor(diff / (1000 * 60 * 60 * 24));
        const h = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const s = Math.floor((diff % (1000 * 60)) / 1000);

        timerElement.innerHTML = `${d}g ${h}s ${m}d ${s}sn`;
    }, 1000);
}