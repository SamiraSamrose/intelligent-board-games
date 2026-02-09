from typing import List, Dict
import asyncio

class CollectiveReasoning:
    def __init__(self, society_of_thought, persona_system, bias_masking):
        self.society = society_of_thought
        self.personas = persona_system
        self.bias = bias_masking
        
    async def make_collective_decision(self, game_state: Dict, 
                                      character_name: str,
                                      available_actions: List[Dict]) -> Dict:
        character_persona = self.personas.personas.get(character_name)
        
        if not character_persona:
            raise ValueError(f"Character {character_name} not initialized")
        
        context = self._build_decision_context(game_state, character_name)
        
        multi_perspective_reasoning = await self.society.generate_multi_perspective_reasoning(
            context=context,
            game_state=game_state
        )
        
        raw_decision = await self.personas.generate_character_decision(
            character_name=character_name,
            game_context=game_state,
            available_actions=available_actions
        )
        
        demographic_cues = {
            'character': character_name,
            'personality': character_persona['base_personality'],
            'historical_behavior': character_persona['interaction_history'][-5:]
        }
        
        final_decision = await self.bias.apply_bias_correction(
            decision_context=context,
            demographic_cues=demographic_cues,
            raw_decision=raw_decision
        )
        
        final_decision['society_reasoning'] = multi_perspective_reasoning
        final_decision['diversity_metrics'] = self.society.measure_diversity()
        
        return final_decision
    
    def _build_decision_context(self, game_state: Dict, character: str) -> str:
        lines = [
            f"Current player: {character}",
            f"Game phase: {game_state.get('phase', 'unknown')}",
            f"Turn: {game_state.get('turn', 0)}",
            f"Resources: {game_state.get('resources', {})}",
            f"Opponents: {game_state.get('other_players', [])}"
        ]
        return "\n".join(lines)
