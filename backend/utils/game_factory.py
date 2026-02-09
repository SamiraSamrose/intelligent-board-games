from games.brass_birmingham import BrassBirmingham
from games.gloomhaven import Gloomhaven
from games.terraforming_mars import TerraformingMars
from games.dune import Dune
from games.dungeons_dragons import DungeonsAndDragons
from games.exploding_kittens import ExplodingKittens

class GameFactory:
    @staticmethod
    def create_game(game_type: str):
        games = {
            'brass_birmingham': BrassBirmingham,
            'gloomhaven': Gloomhaven,
            'terraforming_mars': TerraformingMars,
            'dune': Dune,
            'dungeons_dragons': DungeonsAndDragons,
            'exploding_kittens': ExplodingKittens
        }
        
        game_class = games.get(game_type)
        if game_class:
            return game_class()
        
        raise ValueError(f"Unknown game type: {game_type}")
    
    @staticmethod
    def get_player_count(game_type: str) -> int:
        counts = {
            'brass_birmingham': 4,
            'gloomhaven': 4,
            'terraforming_mars': 5,
            'dune': 6,
            'dungeons_dragons': 6,
            'exploding_kittens': 5
        }
        
        return counts.get(game_type, 4)