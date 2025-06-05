# settings.py

import os
import json
from pathlib import Path

class Settings:
    # ------------------------
    # Paths
    # ------------------------
    BASE_DIR = Path(__file__).resolve().parent.parent
    CONFIG_DIR = BASE_DIR / "config"
    DOWNLOADS_DIR = BASE_DIR / "downloads"
    TOOLS_CONFIG_FILE = CONFIG_DIR / "tools_registry.json"
    ASSETS_DIR = BASE_DIR / "assets"
    LOGO_PATH = ASSETS_DIR / "triple_v_logo.png"
    ICON_PATH = ASSETS_DIR / "triple_v_logo.ico"

    # Ensure necessary directories exist
    CONFIG_DIR.mkdir(exist_ok=True)
    DOWNLOADS_DIR.mkdir(exist_ok=True)
    ASSETS_DIR.mkdir(exist_ok=True)

    # ------------------------
    # Local Version Loading
    # ------------------------
    @staticmethod
    def _load_local_version() -> str:
        """
        Reads the current version from config/Triple_V_Config.json on disk.
        If the file is missing, creates it with a default "1.0.0" and returns that.
        Returns:
            A version string, e.g. "1.0.0". Falls back to "1.0.0" on any error.
        """
        # Calculate paths without referencing Settings class
        base_dir = Path(__file__).resolve().parent.parent
        config_dir = base_dir / "config"
        cfg_path = config_dir / "Triple_V_Config.json"
        default_version = "1.0.0"

        try:
            # If the config file doesn't exist, create it with the default version.
            if not cfg_path.exists():
                config_dir.mkdir(parents=True, exist_ok=True)
                with open(cfg_path, "w", encoding="utf-8") as cf_init:
                    json.dump({"version": default_version}, cf_init, indent=4)
                return default_version

            # Otherwise read whatever is stored in the JSON
            with open(cfg_path, "r", encoding="utf-8") as cf:
                data = json.load(cf)
                return data.get("version", default_version)

        except Exception as e:
            print(f"Error loading version: {e}")
            return default_version

    # ------------------------
    # Application Info
    # ------------------------
    APP_NAME = "Triple V"
    APP_VERSION = _load_local_version()
    ORGANIZATION = "Triple V Platform"

    # ------------------------
    # GitHub / Update Settings
    # ------------------------
    GITHUB_BASE_URL = "https://api.github.com/repos"
    # This URL is used if no valid download_url is provided by the updater manifest.
    UPDATE_CHECK_URL = "https://raw.githubusercontent.com/abdallahIssa1/Triple-V/main/dist/TripleV.zip"

    # ------------------------
    # UI Settings
    # ------------------------
    SIDEBAR_WIDTH = 60
    SIDEBAR_EXPANDED_WIDTH = 250
    ANIMATION_DURATION = 300

    # ------------------------
    # Colors (Hex Codes)
    # ------------------------
    PRIMARY_COLOR    = "#00ff88"
    SECONDARY_COLOR  = "#00cc66"
    BACKGROUND_COLOR = "#1a1a1a"
    SURFACE_COLOR    = "#2d2d2d"
    TEXT_COLOR       = "#ffffff"

    # ------------------------
    # Tools Config Load/Save
    # ------------------------
    @classmethod
    def load_tools_config(cls):
        """
        Load the tools registry from JSON.
        If the file does not exist, return a default structure.
        """
        if cls.TOOLS_CONFIG_FILE.exists():
            try:
                with open(cls.TOOLS_CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading tools config: {e}")
                # Return default structure on error
                return {
                    "Classical_AUTOSAR": [],
                    "Adaptive_AUTOSAR": [],
                    "generic": []
                }
        # Default categories if no file is present
        return {
            "Classical_AUTOSAR": [],
            "Adaptive_AUTOSAR": [],
            "generic": []
        }

    @classmethod
    def save_tools_config(cls, config_data):
        """
        Overwrite the tools registry JSON with config_data.
        """
        try:
            # Ensure directory exists
            cls.TOOLS_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(cls.TOOLS_CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving tools config: {e}")

    @classmethod
    def update_app_version(cls, new_version):
        """
        Update the application version in the local config file.
        """
        cfg_path = cls.CONFIG_DIR / "Triple_V_Config.json"
        try:
            with open(cfg_path, "w", encoding="utf-8") as f:
                json.dump({"version": new_version}, f, indent=4)
            cls.APP_VERSION = new_version
        except Exception as e:
            print(f"Error updating version: {e}")