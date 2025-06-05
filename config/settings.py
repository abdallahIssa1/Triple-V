import os
import json
from pathlib import Path

class Settings:
    # Application info
    APP_NAME = "Triple V"
    APP_VERSION = "1.0.0"
    ORGANIZATION = "Triple V Platform"
    
    # Paths
    BASE_DIR = Path(__file__).resolve().parent.parent
    DOWNLOADS_DIR = BASE_DIR / "downloads"
    CONFIG_DIR = BASE_DIR / "config"
    TOOLS_CONFIG_FILE = CONFIG_DIR / "tools_registry.json"
    
    # Create directories if they don't exist
    DOWNLOADS_DIR.mkdir(exist_ok=True)
    CONFIG_DIR.mkdir(exist_ok=True)
    
    # GitHub settings
    GITHUB_BASE_URL = "https://github.com/"
    UPDATE_CHECK_URL = "https://github.com/YourOrg/TripleV/releases/latest"
    
    # UI Settings
    SIDEBAR_WIDTH = 60
    SIDEBAR_EXPANDED_WIDTH = 250
    ANIMATION_DURATION = 300
    
    # Colors
    PRIMARY_COLOR = "#00ff88"
    SECONDARY_COLOR = "#00cc66"
    BACKGROUND_COLOR = "#1a1a1a"
    SURFACE_COLOR = "#2d2d2d"
    TEXT_COLOR = "#ffffff"
    
    @classmethod
    def load_tools_config(cls):
        """Load tools configuration from JSON file"""
        if cls.TOOLS_CONFIG_FILE.exists():
            with open(cls.TOOLS_CONFIG_FILE, 'r', encoding="utf-8") as f:
                return json.load(f)
        return {
            "autosar": [],
            "non_autosar": [],
            "mixed": []
        }
    
    @classmethod
    def save_tools_config(cls, config):
        """Save tools configuration to JSON file"""
        with open(cls.TOOLS_CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
