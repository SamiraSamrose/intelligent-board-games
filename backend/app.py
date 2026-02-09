from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
import asyncio
from functools import wraps

from models.society_of_thought import SocietyOfThought
from models.persona_system import PersonaSystem
from models.bias_masking import BiasMasking
from models.collective_reasoning import CollectiveReasoning
from ai.gemini_controller import GeminiController
from ai.character_trainer import CharacterTrainer
from ai.decision_engine import DecisionEngine
from ai.nano_banana_pro import NanoBananaPro
from ai.enhanced_character_learning import EnhancedCharacterLearning
from ai.character_mimicry import CharacterMimicry
from ai.genie3_integration import Genie3Integration
from ai.vr_scenario_generator import VRScenarioGenerator
from utils.game_factory import GameFactory
from database.character_profiles import CharacterProfileDatabase
from database.game_state import GameStateDatabase

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

API_KEY = os.getenv("GEMINI_API_KEY", "your-api-key-here")

society_of_thought = SocietyOfThought(API_KEY)
persona_system = PersonaSystem(API_KEY)
bias_masking = BiasMasking(API_KEY, mode='mirror')
collective_reasoning = CollectiveReasoning(society_of_thought, persona_system, bias_masking)
gemini_controller = GeminiController(API_KEY)
character_trainer = CharacterTrainer(API_KEY)
decision_engine = DecisionEngine(collective_reasoning, character_trainer)

nano_banana_pro = NanoBananaPro()
enhanced_learning = EnhancedCharacterLearning(API_KEY, nano_banana_pro)
character_mimicry = CharacterMimicry(API_KEY, enhanced_learning)

genie3_integration = Genie3Integration(API_KEY)
vr_scenario_generator = VRScenarioGenerator(API_KEY, genie3_integration)

character_db = CharacterProfileDatabase()
game_state_db = GameStateDatabase()

active_games = {}
vr_sessions = {}

def async_route(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapped

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "Intelligent Board Games API"})

@app.route('/api/vr/check', methods=['GET'])
@async_route
async def check_vr_availability():
    available = await genie3_integration.check_genie3_availability()
    
    return jsonify({
        "vr_available": available,
        "genie3_status": "active" if available else "unavailable",
        "features": {
            "world_generation": available,
            "character_models": available,
            "physics_simulation": available,
            "real_time_rendering": available
        }
    })

@app.route('/api/games/create', methods=['POST'])
@async_route
async def create_game():
    data = request.json
    game_type = data.get('game_type')
    player_configs = data.get('players', [])
    game_id = data.get('game_id', f"game_{len(active_games)}")
    enable_vr = data.get('enable_vr', False)
    
    try:
        game_instance = GameFactory.create_game(game_type)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    game_state = game_instance.setup_game(player_configs)
    
    active_games[game_id] = {
        "game_type": game_type,
        "instance": game_instance,
        "players": player_configs,
        "vr_enabled": enable_vr
    }
    
    game_state_db.save_game_state(game_id, game_type, game_state)
    
    vr_data = None
    if enable_vr and await genie3_integration.check_genie3_availability():
        vr_world = await genie3_integration.create_vr_world(game_type, game_state)
        
        board_layout = await vr_scenario_generator.generate_board_layout_3d(
            game_type,
            game_state.get('board', {})
        )
        
        vr_data = {
            'world': vr_world,
            'board_layout': board_layout,
            'characters': [],
            'assets': []
        }
    
    for idx, config in enumerate(player_configs):
        if config.get('is_ai', False):
            character_name = config.get('character', config.get('name'))
            
            source_material = await _get_detailed_character_lore(game_type, character_name)
            
            character_data = await enhanced_learning.deep_learn_character(
                game_type,
                character_name,
                source_material
            )
            
            persona_system.create_character_persona(character_name, character_data)
            
            society_of_thought.create_perspective(
                personality_traits=character_data['personality'],
                expertise=character_data.get('tactical_preferences', ['general'])[0] if character_data.get('tactical_preferences') else 'general',
                role='primary'
            )
            
            character_db.store_character_profile(game_type, character_name, character_data)
            
            if enable_vr and vr_data:
                vr_character = await genie3_integration.create_vr_character(
                    game_type,
                    character_name,
                    character_data
                )
                
                if vr_character:
                    vr_data['characters'].append(vr_character)
    
    if vr_data:
        vr_sessions[game_id] = vr_data
    
    return jsonify({
        "game_id": game_id,
        "game_state": game_state,
        "vr_data": vr_data,
        "message": "Game created successfully"
    })

