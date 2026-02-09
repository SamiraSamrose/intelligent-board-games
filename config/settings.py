import os

class Config:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
    
    DATABASE_PATH = os.getenv('DATABASE_PATH', './data')
    
    AI_TEMPERATURE = float(os.getenv('AI_TEMPERATURE', 1.0))
    AI_MAX_TOKENS = int(os.getenv('AI_MAX_TOKENS', 8192))
    
    BIAS_MODE = os.getenv('BIAS_MODE', 'mirror')
    
    SOCIETY_PERSPECTIVES = int(os.getenv('SOCIETY_PERSPECTIVES', 5))
    
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')