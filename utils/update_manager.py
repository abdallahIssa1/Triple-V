import requests
from packaging import version
from PyQt5.QtWidgets import QMessageBox
from config.settings import Settings
import webbrowser

class UpdateManager:
    def __init__(self):
        self.current_version = Settings.APP_VERSION
        
    def check_app_update(self):
        """Check if Triple V itself has an update"""
        try:
            # This would be your actual update check URL
            response = requests.get(Settings.UPDATE_CHECK_URL)
            if response.status_code == 200:
                latest_data = response.json()
                latest_version = latest_data.get("tag_name", "").lstrip("v")
                
                if version.parse(latest_version) > version.parse(self.current_version):
                    return True, latest_version
        except Exception as e:
            print(f"Error checking for updates: {e}")
            
        return False, None
        
    def show_update_dialog(self, parent_widget, new_version):
        """Show update available dialog"""
        reply = QMessageBox.question(
            parent_widget,
            "Update Available",
            f"Triple V {new_version} is available!\n\n"
            f"Current version: {self.current_version}\n"
            f"New version: {new_version}\n\n"
            "Would you like to download the update?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            webbrowser.open(Settings.UPDATE_CHECK_URL)