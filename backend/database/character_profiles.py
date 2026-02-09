import json
from typing import Dict, List, Optional

class CharacterProfileDatabase:
    def __init__(self):
        self.profiles = {}
        self.game_mappings = {}
        
    def store_character_profile(self, game_name: str, character_name: str, 
                                profile_data: Dict):
        key = f"{game_name}_{character_name}"
        self.profiles[key] = {
            "game": game_name,
            "character": character_name,
            "profile": profile_data,
            "training_iterations": 0,
            "performance_metrics": {
                "decisions_made": 0,
                "successful_outcomes": 0,
                "alignment_score": 0.0
            }
        }
        
        if game_name not in self.game_mappings:
            self.game_mappings[game_name] = []
        
        self.game_mappings[game_name].append(character_name)
    
    def get_character_profile(self, game_name: str, character_name: str) -> Optional[Dict]:
        key = f"{game_name}_{character_name}"
        return self.profiles.get(key)
    
    def update_performance_metrics(self, game_name: str, character_name: str, 
                                  metrics: Dict):
        key = f"{game_name}_{character_name}"
        if key in self.profiles:
            self.profiles[key]["performance_metrics"].update(metrics)
    
    def get_all_characters_for_game(self, game_name: str) -> List[str]:
        return self.game_mappings.get(game_name, [])
    
    def export_profiles(self) -> str:
        return json.dumps(self.profiles, indent=2)
    
    def import_profiles(self, json_data: str):
        imported = json.loads(json_data)
        self.profiles.update(imported)
        
        # Rebuild game mappings
        self.game_mappings = {}
        for key, data in self.profiles.items():
            game = data["game"]
            char = data["character"]
            
            if game not in self.game_mappings:
                self.game_mappings[game] = []
            
            if char not in self.game_mappings[game]:
                self.game_mappings[game].append(char)