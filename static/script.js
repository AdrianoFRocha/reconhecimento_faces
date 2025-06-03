const video = document.getElementById('video_feed');
const startButton = document.getElementById('start');
const stopButton = document.getElementById('stop');
const statusText = document.getElementById('status');

startButton.addEventListener('click', () => {
    video.style.display = "block";  // Mostra a transmissão ao iniciar
    statusText.textContent = "Status: Reconhecimento iniciado...";
});

stopButton.addEventListener('click', () => {
    video.style.display = "none";  // Esconde a transmissão ao parar
    statusText.textContent = "Status: Reconhecimento parado";
});
