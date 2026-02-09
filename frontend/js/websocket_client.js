class WebSocketClient {
    constructor() {
        this.socket = null;
        this.gameId = null;
        this.connected = false;
        this.listeners = {};
    }

    connect(serverUrl = 'http://localhost:5000') {
        this.socket = io(serverUrl, {
            transports: ['websocket'],
            upgrade: false
        });

        this.socket.on('connect', () => {
            console.log('Connected to game server');
            this.connected = true;
            this.emit('client_connected', {});
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from game server');
            this.connected = false;
            this.emit('client_disconnected', {});
        });

        this.socket.on('game_update', (data) => {
            console.log('Game update received:', data);
            this.emit('game_update', data);
        });

        this.socket.on('joined', (data) => {
            console.log('Joined game:', data);
            this.emit('game_joined', data);
        });

        this.socket.on('left', (data) => {
            console.log('Left game:', data);
            this.emit('game_left', data);
        });

        this.socket.on('error', (error) => {
            console.error('WebSocket error:', error);
            this.emit('error', error);
        });
    }

    joinGame(gameId) {
        if (!this.connected) {
            console.error('Not connected to server');
            return;
        }

        this.gameId = gameId;
        this.socket.emit('join_game', { game_id: gameId });
    }

    leaveGame() {
        if (!this.connected || !this.gameId) {
            return;
        }

        this.socket.emit('leave_game', { game_id: this.gameId });
        this.gameId = null;
    }

    on(event, callback) {
        if (!this.listeners[event]) {
            this.listeners[event] = [];
        }
        this.listeners[event].push(callback);
    }

    emit(event, data) {
        if (this.listeners[event]) {
            this.listeners[event].forEach(callback => callback(data));
        }
    }

    disconnect() {
        if (this.socket) {
            this.socket.disconnect();
        }
    }
}

const wsClient = new WebSocketClient();