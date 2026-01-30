"""
Configuration loader for Groq AI and other settings
Loads settings from settings.json and environment variables
Priority: Environment Variables > settings.json > Defaults
"""

import json
import os
from typing import Dict, Any
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()


class Config:
    """Load and manage application configuration"""
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration
        
        Args:
            config_path: Path to settings.json. If None, searches in project root.
        """
        if config_path is None:
            # Search for settings.json in project root
            possible_paths = [
                Path(__file__).parent.parent / "settings.json",  # d:\...\PersonalizedTutorAgent\settings.json
                Path.cwd() / "settings.json",  # Current working directory
                "settings.json"  # Relative to current path
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    config_path = path
                    break
            
            if config_path is None:
                raise FileNotFoundError(
                    "settings.json not found. Please create it in the project root.\n"
                    "Expected locations: project root or src/ folder"
                )
        
        self.config_path = config_path
        self.settings = self._load_settings()
    
    def _load_settings(self) -> Dict[str, Any]:
        """
        Load settings from JSON file
        
        Returns:
            Dictionary of settings
        """
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in settings.json: {e}")
        except FileNotFoundError:
            raise FileNotFoundError(f"settings.json not found at {self.config_path}")
    
    def get_groq_api_key(self) -> str:
        """
        Get Groq API key from environment or settings.json
        Priority: GROQ_API_KEY env var > settings.json > error
        
        Returns:
            Groq API key string
            
        Raises:
            ValueError: If API key is not set or is placeholder
        """
        # Check environment variable first
        env_key = os.getenv("GROQ_API_KEY")
        if env_key and env_key != "your_groq_api_key_here":
            return env_key
        
        # Check settings.json
        api_key = self.settings.get("groq", {}).get("api_key", "")
        
        if not api_key or api_key == "YOUR_GROQ_API_KEY_HERE":
            raise ValueError(
                "Groq API key not configured!\n"
                "Choose one of these options:\n\n"
                "Option 1 - settings.json (Recommended):\n"
                "  1. Get key from: https://console.groq.com/keys\n"
                "  2. Update 'groq.api_key' in settings.json\n"
                "  3. Example: \"api_key\": \"gsk_abcd1234...\"\n\n"
                "Option 2 - Environment Variable:\n"
                "  1. Copy .env.example to .env\n"
                "  2. Add: GROQ_API_KEY=gsk_your_key_here\n"
                "  3. Restart your application"
            )
        
        return api_key
    
    def get_groq_model(self) -> str:
        """Get Groq model name"""
        return self.settings.get("groq", {}).get("model", "mixtral-8x7b-32768")
    
    def get_groq_config(self) -> Dict[str, Any]:
        """Get full Groq configuration"""
        return self.settings.get("groq", {})
    
    def get_ai_settings(self) -> Dict[str, Any]:
        """Get AI feature settings"""
        return self.settings.get("ai_settings", {})
    
    def is_feedback_enabled(self) -> bool:
        """Check if AI feedback is enabled"""
        return self.get_ai_settings().get("feedback_enabled", True)
    
    def is_hint_generation_enabled(self) -> bool:
        """Check if AI hint generation is enabled"""
        return self.get_ai_settings().get("hint_generation_enabled", True)
    
    def is_personalized_feedback_enabled(self) -> bool:
        """Check if personalized feedback is enabled"""
        return self.get_ai_settings().get("personalized_feedback", True)
    
    def get_response_timeout(self) -> int:
        """Get timeout for AI responses in seconds"""
        return self.get_ai_settings().get("response_timeout", 30)
    
    def get_retry_attempts(self) -> int:
        """Get number of retry attempts for API calls"""
        return self.get_ai_settings().get("retry_attempts", 3)
    
    def should_log_ai_calls(self) -> bool:
        """Check if AI calls should be logged"""
        return self.settings.get("logging", {}).get("log_ai_calls", True)


# Global config instance
_config = None


def get_config(config_path: str = None) -> Config:
    """
    Get global configuration instance
    
    Args:
        config_path: Optional path to settings.json
        
    Returns:
        Config instance
    """
    global _config
    if _config is None:
        _config = Config(config_path)
    return _config


def reload_config(config_path: str = None):
    """
    Reload configuration
    
    Args:
        config_path: Optional path to settings.json
    """
    global _config
    _config = Config(config_path)
