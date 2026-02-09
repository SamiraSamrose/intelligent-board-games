import google.generativeai as genai
from typing import Dict, List
import asyncio
import json

class VRScenarioGenerator:
    def __init__(self, api_key: str, genie3_integration):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.genie3 = genie3_integration
        
    async def generate_board_layout_3d(self, game_type: str, 
                                      board_data: Dict) -> Dict:
        layout_prompt = f"""Generate detailed 3D board layout for {game_type} in VR space.

Board data:
{json.dumps(board_data, indent=2)}

Create comprehensive 3D layout including:

1. SPATIAL ARRANGEMENT:
   - Board dimensions (width, height, depth in meters)
   - Tile/space positions in 3D coordinates
   - Elevation levels
   - Player viewing angles
   - Optimal camera positions

2. TILE SPECIFICATIONS:
   - Tile size and shape
   - Height variations
   - Border designs
   - Connection pathways
   - Interactive zones

3. VISUAL MARKERS:
   - Resource indicators
   - Territory boundaries
   - Movement paths
   - Action zones
   - Player positions

4. INTERACTIVE ELEMENTS:
   - Clickable areas
   - Hover effects
   - Selection highlights
   - Drag-and-drop zones
   - Animation triggers

5. VR OPTIMIZATION:
   - Hand-reach zones
   - Gaze-interaction points
   - Comfort zones for players
   - Scale adjustments
   - Accessibility features

Return as JSON with precise 3D coordinates and specifications."""

        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                layout_prompt
            )
            
            layout_data = self._parse_json_response(response.text)
            
            if self.genie3.genie3_available:
                await self.genie3.create_vr_asset(
                    game_type,
                    'game_board',
                    layout_data
                )
            
            return layout_data
            
        except Exception as e:
            return self._get_default_board_layout(game_type)
    
    async def generate_card_3d_model(self, game_type: str, 
                                    card_data: Dict) -> Dict:
        card_prompt = f"""Generate detailed 3D card model for {game_type} VR environment.

Card data:
{json.dumps(card_data, indent=2)}

Create comprehensive card specifications:

1. PHYSICAL PROPERTIES:
   - Card dimensions (standard: 63mm x 88mm, thickness: 0.3mm)
   - Material appearance (matte, glossy, textured)
   - Weight and physics behavior
   - Flexibility and bend characteristics

2. FRONT FACE DESIGN:
   - Artwork placement and size
   - Text layout and readability in VR
   - Icon positions
   - Border design
   - Foil or special effects

3. BACK FACE DESIGN:
   - Pattern or artwork
   - Logo placement
   - Color scheme
   - Distinguishing features

4. INTERACTIVE FEATURES:
   - Hover magnification
   - Flip animation
   - Glow effects when playable
   - Hand tracking for holding
   - Gesture recognition

5. VR BEHAVIORS:
   - How card floats when selected
   - Snap-to positions
   - Stack behavior
   - Shuffle animation
   - Deal animation

Return as JSON with 3D model specifications."""

        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                card_prompt
            )
            
            card_model = self._parse_json_response(response.text)
            
            if self.genie3.genie3_available:
                await self.genie3.create_vr_asset(
                    game_type,
                    f"card_{card_data.get('id', 'unknown')}",
                    card_model
                )
            
            return card_model
            
        except Exception as e:
            return self._get_default_card_model()
    
    async def generate_game_piece_3d(self, game_type: str,
                                    piece_type: str,
                                    piece_data: Dict) -> Dict:
        piece_prompt = f"""Generate detailed 3D game piece for {game_type} VR environment.

Piece type: {piece_type}
Piece data:
{json.dumps(piece_data, indent=2)}

Create comprehensive piece specifications:

1. SHAPE AND SIZE:
   - Base shape (cube, cylinder, custom)
   - Dimensions in centimeters
   - Weight in grams (for physics)
   - Center of mass

2. APPEARANCE:
   - Material (wood, plastic, metal, crystal)
   - Color and finish
   - Textures and patterns
   - Player-specific markings
   - Level or value indicators

3. PHYSICS:
   - Collision mesh
   - Friction coefficients
   - Bounciness
   - Stability on surfaces
   - Stacking behavior

4. INTERACTIONS:
   - Grab points
   - Rotation constraints
   - Snap-to-grid behavior
   - Combination with other pieces
   - State changes (flipped, rotated)

5. VR FEATURES:
   - Haptic feedback patterns
   - Audio cues on pickup/place
   - Trail effects during movement
   - Highlight when selectable
   - Preview of valid placements

Return as JSON with complete 3D specifications."""

        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                piece_prompt
            )
            
            piece_model = self._parse_json_response(response.text)
            
            if self.genie3.genie3_available:
                await self.genie3.create_vr_asset(
                    game_type,
                    f"piece_{piece_type}",
                    piece_model
                )
            
            return piece_model
            
        except Exception as e:
            return self._get_default_piece_model(piece_type)
    
    async def generate_environment_effects(self, game_type: str,
                                          game_state: Dict) -> Dict:
        effects_prompt = f"""Generate environmental effects for {game_type} VR experience.

Game state:
{json.dumps(game_state, indent=2)}

Create comprehensive environmental effects:

1. ATMOSPHERIC EFFECTS:
   - Fog or mist
   - Dust particles
   - Steam or smoke
   - Weather effects
   - Time-of-day lighting

2. AMBIENT ANIMATIONS:
   - Flickering lights
   - Flowing water
   - Waving flags
   - Moving clouds
   - Rustling vegetation

3. PARTICLE SYSTEMS:
   - Magic effects
   - Explosions
   - Sparkles and glows
   - Debris and destruction
   - Energy fields

4. AUDIO LANDSCAPE:
   - Ambient background music
   - Environmental sounds
   - Distance-based audio falloff
   - Reverb and echo zones
   - Dynamic music based on game state

5. REACTIVE ELEMENTS:
   - Effects triggered by player actions
   - State-change animations
   - Victory/defeat sequences
   - Turn transition effects
   - Warning indicators

Return as JSON with effect specifications."""

        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                effects_prompt
            )
            
            effects_data = self._parse_json_response(response.text)
            
            return effects_data
            
        except Exception as e:
            return {'effects': []}
    
    def _parse_json_response(self, text: str) -> Dict:
        try:
            import re
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception:
            pass
        
        return {'raw_text': text}
    
    def _get_default_board_layout(self, game_type: str) -> Dict:
        return {
            'dimensions': {'width': 2.0, 'height': 0.1, 'depth': 2.0},
            'tiles': [],
            'center': {'x': 0, 'y': 0, 'z': 0}
        }
    
    def _get_default_card_model(self) -> Dict:
        return {
            'dimensions': {'width': 0.063, 'height': 0.088, 'depth': 0.0003},
            'material': 'cardboard',
            'interactive': True
        }
    
    def _get_default_piece_model(self, piece_type: str) -> Dict:
        return {
            'type': piece_type,
            'shape': 'cylinder',
            'dimensions': {'radius': 0.01, 'height': 0.02},
            'material': 'wood'
        }