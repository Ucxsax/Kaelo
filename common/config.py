import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # AI Service Selection
    AI_SERVICE = os.getenv("AI_SERVICE", "openai").lower()
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    # Ollama
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
    
    # Screen Capture
    SCREEN_CAPTURE_DELAY = float(os.getenv("SCREEN_CAPTURE_DELAY", "0.5"))
    MAX_RETRY_ATTEMPTS = int(os.getenv("MAX_RETRY_ATTEMPTS", "3"))
    
    # Safety
    ENABLE_SAFETY_CHECK = os.getenv("ENABLE_SAFETY_CHECK", "true").lower() == "true"
