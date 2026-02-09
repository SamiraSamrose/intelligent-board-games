import google.generativeai as genai
from typing import Dict, List, Optional
import asyncio

class PersonaSystem:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.personas = {}
        
    def create_character_persona(self, character_name: str, 
                                character_data: Dict) -> Dict:
        persona = {
            'name': character_name,
            'base_personality': character_data.get('personality', {}),
            'skills': character_data.get('skills', []),
            'motivations': character_data.get('motivations', []),
            'behavior_patterns': character_data.get('behavior_patterns', []),
            'decision_weights': character_data.get('decision_weights', {}),
            'risk_tolerance': character_data.get('risk_tolerance', 0.5),
            'cooperation_level': character_data.get('cooperation_level', 0.5),
            'interaction_history': []
        }
        
        self.personas[character_name] = persona
        return persona
    
    async def generate_character_decision(self, character_name: str, 
                                         game_context: Dict,
                                         available_actions: List[Dict]) -> Dict:
        if character_name not in self.personas:
            raise ValueError(f"Character {character_name} not found")
        
        persona = self.personas[character_name]
        
        decision_prompt = self._build_character_prompt(persona, game_context, 
                                                       available_actions)
        
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                decision_prompt
            )
            
            decision = self._parse_decision_response(response.text, available_actions)
            
            self._update_interaction_history(character_name, game_context, decision)
            
            return decision
            
        except Exception as e:
            return {
                'action': available_actions[0] if available_actions else {},
                'reasoning': f"Error: {str(e)}",
                'confidence': 0.0
            }
    
    def _build_character_prompt(self, persona: Dict, context: Dict, 
                               actions: List[Dict]) -> str:
        personality_desc = self._format_personality(persona['base_personality'])
        
        prompt = f"""You are {persona['name']}, a character with these traits:

Personality: {personality_desc}
Skills: {', '.join(persona['skills'])}
Motivations: {', '.join(persona['motivations'])}
Behavior patterns: {', '.join(persona['behavior_patterns'])}
Risk tolerance: {persona['risk_tolerance']:.2f}
Cooperation level: {persona['cooperation_level']:.2f}

Current situation:
{self._format_context(context)}

Available actions:
{self._format_actions(actions)}

Recent interaction history:
{self._format_history(persona['interaction_history'][-3:])}

As {persona['name']}, choose the action that best fits your personality and motivations.
Think through your decision step by step, staying true to your character.

Respond in JSON format:
{{
    "action_id": "selected action ID",
    "reasoning": "your thought process",
    "confidence": 0.0-1.0,
    "alternative_considered": "other action you considered"
}}"""

        return prompt
    
    def _format_personality(self, personality: Dict) -> str:
        return ", ".join([f"{k}: {v}" for k, v in personality.items()])
    
    def _format_context(self, context: Dict) -> str:
        lines = []
        for key, value in context.items():
            lines.append(f"{key}: {value}")
        return "\n".join(lines)
    
    def _format_actions(self, actions: List[Dict]) -> str:
        lines = []
        for idx, action in enumerate(actions):
            lines.append(f"{idx}. {action.get('name', 'Unknown')}: {action.get('description', '')}")
        return "\n".join(lines)
    
    def _format_history(self, history: List[Dict]) -> str:
        if not history:
            return "No previous interactions"
        
        lines = []
        for h in history:
            lines.append(f"- {h.get('summary', 'Unknown action')}")
        return "\n".join(lines)
    
    def _parse_decision_response(self, response_text: str, 
                                actions: List[Dict]) -> Dict:
        try:
            import json
            import re
            
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                decision_data = json.loads(json_match.group())
                
                action_id = decision_data.get('action_id', '')
                selected_action = next((a for a in actions if a.get('id') == action_id), 
                                     actions[0] if actions else {})
                
                return {
                    'action': selected_action,
                    'reasoning': decision_data.get('reasoning', ''),
                    'confidence': decision_data.get('confidence', 0.5),
                    'alternative': decision_data.get('alternative_considered', '')
                }
            else:
                return {
                    'action': actions[0] if actions else {},
                    'reasoning': response_text,
                    'confidence': 0.5
                }
                
        except Exception:
            return {
                'action': actions[0] if actions else {},
                'reasoning': response_text,
                'confidence': 0.5
            }
    
    def _update_interaction_history(self, character_name: str, 
                                   context: Dict, decision: Dict):
        self.personas[character_name]['interaction_history'].append({
            'context': context,
            'decision': decision,
            'summary': f"Chose {decision.get('action', {}).get('name', 'unknown')} - {decision.get('reasoning', '')[:100]}"
        })
        
        if len(self.personas[character_name]['interaction_history']) > 10:
            self.personas[character_name]['interaction_history'].pop(0)
