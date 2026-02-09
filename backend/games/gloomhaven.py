from typing import Dict, List
import random

class Gloomhaven:
    def __init__(self):
        self.players = []
        self.monsters = []
        self.current_turn = 0
        self.scenario = None
        self.board = {}
        self.round_number = 0
        
    def _initialize_board(self, scenario_id: int) -> Dict:
        scenarios = {
            1: {
                "name": "Black Barrow",
                "rooms": {
                    "room_1": {
                        "tiles": [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)],
                        "monsters": [
                            {"type": "bandit_guard", "level": 1, "count": 3},
                            {"type": "living_bones", "level": 1, "count": 2}
                        ],
                        "doors": [(2, 0)]
                    },
                    "room_2": {
                        "tiles": [(3, 0), (3, 1), (4, 0), (4, 1), (5, 0), (5, 1)],
                        "monsters": [
                            {"type": "bandit_archer", "level": 1, "count": 2}
                        ],
                        "treasure": True
                    }
                },
                "goal": "Kill all enemies"
            }
        }
        
        return scenarios.get(scenario_id, scenarios[1])
    
    def setup_game(self, player_configs: List[Dict], scenario_id: int = 1) -> Dict:
        if len(player_configs) != 4:
            raise ValueError("Gloomhaven requires exactly 4 players")
        
        self.scenario = self._initialize_board(scenario_id)
        self.players = []
        
        for idx, config in enumerate(player_configs):
            character_class = config.get("class", "brute")
            player = self._create_character(character_class, idx, config.get("name", f"Player{idx}"))
            self.players.append(player)
        
        self._spawn_monsters()
        
        return self.get_game_state()
    
    def _create_character(self, char_class: str, player_id: int, name: str) -> Dict:
        characters = {
            "brute": {
                "name": name,
                "id": player_id,
                "class": "brute",
                "max_hp": 10,
                "current_hp": 10,
                "position": (0, 0),
                "hand": self._get_starting_hand("brute"),
                "discard": [],
                "lost": [],
                "experience": 0,
                "items": [],
                "conditions": []
            },
            "tinkerer": {
                "name": name,
                "id": player_id,
                "class": "tinkerer",
                "max_hp": 8,
                "current_hp": 8,
                "position": (0, 1),
                "hand": self._get_starting_hand("tinkerer"),
                "discard": [],
                "lost": [],
                "experience": 0,
                "items": [],
                "conditions": []
            },
            "spellweaver": {
                "name": name,
                "id": player_id,
                "class": "spellweaver",
                "max_hp": 6,
                "current_hp": 6,
                "position": (1, 0),
                "hand": self._get_starting_hand("spellweaver"),
                "discard": [],
                "lost": [],
                "experience": 0,
                "items": [],
                "conditions": []
            },
            "scoundrel": {
                "name": name,
                "id": player_id,
                "class": "scoundrel",
                "max_hp": 8,
                "current_hp": 8,
                "position": (1, 1),
                "hand": self._get_starting_hand("scoundrel"),
                "discard": [],
                "lost": [],
                "experience": 0,
                "items": [],
                "conditions": []
            }
        }
        
        return characters.get(char_class, characters["brute"])
    
    def _get_starting_hand(self, char_class: str) -> List[Dict]:
        hands = {
            "brute": [
                {"id": "brute_1", "name": "Trample", "initiative": 72, 
                 "top": {"type": "attack", "value": 3, "move": 0},
                 "bottom": {"type": "move", "value": 3}},
                {"id": "brute_2", "name": "Eye for an Eye", "initiative": 18,
                 "top": {"type": "attack", "value": 1, "retaliate": 2},
                 "bottom": {"type": "shield", "value": 1}},
                {"id": "brute_3", "name": "Spare Dagger", "initiative": 27,
                 "top": {"type": "attack", "value": 3},
                 "bottom": {"type": "move", "value": 2, "attack": 2}},
                {"id": "brute_4", "name": "Warding Strength", "initiative": 32,
                 "top": {"type": "shield", "value": 1},
                 "bottom": {"type": "heal", "value": 2, "range": 1}},
                {"id": "brute_5", "name": "Provoking Roar", "initiative": 10,
                 "top": {"type": "attack", "value": 2, "push": 1},
                 "bottom": {"type": "move", "value": 1, "shield": 1}},
                {"id": "brute_6", "name": "Sweeping Blow", "initiative": 64,
                 "top": {"type": "attack", "value": 2, "target": 2},
                 "bottom": {"type": "move", "value": 2}}
            ],
            "tinkerer": [
                {"id": "tink_1", "name": "Reviving Shock", "initiative": 74,
                 "top": {"type": "heal", "value": 3, "range": 2},
                 "bottom": {"type": "move", "value": 3}},
                {"id": "tink_2", "name": "Ink Bomb", "initiative": 28,
                 "top": {"type": "attack", "value": 2, "range": 3},
                 "bottom": {"type": "shield", "value": 1, "self": True}},
                {"id": "tink_3", "name": "Stun Shot", "initiative": 60,
                 "top": {"type": "attack", "value": 1, "range": 3, "stun": True},
                 "bottom": {"type": "move", "value": 3}},
                {"id": "tink_4", "name": "Enhancement Field", "initiative": 15,
                 "top": {"type": "heal", "value": 1, "range": 3},
                 "bottom": {"type": "move", "value": 2, "attack": 2}},
                {"id": "tink_5", "name": "Poison Dagger", "initiative": 45,
                 "top": {"type": "attack", "value": 2, "poison": True},
                 "bottom": {"type": "move", "value": 2}},
                {"id": "tink_6", "name": "Net Shooter", "initiative": 33,
                 "top": {"type": "attack", "value": 2, "immobilize": True},
                 "bottom": {"type": "heal", "value": 2}}
            ],
            "spellweaver": [
                {"id": "spell_1", "name": "Fire Orbs", "initiative": 62,
                 "top": {"type": "attack", "value": 3, "range": 3},
                 "bottom": {"type": "move", "value": 3}},
                {"id": "spell_2", "name": "Frost Armor", "initiative": 24,
                 "top": {"type": "shield", "value": 2},
                 "bottom": {"type": "attack", "value": 2, "range": 2}},
                {"id": "spell_3", "name": "Mana Bolt", "initiative": 5,
                 "top": {"type": "attack", "value": 3, "range": 4},
                 "bottom": {"type": "move", "value": 2}},
                {"id": "spell_4", "name": "Aid from the Ether", "initiative": 90,
                 "top": {"type": "recover", "value": 1},
                 "bottom": {"type": "move", "value": 3}},
                {"id": "spell_5", "name": "Impaling Eruption", "initiative": 71,
                 "top": {"type": "attack", "value": 4, "range": 3},
                 "bottom": {"type": "shield", "value": 1}},
                {"id": "spell_6", "name": "Reviving Ether", "initiative": 18,
                 "top": {"type": "heal", "value": 3, "range": 3},
                 "bottom": {"type": "move", "value": 2}}
            ],
            "scoundrel": [
                {"id": "scoun_1", "name": "Quick Hands", "initiative": 3,
                 "top": {"type": "loot", "value": 1},
                 "bottom": {"type": "move", "value": 4}},
                {"id": "scoun_2", "name": "Single Out", "initiative": 29,
                 "top": {"type": "attack", "value": 3, "advantage": True},
                 "bottom": {"type": "move", "value": 3}},
                {"id": "scoun_3", "name": "Backstab", "initiative": 12,
                 "top": {"type": "attack", "value": 5},
                 "bottom": {"type": "move", "value": 2}},
                {"id": "scoun_4", "name": "Smoke Bomb", "initiative": 11,
                 "top": {"type": "move", "value": 3, "invisible": True},
                 "bottom": {"type": "attack", "value": 2}},
                {"id": "scoun_5", "name": "Viper Strike", "initiative": 87,
                 "top": {"type": "attack", "value": 3, "poison": True},
                 "bottom": {"type": "move", "value": 2}},
                {"id": "scoun_6", "name": "Thief's Knack", "initiative": 20,
                 "top": {"type": "loot", "value": 2},
                 "bottom": {"type": "move", "value": 2, "attack": 2}}
            ]
        }
        
        return hands.get(char_class, hands["brute"])
    
    def _spawn_monsters(self):
        self.monsters = []
        
        for room_name, room_data in self.scenario["rooms"].items():
            for monster_group in room_data.get("monsters", []):
                for i in range(monster_group["count"]):
                    monster = {
                        "type": monster_group["type"],
                        "level": monster_group["level"],
                        "id": len(self.monsters),
                        "hp": self._get_monster_hp(monster_group["type"], monster_group["level"]),
                        "current_hp": self._get_monster_hp(monster_group["type"], monster_group["level"]),
                        "position": self._get_spawn_position(room_name, i),
                        "conditions": []
                    }
                    self.monsters.append(monster)
    
    def _get_monster_hp(self, monster_type: str, level: int) -> int:
        hp_table = {
            "bandit_guard": {1: 5, 2: 6, 3: 7},
            "living_bones": {1: 5, 2: 6, 3: 7},
            "bandit_archer": {1: 4, 2: 5, 3: 6}
        }
        
        return hp_table.get(monster_type, {1: 5}).get(level, 5)
    
    def _get_spawn_position(self, room_name: str, index: int) -> tuple:
        room = self.scenario["rooms"][room_name]
        tiles = room["tiles"]
        return tiles[min(index, len(tiles) - 1)]
    
    def get_game_state(self) -> Dict:
        return {
            "turn": self.current_turn,
            "round": self.round_number,
            "scenario": self.scenario["name"] if self.scenario else "None",
            "players": self.players,
            "monsters": self.monsters,
            "current_player": self.players[self.current_turn % len(self.players)] if self.players else None
        }
    
    def get_available_actions(self, player_id: int) -> List[Dict]:
        if not self.players or player_id >= len(self.players):
            return []
        
        player = self.players[player_id]
        actions = []
        
        for card in player["hand"]:
            actions.append({
                "id": f"play_{card['id']}_top",
                "type": "play_card",
                "card_id": card["id"],
                "half": "top",
                "action": card["top"],
                "initiative": card["initiative"],
                "description": f"Play {card['name']} (top): {self._describe_action(card['top'])}"
            })
            
            actions.append({
                "id": f"play_{card['id']}_bottom",
                "type": "play_card",
                "card_id": card["id"],
                "half": "bottom",
                "action": card["bottom"],
                "initiative": card["initiative"],
                "description": f"Play {card['name']} (bottom): {self._describe_action(card['bottom'])}"
            })
        
        if len(player["discard"]) > 0:
            actions.append({
                "id": "rest",
                "type": "rest",
                "description": "Rest to recover discarded cards"
            })
        
        return actions
    
    def _describe_action(self, action: Dict) -> str:
        parts = []
        
        if "attack" in action:
            parts.append(f"Attack {action['attack']}")
        if "move" in action:
            parts.append(f"Move {action['move']}")
        if "heal" in action:
            parts.append(f"Heal {action['heal']}")
        if "shield" in action:
            parts.append(f"Shield {action['shield']}")
        if "range" in action:
            parts.append(f"Range {action['range']}")
        
        return ", ".join(parts) if parts else "Special"
    
    def execute_action(self, player_id: int, action: Dict) -> Dict:
        if not self.players or player_id >= len(self.players):
            return {"success": False, "error": "Invalid player"}
        
        player = self.players[player_id]
        action_type = action.get("type")
        
        if action_type == "play_card":
            return self._execute_play_card(player, action)
        elif action_type == "rest":
            return self._execute_rest(player)
        
        return {"success": False, "error": "Unknown action"}
    
    def _execute_play_card(self, player: Dict, action: Dict) -> Dict:
        card_id = action.get("card_id")
        card = next((c for c in player["hand"] if c["id"] == card_id), None)
        
        if not card:
            return {"success": False, "error": "Card not in hand"}
        
        player["hand"].remove(card)
        player["discard"].append(card)
        
        half = action.get("half")
        card_action = card[half]
        
        result = {
            "success": True,
            "card": card["name"],
            "half": half,
            "effects": []
        }
        
        if "attack" in card_action:
            damage = card_action["attack"]
            result["effects"].append(f"Attack for {damage} damage")
        
        if "move" in card_action:
            movement = card_action["move"]
            result["effects"].append(f"Move {movement} spaces")
        
        if "heal" in card_action:
            healing = card_action["heal"]
            player["current_hp"] = min(player["current_hp"] + healing, player["max_hp"])
            result["effects"].append(f"Heal {healing} HP")
        
        return result
    
    def _execute_rest(self, player: Dict) -> Dict:
        if not player["discard"]:
            return {"success": False, "error": "No cards to recover"}
        
        lost_card = random.choice(player["discard"])
        player["discard"].remove(lost_card)
        player["lost"].append(lost_card)
        
        player["hand"].extend(player["discard"])
        player["discard"] = []
        
        return {
            "success": True,
            "action": "rest",
            "recovered": len(player["hand"]),
            "lost": lost_card["name"]
        }
    def advance_turn(self):
        self.current_turn += 1
        
        if self.current_turn % len(self.players) == 0:
            self.round_number += 1
            
            for player in self.players:
                if player["role"] != "dungeon_master":
                    player["energy"] += player["production"]["energy"]
                    player["heat"] += player["energy"]
                    player["energy"] = 0
