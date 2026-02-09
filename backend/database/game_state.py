import json
from typing import Dict, Optional
from datetime import datetime

class GameStateDatabase:
    def __init__(self):
        self.game_states = {}
        self.game_history = {}
        
    def save_game_state(self, game_id: str, game_name: str, state: Dict):
        self.game_states[game_id] = {
            "game_name": game_name,
            "state": state,
            "last_updated": datetime.now().isoformat(),
            "turn_number": state.get("turn", 0)
        }
        
        if game_id not in self.game_history:
            self.game_history[game_id] = []
        
        self.game_history[game_id].append({
            "state": state.copy(),
            "timestamp": datetime.now().isoformat()
        })
    
    def load_game_state(self, game_id: str) -> Optional[Dict]:
        game_data = self.game_states.get(game_id)
        return game_data["state"] if game_data else None
    
    def get_game_history(self, game_id: str) -> List[Dict]:
        return self.game_history.get(game_id, [])
    
    def delete_game(self, game_id: str):
        if game_id in self.game_states:
            del self.game_states[game_id]
        if game_id in self.game_history:
            del self.game_history[game_id]
    
    def list_active_games(self) -> List[Dict]:
        return [
            {
                "game_id": gid,
                "game_name": data["game_name"],
                "turn": data["turn_number"],
                "last_updated": data["last_updated"]
            }
            for gid, data in self.game_states.items()
        ]