from typing import Dict, List
import random

class DungeonsAndDragons:
    def __init__(self):
        self.players = []
        self.current_turn = 0
        self.dungeon_master_id = None
        self.current_encounter = None
        self.initiative_order = []
        self.combat_active = False
        self.board = self._initialize_board()
        
    def _initialize_board(self) -> Dict:
        # Creating actual D&D dungeon grid
        return {
            "grid": [[{"terrain": "empty", "occupant": None, "items": []} 
                     for _ in range(20)] for _ in range(20)],
            "dungeon_level": 1,
            "rooms_discovered": 0,
            "traps": [],
            "treasures": []
        }
    
    def _generate_dungeon_room(self, room_type: str) -> Dict:
        rooms = {
            "corridor": {
                "dimensions": (2, 10),
                "enemies": [],
                "treasure": None,
                "description": "A narrow stone corridor"
            },
            "chamber": {
                "dimensions": (6, 6),
                "enemies": ["goblin", "goblin"],
                "treasure": {"gold": 50, "items": ["potion_healing"]},
                "description": "A medium-sized chamber with flickering torches"
            },
            "throne_room": {
                "dimensions": (10, 8),
                "enemies": ["goblin_boss"],
                "treasure": {"gold": 200, "items": ["magic_sword"]},
                "description": "An ornate throne room"
            },
            "treasure_vault": {
                "dimensions": (4, 4),
                "enemies": [],
                "treasure": {"gold": 500, "items": ["ring_protection", "scroll_fireball"]},
                "description": "A secured treasure vault"
            },
            "dragon_lair": {
                "dimensions": (12, 12),
                "enemies": ["young_dragon"],
                "treasure": {"gold": 1000, "items": ["legendary_armor"]},
                "description": "A massive cavern filled with gold and bones"
            }
        }
        
        return rooms.get(room_type, rooms["corridor"])
    
    def setup_game(self, player_configs: List[Dict]) -> Dict:
        if len(player_configs) != 6:
            raise ValueError("D&D requires exactly 6 players (5 adventurers + 1 DM)")
        
        self.players = []
        
        # First player is Dungeon Master
        dm_config = player_configs[0]
        self.dungeon_master_id = 0
        
        dm = {
            "name": dm_config.get("name", "Dungeon Master"),
            "id": 0,
            "role": "dungeon_master",
            "monsters_controlled": []
        }
        self.players.append(dm)
        
        # Remaining players are adventurers
        character_classes = ["fighter", "wizard", "rogue", "cleric", "ranger"]
        
        for idx, config in enumerate(player_configs[1:], start=1):
            char_class = character_classes[idx - 1]
            character = self._create_character(char_class, idx, config.get("name", f"Player{idx}"))
            self.players.append(character)
        
        # Place characters in starting position
        start_positions = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)]
        for i, player in enumerate(self.players[1:]):
            pos = start_positions[i]
            player["position"] = pos
            self.board["grid"][pos[0]][pos[1]]["occupant"] = player["id"]
        
        # Generate initial room
        self._generate_starting_area()
        
        return self.get_game_state()
    
    def _create_character(self, char_class: str, player_id: int, name: str) -> Dict:
        characters = {
            "fighter": {
                "name": name,
                "id": player_id,
                "class": "fighter",
                "level": 1,
                "hp": 12,
                "max_hp": 12,
                "ac": 16,
                "stats": {
                    "strength": 16,
                    "dexterity": 12,
                    "constitution": 14,
                    "intelligence": 10,
                    "wisdom": 10,
                    "charisma": 8
                },
                "position": (0, 0),
                "inventory": [
                    {"name": "Longsword", "damage": "1d8", "type": "weapon"},
                    {"name": "Shield", "ac_bonus": 2, "type": "armor"},
                    {"name": "Potion of Healing", "heal": "2d4+2", "type": "consumable"}
                ],
                "abilities": ["Second Wind", "Action Surge"],
                "experience": 0
            },
            "wizard": {
                "name": name,
                "id": player_id,
                "class": "wizard",
                "level": 1,
                "hp": 8,
                "max_hp": 8,
                "ac": 12,
                "stats": {
                    "strength": 8,
                    "dexterity": 14,
                    "constitution": 12,
                    "intelligence": 16,
                    "wisdom": 12,
                    "charisma": 10
                },
                "position": (0, 0),
                "inventory": [
                    {"name": "Quarterstaff", "damage": "1d6", "type": "weapon"},
                    {"name": "Spellbook", "type": "tool"}
                ],
                "spells": [
                    {"name": "Magic Missile", "level": 1, "damage": "3d4+3"},
                    {"name": "Shield", "level": 1, "effect": "ac_boost"},
                    {"name": "Burning Hands", "level": 1, "damage": "3d6"}
                ],
                "spell_slots": {"1": 2, "2": 0, "3": 0},
                "abilities": ["Arcane Recovery"],
                "experience": 0
            },
            "rogue": {
                "name": name,
                "id": player_id,
                "class": "rogue",
                "level": 1,
                "hp": 10,
                "max_hp": 10,
                "ac": 14,
                "stats": {
                    "strength": 10,
                    "dexterity": 16,
                    "constitution": 12,
                    "intelligence": 12,
                    "wisdom": 10,
                    "charisma": 14
                },
                "position": (0, 0),
                "inventory": [
                    {"name": "Shortsword", "damage": "1d6", "type": "weapon"},
                    {"name": "Dagger", "damage": "1d4", "type": "weapon"},
                    {"name": "Thieves' Tools", "type": "tool"}
                ],
                "abilities": ["Sneak Attack", "Cunning Action", "Expertise"],
                "experience": 0
            },
            "cleric": {
                "name": name,
                "id": player_id,
                "class": "cleric",
                "level": 1,
                "hp": 10,
                "max_hp": 10,
                "ac": 15,
                "stats": {
                    "strength": 14,
                    "dexterity": 10,
                    "constitution": 14,
                    "intelligence": 10,
                    "wisdom": 16,
                    "charisma": 12
                },
                "position": (0, 0),
                "inventory": [
                    {"name": "Mace", "damage": "1d6", "type": "weapon"},
                    {"name": "Shield", "ac_bonus": 2, "type": "armor"},
                    {"name": "Holy Symbol", "type": "tool"}
                ],
                "spells": [
                    {"name": "Cure Wounds", "level": 1, "heal": "1d8+3"},
                    {"name": "Bless", "level": 1, "effect": "buff"},
                    {"name": "Sacred Flame", "level": 0, "damage": "1d8"}
                ],
                "spell_slots": {"1": 2, "2": 0, "3": 0},
                "abilities": ["Divine Domain", "Channel Divinity"],
                "experience": 0
            },
            "ranger": {
                "name": name,
                "id": player_id,
                "class": "ranger",
                "level": 1,
                "hp": 11,
                "max_hp": 11,
                "ac": 14,
                "stats": {
                    "strength": 12,
                    "dexterity": 16,
                    "constitution": 13,
                    "intelligence": 10,
                    "wisdom": 14,
                    "charisma": 10
                },
                "position": (0, 0),
                "inventory": [
                    {"name": "Longbow", "damage": "1d8", "type": "weapon", "range": 150},
                    {"name": "Shortsword", "damage": "1d6", "type": "weapon"},
                    {"name": "Arrows", "quantity": 20, "type": "ammunition"}
                ],
                "abilities": ["Favored Enemy", "Natural Explorer"],
                "experience": 0
            }
        }
        
        return characters.get(char_class, characters["fighter"])
    
    def _generate_starting_area(self):
        # Create a starting chamber
        for i in range(5):
            for j in range(5):
                self.board["grid"][i][j]["terrain"] = "stone_floor"
        
        # Add exit
        self.board["grid"][2][4]["terrain"] = "door"
    
    def get_game_state(self) -> Dict:
        return {
            "turn": self.current_turn,
            "board": self.board,
            "players": self.players,
            "current_player": self.players[self.current_turn % len(self.players)] if self.players else None,
            "combat_active": self.combat_active,
            "initiative_order": self.initiative_order,
            "current_encounter": self.current_encounter
        }
    
    def get_available_actions(self, player_id: int) -> List[Dict]:
        if not self.players or player_id >= len(self.players):
            return []
        
        player = self.players[player_id]
        actions = []
        
        if player["role"] == "dungeon_master":
            # DM actions
            actions.extend([
                {
                    "id": "spawn_monster",
                    "type": "dm_action",
                    "monster_type": "goblin",
                    "description": "Spawn a goblin"
                },
                {
                    "id": "add_trap",
                    "type": "dm_action",
                    "trap_type": "spike_trap",
                    "description": "Place a spike trap"
                },
                {
                    "id": "generate_room",
                    "type": "dm_action",
                    "room_type": "chamber",
                    "description": "Generate new room"
                }
            ])
            return actions
        
        # Player character actions
        if self.combat_active:
            # Combat actions
            actions.extend([
                {
                    "id": "attack_melee",
                    "type": "attack",
                    "attack_type": "melee",
                    "description": "Make a melee attack"
                },
                {
                    "id": "attack_ranged",
                    "type": "attack",
                    "attack_type": "ranged",
                    "description": "Make a ranged attack"
                }
            ])
            
            # Spell actions for casters
            if "spells" in player:
                for spell in player["spells"]:
                    spell_level = spell["level"]
                    if player["spell_slots"].get(str(spell_level), 0) > 0:
                        actions.append({
                            "id": f"cast_{spell['name'].lower().replace(' ', '_')}",
                            "type": "cast_spell",
                            "spell": spell,
                            "description": f"Cast {spell['name']}"
                        })
            
            # Class abilities
            for ability in player.get("abilities", []):
                actions.append({
                    "id": f"use_{ability.lower().replace(' ', '_')}",
                    "type": "ability",
                    "ability_name": ability,
                    "description": f"Use {ability}"
                })
            
            actions.append({
                "id": "dodge",
                "type": "combat_action",
                "description": "Dodge (disadvantage to attackers)"
            })
            
        else:
            # Exploration actions
            position = player["position"]
            x, y = position
            
            # Movement in 8 directions
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    
                    new_x, new_y = x + dx, y + dy
                    
                    if 0 <= new_x < 20 and 0 <= new_y < 20:
                        cell = self.board["grid"][new_x][new_y]
                        if cell["terrain"] != "wall" and cell["occupant"] is None:
                            actions.append({
                                "id": f"move_{new_x}_{new_y}",
                                "type": "movement",
                                "destination": (new_x, new_y),
                                "description": f"Move to ({new_x}, {new_y})"
                            })
            
            # Search action
            actions.append({
                "id": "search",
                "type": "search",
                "description": "Search the area (Perception check)"
            })
            
            # Check for doors
            if self.board["grid"][x][y]["terrain"] == "door":
                actions.append({
                    "id": "open_door",
                    "type": "interact",
                    "interaction": "door",
                    "description": "Open the door"
                })
            
            # Use items
            for item in player["inventory"]:
                if item.get("type") == "consumable":
                    actions.append({
                        "id": f"use_{item['name'].lower().replace(' ', '_')}",
                        "type": "use_item",
                        "item": item,
                        "description": f"Use {item['name']}"
                    })
        
        actions.append({
            "id": "pass",
            "type": "pass",
            "description": "End turn"
        })
        
        return actions
    
    def execute_action(self, player_id: int, action: Dict) -> Dict:
        if not self.players or player_id >= len(self.players):
            return {"success": False, "error": "Invalid player"}
        
        player = self.players[player_id]
        action_type = action.get("type")
        
        if action_type == "dm_action":
            return self._execute_dm_action(player, action)
        elif action_type == "movement":
            return self._execute_movement(player, action)
        elif action_type == "attack":
            return self._execute_attack(player, action)
        elif action_type == "cast_spell":
            return self._execute_cast_spell(player, action)
        elif action_type == "search":
            return self._execute_search(player)
        elif action_type == "interact":
            return self._execute_interact(player, action)
        elif action_type == "use_item":
            return self._execute_use_item(player, action)
        elif action_type == "pass":
            return {"success": True, "action": "pass"}
        
        return {"success": False, "error": "Unknown action"}
    
    def _execute_dm_action(self, dm: Dict, action: Dict) -> Dict:
        action_id = action.get("id")
        
        if action_id == "spawn_monster":
            monster_type = action.get("monster_type")
            monster = self._create_monster(monster_type)
            dm["monsters_controlled"].append(monster)
            
            return {
                "success": True,
                "action": "spawn_monster",
                "monster": monster
            }
        
        elif action_id == "generate_room":
            room_type = action.get("room_type")
            room = self._generate_dungeon_room(room_type)
            
            return {
                "success": True,
                "action": "generate_room",
                "room": room
            }
        
        return {"success": False, "error": "Unknown DM action"}
    
    def _create_monster(self, monster_type: str) -> Dict:
        monsters = {
            "goblin": {
                "name": "Goblin",
                "type": "goblin",
                "hp": 7,
                "max_hp": 7,
                "ac": 15,
                "damage": "1d6+2",
                "abilities": ["Nimble Escape"]
            },
            "goblin_boss": {
                "name": "Goblin Boss",
                "type": "goblin_boss",
                "hp": 21,
                "max_hp": 21,
                "ac": 17,
                "damage": "2d6+3",
                "abilities": ["Redirect Attack", "Leadership"]
            },
            "young_dragon": {
                "name": "Young Red Dragon",
                "type": "dragon",
                "hp": 178,
                "max_hp": 178,
                "ac": 18,
                "damage": "2d10+6",
                "abilities": ["Fire Breath", "Frightful Presence", "Legendary Actions"]
            }
        }
        
        return monsters.get(monster_type, monsters["goblin"])
    
    def _execute_movement(self, player: Dict, action: Dict) -> Dict:
        destination = action.get("destination")
        
        old_pos = player["position"]
        self.board["grid"][old_pos[0]][old_pos[1]]["occupant"] = None
        
        player["position"] = destination
        self.board["grid"][destination[0]][destination[1]]["occupant"] = player["id"]
        
        return {
            "success": True,
            "action": "movement",
            "from": old_pos,
            "to": destination
        }
    
    def _execute_attack(self, player: Dict, action: Dict) -> Dict:
        attack_type = action.get("attack_type")
        
        # Roll d20 for attack
        attack_roll = random.randint(1, 20)
        
        # Add modifiers
        if attack_type == "melee":
            modifier = (player["stats"]["strength"] - 10) // 2
        else:
            modifier = (player["stats"]["dexterity"] - 10) // 2
        
        total_attack = attack_roll + modifier + 2  # +2 proficiency bonus
        
        # Assume target AC of 15 for now
        target_ac = 15
        
        if total_attack >= target_ac:
            # Roll damage
            damage_roll = random.randint(1, 8) + modifier
            
            return {
                "success": True,
                "action": "attack",
                "attack_roll": attack_roll,
                "total": total_attack,
                "hit": True,
                "damage": damage_roll
            }
        else:
            return {
                "success": True,
                "action": "attack",
                "attack_roll": attack_roll,
                "total": total_attack,
                "hit": False,
                "damage": 0
            }
    
    def _execute_cast_spell(self, player: Dict, action: Dict) -> Dict:
        spell = action.get("spell")
        spell_level = str(spell["level"])
        
        if player["spell_slots"][spell_level] <= 0:
            return {"success": False, "error": "No spell slots available"}
        
        player["spell_slots"][spell_level] -= 1
        
        result = {
            "success": True,
            "action": "cast_spell",
            "spell": spell["name"],
            "slots_remaining": player["spell_slots"][spell_level]
        }
        
        if "damage" in spell:
            # Roll damage
            dice_parts = spell["damage"].split("d")
            if len(dice_parts) == 2:
                num_dice = int(dice_parts[0])
                die_size_parts = dice_parts[1].split("+")
                die_size = int(die_size_parts[0])
                bonus = int(die_size_parts[1]) if len(die_size_parts) > 1 else 0
                
                total_damage = sum(random.randint(1, die_size) for _ in range(num_dice)) + bonus
                result["damage"] = total_damage
        
        if "heal" in spell:
            # Roll healing
            dice_parts = spell["heal"].split("d")
            if len(dice_parts) == 2:
                num_dice = int(dice_parts[0])
                die_size_parts = dice_parts[1].split("+")
                die_size = int(die_size_parts[0])
                bonus = int(die_size_parts[1]) if len(die_size_parts) > 1 else 0
                
                total_healing = sum(random.randint(1, die_size) for _ in range(num_dice)) + bonus
                player["hp"] = min(player["hp"] + total_healing, player["max_hp"])
                result["healing"] = total_healing
                result["new_hp"] = player["hp"]
        
        return result
    
    def _execute_search(self, player: Dict) -> Dict:
        # Roll perception check
        perception_roll = random.randint(1, 20)
        wisdom_mod = (player["stats"]["wisdom"] - 10) // 2
        total = perception_roll + wisdom_mod
        
        findings = []
        
        if total >= 15:
            findings.append("You notice a hidden compartment")
        if total >= 10:
            findings.append("You see tracks on the floor")
        
        return {
            "success": True,
            "action": "search",
            "roll": perception_roll,
            "total": total,
            "findings": findings
        }
    
    def _execute_interact(self, player: Dict, action: Dict) -> Dict:
        interaction = action.get("interaction")
        
        if interaction == "door":
            pos = player["position"]
            self.board["grid"][pos[0]][pos[1]]["terrain"] = "stone_floor"
            
            # Generate new room beyond door
            room = self._generate_dungeon_room("chamber")
            
            return {
                "success": True,
                "action": "open_door",
                "room_discovered": room
            }
        
        return {"success": False, "error": "Unknown interaction"}
    
    def _execute_use_item(self, player: Dict, action: Dict) -> Dict:
        item = action.get("item")
        
        if item.get("type") == "consumable":
            player["inventory"].remove(item)
            
            if "heal" in item:
                # Roll healing
                dice_parts = item["heal"].split("d")
                if len(dice_parts) == 2:
                    num_dice = int(dice_parts[0])
                    die_size_parts = dice_parts[1].split("+")
                    die_size = int(die_size_parts[0])
                    bonus = int(die_size_parts[1]) if len(die_size_parts) > 1 else 0
                    
                    total_healing = sum(random.randint(1, die_size) for _ in range(num_dice)) + bonus
                    player["hp"] = min(player["hp"] + total_healing, player["max_hp"])
                    
                    return {
                        "success": True,
                        "action": "use_item",
                        "item": item["name"],
                        "healing": total_healing,
                        "new_hp": player["hp"]
                    }
    def advance_turn(self):
        self.current_turn += 1
        
        if self.combat_active:
            self._advance_initiative()
        else:
            current_player_idx = self.current_turn % len([p for p in self.players if p["role"] != "dungeon_master"])
            
    def _advance_initiative(self):
        if not self.initiative_order:
            return
        
        current_idx = 0
        for idx, entry in enumerate(self.initiative_order):
            if entry.get('current', False):
                current_idx = idx
                entry['current'] = False
                break
        
        next_idx = (current_idx + 1) % len(self.initiative_order)
        self.initiative_order[next_idx]['current'] = True
        
        return {"success": False, "error": "Cannot use item"}