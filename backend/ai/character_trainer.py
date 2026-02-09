import google.generativeai as genai
from typing import Dict, List
import json
import asyncio

class CharacterTrainer:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.character_db = {}
        
    async def train_character(self, game_name: str, character_name: str, 
                             source_material: str) -> Dict:
        extraction_prompt = f"""Analyze this character from {game_name}:

{source_material}

Extract and return JSON with:
{{
    "personality": {{
        "extraversion": 0.0-1.0,
        "agreeableness": 0.0-1.0,
        "conscientiousness": 0.0-1.0,
        "neuroticism": 0.0-1.0,
        "openness": 0.0-1.0
    }},
    "skills": ["skill1", "skill2"],
    "motivations": ["motivation1", "motivation2"],
    "behavior_patterns": ["pattern1", "pattern2"],
    "decision_weights": {{
        "economic": 0.0-1.0,
        "military": 0.0-1.0,
        "diplomatic": 0.0-1.0,
        "aggressive": 0.0-1.0,
        "defensive": 0.0-1.0
    }},
    "risk_tolerance": 0.0-1.0,
    "cooperation_level": 0.0-1.0,
    "signature_phrases": ["phrase1", "phrase2"],
    "tactical_preferences": ["preference1", "preference2"]
}}"""

        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                extraction_prompt
            )
            
            character_data = self._parse_character_data(response.text)
            
            key = f"{game_name}_{character_name}"
            self.character_db[key] = character_data
            
            return character_data
            
        except Exception as e:
            return self._get_default_character()
    
    def _parse_character_data(self, response_text: str) -> Dict:
        try:
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._get_default_character()
        except Exception:
            return self._get_default_character()
    
    def _get_default_character(self) -> Dict:
        return {
            "personality": {
                "extraversion": 0.5,
                "agreeableness": 0.5,
                "conscientiousness": 0.5,
                "neuroticism": 0.5,
                "openness": 0.5
            },
            "skills": ["general"],
            "motivations": ["win"],
            "behavior_patterns": ["balanced"],
            "decision_weights": {
                "economic": 0.5,
                "military": 0.5,
                "diplomatic": 0.5,
                "aggressive": 0.5,
                "defensive": 0.5
            },
            "risk_tolerance": 0.5,
            "cooperation_level": 0.5,
            "signature_phrases": [],
            "tactical_preferences": []
        }
    
    def get_character(self, game_name: str, character_name: str) -> Optional[Dict]:
        key = f"{game_name}_{character_name}"
        return self.character_db.get(key)
