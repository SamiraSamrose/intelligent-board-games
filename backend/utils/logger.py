import logging
import sys
from datetime import datetime

def setup_logger(name, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
    
    return logger

def log_game_action(game_id, player_id, action, result):
    logger = setup_logger('game_actions')
    logger.info(
        f"Game: {game_id} | Player: {player_id} | Action: {action} | Result: {result}"
    )

def log_ai_decision(game_id, character, decision, reasoning):
    logger = setup_logger('ai_decisions')
    logger.info(
        f"Game: {game_id} | Character: {character} | Decision: {decision} | Reasoning: {reasoning[:100]}..."
    )