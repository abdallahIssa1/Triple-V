import os
import json
import sys
import re
from pathlib import Path

class Settings:
    # ------------------------
    # Paths
    # ------------------------
    BASE_DIR = Path(__file__).resolve().parent.parent
    CONFIG_DIR = BASE_DIR / "config"
    
    # Get the directory where the exe is located
    if getattr(sys, 'frozen', False):
        # Running as exe
        EXE_DIR = Path(sys.executable).parent
    else:
        # Running as script
        EXE_DIR = BASE_DIR / "dist"

    DOWNLOADS_DIR = EXE_DIR / "My Downloaded Tools"

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
        Extract version from executable filename (e.g., TripleV_v2.0.0.exe -> 2.0.0)
        Falls back to "1.0.0" if pattern not found
        """
        default_version = "5.0.0"

        try:
            # Determine path to the running executable or script
            if getattr(sys, "frozen", False):
                # Running as a compiled executable
                exe_path = sys.executable
                filename = Path(exe_path).name  # Get just the filename
            else:
                # Running as a script; look for TripleV_v*.exe in dist folder
                dist_path = Path(__file__).resolve().parent.parent / "dist"
                exe_files  = list(dist_path.glob("TripleV_v*.exe"))
                if exe_files:
                    filename = exe_files[0].name
                else:
                    return default_version

            # Extract version from filename using regex
            match = re.search(r'TripleV_v(\d+\.\d+\.\d+)', filename.replace('.exe', ''))
            if match:
                version_str = match.group(1)
                print(f"[Settings] Extracted version {version} from {filename}")
                return version_str
            else:
                print(f"[Settings] Could not extract version from {filename}, using default")
                return default_version

        except Exception as e:
            print(f"[Settings] Error extracting version: {e}")
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
    GITHUB_API_URL = "https://api.github.com/repos/abdallahIssa1/Triple-V/releases/latest"
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
    PRIMARY_COLOR    = "#40E0D0"
    SECONDARY_COLOR  = "#30C0B0"
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
                    "generic": [],
                    "My downloaded Tools": []
                }
        # Default categories if no file is present
        return {
            "Classical_AUTOSAR": [],
            "Adaptive_AUTOSAR": [],
            "generic": [],
            "My downloaded Tools": []
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
