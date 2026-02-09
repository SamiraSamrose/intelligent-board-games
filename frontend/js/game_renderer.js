class GameRenderer {
    constructor() {
        this.canvas = document.getElementById('game-board');
        this.ctx = this.canvas.getContext('2d');
        this.boardOverlay = document.getElementById('board-overlay');
        this.scale = 1;
        this.offsetX = 0;
        this.offsetY = 0;
    }

    renderBoard(gameType, gameState) {
        this.clearCanvas();

        switch (gameType) {
            case 'brass_birmingham':
                this.renderBrassBirmingham(gameState);
                break;
            case 'gloomhaven':
                this.renderGloomhaven(gameState);
                break;
            case 'terraforming_mars':
                this.renderTerraformingMars(gameState);
                break;
            case 'dune':
                this.renderDune(gameState);
                break;
            case 'dungeons_dragons':
                this.renderDungeonsAndDragons(gameState);
                break;
            case 'exploding_kittens':
                this.renderExplodingKittens(gameState);
                break;
        }
    }

    clearCanvas() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.boardOverlay.innerHTML = '';
    }

    renderBrassBirmingham(gameState) {
        const board = gameState.board;
        if (!board || !board.cities) return;

        this.ctx.fillStyle = '#2a2a2a';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        const cityPositions = this.calculateCityPositions(Object.keys(board.cities));

        this.ctx.strokeStyle = '#666666';
        this.ctx.lineWidth = 3;

        Object.keys(board.cities).forEach(cityName => {
            const city = board.cities[cityName];
            const connections = city.connections || [];

            connections.forEach(connectedCity => {
                if (cityPositions[cityName] && cityPositions[connectedCity]) {
                    const from = cityPositions[cityName];
                    const to = cityPositions[connectedCity];

                    this.ctx.beginPath();
                    this.ctx.moveTo(from.x, from.y);
                    this.ctx.lineTo(to.x, to.y);
                    this.ctx.stroke();
                }
            });
        });

        Object.keys(board.cities).forEach(cityName => {
            const city = board.cities[cityName];
            const pos = cityPositions[cityName];

            if (!pos) return;

            this.ctx.fillStyle = city.type === 'stronghold' ? '#8b4513' : '#4a4a4a';
            this.ctx.beginPath();
            this.ctx.arc(pos.x, pos.y, 30, 0, Math.PI * 2);
            this.ctx.fill();

            this.ctx.strokeStyle = '#ffffff';
            this.ctx.lineWidth = 2;
            this.ctx.stroke();

            this.ctx.fillStyle = '#ffffff';
            this.ctx.font = '12px Arial';
            this.ctx.textAlign = 'center';
            this.ctx.fillText(cityName, pos.x, pos.y - 40);

            if (city.industries && city.industries.length > 0) {
                city.industries.forEach((industry, idx) => {
                    const angle = (idx * Math.PI * 2) / city.industries.length;
                    const ix = pos.x + Math.cos(angle) * 45;
                    const iy = pos.y + Math.sin(angle) * 45;

                    this.ctx.fillStyle = this.getPlayerColor(industry.player);
                    this.ctx.beginPath();
                    this.ctx.arc(ix, iy, 8, 0, Math.PI * 2);
                    this.ctx.fill();
                });
            }
        });

        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = '16px Arial';
        this.ctx.textAlign = 'left';
        this.ctx.fillText(`Coal Market: ${board.coal_market ? board.coal_market.length : 0}`, 20, 30);
        this.ctx.fillText(`Iron Market: ${board.iron_market ? board.iron_market.length : 0}`, 20, 55);
    }

    renderGloomhaven(gameState) {
        if (!gameState.scenario) return;

        this.ctx.fillStyle = '#1a1a1a';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        const scenario = gameState.scenario;
        const rooms = scenario.rooms || {};

        const cellSize = 40;

        Object.keys(rooms).forEach(roomName => {
            const room = rooms[roomName];
            const tiles = room.tiles || [];

            tiles.forEach(([x, y]) => {
                const screenX = x * cellSize + 100;
                const screenY = y * cellSize + 100;

                this.ctx.fillStyle = '#3a3a3a';
                this.ctx.fillRect(screenX, screenY, cellSize - 2, cellSize - 2);

                this.ctx.strokeStyle = '#555555';
                this.ctx.lineWidth = 1;
                this.ctx.strokeRect(screenX, screenY, cellSize - 2, cellSize - 2);
            });
        });

        if (gameState.players) {
            gameState.players.forEach(player => {
                if (player.position) {
                    const [x, y] = player.position;
                    const screenX = x * cellSize + 100;
                    const screenY = y * cellSize + 100;

                    this.ctx.fillStyle = this.getPlayerColor(player.id);
                    this.ctx.beginPath();
                    this.ctx.arc(
                        screenX + cellSize / 2,
                        screenY + cellSize / 2,
                        cellSize / 3,
                        0,
                        Math.PI * 2
                    );
                    this.ctx.fill();

                    this.ctx.strokeStyle = '#ffffff';
                    this.ctx.lineWidth = 2;
                    this.ctx.stroke();

                    this.ctx.fillStyle = '#ffffff';
                    this.ctx.font = 'bold 14px Arial';
                    this.ctx.textAlign = 'center';
                    this.ctx.fillText(
                        player.name[0],
                        screenX + cellSize / 2,
                        screenY + cellSize / 2 + 5
                    );
                }
            });
        }

        if (gameState.monsters) {
            gameState.monsters.forEach(monster => {
                if (monster.position) {
                    const [x, y] = monster.position;
                    const screenX = x * cellSize + 100;
                    const screenY = y * cellSize + 100;

                    this.ctx.fillStyle = '#ff0000';
                    this.ctx.beginPath();
                    this.ctx.arc(
                        screenX + cellSize / 2,
                        screenY + cellSize / 2,
                        cellSize / 3,
                        0,
                        Math.PI * 2
                    );
                    this.ctx.fill();

                    this.ctx.strokeStyle = '#ffffff';
                    this.ctx.lineWidth = 2;
                    this.ctx.stroke();
                }
            });
        }
    }

    renderTerraformingMars(gameState) {
        this.ctx.fillStyle = '#8b4513';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = '24px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('TERRAFORMING MARS', this.canvas.width / 2, 40);

        const params = gameState.global_parameters || {};

        const barWidth = 300;
        const barHeight = 40;
        const startX = 50;
        let currentY = 100;

        this.drawParameterBar(
            'Temperature',
            startX,
            currentY,
            barWidth,
            barHeight,
            params.temperature || -30,
            -30,
            8,
            '#ff4444'
        );
        currentY += 80;

        this.drawParameterBar(
            'Oxygen',
            startX,
            currentY,
            barWidth,
            barHeight,
            params.oxygen || 0,
            0,
            14,
            '#44ff44'
        );
        currentY += 80;

        this.drawParameterBar(
            'Oceans',
            startX,
            currentY,
            barWidth,
            barHeight,
            params.oceans || 0,
            0,
            9,
            '#4444ff'
        );

        if (gameState.players) {
            const playerX = this.canvas.width - 400;
            let playerY = 100;

            this.ctx.fillStyle = '#ffffff';
            this.ctx.font = '18px Arial';
            this.ctx.textAlign = 'left';
            this.ctx.fillText('Players:', playerX, playerY);
            playerY += 40;

            gameState.players.forEach(player => {
                this.ctx.fillStyle = this.getPlayerColor(player.id);
                this.ctx.fillRect(playerX, playerY, 20, 20);

                this.ctx.fillStyle = '#ffffff';
                this.ctx.font = '14px Arial';
                this.ctx.fillText(
                    `${player.name} (${player.corporation || 'Unknown'})`,
                    playerX + 30,
                    playerY + 15
                );
                playerY += 30;

                this.ctx.font = '12px Arial';
                this.ctx.fillStyle = '#cccccc';
                this.ctx.fillText(
                    `MC: ${player.megacredits || 0} | TR: ${player.terraform_rating || 0}`,
                    playerX + 30,
                    playerY
                );
                playerY += 40;
            });
        }
    }

    renderDune(gameState) {
        const board = gameState.board;
        if (!board || !board.territories) return;

        this.ctx.fillStyle = '#d2b48c';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        const territoryPositions = this.calculateTerritoryPositions(
            Object.keys(board.territories)
        );

        this.ctx.strokeStyle = '#8b7355';
        this.ctx.lineWidth = 2;

        Object.keys(board.territories).forEach(territoryName => {
            const territory = board.territories[territoryName];
            const pos = territoryPositions[territoryName];

            if (!pos) return;

            this.ctx.fillStyle = territory.type === 'stronghold' ? '#8b4513' : '#c19a6b';
            this.ctx.fillRect(pos.x - 40, pos.y - 30, 80, 60);

            this.ctx.strokeStyle = '#000000';
            this.ctx.lineWidth = 2;
            this.ctx.strokeRect(pos.x - 40, pos.y - 30, 80, 60);

            this.ctx.fillStyle = '#000000';
            this.ctx.font = '10px Arial';
            this.ctx.textAlign = 'center';
            this.ctx.fillText(territoryName, pos.x, pos.y - 35);

            if (territory.spice > 0) {
                this.ctx.fillStyle = '#ff8c00';
                this.ctx.font = 'bold 14px Arial';
                this.ctx.fillText(`${territory.spice}`, pos.x, pos.y);
            }

            if (territory.occupants && territory.occupants.length > 0) {
                territory.occupants.forEach((occupant, idx) => {
                    const offset = idx * 15 - (territory.occupants.length * 15) / 2;
                    this.ctx.fillStyle = this.getPlayerColor(occupant.player_id);
                    this.ctx.fillRect(pos.x + offset - 5, pos.y + 10, 10, 10);

                    this.ctx.fillStyle = '#ffffff';
                    this.ctx.font = '8px Arial';
                    this.ctx.fillText(occupant.forces, pos.x + offset, pos.y + 18);
                });
            }
        });

        const stormAngle = ((board.storm_position || 0) / 18) * Math.PI * 2;
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        const radius = 200;

        this.ctx.save();
        this.ctx.translate(centerX, centerY);
        this.ctx.rotate(stormAngle);

        this.ctx.fillStyle = 'rgba(139, 69, 19, 0.5)';
        this.ctx.beginPath();
        this.ctx.moveTo(0, 0);
        this.ctx.arc(0, 0, radius, 0, Math.PI / 9);
        this.ctx.closePath();
        this.ctx.fill();

        this.ctx.restore();
    }

    renderDungeonsAndDragons(gameState) {
        const board = gameState.board;
        if (!board || !board.grid) return;

        this.ctx.fillStyle = '#000000';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        const grid = board.grid;
        const cellSize = 30;
        const startX = 50;
        const startY = 50;

        grid.forEach((row, rowIdx) => {
            row.forEach((cell, colIdx) => {
                const x = startX + colIdx * cellSize;
                const y = startY + rowIdx * cellSize;

                if (cell.terrain === 'wall') {
                    this.ctx.fillStyle = '#2a2a2a';
                } else if (cell.terrain === 'stone_floor') {
                    this.ctx.fillStyle = '#4a4a4a';
                } else if (cell.terrain === 'door') {
                    this.ctx.fillStyle = '#8b4513';
                } else {
                    this.ctx.fillStyle = '#1a1a1a';
                }

                this.ctx.fillRect(x, y, cellSize - 1, cellSize - 1);

                this.ctx.strokeStyle = '#333333';
                this.ctx.lineWidth = 1;
                this.ctx.strokeRect(x, y, cellSize - 1, cellSize - 1);

                if (cell.occupant !== null) {
                    this.ctx.fillStyle = this.getPlayerColor(cell.occupant);
                    this.ctx.beginPath();
                    this.ctx.arc(
                        x + cellSize / 2,
                        y + cellSize / 2,
                        cellSize / 3,
                        0,
                        Math.PI * 2
                    );
                    this.ctx.fill();
                }
            });
        });

        if (gameState.players) {
            const infoX = this.canvas.width - 250;
            let infoY = 50;

            gameState.players.forEach(player => {
                if (player.role === 'dungeon_master') return;

                this.ctx.fillStyle = '#ffffff';
                this.ctx.font = '14px Arial';
                this.ctx.textAlign = 'left';
                this.ctx.fillText(`${player.name} (${player.class})`, infoX, infoY);
                infoY += 20;

                this.ctx.font = '12px Arial';
                this.ctx.fillStyle = '#cccccc';
                this.ctx.fillText(
                    `HP: ${player.current_hp}/${player.max_hp} | AC: ${player.ac}`,
                    infoX,
                    infoY
                );
                infoY += 30;
            });
        }
    }

    renderExplodingKittens(gameState) {
        this.ctx.fillStyle = '#2c3e50';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = '28px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('EXPLODING KITTENS', this.canvas.width / 2, 40);

        const deckX = this.canvas.width / 2;
        const deckY = this.canvas.height / 2;

        this.ctx.fillStyle = '#e74c3c';
        this.ctx.fillRect(deckX - 60, deckY - 80, 120, 160);
        this.ctx.strokeStyle = '#c0392b';
        this.ctx.lineWidth = 4;
        this.ctx.strokeRect(deckX - 60, deckY - 80, 120, 160);

        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = '20px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('DECK', deckX, deckY - 10);

        this.ctx.font = '32px Arial';
        this.ctx.fillText(gameState.deck_remaining || 0, deckX, deckY + 30);

        if (gameState.players) {
            const radius = 250;
            const angleStep = (Math.PI * 2) / gameState.players.length;

            gameState.players.forEach((player, idx) => {
                const angle = angleStep * idx - Math.PI / 2;
                const x = deckX + Math.cos(angle) * radius;
                const y = deckY + Math.sin(angle) * radius;

                this.ctx.fillStyle = player.alive ? '#2ecc71' : '#95a5a6';
                this.ctx.beginPath();
                this.ctx.arc(x, y, 40, 0, Math.PI * 2);
                this.ctx.fill();

                this.ctx.strokeStyle = '#ffffff';
                this.ctx.lineWidth = 3;
                this.ctx.stroke();

                this.ctx.fillStyle = '#ffffff';
                this.ctx.font = 'bold 14px Arial';
                this.ctx.textAlign = 'center';
                this.ctx.fillText(player.name, x, y - 50);

                this.ctx.font = '12px Arial';
                this.ctx.fillText(
                    `Cards: ${player.hand ? player.hand.length : 0}`,
                    x,
                    y + 60
                );
            });
        }
    }

    drawParameterBar(label, x, y, width, height, current, min, max, color) {
        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = '16px Arial';
        this.ctx.textAlign = 'left';
        this.ctx.fillText(label, x, y - 10);

        this.ctx.fillStyle = '#333333';
        this.ctx.fillRect(x, y, width, height);

        const progress = Math.max(0, Math.min(1, (current - min) / (max - min)));
        this.ctx.fillStyle = color;
        this.ctx.fillRect(x, y, width * progress, height);

        this.ctx.strokeStyle = '#ffffff';
        this.ctx.lineWidth = 2;
        this.ctx.strokeRect(x, y, width, height);

        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = '18px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(current, x + width / 2, y + height / 2 + 6);
    }

    calculateCityPositions(cities) {
        const positions = {};
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        const radius = 250;

        cities.forEach((city, idx) => {
            const angle = (idx / cities.length) * Math.PI * 2;
            positions[city] = {
                x: centerX + Math.cos(angle) * radius,
                y: centerY + Math.sin(angle) * radius
            };
        });

        return positions;
    }

    calculateTerritoryPositions(territories) {
        const positions = {};
        const cols = 6;
        const cellWidth = this.canvas.width / (cols + 1);
        const cellHeight = 80;

        territories.forEach((territory, idx) => {
            const row = Math.floor(idx / cols);
            const col = idx % cols;

            positions[territory] = {
                x: (col + 1) * cellWidth,
                y: 100 + row * cellHeight
            };
        });

        return positions;
    }

    getPlayerColor(playerId) {
        const colors = [
            '#e74c3c',
            '#3498db',
            '#2ecc71',
            '#f39c12',
            '#9b59b6',
            '#1abc9c',
            '#e67e22',
            '#34495e'
        ];

        return colors[playerId % colors.length];
    }
}

const gameRenderer = new GameRenderer();