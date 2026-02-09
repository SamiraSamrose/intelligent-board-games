import google.generativeai as genai
from typing import Dict, List
import asyncio
import json

class EnhancedCharacterLearning:
    def __init__(self, api_key: str, nano_banana_pro):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.nano = nano_banana_pro
        self.character_knowledge = {}
        
    async def deep_learn_character(self, game_type: str, character_name: str,
                                   source_texts: List[str]) -> Dict:
        
        analysis_prompt = f"""Analyze this character from {game_type}: {character_name}

Source materials:
{chr(10).join(source_texts)}

Extract detailed character profile including:
1. Core personality traits (Big Five model)
2. Tactical preferences and combat/game style
3. Decision-making patterns in different scenarios
4. Relationship dynamics with other characters
5. Signature phrases and communication style
6. Strategic tendencies (aggressive, defensive, balanced)
7. Resource management preferences
8. Risk tolerance in various situations
9. Cooperation vs competition orientation
10. Emotional triggers and reactions

Provide comprehensive JSON analysis."""

        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                analysis_prompt
            )
            
            character_data = self._parse_character_analysis(response.text)
            
            await self.nano.train_character_personality(
                character_name,
                game_type,
                character_data
            )
            
            self.character_knowledge[f"{game_type}_{character_name}"] = character_data
            
            return character_data
            
        except Exception as e:
            return self._get_default_character_profile()
    
    async def learn_from_gameplay(self, game_type: str, character_name: str,
                                 game_history: List[Dict]) -> Dict:
        
        learning_prompt = f"""Analyze gameplay decisions for {character_name} in {game_type}:

Game History:
{json.dumps(game_history, indent=2)}

Identify:
1. Consistent decision patterns
2. Preferred strategies
3. Reaction to specific game states
4. Adaptation to opponent actions
5. Risk-taking behaviors
6. Resource prioritization

Return refined character behavioral model as JSON."""

        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                learning_prompt
            )
            
            refined_data = self._parse_character_analysis(response.text)
            
            key = f"{game_type}_{character_name}"
            if key in self.character_knowledge:
                self.character_knowledge[key] = self._merge_profiles(
                    self.character_knowledge[key],
                    refined_data
                )
            
            return refined_data
            
        except Exception as e:
            return {}
    
    async def simulate_character_reaction(self, game_type: str, character_name: str,
                                         situation: str) -> str:
        
        key = f"{game_type}_{character_name}"
        character_data = self.character_knowledge.get(key, {})
        
        reaction_prompt = f"""You are {character_name} from {game_type}.

Your personality profile:
{json.dumps(character_data, indent=2)}

Current situation:
{situation}

How do you react? Stay completely in character. Use your signature phrases and decision-making style."""

        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                reaction_prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"{character_name} considers the situation carefully."
    
    def _parse_character_analysis(self, response_text: str) -> Dict:
        try:
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                
                normalized = {
                    'personality': {
                        'extraversion': self._normalize_trait(data.get('extraversion', 0.5)),
                        'agreeableness': self._normalize_trait(data.get('agreeableness', 0.5)),
                        'conscientiousness': self._normalize_trait(data.get('conscientiousness', 0.5)),
                        'neuroticism': self._normalize_trait(data.get('neuroticism', 0.5)),
                        'openness': self._normalize_trait(data.get('openness', 0.5))
                    },
                    'decision_weights': {
                        'economic': self._normalize_trait(data.get('economic_preference', 0.5)),
                        'military': self._normalize_trait(data.get('military_preference', 0.5)),
                        'diplomatic': self._normalize_trait(data.get('diplomatic_preference', 0.5)),
                        'aggressive': self._normalize_trait(data.get('aggressiveness', 0.5)),
                        'defensive': self._normalize_trait(data.get('defensiveness', 0.5))
                    },
                    'risk_tolerance': self._normalize_trait(data.get('risk_tolerance', 0.5)),
                    'cooperation_level': self._normalize_trait(data.get('cooperation', 0.5)),
                    'skills': data.get('skills', []),
                    'motivations': data.get('motivations', []),
                    'signature_phrases': data.get('signature_phrases', []),
                    'tactical_preferences': data.get('tactical_preferences', []),
                    'behavior_patterns': data.get('behavior_patterns', [])
                }
                
                return normalized
                
        except Exception:
            pass
        
        return self._get_default_character_profile()
    
    def _normalize_trait(self, value) -> float:
        if isinstance(value, str):
            value_map = {
                'very low': 0.1, 'low': 0.3, 'medium': 0.5,
                'high': 0.7, 'very high': 0.9
            }
            return value_map.get(value.lower(), 0.5)
        
        try:
            return max(0.0, min(1.0, float(value)))
        except:
            return 0.5
    
    def _merge_profiles(self, original: Dict, new: Dict) -> Dict:
        merged = original.copy()
        
        for key in ['personality', 'decision_weights']:
            if key in new:
                if key not in merged:
                    merged[key] = {}
                for trait, value in new[key].items():
                    if trait in merged[key]:
                        merged[key][trait] = (merged[key][trait] * 0.7 + value * 0.3)
                    else:
                        merged[key][trait] = value
        
        for key in ['skills', 'motivations', 'signature_phrases', 'tactical_preferences']:
            if key in new:
                if key not in merged:
                    merged[key] = []
                merged[key] = list(set(merged[key] + new[key]))
        
        return merged
    
    def _get_default_character_profile(self) -> Dict:
        return {
            'personality': {
                'extraversion': 0.5,
                'agreeableness': 0.5,
                'conscientiousness': 0.5,
                'neuroticism': 0.5,
                'openness': 0.5
            },
            'decision_weights': {
                'economic': 0.5,
                'military': 0.5,
                'diplomatic': 0.5,
                'aggressive': 0.5,
                'defensive': 0.5
            },
            'risk_tolerance': 0.5,
            'cooperation_level': 0.5,
            'skills': [],
            'motivations': [],
            'signature_phrases': [],
            'tactical_preferences': [],
            'behavior_patterns': []
        }