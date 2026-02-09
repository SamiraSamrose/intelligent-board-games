from typing import Dict, List
import asyncio

class DecisionEngine:
    def __init__(self, collective_reasoning, character_trainer):
        self.collective = collective_reasoning
        self.trainer = character_trainer
        
    async def process_turn(self, game_name: str, game_state: Dict, 
                          ai_character: str, available_actions: List[Dict]) -> Dict:
        decision = await self.collective.make_collective_decision(
            game_state=game_state,
            character_name=ai_character,
            available_actions=available_actions
        )
        
        decision['timestamp'] = game_state.get('timestamp', '')
        decision['turn_number'] = game_state.get('turn', 0)
        decision['game'] = game_name
        
        return decision
    
    async def evaluate_options(self, game_state: Dict, character: str, 
                              options: List[Dict]) -> List[Dict]:
        evaluations = []
        
        for option in options:
            eval_context = {
                **game_state,
                'evaluating_option': option
            }
            
            decision = await self.collective.make_collective_decision(
                game_state=eval_context,
                character_name=character,
                available_actions=[option]
            )
            
            evaluations.append({
                'option': option,
                'evaluation': decision,
                'score': decision.get('confidence', 0.0)
            })
        
        evaluations.sort(key=lambda x: x['score'], reverse=True)
        return evaluations