async def _get_detailed_character_lore(game_type: str, character_name: str):
    lore_database = {
        "brass_birmingham": {
            "default": [
                "Industrial entrepreneur in Victorian Birmingham during the Industrial Revolution",
                "Focused on building canal and rail networks across the Midlands",
                "Establishes cotton mills, coal mines, iron works, breweries, and potteries",
                "Strategic thinker who balances short-term profits with long-term infrastructure",
                "Competitive but recognizes value of economic cooperation",
                "Values efficiency and careful resource management",
                "Adapts strategy based on available transportation networks",
                "Prioritizes industries that generate income over those that score points immediately"
            ]
        },
        "gloomhaven": {
            "brute": [
                "Inox warrior standing over 7 feet tall with incredible physical strength",
                "Charges into battle without hesitation, leading the front line",
                "Impatient with complex planning, prefers direct action",
                "Loyal to companions who prove themselves in combat",
                "Uses massive weapons and overwhelming force",
                "Protective of weaker party members despite gruff exterior",
                "Dislikes magic and prefers physical solutions",
                "Values honor and straightforward dealings"
            ],
            "tinkerer": [
                "Quatryl inventor barely 3 feet tall with boundless creativity",
                "Creates gadgets, traps, and healing devices",
                "Analytical problem-solver who thinks several steps ahead",
                "Cautious in combat, preferring to support from range",
                "Curious about magical and mechanical phenomena",
                "Patient teacher who explains complex concepts",
                "Values knowledge and innovation over brute force",
                "Often underestimated due to small stature"
            ],
            "spellweaver": [
                "Orchid mage wielding devastating elemental magic",
                "Calculating and precise in spell selection",
                "Balances offensive power with defensive positioning",
                "Values efficiency and optimal resource use",
                "Detached and logical in emotional situations",
                "Respects those who demonstrate tactical intelligence",
                "Fragile physically but immensely powerful magically",
                "Plans around elemental combinations"
            ],
            "scoundrel": [
                "Human rogue skilled in stealth and deception",
                "Opportunistic and treasure-focused",
                "Strikes from shadows with poisoned daggers",
                "Quick-witted and adaptable to changing situations",
                "Distrusts authority and formal structures",
                "Values personal freedom and independence",
                "Willing to take risks for high rewards",
                "Charismatic but keeps emotional distance"
            ],
            "ranger": [
                "Skilled tracker and archer from wilderness regions",
                "Patient observer who gathers information before acting",
                "Methodical in approach to problems",
                "Prefers ranged combat to avoid direct confrontation",
                "Values nature and survival skills",
                "Self-reliant and comfortable alone",
                "Careful planner who considers all angles",
                "Loyal once trust is established"
            ]
        },
        "terraforming_mars": {
            "Credicor": [
                "Banking corporation focused on financial efficiency and credit systems",
                "Conservative in spending, opportunistic in investments",
                "Values economic dominance and market control",
                "Patient strategy, willing to wait for optimal returns",
                "Prefers cards that generate ongoing megacredit income",
                "Risk-averse in early game, aggressive in late game",
                "Builds engine before pushing terraforming parameters",
                "Diplomatic when beneficial, competitive when necessary"
            ],
            "Ecoline": [
                "Environmental specialists focused on plant life and oxygen production",
                "Idealistic about terraforming and ecological balance",
                "Values greenery placement and oxygen generation",
                "Aggressive in claiming areas with plant potential",
                "Cooperative with other green-focused corporations",
                "Long-term thinker about planetary development",
                "Sees Mars terraforming as environmental restoration",
                "Willing to sacrifice short-term gains for ecological goals"
            ],
            "Helion": [
                "Energy corporation specializing in heat and power production",
                "Aggressive in development and temperature increase",
                "Values heat resources and energy production",
                "Quick to act and push game tempo",
                "Competitive and willing to take risks",
                "Focuses on temperature track for fast terraforming rating",
                "Sees Mars as energy resource to be exploited",
                "Direct and confrontational in playstyle"
            ],
            "Mining Guild": [
                "Resource extraction specialists focused on steel and titanium",
                "Pragmatic and focused on industrial expansion",
                "Values asteroid and space projects",
                "Aggressive in claiming mining rights",
                "Builds strong production engine early",
                "Cooperative with other industrial corporations",
                "Sees Mars as resource cache to be mined",
                "Efficient and cost-conscious in operations"
            ],
            "Tharsis Republic": [
                "City builders focused on urban development and infrastructure",
                "Diplomatic and values trade networks",
                "Prefers city placement and adjacency bonuses",
                "Balanced approach to all terraforming parameters",
                "Cooperative and seeks mutually beneficial arrangements",
                "Long-term planner focused on victory points",
                "Sees Mars as future human civilization",
                "Values stability and measured progress"
            ]
        },
        "dune": {
            "atreides": [
                "House Atreides led by Duke Leto, noble and honorable rulers",
                "Paul Atreides possesses prescient visions of possible futures",
                "Values loyalty, justice, and honorable conduct",
                "Strategic thinkers who plan multiple moves ahead",
                "Respected for fair dealing and keeping promises",
                "Military strength through discipline and leadership",
                "Special ability: Prescience lets them see battle plans",
                "Seeks to win through legitimacy and popular support"
            ],
            "harkonnen": [
                "House Harkonnen led by Baron Vladimir, ruthless and treacherous",
                "Values power and control through any means necessary",
                "Deceptive and willing to betray alliances",
                "Brutal military force and economic oppression",
                "Special ability: Can use more treachery cards",
                "Seeks to win through manipulation and force",
                "Views honor as weakness to be exploited",
                "Patient in planning elaborate betrayals"
            ],
            "emperor": [
                "Emperor Shaddam IV backed by fearsome Sardaukar troops",
                "Values order, control, and imperial authority",
                "Politically shrewd and manipulative",
                "Special ability: Sardaukar worth double strength",
                "Balances power between other factions",
                "Seeks to maintain imperial dominance",
                "Uses wealth and military might",
                "Views Arrakis as tool for controlling spice economy"
            ],
            "guild": [
                "Spacing Guild controls all interstellar travel",
                "Neutral but profit-driven merchants",
                "Values spice above all else for navigation",
                "Special ability: Free and unlimited shipment",
                "Plays factions against each other for profit",
                "Patient and willing to wait for best deals",
                "Threatens to cut off transportation",
                "Seeks economic victory through spice monopoly"
            ],
            "bene_gesserit": [
                "Mystical sisterhood with centuries-long plans",
                "Patient, manipulative, values long-term goals",
                "Special ability: Voice allows forcing opponent actions",
                "Predicts winner and turn for victory condition",
                "Uses subtle influence over direct force",
                "Values information and secrets",
                "Appears weak but wields hidden power",
                "Seeks to guide humanity evolution"
            ],
            "fremen": [
                "Desert warriors native to Arrakis, masters of desert survival",
                "Fierce, independent, and resourceful",
                "Special ability: Free desert movement, bonus strength in storms",
                "Values water and freedom above all",
                "Expert guerrilla fighters",
                "Underestimated by off-worlders",
                "Prophesied to follow a messiah Paul",
                "Seeks to reclaim Arrakis from oppressors"
            ]
        },
        "dungeons_dragons": {
            "fighter": [
                "Disciplined warrior trained in martial combat and tactics",
                "Brave and protective of allies in dangerous situations",
                "Values honor, strength, and martial prowess",
                "Direct problem-solver who prefers action",
                "Loyal to companions and code of conduct",
                "Respects worthy opponents and fair combat",
                "Tactical thinker in battle situations",
                "Confident in physical abilities, less so in social situations"
            ],
            "wizard": [
                "Scholarly mage who studied arcane arts for years",
                "Intellectual and cautious, values knowledge",
                "Prefers preparation and planning over improvisation",
                "Curious about magical phenomena and ancient lore",
                "Physically vulnerable, relies on intelligence",
                "Values books and research over physical training",
                "Methodical problem-solver using magical solutions",
                "Respects intelligence and magical skill"
            ],
            "rogue": [
                "Cunning expert in stealth, traps, and deception",
                "Opportunistic and treasure-focused",
                "Quick-thinking and adaptable to situations",
                "Distrusts authority and formal structures",
                "Values personal freedom and independence",
                "Willing to take risks for rewards",
                "Prefers avoiding combat when possible",
                "Loyal to proven friends despite cynical exterior"
            ],
            "cleric": [
                "Divine servant channeling deity power for healing and protection",
                "Compassionate and protective of others",
                "Values life, healing, and supporting allies",
                "Strategic in using limited divine magic",
                "Strong moral compass based on deity teachings",
                "Brave when protecting others despite fear",
                "Diplomatic and seeks peaceful solutions",
                "Balances offensive and defensive capabilities"
            ],
            "ranger": [
                "Wilderness expert and skilled tracker",
                "Patient observer who gathers information",
                "Self-reliant and comfortable in isolation",
                "Values nature and natural order",
                "Methodical in approach to challenges",
                "Loyal once trust is established",
                "Prefers ranged combat and tactics",
                "Quiet but knowledgeable about survival"
            ]
        },
        "exploding_kittens": {
            "default": [
                "Chaotic player who embraces randomness and risk",
                "Opportunistic and adapts quickly to changing circumstances",
                "Values survival and creating chaos for opponents",
                "Willing to take calculated risks with deck probabilities",
                "Enjoys psychological warfare and bluffing",
                "Balances aggression with self-preservation",
                "Watches opponents behavior for tells",
                "Strategic about when to use powerful cards"
            ]
        }
    }
    
    game_lore = lore_database.get(game_type, {})
    character_lore = game_lore.get(character_name, game_lore.get('default', ['Generic player']))
    
    return character_lore

