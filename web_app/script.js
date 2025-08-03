const ipInput = document.getElementById('ipInput');
const statusLabel = document.getElementById('statusLabel');
const connectButton = document.getElementById('connectButton');
const commandButtonsLayout = document.getElementById('commandButtonsLayout');
const APP_PASSWORD = 'admin';  // 💥 Set your UI password here

let currentIP = '';  // Store the connected IP
const SECRET_TOKEN = 'XjD9f8#@df0s8d2kFz';  // MUST match the server.py token

connectButton.addEventListener('click', function() {
    const ip = ipInput.value.trim();

    if (!ip) {
        statusLabel.textContent = "Status: IP is required";
        statusLabel.style.color = "red";
        return;
    }

    const url = `http://${ip}:5000/command`;
    const payload = JSON.stringify({ "command": "ping" });

    fetch(url, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': SECRET_TOKEN // 🔥 Token added here
        },
        body: payload
    })
    .then(response => {
        if (!response.ok) throw new Error('Unauthorized or server error');
        return response.json();
    })
    .then(data => {
        statusLabel.textContent = "Status: Connected!";
        statusLabel.style.color = "green";
        commandButtonsLayout.style.display = 'block';
        currentIP = ip;  // Save IP for future commands
    })
    .catch(error => {
        statusLabel.textContent = "Status: Connection failed";
        statusLabel.style.color = "red";
        console.error('Error:', error);
    });
});

function sendCommand(command) {
    if (!currentIP) {
        alert("Connect first!");
        return;
    }

    const url = `http://${currentIP}:5000/command`;
    const payload = JSON.stringify({ "command": command });

    fetch(url, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': SECRET_TOKEN // 🔥 Token added here too
        },
        body: payload
    })
    .then(response => {
        if (!response.ok) throw new Error('Unauthorized or server error');
        return response.json();
    })
    .then(data => {
        alert(`Command '${command}' executed: ${data.message}`);
    })
    .catch(error => {
        alert('Failed to execute command');
        console.error('Error:', error);
    });
}

function checkPassword() {
    const inputPassword = document.getElementById('passwordInput').value;
    const loginStatus = document.getElementById('loginStatus');

    if(inputPassword === APP_PASSWORD) {
        // Password correct
        document.getElementById('loginSection').style.display = 'none';
        document.getElementById('mainApp').style.display = 'block';
    } else {
        loginStatus.textContent = "Incorrect password!";
        loginStatus.style.color = "red";
    }
}
