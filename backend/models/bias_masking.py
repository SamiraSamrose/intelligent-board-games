import google.generativeai as genai
from typing import Dict, List
import asyncio

class BiasMasking:
    def __init__(self, api_key: str, mode: str = 'mirror'):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.mode = mode
        self.bias_log = []
        
    async def apply_bias_correction(self, decision_context: Dict, 
                                   demographic_cues: Dict,
                                   raw_decision: Dict) -> Dict:
        if self.mode == 'mirror':
            return await self._mirror_mode(decision_context, demographic_cues, 
                                          raw_decision)
        elif self.mode == 'mask':
            return await self._mask_mode(decision_context, demographic_cues, 
                                        raw_decision)
        else:
            return raw_decision
    
    async def _mirror_mode(self, context: Dict, demographics: Dict, 
                          decision: Dict) -> Dict:
        prompt = f"""You are analyzing a decision with full demographic context.
Mirror human decision patterns including their biases.

Decision context:
{context}

Demographic information:
{demographics}

Proposed decision:
{decision}

Adjust the decision to reflect realistic human biases based on demographics.
Consider:
- Gender-based leadership expectations
- Confidence-competence perception gaps
- Self-promotion patterns
- Peer evaluation biases

Return JSON with adjusted decision."""

        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            
            adjusted = self._parse_adjustment(response.text, decision)
            self._log_bias_adjustment('mirror', context, decision, adjusted)
            return adjusted
            
        except Exception:
            return decision
    
    async def _mask_mode(self, context: Dict, demographics: Dict, 
                        decision: Dict) -> Dict:
        prompt = f"""You are analyzing a decision to remove bias and optimize outcomes.
Mask human biases and select the most competent option.

Decision context:
{context}

Demographic information (use only to compensate for bias):
{demographics}

Proposed decision:
{decision}

Adjust the decision to:
- Ignore demographic stereotypes
- Focus on competence metrics
- Reduce peer-exclusion bias
- Correct for self-nomination gaps

Return JSON with optimized decision."""

        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            
            adjusted = self._parse_adjustment(response.text, decision)
            self._log_bias_adjustment('mask', context, decision, adjusted)
            return adjusted
            
        except Exception:
            return decision
    
    def _parse_adjustment(self, response_text: str, original: Dict) -> Dict:
        try:
            import json
            import re
            
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return original
        except Exception:
            return original
    
    def _log_bias_adjustment(self, mode: str, context: Dict, 
                           original: Dict, adjusted: Dict):
        self.bias_log.append({
            'mode': mode,
            'context': context,
            'original': original,
            'adjusted': adjusted
        })
        
        if len(self.bias_log) > 100:
            self.bias_log.pop(0)
    
    def get_bias_metrics(self) -> Dict:
        if not self.bias_log:
            return {'adjustments': 0, 'mode': self.mode}
        
        return {
            'total_adjustments': len(self.bias_log),
            'mode': self.mode,
            'recent_adjustments': self.bias_log[-10:]
        }