@app.route('/api/games/<game_id>/vr/update', methods=['POST'])
@async_route
async def update_vr_world(game_id):
    if game_id not in active_games:
        return jsonify({"error": "Game not found"}), 404
    
    game_data = active_games[game_id]
    
    if not game_data.get('vr_enabled'):
        return jsonify({"error": "VR not enabled for this game"}), 400
    
    data = request.json
    state_changes = data.get('state_changes', {})
    
    game_type = game_data['game_type']
    
    success = await genie3_integration.update_vr_world_state(game_type, state_changes)
    
    if success:
        socketio.emit('vr_update', {
            "game_id": game_id,
            "changes": state_changes
        }, room=game_id)
    
    return jsonify({"success": success})

@app.route('/api/games/<game_id>/vr/session', methods=['GET'])
def get_vr_session(game_id):
    if game_id not in active_games:
        return jsonify({"error": "Game not found"}), 404
    
    game_data = active_games[game_id]
    game_type = game_data['game_type']
    
    vr_data = genie3_integration.get_vr_session_data(game_type)
    
    return jsonify({
        "game_id": game_id,
        "vr_session": vr_data,
        "vr_enabled": game_data.get('vr_enabled', False)
    })

@app.route('/api/games/<game_id>/ai_turn', methods=['POST'])
@async_route
async def execute_ai_turn(game_id):
    if game_id not in active_games:
        return jsonify({"error": "Game not found"}), 404
    
    data = request.json
    ai_player_id = data.get('player_id')
    
    game_data = active_games[game_id]
    game_instance = game_data["instance"]
    game_type = game_data["game_type"]
    
    game_state = game_instance.get_game_state()
    available_actions = game_instance.get_available_actions(ai_player_id)
    
    player_config = game_data["players"][ai_player_id]
    character_name = player_config.get('character', player_config.get('name'))
    
    mimic_decision = await character_mimicry.mimic_character_decision(
        game_type,
        character_name,
        game_state,
        available_actions
    )
    
    nano_prediction = await nano_banana_pro.predict_action(
        character_name,
        game_type,
        available_actions,
        game_state
    )
    
    society_decision = await decision_engine.process_turn(
        game_name=game_type,
        game_state=game_state,
        ai_character=character_name,
        available_actions=available_actions
    )
    
    final_action = mimic_decision.get('action')
    
    result = game_instance.execute_action(ai_player_id, final_action)
    
    if result.get('success'):
        new_state = game_instance.get_game_state()
        game_state_db.save_game_state(game_id, game_type, new_state)
        
        character_db.update_performance_metrics(
            game_type,
            character_name,
            {
                "decisions_made": 1,
                "successful_outcomes": 1
            }
        )
        
        dialogue = await character_mimicry.generate_character_dialogue(
            game_type,
            character_name,
            f"Just executed: {final_action.get('description', 'action')}"
        )
        
        if game_data.get('vr_enabled'):
            await genie3_integration.animate_character_action(
                game_type,
                character_name,
                final_action.get('type', 'action'),
                {'target': final_action}
            )
        
        socketio.emit('game_update', {
            "game_id": game_id,
            "state": new_state,
            "last_action": result,
            "ai_reasoning": mimic_decision.get('reasoning'),
            "character_quote": mimic_decision.get('in_character_quote'),
            "dialogue": dialogue,
            "nano_confidence": nano_prediction.get('confidence'),
            "society_reasoning": society_decision.get('society_reasoning')
        }, room=game_id)
    
    return jsonify({
        "result": result,
        "mimic_decision": mimic_decision,
        "nano_prediction": nano_prediction,
        "society_metrics": society_decision.get('diversity_metrics')
    })

