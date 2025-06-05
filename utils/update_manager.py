# update_manager.py

import os
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
        # We will load the up‐to‐date version from disk each time we check for updates.
        self.current_version = None

        # Remote JSON that holds { "version": "X.Y.Z", "download_url": "<raw URL to TripleV.zip>" }
        self.update_config_url = (
            "https://raw.githubusercontent.com/abdallahIssa1/Triple-V/main/config/Triple_V_Updater.json"
        )

        # Fallback raw‐GitHub ZIP URL in case update_data["download_url"] is not a .zip
        self.fallback_zip_url = (
            "https://raw.githubusercontent.com/abdallahIssa1/Triple-V/main/dist/TripleV.zip"
        )

    def _get_local_version(self) -> str:
        """
        Read the current version from config/Triple_V_Config.json on disk.
        Returns a string like "1.0.0", or Settings.APP_VERSION if anything goes wrong.
        """
        try:
            cfg_path = Settings.CONFIG_DIR / "Triple_V_Config.json"
            with open(cfg_path, "r", encoding="utf-8") as cf:
                cfg = json.load(cf)
                return cfg.get("version", Settings.APP_VERSION)
        except Exception:
            return Settings.APP_VERSION

    def check_app_update(self):
        """
        Fetch Triple_V_Updater.json and compare remote version to local.
        Returns a tuple: (is_update_available: bool, latest_version: str, update_data: dict).
        """
        # Always reload the local version from disk before comparing
        self.current_version = self._get_local_version()

        try:
            response = requests.get(self.update_config_url, timeout=10)
            response.raise_for_status()
            update_data = response.json()

            latest_version = update_data.get("version", "0.0.0")
            if version.parse(latest_version) > version.parse(self.current_version):
                return True, latest_version, update_data

        except Exception as e:
            print(f"[UpdateManager] Error while checking for updates: {e}")

        return False, None, None

    def show_update_dialog(self, parent_widget, new_version, update_data=None):
        """
        1) Ask user if they want to download TripleV.zip.
        2) If yes, download the ZIP with a progress dialog.
        3) Extract TripleV.exe from the ZIP and replace the old EXE.
        4) Update Triple_V_Config.json with new version.
        """
        reply = QMessageBox.question(
            parent_widget,
            "Update Available",
            (
                f"Triple V version {new_version} is available!\n"
                f"Current version: {self.current_version}\n\n"
                "Download and install the update now?"
            ),
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        # Determine download URL (expecting a .zip containing TripleV.exe)
        download_url = None
        if update_data and isinstance(update_data.get("download_url"), str):
            download_url = update_data["download_url"]
        # If the provided URL does not end with ".zip", use the fallback raw‐GitHub path
        if not download_url or not download_url.lower().endswith(".zip"):
            download_url = self.fallback_zip_url

        try:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            success = self._download_extract_replace(parent_widget, download_url)

            if success:
                # 1) Persist the new version on disk
                cfg_path = Settings.CONFIG_DIR / "Triple_V_Config.json"
                try:
                    with open(cfg_path, "r+", encoding="utf-8") as cf:
                        cfg = json.load(cf)
                        cfg["version"] = new_version
                        cf.seek(0)
                        json.dump(cfg, cf, indent=4)
                        cf.truncate()
                except Exception as e:
                    print(f"[UpdateManager] Failed to update Triple_V_Config.json: {e}")

                # 2) Also update our in‐memory current_version so subsequent calls see the change
                self.current_version = new_version

                QMessageBox.information(
                    parent_widget,
                    "Update Complete",
                    f"Triple V has been updated to version {new_version}!"
                )
            else:
                QMessageBox.warning(
                    parent_widget,
                    "Update Failed",
                    "Download or installation failed. Please try again."
                )
        finally:
            QApplication.restoreOverrideCursor()

    def _download_extract_replace(self, parent, url):
        """
        Download a ZIP containing TripleV.exe, show progress, then extract and replace.
        Returns True on success, False otherwise.
        """
        dist_dir = Settings.BASE_DIR / "dist"
        old_exe_path = dist_dir / "TripleV.exe"

        try:
            # 1) Stream-download the ZIP
            with requests.get(url, stream=True, timeout=15) as response:
                response.raise_for_status()
                total_size = int(response.headers.get("Content-Length", 0))

                progress = QProgressDialog(
                    "Downloading update...",
                    "Cancel",
                    0,
                    total_size,
                    parent
                )
                progress.setWindowTitle("Updating Triple V")
                progress.setWindowModality(Qt.WindowModal)
                progress.setMinimumDuration(500)
                progress.setValue(0)

                # Save ZIP to a temporary file
                fd, temp_zip_path = tempfile.mkstemp(suffix=".zip")
                os.close(fd)
                bytes_downloaded = 0

                with open(temp_zip_path, "wb") as tmp_zip:
                    chunk_size = 8192
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            tmp_zip.write(chunk)
                            bytes_downloaded += len(chunk)
                            progress.setValue(bytes_downloaded)
                            QApplication.processEvents()
                            if progress.wasCanceled():
                                tmp_zip.close()
                                os.remove(temp_zip_path)
                                return False

                progress.setValue(total_size)
                progress.close()

            # 2) Open the ZIP and extract TripleV.exe to a temp location
            with zipfile.ZipFile(temp_zip_path, "r") as z:
                members = z.namelist()
                if "TripleV.exe" not in members:
                    print(f"[UpdateManager] ZIP does not contain TripleV.exe; contents: {members}")
                    os.remove(temp_zip_path)
                    return False

                # Extract to a new temporary file
                fd2, temp_exe_path = tempfile.mkstemp(suffix=".exe")
                os.close(fd2)
                with z.open("TripleV.exe") as zipped_exe, open(temp_exe_path, "wb") as out_exe:
                    shutil.copyfileobj(zipped_exe, out_exe)

            # 3) Replace the old EXE
            if old_exe_path.exists():
                try:
                    old_exe_path.unlink()
                except Exception as e:
                    print(f"[UpdateManager] Could not delete old EXE: {e}")
                    # Proceed anyway—moving new EXE may overwrite or fail

            # Ensure dist directory exists
            dist_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(temp_exe_path, str(old_exe_path))

            # 4) Clean up the downloaded ZIP
            os.remove(temp_zip_path)

            return True

        except zipfile.BadZipFile:
            print("[UpdateManager] Downloaded file is not a valid ZIP.")
            try:
                if os.path.exists(temp_zip_path):
                    os.remove(temp_zip_path)
            except:
                pass
            return False

        except Exception as e:
            print(f"[UpdateManager] Download/extract/replace failed: {e}")
            # Clean up temp files if they exist
            try:
                if os.path.exists(temp_zip_path):
                    os.remove(temp_zip_path)
            except:
                pass
            try:
                if os.path.exists(temp_exe_path):
                    os.remove(temp_exe_path)
            except:
                pass
            return False
