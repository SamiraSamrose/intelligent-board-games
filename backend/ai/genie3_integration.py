import google.generativeai as genai
from typing import Dict, List, Optional
import asyncio
import json
import base64
import requests

class Genie3Integration:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.genie3_available = False
        self.genie3_endpoint = "https://generativeplaygrounds.googleapis.com/v1/genie3"
        self.api_key = api_key
        self.generated_worlds = {}
        self.generated_characters = {}
        self.generated_assets = {}
        
    async def check_genie3_availability(self) -> bool:
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = await asyncio.to_thread(
                requests.get,
                f"{self.genie3_endpoint}/status",
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                self.genie3_available = True
                return True
                
        except Exception as e:
            print(f"Genie3 not available: {e}")
        
        self.genie3_available = False
        return False
    
    async def generate_game_world_prompt(self, game_type: str, game_state: Dict) -> str:
        world_generation_prompt = f"""Generate a detailed 3D world description for {game_type} that Genie3 can use to create an interactive VR environment.

Current game state:
{json.dumps(game_state, indent=2)}

Create comprehensive world description including:

1. ENVIRONMENT LAYOUT:
   - Spatial dimensions and boundaries
   - Terrain types and elevations
   - Lighting conditions and atmosphere
   - Weather and environmental effects
   - Key landmarks and structures

2. PHYSICAL PROPERTIES:
   - Gravity and physics rules
   - Material properties (wood, metal, stone)
   - Interactive elements and mechanics
   - Collision boundaries
   - Movement constraints

3. VISUAL AESTHETICS:
   - Art style (realistic, stylized, fantasy)
   - Color palette and mood
   - Texture details
   - Particle effects
   - Visual feedback for actions

4. INTERACTIVE ZONES:
   - Player spawn points
   - Action areas (building, combat, resource gathering)
   - Restricted zones
   - Transition areas

5. AUDIO ENVIRONMENT:
   - Ambient sounds
   - Environmental audio cues
   - Music themes
   - Sound effects for interactions

Format as detailed JSON for Genie3 world generation API."""

        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                world_generation_prompt
            )
            
            return response.text
            
        except Exception as e:
            return self._get_fallback_world_prompt(game_type)
    
    async def generate_character_model_prompt(self, game_type: str, 
                                             character_name: str,
                                             character_data: Dict) -> str:
        character_prompt = f"""Generate detailed 3D character model specifications for {character_name} in {game_type} for Genie3 VR rendering.

Character profile:
{json.dumps(character_data, indent=2)}

Create comprehensive character description including:

1. PHYSICAL APPEARANCE:
   - Height, build, proportions
   - Facial features and expressions
   - Hair style, color, and physics
   - Skin tone and textures
   - Distinctive markings or scars

2. CLOTHING AND EQUIPMENT:
   - Outfit design and materials
   - Armor or protective gear
   - Weapons and tools
   - Accessories and ornaments
   - Cloth physics and dynamics

3. ANIMATION RIGGING:
   - Skeletal structure
   - Joint positions and constraints
   - IK (inverse kinematics) setups
   - Facial blend shapes
   - Animation states (idle, walk, run, attack, defend)

4. PERSONALITY VISUALIZATION:
   - Posture and stance
   - Gesture patterns
   - Movement style (aggressive, cautious, graceful)
   - Idle animations
   - Reaction animations

5. SPECIAL EFFECTS:
   - Magical auras or energy
   - Particle effects
   - Trail effects for movement
   - Combat visual feedback
   - Status indicators

6. VOICE AND AUDIO:
   - Voice type and tone
   - Signature sounds
   - Footstep sounds
   - Combat grunts and exclamations
   - Dialogue style

Format as detailed JSON for Genie3 character generation API."""

        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                character_prompt
            )
            
            return response.text
            
        except Exception as e:
            return self._get_fallback_character_prompt(character_name)
    
    async def generate_game_asset_prompt(self, game_type: str, 
                                        asset_type: str,
                                        asset_context: Dict) -> str:
        asset_prompt = f"""Generate detailed 3D asset specifications for {asset_type} in {game_type} for Genie3 VR environment.

Asset context:
{json.dumps(asset_context, indent=2)}

Create comprehensive asset description including:

1. VISUAL DESIGN:
   - Shape and dimensions
   - Material composition
   - Surface textures
   - Color scheme
   - Level of detail (LOD) specifications

2. FUNCTIONALITY:
   - Interactive elements
   - Movement mechanics
   - State changes (open/closed, active/inactive)
   - Trigger zones
   - Feedback mechanisms

3. PHYSICS PROPERTIES:
   - Mass and weight
   - Collision meshes
   - Breakability
   - Physics reactions
   - Constraints

4. VISUAL EFFECTS:
   - Shader properties
   - Emission and glow
   - Particle systems
   - Animation loops
   - Environmental interactions

5. AUDIO DESIGN:
   - Interaction sounds
   - Ambient audio
   - State change sounds
   - Material-specific sounds

Format as detailed JSON for Genie3 asset generation API."""

        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                asset_prompt
            )
            
            return response.text
            
        except Exception as e:
            return self._get_fallback_asset_prompt(asset_type)
    
    async def create_vr_world(self, game_type: str, game_state: Dict) -> Optional[Dict]:
        if not self.genie3_available:
            return None
        
        world_prompt = await self.generate_game_world_prompt(game_type, game_state)
        
        try:
            parsed_prompt = self._parse_json_from_text(world_prompt)
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'world_description': parsed_prompt,
                'game_type': game_type,
                'physics_engine': 'realistic',
                'render_quality': 'high',
                'vr_optimized': True
            }
            
            response = await asyncio.to_thread(
                requests.post,
                f"{self.genie3_endpoint}/worlds/create",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                world_data = response.json()
                world_id = world_data.get('world_id')
                
                self.generated_worlds[game_type] = world_data
                
                return world_data
            
        except Exception as e:
            print(f"Error creating VR world: {e}")
        
        return None
    
    async def create_vr_character(self, game_type: str, character_name: str,
                                 character_data: Dict) -> Optional[Dict]:
        if not self.genie3_available:
            return None
        
        character_prompt = await self.generate_character_model_prompt(
            game_type,
            character_name,
            character_data
        )
        
        try:
            parsed_prompt = self._parse_json_from_text(character_prompt)
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'character_description': parsed_prompt,
                'game_type': game_type,
                'character_name': character_name,
                'animation_set': 'complete',
                'vr_optimized': True
            }
            
            response = await asyncio.to_thread(
                requests.post,
                f"{self.genie3_endpoint}/characters/create",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                character_model = response.json()
                
                key = f"{game_type}_{character_name}"
                self.generated_characters[key] = character_model
                
                return character_model
            
        except Exception as e:
            print(f"Error creating VR character: {e}")
        
        return None
    
    async def create_vr_asset(self, game_type: str, asset_type: str,
                             asset_context: Dict) -> Optional[Dict]:
        if not self.genie3_available:
            return None
        
        asset_prompt = await self.generate_game_asset_prompt(
            game_type,
            asset_type,
            asset_context
        )
        
        try:
            parsed_prompt = self._parse_json_from_text(asset_prompt)
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'asset_description': parsed_prompt,
                'game_type': game_type,
                'asset_type': asset_type,
                'vr_optimized': True
            }
            
            response = await asyncio.to_thread(
                requests.post,
                f"{self.genie3_endpoint}/assets/create",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                asset_data = response.json()
                
                key = f"{game_type}_{asset_type}"
                self.generated_assets[key] = asset_data
                
                return asset_data
            
        except Exception as e:
            print(f"Error creating VR asset: {e}")
        
        return None
    
    async def update_vr_world_state(self, game_type: str, 
                                   game_state_changes: Dict) -> bool:
        if not self.genie3_available:
            return False
        
        if game_type not in self.generated_worlds:
            return False
        
        world_data = self.generated_worlds[game_type]
        world_id = world_data.get('world_id')
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'world_id': world_id,
                'state_changes': game_state_changes
            }
            
            response = await asyncio.to_thread(
                requests.post,
                f"{self.genie3_endpoint}/worlds/{world_id}/update",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"Error updating VR world: {e}")
            return False
    
    async def animate_character_action(self, game_type: str, character_name: str,
                                      action: str, parameters: Dict) -> bool:
        if not self.genie3_available:
            return False
        
        key = f"{game_type}_{character_name}"
        if key not in self.generated_characters:
            return False
        
        character_data = self.generated_characters[key]
        character_id = character_data.get('character_id')
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'character_id': character_id,
                'action': action,
                'parameters': parameters
            }
            
            response = await asyncio.to_thread(
                requests.post,
                f"{self.genie3_endpoint}/characters/{character_id}/animate",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"Error animating character: {e}")
            return False
    
    def _parse_json_from_text(self, text: str) -> Dict:
        try:
            import re
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception:
            pass
        
        return {
            'raw_description': text,
            'parsing_failed': True
        }
    
    def _get_fallback_world_prompt(self, game_type: str) -> str:
        fallbacks = {
            'brass_birmingham': {
                'environment': 'Victorian industrial city with canal networks',
                'atmosphere': 'Smoky, industrial, busy',
                'key_features': ['canals', 'factories', 'rail stations']
            },
            'gloomhaven': {
                'environment': 'Dark fantasy dungeon with stone corridors',
                'atmosphere': 'Ominous, mysterious, dangerous',
                'key_features': ['torch-lit passages', 'monster lairs', 'treasure chests']
            },
            'terraforming_mars': {
                'environment': 'Red martian landscape with settlements',
                'atmosphere': 'Barren, hostile, futuristic',
                'key_features': ['domed cities', 'mining operations', 'terraforming stations']
            },
            'dune': {
                'environment': 'Vast desert with sandworms and spice',
                'atmosphere': 'Harsh, majestic, dangerous',
                'key_features': ['sand dunes', 'rock outcroppings', 'spice deposits']
            },
            'dungeons_dragons': {
                'environment': 'Medieval fantasy dungeon',
                'atmosphere': 'Ancient, magical, perilous',
                'key_features': ['stone rooms', 'traps', 'magical artifacts']
            },
            'exploding_kittens': {
                'environment': 'Colorful chaotic cartoon world',
                'atmosphere': 'Whimsical, explosive, unpredictable',
                'key_features': ['card stacks', 'kitten animations', 'explosion effects']
            }
        }
        
        return json.dumps(fallbacks.get(game_type, {}))
    
    def _get_fallback_character_prompt(self, character_name: str) -> str:
        return json.dumps({
            'name': character_name,
            'appearance': 'Standard humanoid form',
            'animations': ['idle', 'walk', 'run', 'action']
        })
    
    def _get_fallback_asset_prompt(self, asset_type: str) -> str:
        return json.dumps({
            'type': asset_type,
            'visual': 'Standard game asset',
            'interactive': True
        })
    
    def get_vr_session_data(self, game_type: str) -> Dict:
        return {
            'genie3_available': self.genie3_available,
            'world': self.generated_worlds.get(game_type),
            'characters': {k: v for k, v in self.generated_characters.items() if k.startswith(game_type)},
            'assets': {k: v for k, v in self.generated_assets.items() if k.startswith(game_type)}
        }