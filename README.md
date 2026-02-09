# Intelligent Board Games (Brass Birmingham, Gloomhaven, Terraforming Mars, Dune, Dungeons & Dragons, Exploding Kittens) with AI Opponents

Advanced board game platform powered by Google Gemini AI with Genie3 VR integration, implementing research from "Societies of Thought" and "To Mask or to Mirror" research papers.

This system implements board game AI using research from "Societies of Thought" and "To Mask or to Mirror" papers. The backend executes six complete board games (Brass Birmingham, Gloomhaven, Terraforming Mars, Dune, Dungeons & Dragons, Exploding Kittens) with turn-based state management. AI opponents use Society of Thought reasoning where multiple cognitive perspectives with distinct personalities debate actions internally before deciding. Each perspective represents different expertise and personality traits based on Big Five model extraction from character lore text.

## Links
- **Source Code**: https://github.com/SamiraSamrose/intelligent-board-games
- **Video Demo**: https://youtu.be/UEFOnoHkMtE
- **Notebooks Complementing The Research Papers**:
[Notebook containing extended research for Societies of Thought Paper](https://github.com/SamiraSamrose/intelligent-board-games/blob/main/notebooks%20complement%20the%20research%20papers/Reasoning%20Models%20Generate%20Societies%20of%20Thought/Comprehensive%20Reviews%20and%20Supplementary%20Research%20on%20%22Reasoning%20Models%20Generate%20Societies%20of%20Thought%22%20%20Research%20Paper.ipynb)
[Notebook containing extended research for Mask or to Mirror Paper](https://github.com/SamiraSamrose/intelligent-board-games/blob/main/notebooks%20complement%20the%20research%20papers/To%20Mask%20or%20to%20Mirror-%20Human-AI%20Alignment%20in%20Collective%20Reasoning/Comprehensive_Reviews_and_Supplementary_Research_on_%22To_Mask_or_to_Mirror_Human_AI_Alignment_in_Collective_Reasoning%22_Research_Paper.ipynb)
- **Research Papaer 1**:"Reasoning Models Generate Societies of Thought" (2025) Research Paper [Read the paper](https://arxiv.org/abs/2601.10825)
- **Research Paper 2**: "To Mask or to Mirror: Human-AI Alignment in Collective Reasoning" Research Paper (2025) [Read the paper](https://deepmind.google/research/publications/180362/)

## Features

### AI Intelligence
- **Society of Thought**: Multi-perspective reasoning with internal debate
- **Character Mimicry**: AI opponents that behave exactly like game characters
- **Nano Banana Pro**: Advanced image generation with advanced reasoning and layout engine
- **Enhanced Learning**: Deep character personality analysis
- **Bias Handling**: Mirror or mask human decision biases

### VR Integration
- **Genie3 Support**: Full VR world generation when Genie3 is available
- **Fallback Mode**: Fully functional 2D gameplay without VR
- **Dynamic Environments**: Real-time 3D board and character rendering
- **Physics Simulation**: Realistic game piece interactions
- **Character Animation**: AI characters animated in VR space

### Games Included
1. **Brass: Birmingham** (4 players) - Industrial era economic strategy
2. **Gloomhaven** (4 players) - Tactical dungeon combat
3. **Terraforming Mars** (5 players) - Planetary development
4. **Dune** (6 players) - Desert planet conquest
5. **Dungeons & Dragons** (6 players) - Fantasy adventure
6. **Exploding Kittens** (5 players) - Chaotic card game

## Installation

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key
- Modern web browser
- 2GB RAM minimum
- 1GB disk space

### Quick Start

1. Clone or download the project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure API key:
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

4. Run the application:
```bash
python start.py
```

5. Open browser to http://localhost:8000

## Configuration

### Environment Variables (.env)

```
GEMINI_API_KEY=your-api-key-here
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=True
CORS_ORIGINS=*
DATABASE_PATH=./data
AI_TEMPERATURE=1.0
AI_MAX_TOKENS=8192
BIAS_MODE=mirror
SOCIETY_PERSPECTIVES=5
LOG_LEVEL=INFO
```

### API Key Setup
1. Visit https://makersuite.google.com/app/apikey
2. Create new API key
3. Copy to .env file

### VR Setup (Optional)
- Genie3 integration is automatic when available
- No additional configuration needed
- Falls back to 2D mode if unavailable

## Usage

### Starting a Game

1. Select game type from dropdown
2. Configure players (human or AI)
3. Choose character for each player
4. Enable VR mode (optional)
5. Click "Start Game"

### Playing

**Human Turn:**
- View available actions in sidebar
- Click action to execute
- Confirm selection

**AI Turn:**
- AI analyzes game state
- Society of thought debates options
- Character mimics personality
- Action executed automatically

### VR Mode

When enabled:
- 3D game world generated
- Characters rendered as 3D models
- Physics-based interactions
- Immersive environment effects

## API Documentation

### REST Endpoints

**Health Check**
```
GET /api/health
Response: { "status": "healthy", "service": "..." }
```

**Create Game**
```
POST /api/games/create
Body: {
  "game_type": "brass_birmingham",
  "players": [...],
  "enable_vr": true
}
Response: { "game_id": "...", "game_state": {...}, "vr_data": {...} }
```

**Get Game State**
```
GET /api/games/<game_id>/state
Response: { "turn": 0, "players": [...], ... }
```

**Get Available Actions**
```
GET /api/games/<game_id>/actions?player_id=0
Response: { "actions": [...] }
```

**Execute Action**
```
POST /api/games/<game_id>/execute
Body: { "player_id": 0, "action": {...} }
Response: { "success": true, ... }
```

**Execute AI Turn**
```
POST /api/games/<game_id>/ai_turn
Body: { "player_id": 1 }
Response: {
  "result": {...},
  "mimic_decision": {...},
  "nano_prediction": {...},
  "society_metrics": {...}
}
```

**Check VR Availability**
```
GET /api/vr/check
Response: { "vr_available": true, "features": {...} }
```

**Update VR World**
```
POST /api/games/<game_id>/vr/update
Body: { "state_changes": {...} }
Response: { "success": true }
```

### WebSocket Events

**Client to Server:**
- `join_game`: Join game room
- `leave_game`: Leave game room

**Server to Client:**
- `joined`: Confirmation of room join
- `left`: Confirmation of room leave
- `game_update`: Game state changed
- `vr_update`: VR world updated

## Research Implementation

### Society of Thought
Based on "Reasoning Models Generate Societies of Thought" paper:
- Creates multiple cognitive perspectives
- Each perspective has distinct personality and expertise
- Internal debate through question-answering
- Perspective shifts and conflict resolution
- Diversity metrics tracking

### Bias Handling
Based on "To Mask or to Mirror" paper:
- **Mirror Mode**: Reproduces human biases faithfully
- **Mask Mode**: Compensates for biases, optimizes outcomes
- Context-dependent alignment
- Demographic cue processing

### Character Learning
- Deep personality extraction from lore
- Big Five personality model
- Tactical preference analysis
- Decision weight calibration
- Behavioral pattern recognition

## Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Change ports in .env
FLASK_PORT=5001
# Then run: python start.py
```

**API Key Invalid**
```bash
# Verify key in .env
# Get new key from https://makersuite.google.com/app/apikey
```

**Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**VR Not Available**
- Normal behavior if Genie3 not accessible
- Game functions fully in 2D mode
- Check logs for Genie3 connection status

### Logs

Logs are written to:
- Console output
- `logs/` directory (if created)

## Performance

### System Requirements
- **Minimum**: 2GB RAM, 2 CPU cores
- **Recommended**: 4GB RAM, 4 CPU cores
- **VR Mode**: 8GB RAM, dedicated GPU

### Optimization
- AI reasoning cached per character
- Game state stored in memory
- WebSocket for real-time updates
- Lazy loading of VR assets

## Development

### Running Tests
```bash
python test_integration.py
```

### Adding New Games
1. Create game class in `backend/games/`
2. Implement required methods
3. Add to `GameFactory`
4. Create character lore
5. Test integration

### Custom Characters
1. Add lore to `_get_detailed_character_lore()`
2. Train with `enhanced_learning.deep_learn_character()`
3. Test personality mimicry

## Contributing

This is a research implementation demonstrating AI techniques from academic papers.

## Credits

Research Papers:
- "Reasoning Models Generate Societies of Thought" (2025) [Read](https://arxiv.org/abs/2601.10825)
- "To Mask or to Mirror: Human-AI Alignment in Collective Reasoning" (2025) Read](https://deepmind.google/research/publications/180362/)


Technologies:
- Google Gemini AI
- Genie3 VR (when available)
- Flask + SocketIO
- HTML5 Canvas