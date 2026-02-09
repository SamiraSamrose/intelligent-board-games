document.addEventListener('DOMContentLoaded', () => {
    wsClient.connect('http://localhost:5000');
    
    wsClient.on('client_connected', () => {
        console.log('WebSocket connected successfully');
    });
    
    wsClient.on('error', (error) => {
        console.error('WebSocket error:', error);
        alert('Connection error. Please refresh the page.');
    });
});