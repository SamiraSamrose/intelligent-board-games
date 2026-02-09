import google.generativeai as genai
from typing import List, Dict, Any
import asyncio
import json

class SocietyOfThought:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.perspectives = []
        self.conversation_history = []
        
    def create_perspective(self, personality_traits: Dict[str, float], 
                          expertise: str, role: str) -> Dict:
        perspective = {
            'personality': {
                'extraversion': personality_traits.get('extraversion', 0.5),
                'agreeableness': personality_traits.get('agreeableness', 0.5),
                'conscientiousness': personality_traits.get('conscientiousness', 0.5),
                'neuroticism': personality_traits.get('neuroticism', 0.5),
                'openness': personality_traits.get('openness', 0.5)
            },
            'expertise': expertise,
            'role': role,
            'activation_count': 0
        }
        self.perspectives.append(perspective)
        return perspective
    
    async def generate_multi_perspective_reasoning(self, context: str, 
                                                   game_state: Dict) -> str:
        reasoning_traces = []
        
        for idx, perspective in enumerate(self.perspectives):
            persona_prompt = self._build_persona_prompt(perspective, context, game_state)
            
            try:
                response = await asyncio.to_thread(
                    self.model.generate_content,
                    persona_prompt
                )
                
                reasoning_trace = {
                    'perspective_id': idx,
                    'personality': perspective['personality'],
                    'reasoning': response.text,
                    'role': perspective['role']
                }
                reasoning_traces.append(reasoning_trace)
                perspective['activation_count'] += 1
                
            except Exception as e:
                reasoning_traces.append({
                    'perspective_id': idx,
                    'error': str(e)
                })
        
        debate_result = await self._conduct_internal_debate(reasoning_traces, context)
        return debate_result
    
    def _build_persona_prompt(self, perspective: Dict, context: str, 
                             game_state: Dict) -> str:
        personality_desc = self._personality_to_description(perspective['personality'])
        
        prompt = f"""You are reasoning from a specific cognitive perspective with these traits:
{personality_desc}

Your role: {perspective['role']}
Your expertise: {perspective['expertise']}

Current game context:
{context}

Game state:
{json.dumps(game_state, indent=2)}

Provide your perspective on the best action to take. Consider:
1. Question current assumptions
2. Offer alternative viewpoints
3. Challenge weak reasoning
4. Reconcile conflicting ideas

Express uncertainty where appropriate. Use markers like "Wait", "However", "But" when shifting perspectives."""

        return prompt
    
    def _personality_to_description(self, personality: Dict) -> str:
        traits = []
        
        if personality['extraversion'] > 0.6:
            traits.append("outgoing and assertive")
        elif personality['extraversion'] < 0.4:
            traits.append("reserved and thoughtful")
            
        if personality['agreeableness'] > 0.6:
            traits.append("cooperative and trusting")
        elif personality['agreeableness'] < 0.4:
            traits.append("skeptical and challenging")
            
        if personality['conscientiousness'] > 0.6:
            traits.append("methodical and thorough")
        elif personality['conscientiousness'] < 0.4:
            traits.append("flexible and spontaneous")
            
        if personality['neuroticism'] > 0.6:
            traits.append("cautious and risk-aware")
        elif personality['neuroticism'] < 0.4:
            traits.append("calm and stable")
            
        if personality['openness'] > 0.6:
            traits.append("creative and exploratory")
        elif personality['openness'] < 0.4:
            traits.append("practical and traditional")
            
        return ", ".join(traits) if traits else "balanced"
    
    async def _conduct_internal_debate(self, reasoning_traces: List[Dict], 
                                      context: str) -> str:
        debate_prompt = f"""Multiple cognitive perspectives have analyzed this situation:

{self._format_perspectives(reasoning_traces)}

Now synthesize these perspectives into a coherent decision through internal debate:
1. Identify conflicts between perspectives
2. Verify assumptions through self-questioning
3. Backtrack on weak reasoning
4. Reconcile different viewpoints
5. Arrive at a final decision

Context: {context}

Provide the final decision with reasoning."""

        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                debate_prompt
            )
            return response.text
        except Exception as e:
            return reasoning_traces[0]['reasoning'] if reasoning_traces else ""
    
    def _format_perspectives(self, traces: List[Dict]) -> str:
        formatted = []
        for trace in traces:
            if 'error' not in trace:
                formatted.append(f"Perspective {trace['perspective_id']} ({trace['role']}):\n{trace['reasoning']}\n")
        return "\n".join(formatted)
    
    def measure_diversity(self) -> Dict[str, float]:
        if not self.perspectives:
            return {'personality_diversity': 0.0, 'activation_entropy': 0.0}
        
        personality_variance = {}
        for trait in ['extraversion', 'agreeableness', 'conscientiousness', 
                     'neuroticism', 'openness']:
            values = [p['personality'][trait] for p in self.perspectives]
            variance = sum((v - sum(values)/len(values))**2 for v in values) / len(values)
            personality_variance[trait] = variance
        
        activations = [p['activation_count'] for p in self.perspectives]
        total_activations = sum(activations)
        
        if total_activations > 0:
            entropy = -sum((a/total_activations) * (a/total_activations) 
                          for a in activations if a > 0)
        else:
            entropy = 0.0
        
        return {
            'personality_diversity': sum(personality_variance.values()) / len(personality_variance),
            'activation_entropy': entropy
        }
