from typing import Dict, List
import random

class Dune:
    def __init__(self):
        self.players = []
        self.current_turn = 0
        self.current_phase = "bidding"
        self.round_number = 1
        self.storm_position = 0
        self.spice_deck = []
        self.treachery_deck = []
        self.board = self._initialize_board()
        
    def _initialize_board(self) -> Dict:
        # Implementing actual Dune board with territories and connections
        territories = {
            "arrakeen": {
                "type": "stronghold",
                "connections": ["carthag", "funeral_plain", "habbanya_ridge"],
                "occupants": [],
                "spice": 0,
                "sectors": [0, 1]
            },
            "carthag": {
                "type": "stronghold",
                "connections": ["arrakeen", "imperial_basin", "harg_pass"],
                "occupants": [],
                "spice": 0,
                "sectors": [2, 3]
            },
            "tueks_sietch": {
                "type": "stronghold",
                "connections": ["habbanya_ridge", "sietch_tabr", "false_wall_south"],
                "occupants": [],
                "spice": 0,
                "sectors": [4, 5]
            },
            "sietch_tabr": {
                "type": "stronghold",
                "connections": ["tueks_sietch", "red_chasm", "habbanya_ridge"],
                "occupants": [],
                "spice": 0,
                "sectors": [6, 7]
            },
            "habbanya_ridge": {
                "type": "territory",
                "connections": ["arrakeen", "tueks_sietch", "sietch_tabr", "funeral_plain"],
                "occupants": [],
                "spice": 0,
                "sectors": [8, 9]
            },
            "funeral_plain": {
                "type": "territory",
                "connections": ["arrakeen", "habbanya_ridge", "the_greater_flat"],
                "occupants": [],
                "spice": 0,
                "sectors": [10, 11]
            },
            "imperial_basin": {
                "type": "territory",
                "connections": ["carthag", "harg_pass", "cielago_depression"],
                "occupants": [],
                "spice": 0,
                "sectors": [12, 13]
            },
            "harg_pass": {
                "type": "territory",
                "connections": ["carthag", "imperial_basin", "false_wall_west"],
                "occupants": [],
                "spice": 0,
                "sectors": [14, 15]
            },
            "false_wall_south": {
                "type": "territory",
                "connections": ["tueks_sietch", "the_minor_erg", "pasty_mesa"],
                "occupants": [],
                "spice": 0,
                "sectors": [16, 17]
            },
            "false_wall_west": {
                "type": "territory",
                "connections": ["harg_pass", "pasty_mesa", "false_wall_south"],
                "occupants": [],
                "spice": 0,
                "sectors": [18, 19]
            },
            "red_chasm": {
                "type": "territory",
                "connections": ["sietch_tabr", "south_mesa", "rimwall_west"],
                "occupants": [],
                "spice": 0,
                "sectors": [20, 21]
            },
            "the_greater_flat": {
                "type": "territory",
                "connections": ["funeral_plain", "habbanya_ridge", "cielago_depression"],
                "occupants": [],
                "spice": 0,
                "sectors": [22, 23]
            },
            "cielago_depression": {
                "type": "territory",
                "connections": ["imperial_basin", "the_greater_flat", "south_mesa"],
                "occupants": [],
                "spice": 0,
                "sectors": [24, 25]
            },
            "south_mesa": {
                "type": "territory",
                "connections": ["red_chasm", "cielago_depression", "the_minor_erg"],
                "occupants": [],
                "spice": 0,
                "sectors": [26, 27]
            },
            "the_minor_erg": {
                "type": "territory",
                "connections": ["false_wall_south", "south_mesa", "pasty_mesa"],
                "occupants": [],
                "spice": 0,
                "sectors": [28, 29]
            },
            "pasty_mesa": {
                "type": "territory",
                "connections": ["false_wall_south", "false_wall_west", "the_minor_erg"],
                "occupants": [],
                "spice": 0,
                "sectors": [30, 31]
            },
            "rimwall_west": {
                "type": "territory",
                "connections": ["red_chasm"],
                "occupants": [],
                "spice": 0,
                "sectors": [32, 33]
            },
            "polar_sink": {
                "type": "special",
                "connections": [],
                "occupants": [],
                "spice": 0,
                "sectors": [34, 35]
            }
        }
        
        return {
            "territories": territories,
            "storm_position": 0,
            "sandworms": []
        }
    
    def _initialize_decks(self):
        # Creating actual Dune treachery cards
        self.treachery_deck = [
            {"id": "crysknife", "type": "weapon", "strength": 2, "name": "Crysknife"},
            {"id": "maula_pistol", "type": "weapon", "strength": 3, "name": "Maula Pistol"},
            {"id": "lasgun", "type": "weapon", "strength": 4, "name": "Lasgun"},
            {"id": "poison_blade", "type": "weapon", "strength": 5, "name": "Poison Blade"},
            {"id": "hunter_seeker", "type": "weapon", "strength": 3, "name": "Hunter Seeker"},
            {"id": "shield", "type": "defense", "strength": 1, "name": "Shield"},
            {"id": "snooper", "type": "defense", "strength": 2, "name": "Snooper"},
            {"id": "chemistry", "type": "defense", "strength": 3, "name": "Chemistry"},
            {"id": "tleilaxu_ghola", "type": "special", "name": "Tleilaxu Ghola"},
            {"id": "weather_control", "type": "special", "name": "Weather Control"},
            {"id": "karama", "type": "special", "name": "Karama"},
            {"id": "truthtrance", "type": "special", "name": "Truthtrance"},
            {"id": "family_atomics", "type": "weapon", "strength": 5, "name": "Family Atomics"},
            {"id": "poison_tooth", "type": "weapon", "strength": 4, "name": "Poison Tooth"},
            {"id": "cheap_hero", "type": "special", "name": "Cheap Hero"},
            {"id": "worthless_1", "type": "worthless", "name": "Worthless Card"},
            {"id": "worthless_2", "type": "worthless", "name": "Worthless Card"},
            {"id": "worthless_3", "type": "worthless", "name": "Worthless Card"}
        ]
        
        random.shuffle(self.treachery_deck)
        
        # Creating spice blow cards
        self.spice_deck = []
        for i in range(20):
            self.spice_deck.append({
                "territory": random.choice(list(self.board["territories"].keys())),
                "amount": random.randint(2, 5),
                "sandworm": random.random() < 0.3
            })
    
    def setup_game(self, player_configs: List[Dict]) -> Dict:
        if len(player_configs) != 6:
            raise ValueError("Dune requires exactly 6 players")
        
        # Actual Dune factions with their abilities
        factions = {
            "atreides": {
                "name": "House Atreides",
                "special_ability": "prescience",
                "starting_forces": 10,
                "starting_spice": 10,
                "strongholds": ["arrakeen"],
                "ally_bonus": "See one random treachery card from battle opponent"
            },
            "harkonnen": {
                "name": "House Harkonnen",
                "special_ability": "treachery",
                "starting_forces": 10,
                "starting_spice": 10,
                "strongholds": ["carthag"],
                "ally_bonus": "Can use two treachery cards in battle"
            },
            "emperor": {
                "name": "Emperor",
                "special_ability": "sardaukar",
                "starting_forces": 10,
                "starting_spice": 10,
                "strongholds": [],
                "ally_bonus": "Sardaukar are worth 2 strength each"
            },
            "guild": {
                "name": "Spacing Guild",
                "special_ability": "movement",
                "starting_forces": 5,
                "starting_spice": 5,
                "strongholds": ["tueks_sietch"],
                "ally_bonus": "Free shipment for ally"
            },
            "bene_gesserit": {
                "name": "Bene Gesserit",
                "special_ability": "voice",
                "starting_forces": 1,
                "starting_spice": 5,
                "strongholds": [],
                "ally_bonus": "Use voice in battle"
            },
            "fremen": {
                "name": "Fremen",
                "special_ability": "desert_power",
                "starting_forces": 10,
                "starting_spice": 3,
                "strongholds": ["sietch_tabr"],
                "ally_bonus": "Half price desert movement"
            }
        }
        
        faction_names = list(factions.keys())
        self.players = []
        
        for idx, config in enumerate(player_configs):
            faction_key = faction_names[idx]
            faction = factions[faction_key]
            
            player = {
                "name": config.get("name", f"Player{idx}"),
                "id": idx,
                "faction": faction_key,
                "faction_data": faction,
                "spice": faction["starting_spice"],
                "forces": faction["starting_forces"],
                "forces_reserve": 10,
                "treachery_cards": [],
                "leaders": self._get_faction_leaders(faction_key),
                "controlled_territories": faction["strongholds"].copy(),
                "alliances": []
            }
            
            # Draw initial treachery cards
            for _ in range(4):
                if self.treachery_deck:
                    player["treachery_cards"].append(self.treachery_deck.pop())
            
            self.players.append(player)
        
        self._initialize_decks()
        
        # Place initial forces
        for player in self.players:
            for stronghold in player["faction_data"]["strongholds"]:
                if stronghold in self.board["territories"]:
                    self.board["territories"][stronghold]["occupants"].append({
                        "player_id": player["id"],
                        "forces": player["forces"]
                    })
        
        return self.get_game_state()
    
    def _get_faction_leaders(self, faction: str) -> List[Dict]:
        leaders = {
            "atreides": [
                {"name": "Paul Atreides", "strength": 5, "alive": True},
                {"name": "Leto Atreides", "strength": 3, "alive": True},
                {"name": "Gurney Halleck", "strength": 4, "alive": True},
                {"name": "Duncan Idaho", "strength": 2, "alive": True},
                {"name": "Thufir Hawat", "strength": 5, "alive": True}
            ],
            "harkonnen": [
                {"name": "Baron Harkonnen", "strength": 4, "alive": True},
                {"name": "Feyd-Rautha", "strength": 6, "alive": True},
                {"name": "Beast Rabban", "strength": 4, "alive": True},
                {"name": "Piter de Vries", "strength": 3, "alive": True},
                {"name": "Captain Iakin", "strength": 2, "alive": True}
            ],
            "emperor": [
                {"name": "Shaddam IV", "strength": 5, "alive": True},
                {"name": "Bashar", "strength": 5, "alive": True},
                {"name": "Captain Aramsham", "strength": 2, "alive": True},
                {"name": "Burseg", "strength": 3, "alive": True},
                {"name": "Caid", "strength": 3, "alive": True}
            ],
            "guild": [
                {"name": "Steersman", "strength": 5, "alive": True},
                {"name": "Guild Rep", "strength": 3, "alive": True},
                {"name": "Master Bewt", "strength": 2, "alive": True},
                {"name": "Guild Agent", "strength": 1, "alive": True},
                {"name": "Navigator", "strength": 4, "alive": True}
            ],
            "bene_gesserit": [
                {"name": "Reverend Mother", "strength": 5, "alive": True},
                {"name": "Princess Irulan", "strength": 1, "alive": True},
                {"name": "Wanna Marcus", "strength": 1, "alive": True},
                {"name": "Lady Margot", "strength": 2, "alive": True},
                {"name": "Captain Arkie", "strength": 2, "alive": True}
            ],
            "fremen": [
                {"name": "Stilgar", "strength": 6, "alive": True},
                {"name": "Chani", "strength": 3, "alive": True},
                {"name": "Otheym", "strength": 4, "alive": True},
                {"name": "Shadout Mapes", "strength": 2, "alive": True},
                {"name": "Jamis", "strength": 2, "alive": True}
            ]
        }
        
        return leaders.get(faction, [])
    
    def get_game_state(self) -> Dict:
        return {
            "turn": self.current_turn,
            "round": self.round_number,
            "phase": self.current_phase,
            "storm_position": self.storm_position,
            "board": self.board,
            "players": self.players,
            "current_player": self.players[self.current_turn % len(self.players)] if self.players else None,
            "spice_deck_remaining": len(self.spice_deck)
        }
    
    def get_available_actions(self, player_id: int) -> List[Dict]:
        if not self.players or player_id >= len(self.players):
            return []
        
        player = self.players[player_id]
        actions = []
        
        if self.current_phase == "bidding":
            # Bidding on treachery cards
            for amount in range(0, min(player["spice"] + 1, 20)):
                actions.append({
                    "id": f"bid_{amount}",
                    "type": "bid",
                    "amount": amount,
                    "description": f"Bid {amount} spice for treachery card"
                })
        
        elif self.current_phase == "revival":
            # Revive forces from Tleilaxu tanks
            revival_costs = [2, 2, 2, 3, 3, 3, 4, 4, 4, 5]
            for i in range(min(len(revival_costs), player["forces_reserve"])):
                cost = revival_costs[i]
                if player["spice"] >= cost:
                    actions.append({
                        "id": f"revive_{i+1}",
                        "type": "revive",
                        "forces": i + 1,
                        "cost": sum(revival_costs[:i+1]),
                        "description": f"Revive {i+1} forces for {sum(revival_costs[:i+1])} spice"
                    })
        
        elif self.current_phase == "shipment":
            # Ship forces from reserves
            for territory in player["controlled_territories"]:
                for forces in range(1, min(player["forces_reserve"] + 1, 8)):
                    cost = 1 if player["faction"] == "guild" else forces
                    if player["spice"] >= cost:
                        actions.append({
                            "id": f"ship_{territory}_{forces}",
                            "type": "shipment",
                            "territory": territory,
                            "forces": forces,
                            "cost": cost,
                            "description": f"Ship {forces} forces to {territory} for {cost} spice"
                        })
        
        elif self.current_phase == "movement":
            # Movement actions
            for territory, data in self.board["territories"].items():
                for occupant in data["occupants"]:
                    if occupant["player_id"] == player_id:
                        for connected in data["connections"]:
                            movement_cost = self._calculate_movement_cost(
                                player, territory, connected, occupant["forces"]
                            )
                            
                            if player["spice"] >= movement_cost:
                                actions.append({
                                    "id": f"move_{territory}_{connected}",
                                    "type": "movement",
                                    "from": territory,
                                    "to": connected,
                                    "forces": occupant["forces"],
                                    "cost": movement_cost,
                                    "description": f"Move {occupant['forces']} from {territory} to {connected}"
                                })
        
        elif self.current_phase == "battle":
            # Battle actions - select leader and treachery cards
            for leader in player["leaders"]:
                if leader["alive"]:
                    for weapon in [None] + [c for c in player["treachery_cards"] if c.get("type") == "weapon"]:
                        for defense in [None] + [c for c in player["treachery_cards"] if c.get("type") == "defense"]:
                            actions.append({
                                "id": f"battle_{leader['name']}_{weapon['id'] if weapon else 'none'}_{defense['id'] if defense else 'none'}",
                                "type": "battle_plan",
                                "leader": leader,
                                "weapon": weapon,
                                "defense": defense,
                                "description": f"Fight with {leader['name']}" + 
                                             (f" using {weapon['name']}" if weapon else "") +
                                             (f" and {defense['name']}" if defense else "")
                            })
        
        elif self.current_phase == "spice_collection":
            # Collect spice from occupied territories
            for territory, data in self.board["territories"].items():
                if data["spice"] > 0:
                    for occupant in data["occupants"]:
                        if occupant["player_id"] == player_id:
                            actions.append({
                                "id": f"collect_{territory}",
                                "type": "collect_spice",
                                "territory": territory,
                                "amount": data["spice"],
                                "description": f"Collect {data['spice']} spice from {territory}"
                            })
        
        actions.append({
            "id": "pass",
            "type": "pass",
            "description": "Pass current phase"
        })
        
        return actions
    
    def _calculate_movement_cost(self, player: Dict, from_territory: str, 
                                 to_territory: str, forces: int) -> int:
        # Fremen pay half for desert movement
        if player["faction"] == "fremen":
            if self.board["territories"][to_territory]["type"] != "stronghold":
                return max(1, forces // 2)
        
        # Guild faction gets free movement
        if player["faction"] == "guild":
            return 0
        
        return forces
    
    def execute_action(self, player_id: int, action: Dict) -> Dict:
        if not self.players or player_id >= len(self.players):
            return {"success": False, "error": "Invalid player"}
        
        player = self.players[player_id]
        action_type = action.get("type")
        
        if action_type == "bid":
            return self._execute_bid(player, action)
        elif action_type == "revive":
            return self._execute_revive(player, action)
        elif action_type == "shipment":
            return self._execute_shipment(player, action)
        elif action_type == "movement":
            return self._execute_movement(player, action)
        elif action_type == "battle_plan":
            return self._execute_battle(player, action)
        elif action_type == "collect_spice":
            return self._execute_collect(player, action)
        elif action_type == "pass":
            return {"success": True, "action": "pass"}
        
        return {"success": False, "error": "Unknown action"}
    
    def _execute_bid(self, player: Dict, action: Dict) -> Dict:
        amount = action.get("amount", 0)
        
        if player["spice"] < amount:
            return {"success": False, "error": "Insufficient spice"}
        
        player["spice"] -= amount
        
        if self.treachery_deck:
            card = self.treachery_deck.pop()
            player["treachery_cards"].append(card)
            
            return {
                "success": True,
                "action": "bid",
                "amount": amount,
                "card_received": card["name"]
            }
        
        return {"success": False, "error": "No cards available"}
    
    def _execute_revive(self, player: Dict, action: Dict) -> Dict:
        forces = action.get("forces", 0)
        cost = action.get("cost", 0)
        
        if player["spice"] < cost:
            return {"success": False, "error": "Insufficient spice"}
        
        if player["forces_reserve"] < forces:
            return {"success": False, "error": "Not enough forces in reserve"}
        
        player["spice"] -= cost
        player["forces_reserve"] -= forces
        player["forces"] += forces
        
        return {
            "success": True,
            "action": "revive",
            "forces": forces,
            "cost": cost
        }
    
    def _execute_shipment(self, player: Dict, action: Dict) -> Dict:
        territory = action.get("territory")
        forces = action.get("forces", 0)
        cost = action.get("cost", 0)
        
        if player["spice"] < cost:
            return {"success": False, "error": "Insufficient spice"}
        
        if player["forces_reserve"] < forces:
            return {"success": False, "error": "Not enough forces"}
        
        player["spice"] -= cost
        player["forces_reserve"] -= forces
        
        # Add forces to territory
        territory_data = self.board["territories"][territory]
        existing = next((o for o in territory_data["occupants"] if o["player_id"] == player["id"]), None)
        
        if existing:
            existing["forces"] += forces
        else:
            territory_data["occupants"].append({
                "player_id": player["id"],
                "forces": forces
            })
        
        return {
            "success": True,
            "action": "shipment",
            "territory": territory,
            "forces": forces,
            "cost": cost
        }
    
    def _execute_movement(self, player: Dict, action: Dict) -> Dict:
        from_territory = action.get("from")
        to_territory = action.get("to")
        forces = action.get("forces", 0)
        cost = action.get("cost", 0)
        
        if player["spice"] < cost:
            return {"success": False, "error": "Insufficient spice"}
        
        player["spice"] -= cost
        
        # Remove from source
        from_data = self.board["territories"][from_territory]
        occupant = next((o for o in from_data["occupants"] if o["player_id"] == player["id"]), None)
        
        if not occupant or occupant["forces"] < forces:
            return {"success": False, "error": "Not enough forces"}
        
        occupant["forces"] -= forces
        if occupant["forces"] == 0:
            from_data["occupants"].remove(occupant)
        
        # Add to destination
        to_data = self.board["territories"][to_territory]
        existing = next((o for o in to_data["occupants"] if o["player_id"] == player["id"]), None)
        
        if existing:
            existing["forces"] += forces
        else:
            to_data["occupants"].append({
                "player_id": player["id"],
                "forces": forces
            })
        
        return {
            "success": True,
            "action": "movement",
            "from": from_territory,
            "to": to_territory,
            "forces": forces
        }
    
    def _execute_battle(self, player: Dict, action: Dict) -> Dict:
        leader = action.get("leader")
        weapon = action.get("weapon")
        defense = action.get("defense")
        
        total_strength = leader["strength"]
        
        if weapon:
            total_strength += weapon.get("strength", 0)
            player["treachery_cards"].remove(weapon)
        
        return {
            "success": True,
            "action": "battle_plan",
            "leader": leader["name"],
            "total_strength": total_strength,
            "weapon_used": weapon["name"] if weapon else None,
            "defense_used": defense["name"] if defense else None
        }
    
    def _execute_collect(self, player: Dict, action: Dict) -> Dict:
        territory = action.get("territory")
        amount = action.get("amount", 0)
        
        territory_data = self.board["territories"][territory]
        
        if territory_data["spice"] < amount:
            return {"success": False, "error": "Not enough spice"}
        
        territory_data["spice"] -= amount
        player["spice"] += amount
        
        return {
            "success": True,
            "action": "collect_spice",
            "territory": territory,
            "amount": amount,
            "new_total": player["spice"]
        }
    
    def advance_storm(self):
        # Storm moves 1-6 sectors clockwise
        movement = random.randint(1, 6)
        self.storm_position = (self.storm_position + movement) % 18
        
        # Remove forces caught in storm
        for territory, data in self.board["territories"].items():
            if self.storm_position in data["sectors"]:
                for occupant in data["occupants"]:
                    player = self.players[occupant["player_id"]]
                    player["forces_reserve"] += occupant["forces"]
                
                data["occupants"] = []

    def advance_turn(self):
        self.current_turn += 1
        
        phases = ["storm", "spice_blow", "bidding", "revival", "shipment", "movement", "battle", "spice_collection", "mentat_pause"]
        
        current_phase_index = phases.index(self.current_phase)
        next_phase_index = (current_phase_index + 1) % len(phases)
        
        self.current_phase = phases[next_phase_index]
        
        if self.current_phase == "storm":
            self.round_number += 1
            self.advance_storm()