@app.route('/api/games/<game_id>/state', methods=['GET'])
def get_game_state(game_id):
    if game_id not in active_games:
        return jsonify({"error": "Game not found"}), 404
    
    game_instance = active_games[game_id]["instance"]
    state = game_instance.get_game_state()
    
    return jsonify(state)

@app.route('/api/games/<game_id>/actions', methods=['GET'])
def get_available_actions(game_id):
    if game_id not in active_games:
        return jsonify({"error": "Game not found"}), 404
    
    player_id = int(request.args.get('player_id', 0))
    
    game_instance = active_games[game_id]["instance"]
    actions = game_instance.get_available_actions(player_id)
    
    return jsonify({"actions": actions})

@app.route('/api/games/<game_id>/execute', methods=['POST'])
@async_route
async def execute_action(game_id):
    if game_id not in active_games:
        return jsonify({"error": "Game not found"}), 404
    
    data = request.json
    player_id = data.get('player_id')
    action = data.get('action')
    
    game_data = active_games[game_id]
    game_instance = game_data["instance"]
    
    result = game_instance.execute_action(player_id, action)
    
    if result.get('success'):
        new_state = game_instance.get_game_state()
        game_state_db.save_game_state(game_id, game_data["game_type"], new_state)
        
        if game_data.get('vr_enabled'):
            await genie3_integration.update_vr_world_state(
                game_data["game_type"],
                {'action_executed': action, 'new_state': new_state}
            )
        
        socketio.emit('game_update', {
            "game_id": game_id,
            "state": new_state,
            "last_action": result
        }, room=game_id)
    
    return jsonify(result)

@socketio.on('join_game')
def handle_join_game(data):
    game_id = data.get('game_id')
    join_room(game_id)
    emit('joined', {"game_id": game_id})

@socketio.on('leave_game')
def handle_leave_game(data):
    game_id = data.get('game_id')
    leave_room(game_id)
    emit('left', {"game_id": game_id})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)