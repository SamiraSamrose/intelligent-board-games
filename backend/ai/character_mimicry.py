import google.generativeai as genai
from typing import Dict, List
import asyncio

class CharacterMimicry:
    def __init__(self, api_key: str, character_learning):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.learning = character_learning
        
    async def mimic_character_decision(self, game_type: str, character_name: str,
                                      game_state: Dict, available_actions: List[Dict]) -> Dict:
        
        character_data = self.learning.character_knowledge.get(
            f"{game_type}_{character_name}",
            {}
        )
        
        mimic_prompt = f"""You are EXACTLY {character_name} from {game_type}.

Your complete character profile:
Personality: {character_data.get('personality', {})}
Decision weights: {character_data.get('decision_weights', {})}
Risk tolerance: {character_data.get('risk_tolerance', 0.5)}
Cooperation level: {character_data.get('cooperation_level', 0.5)}
Signature phrases: {character_data.get('signature_phrases', [])}
Tactical preferences: {character_data.get('tactical_preferences', [])}
Behavior patterns: {character_data.get('behavior_patterns', [])}

Current game state:
{self._format_game_state(game_state)}

Available actions:
{self._format_actions(available_actions)}

Choose the action that {character_name} would EXACTLY choose. Think as {character_name} would think.
Consider their personality, their typical strategies, their risk tolerance.

Respond with JSON:
{{
    "action_id": "chosen action ID",
    "reasoning": "why {character_name} would choose this, using their thought process",
    "in_character_quote": "what {character_name} would say about this decision",
    "confidence": 0.0-1.0
}}"""

        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                mimic_prompt
            )
            
            decision = self._parse_decision(response.text, available_actions)
            
            return decision
            
        except Exception as e:
            return {
                'action': available_actions[0] if available_actions else {},
                'reasoning': f"Default action due to error: {str(e)}",
                'confidence': 0.3
            }
    
    async def generate_character_dialogue(self, game_type: str, character_name: str,
                                         context: str) -> str:
        
        character_data = self.learning.character_knowledge.get(
            f"{game_type}_{character_name}",
            {}
        )
        
        dialogue_prompt = f"""You are {character_name} from {game_type}.

Personality traits: {character_data.get('personality', {})}
Signature phrases: {character_data.get('signature_phrases', [])}

Context: {context}

Generate dialogue that {character_name} would say in this situation. Use their speech patterns, vocabulary, and personality. Be authentic to the character."""

        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                dialogue_prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"{character_name} remains silent."
    
    def _format_game_state(self, state: Dict) -> str:
        lines = []
        
        if 'turn' in state:
            lines.append(f"Turn: {state['turn']}")
        if 'phase' in state:
            lines.append(f"Phase: {state['phase']}")
        if 'current_player' in state:
            lines.append(f"Current player: {state.get('current_player', {}).get('name', 'Unknown')}")
        
        if 'players' in state:
            lines.append("\nPlayers:")
            for player in state['players']:
                lines.append(f"  - {player.get('name', 'Unknown')}")
        
        if 'resources' in state:
            lines.append(f"\nResources: {state['resources']}")
        
        return "\n".join(lines)
    
    def _format_actions(self, actions: List[Dict]) -> str:
        lines = []
        
        for idx, action in enumerate(actions):
            lines.append(f"{idx + 1}. ID: {action.get('id', 'unknown')}")
            lines.append(f"   Type: {action.get('type', 'unknown')}")
            lines.append(f"   Description: {action.get('description', 'No description')}")
            if 'cost' in action:
                lines.append(f"   Cost: {action['cost']}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _parse_decision(self, response_text: str, available_actions: List[Dict]) -> Dict:
        try:
            import json
            import re
            
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                
                action_id = data.get('action_id', '')
                selected_action = next(
                    (a for a in available_actions if a.get('id') == action_id),
                    available_actions[0] if available_actions else {}
                )
                
                return {
                    'action': selected_action,
                    'reasoning': data.get('reasoning', ''),
                    'in_character_quote': data.get('in_character_quote', ''),
                    'confidence': float(data.get('confidence', 0.5))
                }
        except Exception:
            pass
        
        return {
            'action': available_actions[0] if available_actions else {},
            'reasoning': response_text,
            'confidence': 0.5
        }