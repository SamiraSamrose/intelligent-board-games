import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from models.society_of_thought import SocietyOfThought
from models.persona_system import PersonaSystem
from models.bias_masking import BiasMasking
from models.collective_reasoning import CollectiveReasoning
from ai.character_trainer import CharacterTrainer
from ai.decision_engine import DecisionEngine
from games.brass_birmingham import BrassBirmingham

async def test_brass_birmingham():
    print("Testing Brass Birmingham Integration...")
    
    api_key = os.getenv('GEMINI_API_KEY', 'test-key')
    
    society = SocietyOfThought(api_key)
    persona_system = PersonaSystem(api_key)
    bias_masking = BiasMasking(api_key, mode='mirror')
    collective = CollectiveReasoning(society, persona_system, bias_masking)
    trainer = CharacterTrainer(api_key)
    engine = DecisionEngine(collective, trainer)
    
    game = BrassBirmingham()
    players = ['Alice', 'Bob', 'Charlie', 'Diana']
    
    print("Setting up game...")
    game_state = game.setup_game(players)
    print(f"Game initialized with {len(game_state['players'])} players")
    
    character_data = await trainer.train_character(
        'brass_birmingham',
        'industrialist',
        'Strategic entrepreneur in Victorian Birmingham'
    )
    print(f"Character trained: {character_data}")
    
    persona_system.create_character_persona('industrialist', character_data)
    print("Persona created")
    
    society.create_perspective(
        personality_traits=character_data['personality'],
        expertise='economics',
        role='strategist'
    )
    print("Society perspective added")
    
    available_actions = game.get_available_actions(0)
    print(f"Available actions: {len(available_actions)}")
    
    if available_actions:
        decision = await engine.process_turn(
            game_name='brass_birmingham',
            game_state=game_state,
            ai_character='industrialist',
            available_actions=available_actions[:5]
        )
        print(f"AI Decision: {decision.get('action', {}).get('description', 'No action')}")
        print(f"Reasoning: {decision.get('reasoning', 'No reasoning')[:200]}...")
    
    print("\nTest completed successfully!")

if __name__ == '__main__':
    asyncio.run(test_brass_birmingham())