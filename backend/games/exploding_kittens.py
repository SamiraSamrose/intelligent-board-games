from typing import Dict, List
import random

class ExplodingKittens:
    def __init__(self):
        self.players = []
        self.current_turn = 0
        self.deck = []
        self.discard_pile = []
        self.exploded_players = []
        self.turn_count = 0
        
    def _initialize_deck(self, num_players: int) -> List[Dict]:
        deck = []
        
        # Core cards
        deck.extend([
            {"id": f"attack_{i}", "type": "attack", "name": "Attack"} 
            for i in range(4)
        ])
        deck.extend([
            {"id": f"skip_{i}", "type": "skip", "name": "Skip"} 
            for i in range(4)
        ])
        deck.extend([
            {"id": f"favor_{i}", "type": "favor", "name": "Favor"} 
            for i in range(4)
        ])
        deck.extend([
            {"id": f"shuffle_{i}", "type": "shuffle", "name": "Shuffle"} 
            for i in range(4)
        ])
        deck.extend([
            {"id": f"see_future_{i}", "type": "see_future", "name": "See the Future"} 
            for i in range(5)
        ])
        deck.extend([
            {"id": f"nope_{i}", "type": "nope", "name": "Nope"} 
            for i in range(5)
        ])
        
        # Cat cards (pairs for stealing)
        cat_types = ["tacocat", "rainbow_cat", "beard_cat", "cattermelon", "hairy_potato_cat"]
        for cat in cat_types:
            deck.extend([
                {"id": f"{cat}_{i}", "type": "cat", "subtype": cat, "name": cat.replace("_", " ").title()} 
                for i in range(4)
            ])
        
        # Defuse cards (num_players + 2 total, distribute to players + extras)
        defuse_cards = [
            {"id": f"defuse_{i}", "type": "defuse", "name": "Defuse"} 
            for i in range(num_players + 2)
        ]
        
        # Exploding kittens (num_players - 1)
        exploding_cards = [
            {"id": f"exploding_{i}", "type": "exploding", "name": "Exploding Kitten"} 
            for i in range(num_players - 1)
        ]
        
        random.shuffle(deck)
        
        return deck, defuse_cards, exploding_cards
    
    def setup_game(self, player_names: List[str]) -> Dict:
        if len(player_names) != 5:
            raise ValueError("Exploding Kittens requires exactly 5 players")
        
        # Initialize deck
        main_deck, defuse_cards, exploding_cards = self._initialize_deck(len(player_names))
        
        self.players = []
        
        # Deal cards to players
        for idx, name in enumerate(player_names):
            player = {
                "name": name,
                "id": idx,
                "hand": [],
                "alive": True,
                "turns_to_take": 1
            }
            
            # Deal 7 cards + 1 defuse
            for _ in range(7):
                if main_deck:
                    player["hand"].append(main_deck.pop())
            
            player["hand"].append(defuse_cards.pop())
            
            self.players.append(player)
        
        # Add remaining defuse cards to deck
        main_deck.extend(defuse_cards)
        
        # Shuffle and add exploding kittens
        random.shuffle(main_deck)
        main_deck.extend(exploding_cards)
        random.shuffle(main_deck)
        
        self.deck = main_deck
        
        return self.get_game_state()
    
    def get_game_state(self) -> Dict:
        return {
            "turn": self.current_turn,
            "turn_count": self.turn_count,
            "deck_remaining": len(self.deck),
            "players": self.players,
            "current_player": self.players[self.current_turn % len([p for p in self.players if p["alive"]])] if any(p["alive"] for p in self.players) else None,
            "discard_pile": self.discard_pile[-5:] if self.discard_pile else [],
            "exploded_players": self.exploded_players,
            "game_over": len([p for p in self.players if p["alive"]]) <= 1
        }
    
    def get_available_actions(self, player_id: int) -> List[Dict]:
        if not self.players or player_id >= len(self.players):
            return []
        
        player = self.players[player_id]
        
        if not player["alive"]:
            return []
        
        actions = []
        
        # Play cards from hand
        for card in player["hand"]:
            card_type = card["type"]
            
            if card_type == "attack":
                actions.append({
                    "id": f"play_{card['id']}",
                    "type": "play_card",
                    "card": card,
                    "description": f"Play {card['name']} - End turn without drawing, next player takes 2 turns"
                })
            
            elif card_type == "skip":
                actions.append({
                    "id": f"play_{card['id']}",
                    "type": "play_card",
                    "card": card,
                    "description": f"Play {card['name']} - End turn without drawing"
                })
            
            elif card_type == "favor":
                for target in self.players:
                    if target["id"] != player_id and target["alive"] and target["hand"]:
                        actions.append({
                            "id": f"play_{card['id']}_target_{target['id']}",
                            "type": "play_card",
                            "card": card,
                            "target": target["id"],
                            "description": f"Play {card['name']} on {target['name']} - Take a card from them"
                        })
            
            elif card_type == "shuffle":
                actions.append({
                    "id": f"play_{card['id']}",
                    "type": "play_card",
                    "card": card,
                    "description": f"Play {card['name']} - Shuffle the draw pile"
                })
            
            elif card_type == "see_future":
                actions.append({
                    "id": f"play_{card['id']}",
                    "type": "play_card",
                    "card": card,
                    "description": f"Play {card['name']} - See the top 3 cards"
                })
            
            elif card_type == "nope":
                # Nope can be played reactively
                actions.append({
                    "id": f"play_{card['id']}",
                    "type": "play_card",
                    "card": card,
                    "description": f"Play {card['name']} - Nope an action"
                })
            
            elif card_type == "cat":
                # Can play pairs to steal
                matching_cats = [c for c in player["hand"] 
                               if c["type"] == "cat" and c["subtype"] == card["subtype"] and c["id"] != card["id"]]
                
                if matching_cats:
                    for target in self.players:
                        if target["id"] != player_id and target["alive"] and target["hand"]:
                            actions.append({
                                "id": f"play_pair_{card['id']}_{matching_cats[0]['id']}_target_{target['id']}",
                                "type": "play_pair",
                                "cards": [card, matching_cats[0]],
                                "target": target["id"],
                                "description": f"Play pair of {card['name']} on {target['name']} - Steal a random card"
                            })
        
        # Draw card action (ends turn)
        actions.append({
            "id": "draw_card",
            "type": "draw",
            "description": "Draw a card from the deck"
        })
        
        return actions
    
    def execute_action(self, player_id: int, action: Dict) -> Dict:
        if not self.players or player_id >= len(self.players):
            return {"success": False, "error": "Invalid player"}
        
        player = self.players[player_id]
        
        if not player["alive"]:
            return {"success": False, "error": "Player is eliminated"}
        
        action_type = action.get("type")
        
        if action_type == "play_card":
            return self._execute_play_card(player, action)
        elif action_type == "play_pair":
            return self._execute_play_pair(player, action)
        elif action_type == "draw":
            return self._execute_draw(player)
        
        return {"success": False, "error": "Unknown action"}
    
    def _execute_play_card(self, player: Dict, action: Dict) -> Dict:
        card = action.get("card")
        
        if card not in player["hand"]:
            return {"success": False, "error": "Card not in hand"}
        
        player["hand"].remove(card)
        self.discard_pile.append(card)
        
        result = {
            "success": True,
            "action": "play_card",
            "card": card["name"],
            "effects": []
        }
        
        if card["type"] == "attack":
            # Next player takes 2 turns
            next_player_idx = (player["id"] + 1) % len(self.players)
            while not self.players[next_player_idx]["alive"]:
                next_player_idx = (next_player_idx + 1) % len(self.players)
            
            self.players[next_player_idx]["turns_to_take"] += 2
            player["turns_to_take"] -= 1
            
            result["effects"].append("Next player must take 2 turns")
        
        elif card["type"] == "skip":
            # End turn without drawing
            player["turns_to_take"] -= 1
            result["effects"].append("Turn ended without drawing")
        
        elif card["type"] == "favor":
            target_id = action.get("target")
            target = self.players[target_id]
            
            if target["hand"]:
                stolen_card = random.choice(target["hand"])
                target["hand"].remove(stolen_card)
                player["hand"].append(stolen_card)
                
                result["effects"].append(f"Received {stolen_card['name']} from {target['name']}")
        
        elif card["type"] == "shuffle":
            random.shuffle(self.deck)
            result["effects"].append("Deck shuffled")
        
        elif card["type"] == "see_future":
            top_cards = self.deck[-3:] if len(self.deck) >= 3 else self.deck[:]
            result["effects"].append(f"Top cards: {[c['name'] for c in reversed(top_cards)]}")
            result["revealed_cards"] = [c["name"] for c in reversed(top_cards)]
        
        return result
    
    def _execute_play_pair(self, player: Dict, action: Dict) -> Dict:
        cards = action.get("cards", [])
        
        for card in cards:
            if card in player["hand"]:
                player["hand"].remove(card)
                self.discard_pile.append(card)
        
        target_id = action.get("target")
        target = self.players[target_id]
        
        if target["hand"]:
            stolen_card = random.choice(target["hand"])
            target["hand"].remove(stolen_card)
            player["hand"].append(stolen_card)
            
            return {
                "success": True,
                "action": "play_pair",
                "cards_played": [c["name"] for c in cards],
                "stolen_card": stolen_card["name"],
                "from_player": target["name"]
            }
        
        return {
            "success": True,
            "action": "play_pair",
            "cards_played": [c["name"] for c in cards],
            "stolen_card": None
        }
    
    def _execute_draw(self, player: Dict) -> Dict:
        if not self.deck:
            return {"success": False, "error": "Deck is empty"}
        
        drawn_card = self.deck.pop()
        
        result = {
            "success": True,
            "action": "draw",
            "card_type": drawn_card["type"]
        }
        
        if drawn_card["type"] == "exploding":
            # Check for defuse card
            defuse_cards = [c for c in player["hand"] if c["type"] == "defuse"]
            
            if defuse_cards:
                # Player can defuse
                result["exploded"] = False
                result["can_defuse"] = True
                result["message"] = f"Drew Exploding Kitten! Use defuse card to survive."
                
                # Auto-use defuse
                defuse = defuse_cards[0]
                player["hand"].remove(defuse)
                self.discard_pile.append(defuse)
                
                # Put exploding kitten back in deck
                insert_position = random.randint(0, len(self.deck))
                self.deck.insert(insert_position, drawn_card)
                
                result["defused"] = True
                result["message"] += f" Defused! Exploding Kitten returned to deck."
            else:
                # Player explodes
                player["alive"] = False
                self.exploded_players.append(player["name"])
                
                result["exploded"] = True
                result["message"] = f"{player['name']} exploded!"
        else:
            player["hand"].append(drawn_card)
            result["card_drawn"] = drawn_card["name"]
            result["exploded"] = False
        
        # Decrease turns to take
        player["turns_to_take"] -= 1
        
        return result
    
    def advance_turn(self):
        # Find next alive player
        while True:
            self.current_turn = (self.current_turn + 1) % len(self.players)
            current_player = self.players[self.current_turn]
            
            if current_player["alive"]:
                if current_player["turns_to_take"] <= 0:
                    current_player["turns_to_take"] = 1
                break
        
        self.turn_count += 1