import os
import sys
import subprocess
import json
import tempfile
import shutil
import zipfile
import requests
from packaging import version
from pathlib import Path

from PyQt5.QtWidgets import (
    QMessageBox,
    QProgressDialog,
    QApplication
)
from PyQt5.QtCore import Qt

from config.settings import Settings


class UpdateManager:
    def __init__(self):
        # Current version extracted from filename
        self.current_version = Settings.APP_VERSION
        
        # GitHub API URL
        self.github_api_url = Settings.GITHUB_API_URL


    def check_app_update(self):
        """
        Query GitHub Releases API and compare versions
        Returns: (is_update_available: bool, latest_version: str, release_data: dict)
        """
        

        try:
            print(f"[UpdateManager] Current version: {self.current_version}")
            print(f"[UpdateManager] Checking GitHub releases: {self.github_api_url}")
            response = requests.get(self.github_api_url, timeout=10)
            response.raise_for_status()
            release_data = response.json()
            # Extract version from tag_name (e.g., "v2.0.0" -> "2.0.0")
            tag_name = release_data.get("tag_name", "")
            latest_version = tag_name.lstrip("v")
            
            print(f"[UpdateManager] Latest release version: {latest_version}")


            if version.parse(latest_version) > version.parse(self.current_version):
                print(f"[UpdateManager] Update available: {self.current_version} -> {latest_version}")
                return True, latest_version, release_data
            else:
                print(f"[UpdateManager] Already up to date")
                
        except Exception as e:
            print(f"[UpdateManager] Error checking for updates: {e}")

        return False, None, None

    def show_update_dialog(self, parent_widget, new_version, release_data=None):
        """
        Show update dialog and handle the update process
        """
        reply = QMessageBox.question(
            parent_widget,
            "Update Available",
            (
                f"Triple V v{new_version} is available!\n\n"
                f"Current version: v{self.current_version}\n"
                f"New version: v{new_version}\n\n"
                "Download and install now?"
            ),
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            print("[UpdateManager] User chose not to update.")
            return

        # Find the ZIP asset in the release
        download_url = None
        if release_data and "assets" in release_data:
            for asset in release_data["assets"]:
                if asset["name"].endswith(".zip") and "TripleV" in asset["name"]:
                    download_url = asset["browser_download_url"]
                    break
        
        if not download_url:
            QMessageBox.warning(parent_widget, "Error", 
                              "Could not find download URL for the update.")
            return

        try:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            success = self._download_and_install_update(parent_widget, download_url, new_version)

            if success:
                QMessageBox.information(
                    parent_widget,
                    "Update Complete",
                    f"Triple V has been updated to v{new_version}!\n\n"
                    "Please restart the application to apply changes."
                )
            else:
                QMessageBox.warning(
                    parent_widget,
                    "Update Failed",
                    "Failed to install the update. Please try again."
                )
        finally:
            QApplication.restoreOverrideCursor()

    def _download_and_install_update(self, parent, url, new_version):
        """
        Download ZIP, extract new exe, rename old exe, and install new one
        """
        
        try:
            # 1. Download the ZIP file
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            total_size = int(response.headers.get("content-length", 0))
            
            progress = QProgressDialog("Downloading update...", "Cancel", 0, total_size, parent)
            progress.setWindowModality(Qt.WindowModal)
            progress.setMinimumDuration(0)
            
            # Download to temp file
            temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
            downloaded = 0
            
            for chunk in response.iter_content(chunk_size=8192):
                if progress.wasCanceled():
                    temp_zip.close()
                    os.unlink(temp_zip.name)
                    return False
                    
                if chunk:
                    temp_zip.write(chunk)
                    downloaded += len(chunk)
                    progress.setValue(downloaded)
                    
            temp_zip.close()
            progress.close()
            
            # 2. Extract the new executable
            with zipfile.ZipFile(temp_zip.name, 'r') as zip_ref:
                # Find the exe file in the zip
                exe_name = None
                for name in zip_ref.namelist():
                    if name.endswith('.exe') and 'TripleV' in name:
                        exe_name = name
                        break
                        
                if not exe_name:
                    raise Exception("No TripleV executable found in update package")
                
                # Extract to temp location
                temp_dir = tempfile.mkdtemp()
                zip_ref.extract(exe_name, temp_dir)
                new_exe_path = Path(temp_dir) / exe_name
            
            # 3. Rename current executable
            if getattr(sys, 'frozen', False):
                current_exe = Path(sys.executable)
            else:
                # Running as script, look for exe in dist
                dist_dir = Settings.BASE_DIR / "dist"
                current_exe = None
                for exe_file in dist_dir.glob("TripleV*.exe"):
                    current_exe = exe_file
                    break
            
            if current_exe and current_exe.exists():
                # Rename old exe to include its version
                old_version = self.current_version
                backup_name = f"TripleV_v{old_version}_old_{old_version}.exe"
                backup_path = current_exe.parent / backup_name
                
                # Use a batch script to rename the running exe
                if getattr(sys, 'frozen', False):
                    batch_content = f"""
@echo off
timeout /t 2 /nobreak > nul
move /y "{current_exe}" "{backup_path}"
move /y "{new_exe_path}" "{current_exe.parent / f'TripleV_v{new_version}.exe'}"
del "%~f0"
"""
                    batch_path = current_exe.parent / "update.bat"
                    with open(batch_path, 'w') as f:
                        f.write(batch_content)
                    
                    # Execute batch script
                    subprocess.Popen(str(batch_path), shell=True)
                else:
                    # Not frozen, just move files directly
                    if current_exe.exists():
                        current_exe.rename(backup_path)
                    new_exe_path.rename(current_exe.parent / f"TripleV_v{new_version}.exe")
            
            # Clean up
            os.unlink(temp_zip.name)
            
            return True

        except Exception as e:
            print(f"[UpdateManager] Update failed: {e}")
            try:
                if 'temp_zip' in locals():
                    os.unlink(temp_zip.name)
            except Exception:
                pass
                return False
