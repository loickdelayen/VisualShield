document.addEventListener('DOMContentLoaded', function() {
    const cameraFeed = document.getElementById('camera-feed');
    const cameraStatus = document.getElementById('camera-status');
    
    function updateCameraFeed() {
        const timestamp = new Date().getTime();
        cameraFeed.src = "/video_feed?t=" + timestamp;
    }
    
    function checkCameraStatus() {
        fetch('/camera_status')
            .then(response => {
                if (!response.ok) throw new Error("Erro na resposta");
                return response.json();
            })
            .then(data => {
                if (data.status === 'active') {
                    cameraStatus.textContent = "Câmera ativa";
                    cameraStatus.style.backgroundColor = "#2a9d8f";
                    updateCameraFeed();
                } else {
                    cameraStatus.textContent = "Câmera inativa";
                    cameraStatus.style.backgroundColor = "#e63946";
                }
            })
            .catch(error => {
                console.error("Erro ao verificar status da câmera:", error);
                cameraStatus.textContent = "Erro de conexão";
                cameraStatus.style.backgroundColor = "#e63946";
            });
    }
    
    // Verifica a cada 3 segundos
    checkCameraStatus();
    setInterval(checkCameraStatus, 3000);
    
    // Atualiza o feed periodicamente
    setInterval(updateCameraFeed, 1000);
});