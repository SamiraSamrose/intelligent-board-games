from typing import Dict, List
import random

class TerraformingMars:
    def __init__(self):
        self.players = []
        self.current_turn = 0
        self.generation = 1
        self.global_parameters = {
            "temperature": -30,
            "oxygen": 0,
            "oceans": 0
        }
        self.board = self._initialize_board()
        self.cards = self._initialize_cards()
        
    def _initialize_board(self) -> Dict:
        return {
            "tiles": {},
            "milestones": {
                "terraformer": {"claimed": False, "player": None},
                "mayor": {"claimed": False, "player": None},
                "gardener": {"claimed": False, "player": None},
                "builder": {"claimed": False, "player": None},
                "planner": {"claimed": False, "player": None}
            },
            "awards": {
                "landlord": {"funded": False, "player": None},
                "banker": {"funded": False, "player": None},
                "scientist": {"funded": False, "player": None},
                "thermalist": {"funded": False, "player": None},
                "miner": {"funded": False, "player": None}
            }
        }
    
    def _initialize_cards(self) -> List[Dict]:
        return [
            {"id": "ai_central", "name": "AI Central", "cost": 21, "tags": ["science", "building"],
             "effects": {"vp": 1, "cards_per_gen": 2}},
            {"id": "asteroid", "name": "Asteroid", "cost": 14, "tags": ["space"],
             "effects": {"temperature": 1, "titanium": 2}},
            {"id": "comet", "name": "Comet", "cost": 21, "tags": ["space"],
             "effects": {"temperature": 1, "ocean": 1}},
            {"id": "big_asteroid", "name": "Big Asteroid", "cost": 27, "tags": ["space"],
             "effects": {"temperature": 2, "titanium": 4}},
            {"id": "water_import", "name": "Water Import from Europa", "cost": 25, "tags": ["space", "jovian"],
             "effects": {"ocean": 1, "vp": 1}},
            {"id": "space_elevator", "name": "Space Elevator", "cost": 27, "tags": ["space", "building"],
             "effects": {"titanium_value": 1, "vp": 2}},
            {"id": "development_center", "name": "Development Center", "cost": 11, "tags": ["science", "building"],
             "effects": {"cards": 1}},
            {"id": "fusion_power", "name": "Fusion Power", "cost": 14, "tags": ["science", "power", "building"],
             "effects": {"energy": 3}},
            {"id": "geothermal", "name": "Geothermal Power", "cost": 11, "tags": ["power", "building"],
             "effects": {"energy": 2}},
            {"id": "trees", "name": "Trees", "cost": 13, "tags": ["plant"],
             "effects": {"oxygen": 1, "plant": 3, "vp": 1}},
            {"id": "fish", "name": "Fish", "cost": 9, "tags": ["animal"],
             "effects": {"animal_resource": 1, "vp_per_animal": 1}},
            {"id": "livestock", "name": "Livestock", "cost": 10, "tags": ["animal"],
             "effects": {"animal_resource": 1, "plant": -1}},
            {"id": "ironworks", "name": "Ironworks", "cost": 11, "tags": ["building"],
             "effects": {"oxygen": 1, "energy": -1}},
            {"id": "mine", "name": "Mine", "cost": 4, "tags": ["building"],
             "effects": {"steel": 1}},
            {"id": "aquifer", "name": "Aquifer Pumping", "cost": 18, "tags": [],
             "effects": {"ocean": 1}}
        ]
    
    def setup_game(self, player_names: List[str]) -> Dict:
        if len(player_names) != 5:
            raise ValueError("Terraforming Mars requires exactly 5 players")
        
        self.players = []
        
        corporations = ["Credicor", "Ecoline", "Helion", "Mining Guild", "Tharsis Republic"]
        
        for idx, name in enumerate(player_names):
            corp = corporations[idx]
            
            player = {
                "name": name,
                "id": idx,
                "corporation": corp,
                "megacredits": self._get_starting_credits(corp),
                "steel": 0,
                "titanium": 0,
                "plants": 0,
                "energy": 0,
                "heat": 0,
                "production": {
                    "megacredits": self._get_starting_production(corp),
                    "steel": 0,
                    "titanium": 0,
                    "plants": 0,
                    "energy": 0,
                    "heat": 0
                },
                "cards": [],
                "played_cards": [],
                "terraform_rating": 20,
                "vp": 0
            }
            
            starting_cards = random.sample(self.cards, 10)
            player["cards"] = starting_cards
            
            self.players.append(player)
        
        return self.get_game_state()
    
    def _get_starting_credits(self, corp: str) -> int:
        credits = {
            "Credicor": 57,
            "Ecoline": 36,
            "Helion": 42,
            "Mining Guild": 30,
            "Tharsis Republic": 40
        }
        return credits.get(corp, 40)
    
    def _get_starting_production(self, corp: str) -> int:
        production = {
            "Credicor": 0,
            "Ecoline": 0,
            "Helion": 0,
            "Mining Guild": 0,
            "Tharsis Republic": 0
        }
        return production.get(corp, 0)
    
    def get_game_state(self) -> Dict:
        return {
            "turn": self.current_turn,
            "generation": self.generation,
            "global_parameters": self.global_parameters,
            "board": self.board,
            "players": self.players,
            "current_player": self.players[self.current_turn % len(self.players)] if self.players else None,
            "game_end": self._check_game_end()
        }
    
    def _check_game_end(self) -> bool:
        return (self.global_parameters["temperature"] >= 8 and
                self.global_parameters["oxygen"] >= 14 and
                self.global_parameters["oceans"] >= 9)
    
    def get_available_actions(self, player_id: int) -> List[Dict]:
        if not self.players or player_id >= len(self.players):
            return []
        
        player = self.players[player_id]
        actions = []
        
        for card in player["cards"]:
            cost = card["cost"]
            
            steel_discount = card["tags"].count("building") * 2
            titanium_discount = card["tags"].count("space") * 3
            
            can_afford = player["megacredits"] >= cost - steel_discount - titanium_discount
            
            if can_afford:
                actions.append({
                    "id": f"play_{card['id']}",
                    "type": "play_card",
                    "card": card,
                    "cost": cost,
                    "description": f"Play {card['name']} for {cost} MC"
                })
        
        standard_projects = [
            {
                "id": "sell_patents",
                "type": "standard_project",
                "name": "Sell Patents",
                "cost": 0,
                "effect": "Discard cards for 1 MC each",
                "description": "Sell patents for credits"
            },
            {
                "id": "power_plant",
                "type": "standard_project",
                "name": "Power Plant",
                "cost": 11,
                "effect": "Increase energy production by 1",
                "description": "Build power plant for 11 MC"
            },
            {
                "id": "asteroid_project",
                "type": "standard_project",
                "name": "Asteroid",
                "cost": 14,
                "effect": "Increase temperature by 1",
                "description": "Send asteroid for 14 MC"
            },
            {
                "id": "aquifer_project",
                "type": "standard_project",
                "name": "Aquifer",
                "cost": 18,
                "effect": "Place ocean tile",
                "description": "Create aquifer for 18 MC"
            },
            {
                "id": "greenery_project",
                "type": "standard_project",
                "name": "Greenery",
                "cost": 23,
                "effect": "Place greenery tile, increase oxygen by 1",
                "description": "Plant greenery for 23 MC"
            },
            {
                "id": "city_project",
                "type": "standard_project",
                "name": "City",
                "cost": 25,
                "effect": "Place city tile",
                "description": "Build city for 25 MC"
            }
        ]
        
        for project in standard_projects:
            if player["megacredits"] >= project["cost"]:
                actions.append(project)
        
        if player["plants"] >= 8:
            actions.append({
                "id": "convert_plants",
                "type": "convert",
                "resource": "plants",
                "description": "Convert 8 plants to greenery"
            })
        
        if player["heat"] >= 8:
            actions.append({
                "id": "convert_heat",
                "type": "convert",
                "resource": "heat",
                "description": "Convert 8 heat to raise temperature"
            })
        
        actions.append({
            "id": "pass",
            "type": "pass",
            "description": "Pass turn"
        })
        
        return actions
    
    def execute_action(self, player_id: int, action: Dict) -> Dict:
        if not self.players or player_id >= len(self.players):
            return {"success": False, "error": "Invalid player"}
        
        player = self.players[player_id]
        action_type = action.get("type")
        
        if action_type == "play_card":
            return self._execute_play_card(player, action)
        elif action_type == "standard_project":
            return self._execute_standard_project(player, action)
        elif action_type == "convert":
            return self._execute_convert(player, action)
        elif action_type == "pass":
            return self._execute_pass(player)
        
        return {"success": False, "error": "Unknown action"}
    
    def _execute_play_card(self, player: Dict, action: Dict) -> Dict:
        card = action.get("card")
        cost = card["cost"]
        
        if player["megacredits"] < cost:
            return {"success": False, "error": "Insufficient credits"}
        
        player["megacredits"] -= cost
        player["cards"].remove(card)
        player["played_cards"].append(card)
        
        effects = card.get("effects", {})
        results = []
        
        if "temperature" in effects:
            temp_increase = effects["temperature"]
            self.global_parameters["temperature"] = min(8, self.global_parameters["temperature"] + temp_increase * 2)
            player["terraform_rating"] += temp_increase
            results.append(f"Temperature +{temp_increase * 2}")
        
        if "oxygen" in effects:
            oxy_increase = effects["oxygen"]
            self.global_parameters["oxygen"] = min(14, self.global_parameters["oxygen"] + oxy_increase)
            player["terraform_rating"] += oxy_increase
            results.append(f"Oxygen +{oxy_increase}")
        
        if "ocean" in effects:
            ocean_increase = effects["ocean"]
            self.global_parameters["oceans"] = min(9, self.global_parameters["oceans"] + ocean_increase)
            player["terraform_rating"] += ocean_increase
            results.append(f"Ocean +{ocean_increase}")
        
        if "energy" in effects:
            player["production"]["energy"] += effects["energy"]
            results.append(f"Energy production +{effects['energy']}")
        
        if "vp" in effects:
            player["vp"] += effects["vp"]
            results.append(f"VP +{effects['vp']}")
        
        return {
            "success": True,
            "card": card["name"],
            "effects": results,
            "remaining_credits": player["megacredits"]
        }
    
    def _execute_standard_project(self, player: Dict, action: Dict) -> Dict:
        project_id = action.get("id")
        cost = action.get("cost", 0)
        
        if player["megacredits"] < cost:
            return {"success": False, "error": "Insufficient credits"}
        
        player["megacredits"] -= cost
        
        results = []
        
        if project_id == "power_plant":
            player["production"]["energy"] += 1
            results.append("Energy production +1")
        elif project_id == "asteroid_project":
            self.global_parameters["temperature"] = min(8, self.global_parameters["temperature"] + 2)
            player["terraform_rating"] += 1
            results.append("Temperature +2")
        elif project_id == "aquifer_project":
            self.global_parameters["oceans"] = min(9, self.global_parameters["oceans"] + 1)
            player["terraform_rating"] += 1
            results.append("Ocean +1")
        elif project_id == "greenery_project":
            self.global_parameters["oxygen"] = min(14, self.global_parameters["oxygen"] + 1)
            player["terraform_rating"] += 1
            results.append("Oxygen +1")
        
        return {
            "success": True,
            "project": action.get("name"),
            "effects": results,
            "remaining_credits": player["megacredits"]
        }
    
    def _execute_convert(self, player: Dict, action: Dict) -> Dict:
        resource = action.get("resource")
        
        if resource == "plants":
            if player["plants"] < 8:
                return {"success": False, "error": "Need 8 plants"}
            
            player["plants"] -= 8
            self.global_parameters["oxygen"] = min(14, self.global_parameters["oxygen"] + 1)
            player["terraform_rating"] += 1
            
            return {
                "success": True,
                "action": "convert_plants",
                "effect": "Oxygen +1"
            }
        
        elif resource == "heat":
            if player["heat"] < 8:
                return {"success": False, "error": "Need 8 heat"}
            
            player["heat"] -= 8
            self.global_parameters["temperature"] = min(8, self.global_parameters["temperature"] + 2)
            player["terraform_rating"] += 1
            
            return {
                "success": True,
                "action": "convert_heat",
                "effect": "Temperature +2"
            }
        
        return {"success": False, "error": "Invalid resource"}
    
    def _execute_pass(self, player: Dict) -> Dict:
        return {
            "success": True,
            "action": "pass"
        }
    def advance_turn(self):
        self.current_turn += 1
        
        if self.current_turn % len(self.players) == 0:
            self.generation += 1
            
            for player in self.players:
                player["megacredits"] += player["production"]["megacredits"]
                player["steel"] += player["production"]["steel"]
                player["titanium"] += player["production"]["titanium"]
                player["plants"] += player["production"]["plants"]
                player["energy"] += player["production"]["energy"]
                
                player["heat"] += player["energy"]
                player["energy"] = 0
                
                player["megacredits"] += player["terraform_rating"]
                
                if self.deck:
                    for _ in range(4):
                        if self.deck:
                            player["cards"].append(self.deck.pop())
