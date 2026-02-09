from typing import Dict, List, Any

def validate_game_type(game_type: str) -> bool:
    valid_games = [
        'brass_birmingham',
        'gloomhaven',
        'terraforming_mars',
        'dune',
        'dungeons_dragons',
        'exploding_kittens'
    ]
    return game_type in valid_games

def validate_player_count(game_type: str, player_count: int) -> bool:
    required_counts = {
        'brass_birmingham': 4,
        'gloomhaven': 4,
        'terraforming_mars': 5,
        'dune': 6,
        'dungeons_dragons': 6,
        'exploding_kittens': 5
    }
    
    return player_count == required_counts.get(game_type, 0)

def validate_player_config(config: Dict[str, Any]) -> bool:
    required_fields = ['name']
    return all(field in config for field in required_fields)

def validate_action(action: Dict[str, Any]) -> bool:
    required_fields = ['type']
    return all(field in action for field in required_fields)