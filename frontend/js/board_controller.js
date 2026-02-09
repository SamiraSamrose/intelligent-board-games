class BoardController {
    constructor() {
        this.currentGame = null;
        this.gameState = null;
        this.currentPlayerId = null;
        this.selectedAction = null;
        this.apiBaseUrl = 'http://localhost:5000/api';
        this.vrEnabled = false;
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        document.getElementById('new-game-btn').addEventListener('click', () => {
            this.showGameSetup();
        });

        document.getElementById('game-selector').addEventListener('change', (e) => {
            const gameType = e.target.value;
            if (gameType) {
                this.setupPlayerConfiguration(gameType);
            }
        });

        document.getElementById('start-game-btn').addEventListener('click', () => {
            this.createNewGame();
        });

        wsClient.on('game_update', (data) => {
            this.handleGameUpdate(data);
        });

        wsClient.on('vr_update', (data) => {
            this.handleVRUpdate(data);
        });

        wsClient.on('client_connected', () => {
            this.addLogEntry('Connected to game server', 'game-event');
            vrController.checkVRAvailability().then(available => {
                console.log('VR availability:', available);
            });
        });
    }

    showGameSetup() {
        document.getElementById('game-setup').classList.remove('hidden');
        document.getElementById('game-container').classList.add('hidden');
    }

    setupPlayerConfiguration(gameType) {
        const playerConfigContainer = document.getElementById('player-config');
        playerConfigContainer.innerHTML = '';

        const playerCounts = {
            'brass_birmingham': 4,
            'gloomhaven': 4,
            'terraforming_mars': 5,
            'dune': 6,
            'dungeons_dragons': 6,
            'exploding_kittens': 5
        };

        const numPlayers = playerCounts[gameType] || 4;

        const characterOptions = this.getCharacterOptions(gameType);

        for (let i = 0; i < numPlayers; i++) {
            const playerSlot = document.createElement('div');
            playerSlot.className = 'player-slot';
            playerSlot.innerHTML = `
                <h4>Player ${i + 1}</h4>
                <input type="text" id="player-${i}-name" placeholder="Player Name" value="Player ${i + 1}">
                <select id="player-${i}-character">
                    ${characterOptions.map(opt => `<option value="${opt.value}">${opt.label}</option>`).join('')}
                </select>
                <label>
                    <input type="checkbox" id="player-${i}-ai" ${i > 0 ? 'checked' : ''}>
                    AI Controlled
                </label>
            `;
            playerConfigContainer.appendChild(playerSlot);
        }
    }

    getCharacterOptions(gameType) {
        const options = {
            'brass_birmingham': [
                { value: 'default', label: 'Industrialist' }
            ],
            'gloomhaven': [
                { value: 'brute', label: 'Brute' },
                { value: 'tinkerer', label: 'Tinkerer' },
                { value: 'spellweaver', label: 'Spellweaver' },
                { value: 'scoundrel', label: 'Scoundrel' },
                { value: 'ranger', label: 'Ranger' }
            ],
            'terraforming_mars': [
                { value: 'Credicor', label: 'Credicor' },
                { value: 'Ecoline', label: 'Ecoline' },
                { value: 'Helion', label: 'Helion' },
                { value: 'Mining Guild', label: 'Mining Guild' },
                { value: 'Tharsis Republic', label: 'Tharsis Republic' }
            ],
            'dune': [
                { value: 'atreides', label: 'House Atreides' },
                { value: 'harkonnen', label: 'House Harkonnen' },
                { value: 'emperor', label: 'Emperor' },
                { value: 'guild', label: 'Spacing Guild' },
                { value: 'bene_gesserit', label: 'Bene Gesserit' },
                { value: 'fremen', label: 'Fremen' }
            ],
            'dungeons_dragons': [
                { value: 'dungeon_master', label: 'Dungeon Master' },
                { value: 'fighter', label: 'Fighter' },
                { value: 'wizard', label: 'Wizard' },
                { value: 'rogue', label: 'Rogue' },
                { value: 'cleric', label: 'Cleric' },
                { value: 'ranger', label: 'Ranger' }
            ],
            'exploding_kittens': [
                { value: 'default', label: 'Player' }
            ]
        };

        return options[gameType] || [{ value: 'default', label: 'Player' }];
    }

    async createNewGame() {
        const gameType = document.getElementById('game-selector').value;
        if (!gameType) {
            alert('Please select a game type');
            return;
        }

        const playerConfigs = this.collectPlayerConfigurations(gameType);
        const gameId = `game_${Date.now()}`;
        const enableVR = document.getElementById('enable-vr').checked;

        try {
            const response = await fetch(`${this.apiBaseUrl}/games/create`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    game_type: gameType,
                    players: playerConfigs,
                    game_id: gameId,
                    enable_vr: enableVR
                })
            });

            const data = await response.json();

            if (data.game_id) {
                this.currentGame = {
                    id: data.game_id,
                    type: gameType
                };
                this.gameState = data.game_state;
                this.currentPlayerId = 0;

                wsClient.joinGame(data.game_id);

                if (enableVR && data.vr_data) {
                    this.vrEnabled = true;
                    await vrController.enableVRForGame(data.game_id);
                    this.addLogEntry('VR mode enabled with Genie3', 'game-event');
                }

                document.getElementById('game-setup').classList.add('hidden');
                document.getElementById('game-container').classList.remove('hidden');

                this.renderGameState();
                this.addLogEntry(`Game started: ${gameType}`, 'game-event');
            } else {
                alert('Failed to create game');
            }
        } catch (error) {
            console.error('Error creating game:', error);
            alert('Error creating game: ' + error.message);
        }
    }

    collectPlayerConfigurations(gameType) {
        const playerCounts = {
            'brass_birmingham': 4,
            'gloomhaven': 4,
            'terraforming_mars': 5,
            'dune': 6,
            'dungeons_dragons': 6,
            'exploding_kittens': 5
        };

        const numPlayers = playerCounts[gameType] || 4;
        const configs = [];

        for (let i = 0; i < numPlayers; i++) {
            const nameEl = document.getElementById(`player-${i}-name`);
            const characterEl = document.getElementById(`player-${i}-character`);
            const aiEl = document.getElementById(`player-${i}-ai`);
            
            if (!nameEl || !characterEl || !aiEl) {
                configs.push({
                    name: `Player ${i + 1}`,
                    character: 'default',
                    is_ai: i > 0,
                    class: 'default'
                });
                continue;
            }

            configs.push({
                name: nameEl.value,
                character: characterEl.value,
                is_ai: aiEl.checked,
                class: characterEl.value
            });
        }

        return configs;
    }

    renderGameState() {
        if (!this.gameState) return;

        this.updateGameInfo();
        this.updatePlayerList();
        this.loadAvailableActions();
        gameRenderer.renderBoard(this.currentGame.type, this.gameState);
    }

    updateGameInfo() {
        const turnInfo = document.getElementById('turn-info');
        const phaseInfo = document.getElementById('phase-info');

        turnInfo.innerHTML = `
            <strong>Turn:</strong> ${this.gameState.turn || 0}
            ${this.gameState.round ? `<br><strong>Round:</strong> ${this.gameState.round}` : ''}
            ${this.gameState.generation ? `<br><strong>Generation:</strong> ${this.gameState.generation}` : ''}
        `;

        if (this.gameState.phase) {
            phaseInfo.innerHTML = `<strong>Phase:</strong> ${this.gameState.phase}`;
        }

        if (this.gameState.current_player) {
            const currentPlayer = this.gameState.current_player;
            turnInfo.innerHTML += `<br><strong>Current Player:</strong> ${currentPlayer.name}`;
        }
    }

    updatePlayerList() {
        const playersContainer = document.getElementById('players-container');
        playersContainer.innerHTML = '';

        if (!this.gameState.players) return;

        this.gameState.players.forEach((player, index) => {
            const playerItem = document.createElement('div');
            playerItem.className = 'player-item';
            
            if (this.gameState.current_player && player.id === this.gameState.current_player.id) {
                playerItem.classList.add('active');
            }

            const stats = this.getPlayerStats(player, this.currentGame.type);

            playerItem.innerHTML = `
                <h4>${player.name}</h4>
                ${player.class ? `<div style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">${player.class}</div>` : ''}
                ${player.faction ? `<div style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">${player.faction}</div>` : ''}
                <div class="player-stats">
                    ${stats.map(stat => `
                        <div class="stat-item">
                            <span class="stat-label">${stat.label}:</span>
                            <span class="stat-value">${stat.value}</span>
                        </div>
                    `).join('')}
                </div>
            `;

            playersContainer.appendChild(playerItem);
        });
    }

    getPlayerStats(player, gameType) {
        const stats = [];

        if (gameType === 'brass_birmingham') {
            stats.push({ label: 'Money', value: `£${player.money || 0}` });
            stats.push({ label: 'Income', value: player.income || 0 });
            stats.push({ label: 'Score', value: player.score || 0 });
        } else if (gameType === 'gloomhaven') {
            stats.push({ label: 'HP', value: `${player.current_hp || 0}/${player.max_hp || 0}` });
            stats.push({ label: 'XP', value: player.experience || 0 });
            stats.push({ label: 'Cards', value: player.hand ? player.hand.length : 0 });
        } else if (gameType === 'terraforming_mars') {
            stats.push({ label: 'MC', value: player.megacredits || 0 });
            stats.push({ label: 'TR', value: player.terraform_rating || 0 });
            stats.push({ label: 'Steel', value: player.steel || 0 });
            stats.push({ label: 'Titanium', value: player.titanium || 0 });
        } else if (gameType === 'dune') {
            stats.push({ label: 'Spice', value: player.spice || 0 });
            stats.push({ label: 'Forces', value: player.forces || 0 });
            stats.push({ label: 'Cards', value: player.treachery_cards ? player.treachery_cards.length : 0 });
        } else if (gameType === 'dungeons_dragons') {
            if (player.role !== 'dungeon_master') {
                stats.push({ label: 'HP', value: `${player.current_hp || 0}/${player.max_hp || 0}` });
                stats.push({ label: 'AC', value: player.ac || 0 });
                stats.push({ label: 'Level', value: player.level || 1 });
            }
        } else if (gameType === 'exploding_kittens') {
            stats.push({ label: 'Cards', value: player.hand ? player.hand.length : 0 });
            stats.push({ label: 'Status', value: player.alive ? 'Alive' : 'Eliminated' });
        }

        return stats;
    }

    async loadAvailableActions() {
        if (!this.currentGame || this.currentPlayerId === null) return;

        try {
            const response = await fetch(
                `${this.apiBaseUrl}/games/${this.currentGame.id}/actions?player_id=${this.currentPlayerId}`
            );
            const data = await response.json();

            this.displayActions(data.actions || []);
        } catch (error) {
            console.error('Error loading actions:', error);
        }
    }

    displayActions(actions) {
        const actionsContainer = document.getElementById('actions-container');
        actionsContainer.innerHTML = '';

        if (actions.length === 0) {
            actionsContainer.innerHTML = '<p>No actions available</p>';
            return;
        }

        actions.forEach(action => {
            const actionItem = document.createElement('div');
            actionItem.className = 'action-item';
            actionItem.innerHTML = `
                <h5>${action.name || action.type || 'Action'}</h5>
                <p>${action.description || ''}</p>
                ${action.cost ? `<p style="color: #f5576c;">Cost: ${action.cost}</p>` : ''}
            `;

            actionItem.addEventListener('click', () => {
                this.selectAction(action);
            });

            actionsContainer.appendChild(actionItem);
        });
    }

    async selectAction(action) {
        this.selectedAction = action;

        const confirmed = confirm(`Execute action: ${action.description || action.type}?`);
        if (!confirmed) return;

        try {
            const response = await fetch(`${this.apiBaseUrl}/games/${this.currentGame.id}/execute`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player_id: this.currentPlayerId,
                    action: action
                })
            });

            const result = await response.json();

            if (result.success) {
                this.addLogEntry(
                    `Player action: ${action.description || action.type}`,
                    'player-action'
                );

                await this.refreshGameState();
                
                if (this.vrEnabled) {
                    await vrController.updateVRWorld(this.currentGame.id, {
                        action: action,
                        player: this.currentPlayerId
                    });
                }
                
                await this.processAITurns();
            } else {
                alert(`Action failed: ${result.error || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Error executing action:', error);
            alert('Error executing action: ' + error.message);
        }
    }

    async refreshGameState() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/games/${this.currentGame.id}/state`);
            const data = await response.json();

            this.gameState = data;
            this.renderGameState();
        } catch (error) {
            console.error('Error refreshing game state:', error);
        }
    }

    async processAITurns() {
        if (!this.gameState.current_player) return;

        const currentPlayer = this.gameState.current_player;
        
        const playerConfigs = this.collectPlayerConfigurations(this.currentGame.type);
        const isAI = playerConfigs[currentPlayer.id] && playerConfigs[currentPlayer.id].is_ai;

        if (isAI) {
            await this.sleep(1000);

            try {
                const response = await fetch(`${this.apiBaseUrl}/games/${this.currentGame.id}/ai_turn`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        player_id: currentPlayer.id
                    })
                });

                const result = await response.json();

                if (result.result && result.result.success) {
                    this.addLogEntry(
                        `AI action (${currentPlayer.name}): ${result.result.action || 'Unknown'}`,
                        'ai-action'
                    );

                    if (result.mimic_decision && result.mimic_decision.reasoning) {
                        this.displayAIReasoning(result.mimic_decision);
                    }

                    await this.refreshGameState();
                    await this.processAITurns();
                }
            } catch (error) {
                console.error('Error processing AI turn:', error);
            }
        }
    }

    isAIPlayer(playerId) {
        if (!this.currentGame || !this.currentGame.type) {
            return false;
        }
        
        const playerCounts = {
            'brass_birmingham': 4,
            'gloomhaven': 4,
            'terraforming_mars': 5,
            'dune': 6,
            'dungeons_dragons': 6,
            'exploding_kittens': 5
        };
        
        const numPlayers = playerCounts[this.currentGame.type] || 4;
        
        for (let i = 0; i < numPlayers; i++) {
            const aiCheckbox = document.getElementById(`player-${i}-ai`);
            if (aiCheckbox && i === playerId) {
                return aiCheckbox.checked;
            }
        }
        
        return playerId > 0;
    }

    displayAIReasoning(decision) {
        const reasoningContent = document.getElementById('reasoning-content');
        
        let reasoning = decision.reasoning || 'No reasoning provided';
        
        if (decision.in_character_quote) {
            reasoning += `\n\n"${decision.in_character_quote}"`;
        }
        
        if (decision.society_reasoning) {
            reasoning += `\n\nSociety of Thought:\n${decision.society_reasoning}`;
        }

        if (decision.diversity_metrics) {
            reasoning += `\n\nDiversity: ${JSON.stringify(decision.diversity_metrics, null, 2)}`;
        }

        reasoningContent.textContent = reasoning;
    }

    handleGameUpdate(data) {
        if (data.game_id !== this.currentGame.id) return;

        this.gameState = data.state;
        this.renderGameState();

        if (data.last_action) {
            const actionText = data.last_action.action || 'Unknown action';
            this.addLogEntry(`Game update: ${actionText}`, 'game-event');
        }

        if (data.ai_reasoning) {
            this.displayAIReasoning({ reasoning: data.ai_reasoning });
        }
        
        if (data.character_quote) {
            this.addLogEntry(`Character: "${data.character_quote}"`, 'ai-action');
        }
    }

    handleVRUpdate(data) {
        if (data.game_id !== this.currentGame.id) return;
        
        console.log('VR world updated:', data.changes);
        this.addLogEntry('VR environment updated', 'game-event');
    }

    addLogEntry(message, type = 'game-event') {
        const logContent = document.getElementById('log-content');
        
        const entry = document.createElement('div');
        entry.className = `log-entry ${type}`;
        
        const timestamp = new Date().toLocaleTimeString();
        entry.innerHTML = `
            <div class="log-timestamp">${timestamp}</div>
            <div>${message}</div>
        `;

        logContent.insertBefore(entry, logContent.firstChild);

        if (logContent.children.length > 50) {
            logContent.removeChild(logContent.lastChild);
        }
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

const boardController = new BoardController();