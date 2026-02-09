import google.generativeai as genai
from typing import Dict, List, Optional
import asyncio

class GeminiController:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.models = {
            'reasoning': genai.GenerativeModel('gemini-2.0-flash-exp'),
            'fast': genai.GenerativeModel('gemini-1.5-flash')
        }
        
    async def generate_response(self, prompt: str, 
                               model_type: str = 'reasoning') -> str:
        model = self.models.get(model_type, self.models['reasoning'])
        
        try:
            response = await asyncio.to_thread(
                model.generate_content,
                prompt
            )
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def batch_generate(self, prompts: List[str], 
                            model_type: str = 'reasoning') -> List[str]:
        tasks = [self.generate_response(p, model_type) for p in prompts]
        return await asyncio.gather(*tasks)
