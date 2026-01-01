const socket = io();
const video = document.getElementById('videoElement');
const canvas = document.getElementById('videoCanvas');
const ctx = canvas.getContext('2d');
const trustScoreValue = document.getElementById('trustScoreValue');
const circle = document.querySelector('.progress-ring__circle');
const alertOverlay = document.getElementById('alertOverlay');
const alertMessage = document.getElementById('alertMessage');
const logContainer = document.getElementById('logContainer');
const statusText = document.getElementById('statusText');
const faceCountText = document.getElementById('faceCount');
const connectionStatus = document.getElementById('connectionStatus');

const radius = circle.r.baseVal.value;
const circumference = radius * 2 * Math.PI;

circle.style.strokeDasharray = `${circumference} ${circumference}`;
circle.style.strokeDashoffset = 0;

function setProgress(percent) {
    const offset = circumference - (percent / 100) * circumference;
    circle.style.strokeDashoffset = offset;
    trustScoreValue.textContent = `${percent}%`;
    
    if (percent < 50) {
        circle.style.stroke = 'var(--danger-color)';
    } else if (percent < 80) {
        circle.style.stroke = 'orange';
    } else {
        circle.style.stroke = 'var(--success-color)';
    }
}

// Access Webcam
navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } })
    .then(stream => {
        video.srcObject = stream;
        
        // Send frames every 400ms
        setInterval(() => {
            if (video.readyState === video.HAVE_ENOUGH_DATA) {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                
                const dataURL = canvas.toDataURL('image/jpeg', 0.5);
                socket.emit('video_frame', { image: dataURL });
            }
        }, 400);
    })
    .catch(err => {
        console.error("Error accessing webcam:", err);
        statusText.textContent = "Camera Error";
    });

// Socket Events
socket.on('connect', () => {
    connectionStatus.textContent = "Live";
    connectionStatus.style.background = "var(--success-color)";
});

socket.on('disconnect', () => {
    connectionStatus.textContent = "Disconnected";
    connectionStatus.style.background = "var(--danger-color)";
});

socket.on('proctor_result', (data) => {
    // Update Trust Score
    setProgress(data.trust_score);
    
    // Update Face Count
    faceCountText.textContent = `Faces: ${data.face_count}`;
    
    // Handle Infractions
    if (data.is_infraction) {
        alertOverlay.style.opacity = 1;
        
        let msg = "";
        if (data.infraction_type === 'multiple_faces') msg = "Multiple Faces Detected!";
        else if (data.infraction_type === 'looking_away') msg = "Looking Away Detected!";
        else if (data.infraction_type === 'no_face') msg = "No Face Detected!";
        
        alertMessage.textContent = msg;
        statusText.textContent = "Infraction Detected";
        statusText.style.color = "var(--danger-color)";
        
        addLog(msg, true);
    } else {
        alertOverlay.style.opacity = 0;
        statusText.textContent = "Monitoring";
        statusText.style.color = "var(--text-secondary)";
    }
});

function addLog(message, isViolation) {
    const div = document.createElement('div');
    div.className = `log-entry ${isViolation ? 'violation' : ''}`;
    const time = new Date().toLocaleTimeString();
    div.textContent = `[${time}] ${message}`;
    logContainer.prepend(div);
    
    // Limit logs
    if (logContainer.children.length > 20) {
        logContainer.removeChild(logContainer.lastChild);
    }
}
