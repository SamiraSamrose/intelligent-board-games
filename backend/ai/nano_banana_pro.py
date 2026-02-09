import asyncio
from typing import Dict, List
import numpy as np

class NanoBananaPro:
    def __init__(self):
        self.character_embeddings = {}
        self.behavioral_patterns = {}
        self.decision_cache = {}
        
    async def train_character_personality(self, character_name: str, 
                                         game_type: str,
                                         personality_data: Dict) -> Dict:
        embedding = self._create_personality_embedding(personality_data)
        
        key = f"{game_type}_{character_name}"
        self.character_embeddings[key] = embedding
        
        behavioral_model = self._build_behavioral_model(personality_data)
        self.behavioral_patterns[key] = behavioral_model
        
        return {
            "character": character_name,
            "embedding_dimensions": len(embedding),
            "behavioral_rules": len(behavioral_model),
            "training_complete": True
        }
    
    def _create_personality_embedding(self, personality_data: Dict) -> np.ndarray:
        features = []
        
        personality = personality_data.get('personality', {})
        features.extend([
            personality.get('extraversion', 0.5),
            personality.get('agreeableness', 0.5),
            personality.get('conscientiousness', 0.5),
            personality.get('neuroticism', 0.5),
            personality.get('openness', 0.5)
        ])
        
        decision_weights = personality_data.get('decision_weights', {})
        features.extend([
            decision_weights.get('economic', 0.5),
            decision_weights.get('military', 0.5),
            decision_weights.get('diplomatic', 0.5),
            decision_weights.get('aggressive', 0.5),
            decision_weights.get('defensive', 0.5)
        ])
        
        features.append(personality_data.get('risk_tolerance', 0.5))
        features.append(personality_data.get('cooperation_level', 0.5))
        
        skills = personality_data.get('skills', [])
        features.append(len(skills) / 10.0)
        
        motivations = personality_data.get('motivations', [])
        features.append(len(motivations) / 10.0)
        
        return np.array(features, dtype=np.float32)
    
    def _build_behavioral_model(self, personality_data: Dict) -> Dict:
        model = {
            'action_preferences': {},
            'situation_responses': {},
            'interaction_patterns': {}
        }
        
        personality = personality_data.get('personality', {})
        
        if personality.get('extraversion', 0.5) > 0.6:
            model['action_preferences']['social'] = 0.8
            model['interaction_patterns']['initiative'] = 0.7
        else:
            model['action_preferences']['solo'] = 0.8
            model['interaction_patterns']['reactive'] = 0.7
        
        if personality.get('agreeableness', 0.5) > 0.6:
            model['interaction_patterns']['cooperation'] = 0.9
            model['situation_responses']['conflict'] = 'avoid'
        else:
            model['interaction_patterns']['competition'] = 0.9
            model['situation_responses']['conflict'] = 'engage'
        
        if personality.get('conscientiousness', 0.5) > 0.6:
            model['action_preferences']['planning'] = 0.9
            model['situation_responses']['uncertainty'] = 'analyze'
        else:
            model['action_preferences']['improvisation'] = 0.9
            model['situation_responses']['uncertainty'] = 'act_quickly'
        
        risk_tolerance = personality_data.get('risk_tolerance', 0.5)
        if risk_tolerance > 0.7:
            model['action_preferences']['aggressive'] = 0.9
        elif risk_tolerance < 0.3:
            model['action_preferences']['conservative'] = 0.9
        else:
            model['action_preferences']['balanced'] = 0.8
        
        decision_weights = personality_data.get('decision_weights', {})
        for key, value in decision_weights.items():
            model['action_preferences'][key] = value
        
        return model
    
    async def predict_action(self, character_name: str, game_type: str,
                            available_actions: List[Dict],
                            game_context: Dict) -> Dict:
        key = f"{game_type}_{character_name}"
        
        if key not in self.character_embeddings:
            return available_actions[0] if available_actions else {}
        
        embedding = self.character_embeddings[key]
        behavioral_model = self.behavioral_patterns[key]
        
        action_scores = []
        
        for action in available_actions:
            score = self._score_action(action, behavioral_model, game_context, embedding)
            action_scores.append({
                'action': action,
                'score': score
            })
        
        action_scores.sort(key=lambda x: x['score'], reverse=True)
        
        top_action = action_scores[0]['action'] if action_scores else {}
        
        return {
            'selected_action': top_action,
            'confidence': action_scores[0]['score'] if action_scores else 0.0,
            'alternatives': [a['action'] for a in action_scores[1:4]]
        }
    
    def _score_action(self, action: Dict, behavioral_model: Dict,
                     context: Dict, embedding: np.ndarray) -> float:
        score = 0.5
        
        action_type = action.get('type', '')
        
        preferences = behavioral_model.get('action_preferences', {})
        
        if 'attack' in action_type or 'battle' in action_type:
            score += preferences.get('aggressive', 0.5) * 0.3
            score += preferences.get('military', 0.5) * 0.2
        
        if 'build' in action_type or 'construct' in action_type:
            score += preferences.get('economic', 0.5) * 0.3
            score += preferences.get('planning', 0.5) * 0.2
        
        if 'trade' in action_type or 'negotiate' in action_type:
            score += preferences.get('diplomatic', 0.5) * 0.3
            score += preferences.get('cooperation', 0.5) * 0.2
        
        if 'defend' in action_type or 'shield' in action_type:
            score += preferences.get('defensive', 0.5) * 0.3
            score += preferences.get('conservative', 0.5) * 0.2
        
        cost = action.get('cost', 0)
        if cost > 0:
            risk_tolerance = embedding[10] if len(embedding) > 10 else 0.5
            cost_factor = 1.0 - (cost / 100.0)
            score += cost_factor * risk_tolerance * 0.2
        
        if context.get('in_danger', False):
            responses = behavioral_model.get('situation_responses', {})
            if responses.get('conflict') == 'avoid':
                if 'retreat' in action_type or 'escape' in action_type:
                    score += 0.3
            else:
                if 'attack' in action_type or 'counter' in action_type:
                    score += 0.3
        
        return min(1.0, max(0.0, score))
    
    def get_character_profile(self, character_name: str, game_type: str) -> Dict:
        key = f"{game_type}_{character_name}"
        
        if key not in self.character_embeddings:
            return {}
        
        embedding = self.character_embeddings[key]
        behavioral_model = self.behavioral_patterns[key]
        
        return {
            'embedding': embedding.tolist(),
            'behavioral_model': behavioral_model,
            'trained': True
        }