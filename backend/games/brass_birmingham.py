from typing import Dict, List, Optional
import json

class BrassBirmingham:
    def __init__(self):
        self.players = []
        self.current_turn = 0
        self.current_phase = "canal"
        self.board = self._initialize_board()
        self.deck = self._initialize_deck()
        self.discarded = []
        
    def _initialize_board(self) -> Dict:
        cities = {
            "birmingham": {"connections": ["coventry", "walsall", "wolverhampton"], 
                          "industries": [], "beer": 0},
            "coventry": {"connections": ["birmingham", "nuneaton"], 
                        "industries": [], "beer": 0},
            "wolverhampton": {"connections": ["birmingham", "walsall", "kidderminster"], 
                             "industries": [], "beer": 0},
            "walsall": {"connections": ["birmingham", "wolverhampton", "cannock"], 
                       "industries": [], "beer": 0},
            "kidderminster": {"connections": ["wolverhampton", "worcester"], 
                             "industries": [], "beer": 0},
            "worcester": {"connections": ["kidderminster", "gloucester"], 
                         "industries": [], "beer": 0},
            "gloucester": {"connections": ["worcester"], "industries": [], "beer": 0},
            "nuneaton": {"connections": ["coventry", "tamworth"], 
                        "industries": [], "beer": 0},
            "tamworth": {"connections": ["nuneaton", "burton"], 
                        "industries": [], "beer": 0},
            "burton": {"connections": ["tamworth", "derby"], 
                      "industries": [], "beer": 0},
            "derby": {"connections": ["burton", "belper"], "industries": [], "beer": 0},
            "belper": {"connections": ["derby"], "industries": [], "beer": 0},
            "cannock": {"connections": ["walsall", "stafford"], 
                       "industries": [], "beer": 0},
            "stafford": {"connections": ["cannock", "stone"], 
                        "industries": [], "beer": 0},
            "stone": {"connections": ["stafford", "uttoxeter"], 
                     "industries": [], "beer": 0},
            "uttoxeter": {"connections": ["stone", "burton"], 
                         "industries": [], "beer": 0}
        }
        
        return {
            "cities": cities,
            "canals": [],
            "rails": [],
            "coal_market": [1, 1, 2, 2, 3, 3, 4, 4],
            "iron_market": [1, 1, 2, 2, 3, 3, 4, 4]
        }
    
    def _initialize_deck(self) -> List[Dict]:
        cards = []
        
        cities = list(self.board["cities"].keys())
        for city in cities:
            cards.extend([{"type": "location", "value": city}] * 2)
        
        industries = ["cotton", "coal", "iron", "pottery", "brewery", "manufacturer"]
        for industry in industries:
            cards.extend([{"type": "industry", "value": industry}] * 3)
        
        import random
        random.shuffle(cards)
        return cards
    
    def setup_game(self, player_names: List[str]) -> Dict:
        if len(player_names) != 4:
            raise ValueError("Brass Birmingham requires exactly 4 players")
        
        self.players = []
        for idx, name in enumerate(player_names):
            player = {
                "name": name,
                "id": idx,
                "money": 17 if idx < 2 else 17,
                "income": 10,
                "hand": [],
                "industries": {
                    "cotton": [1, 1, 1, 2, 2, 3, 3],
                    "coal": [1, 1, 2, 2, 3, 3],
                    "iron": [1, 1, 2, 2, 3, 3],
                    "pottery": [1, 1, 1, 2, 2],
                    "brewery": [1, 1, 1, 1],
                    "manufacturer": [1, 1, 1, 1]
                },
                "links": 10,
                "scored_industries": [],
                "score": 0
            }
            
            for _ in range(8):
                if self.deck:
                    player["hand"].append(self.deck.pop())
            
            self.players.append(player)
        
        return self.get_game_state()
    
    def get_game_state(self) -> Dict:
        return {
            "turn": self.current_turn,
            "phase": self.current_phase,
            "board": self.board,
            "players": self.players,
            "current_player": self.players[self.current_turn % len(self.players)] if self.players else None,
            "deck_remaining": len(self.deck)
        }
    
    def get_available_actions(self, player_id: int) -> List[Dict]:
        if not self.players or player_id >= len(self.players):
            return []
        
        player = self.players[player_id]
        actions = []
        
        for card in player["hand"]:
            if card["type"] == "location":
                city = card["value"]
                
                for industry_type in player["industries"]:
                    if player["industries"][industry_type]:
                        level = player["industries"][industry_type][0]
                        cost = self._calculate_build_cost(industry_type, level, city)
                        
                        if player["money"] >= cost:
                            actions.append({
                                "id": f"build_{industry_type}_{city}",
                                "type": "build",
                                "industry": industry_type,
                                "location": city,
                                "level": level,
                                "cost": cost,
                                "description": f"Build level {level} {industry_type} in {city} for £{cost}"
                            })
            
            elif card["type"] == "industry":
                industry_type = card["value"]
                for city in self.board["cities"]:
                    if player["industries"][industry_type]:
                        level = player["industries"][industry_type][0]
                        cost = self._calculate_build_cost(industry_type, level, city)
                        
                        if player["money"] >= cost:
                            actions.append({
                                "id": f"build_{industry_type}_{city}",
                                "type": "build",
                                "industry": industry_type,
                                "location": city,
                                "level": level,
                                "cost": cost,
                                "description": f"Build level {level} {industry_type} in {city} for £{cost}"
                            })
        
        for city1 in self.board["cities"]:
            for city2 in self.board["cities"][city1]["connections"]:
                link_cost = 3 if self.current_phase == "canal" else 5
                
                if player["money"] >= link_cost and player["links"] > 0:
                    actions.append({
                        "id": f"link_{city1}_{city2}",
                        "type": "link",
                        "from": city1,
                        "to": city2,
                        "cost": link_cost,
                        "description": f"Build link from {city1} to {city2} for £{link_cost}"
                    })
        
        actions.append({
            "id": "take_loan",
            "type": "loan",
            "amount": 30,
            "income_penalty": -3,
            "description": "Take £30 loan (reduce income by 3)"
        })
        
        actions.append({
            "id": "pass",
            "type": "pass",
            "description": "Pass turn"
        })
        
        return actions
    
    def _calculate_build_cost(self, industry: str, level: int, city: str) -> int:
        base_costs = {
            "cotton": [12, 16, 20],
            "coal": [8, 10, 12],
            "iron": [8, 10, 12],
            "pottery": [10, 14],
            "brewery": [6, 8, 10, 12],
            "manufacturer": [10, 14, 18, 22]
        }
        
        costs = base_costs.get(industry, [10])
        base_cost = costs[min(level - 1, len(costs) - 1)]
        
        if city == "birmingham":
            base_cost += 2
        
        return base_cost
    
    def execute_action(self, player_id: int, action: Dict) -> Dict:
        if not self.players or player_id >= len(self.players):
            return {"success": False, "error": "Invalid player"}
        
        player = self.players[player_id]
        action_type = action.get("type")
        
        if action_type == "build":
            return self._execute_build(player, action)
        elif action_type == "link":
            return self._execute_link(player, action)
        elif action_type == "loan":
            return self._execute_loan(player, action)
        elif action_type == "pass":
            return self._execute_pass(player, action)
        
        return {"success": False, "error": "Unknown action type"}
    
    def _execute_build(self, player: Dict, action: Dict) -> Dict:
        industry = action["industry"]
        location = action["location"]
        level = action["level"]
        cost = action["cost"]
        
        if player["money"] < cost:
            return {"success": False, "error": "Insufficient funds"}
        
        if not player["industries"][industry]:
            return {"success": False, "error": "No industries available"}
        
        player["money"] -= cost
        player["industries"][industry].pop(0)
        
        self.board["cities"][location]["industries"].append({
            "player": player["id"],
            "type": industry,
            "level": level,
            "flipped": False
        })
        
        if industry == "brewery":
            self.board["cities"][location]["beer"] += level
        
        return {
            "success": True,
            "action": "build",
            "details": f"Built level {level} {industry} in {location}",
            "new_money": player["money"]
        }
    
    def _execute_link(self, player: Dict, action: Dict) -> Dict:
        from_city = action["from"]
        to_city = action["to"]
        cost = action["cost"]
        
        if player["money"] < cost:
            return {"success": False, "error": "Insufficient funds"}
        
        if player["links"] <= 0:
            return {"success": False, "error": "No links available"}
        
        player["money"] -= cost
        player["links"] -= 1
        
        link_type = "canals" if self.current_phase == "canal" else "rails"
        self.board[link_type].append({
            "player": player["id"],
            "from": from_city,
            "to": to_city
        })
        
        return {
            "success": True,
            "action": "link",
            "details": f"Built link from {from_city} to {to_city}",
            "new_money": player["money"],
            "links_remaining": player["links"]
        }
    
    def _execute_loan(self, player: Dict, action: Dict) -> Dict:
        player["money"] += 30
        player["income"] = max(player["income"] - 3, 0)
        
        return {
            "success": True,
            "action": "loan",
            "details": "Took £30 loan",
            "new_money": player["money"],
            "new_income": player["income"]
        }
    
    def _execute_pass(self, player: Dict, action: Dict) -> Dict:
        return {
            "success": True,
            "action": "pass",
            "details": f"Player {player['name']} passed"
        }
    
    def advance_turn(self):
        self.current_turn += 1
        
        if self.current_turn % (len(self.players) * 2) == 0:
            if self.current_phase == "canal":
                self.current_phase = "rail"
                self._phase_transition()

    def advance_turn(self):
        self.current_turn += 1
        
        if self.current_turn % (len(self.players) * 2) == 0:
            if self.current_phase == "canal":
                self.current_phase = "rail"
                self._phase_transition()
            elif self.current_phase == "rail":
                self._game_end()
    
    def _phase_transition(self):
        for player in self.players:
            player["hand"] = []
            for _ in range(8):
                if self.deck:
                    player["hand"].append(self.deck.pop())
            
            player["income_collected"] = False
        
        self.board["canals"] = []
    
    def _game_end(self):
        for player in self.players:
            for territory, data in self.board["cities"].items():
                for industry in data["industries"]:
                    if industry["player"] == player["id"] and not industry["flipped"]:
                        industry["flipped"] = True
                        player["score"] += industry["level"]
            
            player["score"] += player["money"] // 10
