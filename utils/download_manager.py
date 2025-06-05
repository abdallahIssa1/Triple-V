import os
import json
import zipfile
import requests
import shutil
from pathlib import Path
from packaging import version
from PyQt5.QtWidgets import QMessageBox, QProgressDialog
from PyQt5.QtCore import Qt
from config.settings import Settings

class DownloadManager:
    def __init__(self):
        self.downloads_dir = Settings.DOWNLOADS_DIR
        self.installed_tools_file = self.downloads_dir / "installed_tools.json"
        self.load_installed_tools()
        
    def load_installed_tools(self):
        """Load the registry of installed tools"""
        if self.installed_tools_file.exists():
            with open(self.installed_tools_file, 'r') as f:
                self.installed_tools = json.load(f)
        else:
            self.installed_tools = {}
            
    def save_installed_tools(self):
        """Save the registry of installed tools"""
        with open(self.installed_tools_file, 'w') as f:
            json.dump(self.installed_tools, f, indent=4)
            
    def is_tool_installed(self, tool_name):
        """Check if a tool is installed and return version"""
        if tool_name in self.installed_tools:
            tool_info = self.installed_tools[tool_name]
            tool_path = Path(tool_info["path"])
            if tool_path.exists():
                return True, tool_info["version"]
        return False, None
        
    def parse_github_url(self, github_url):
        """Extract owner and repo from GitHub URL"""
        # Remove https://github.com/ and split
        parts = github_url.replace("https://github.com/", "").split("/")
        if len(parts) >= 2:
            return parts[0], parts[1]
        return None, None
    
    def convert_to_raw_url(self, github_url):
        """Convert GitHub blob URL to raw content URL"""
        # Convert from: https://github.com/owner/repo/blob/main/file
        # To: https://raw.githubusercontent.com/owner/repo/main/file
        
        if "blob" in github_url:
            # Replace github.com with raw.githubusercontent.com and remove /blob
            raw_url = github_url.replace("github.com", "raw.githubusercontent.com")
            raw_url = raw_url.replace("/blob/", "/")
            return raw_url
        
        # If it's already a raw URL or other format, return as is
        return github_url
        
    def fetch_tool_config(self, github_url):
        """Fetch Triple_V_Config.json from GitHub repo"""
        owner, repo = self.parse_github_url(github_url)
        if not owner or not repo:
            print(f"Could not parse GitHub URL: {github_url}")
            return None
        
        # Try multiple possible locations for the config file
        config_urls = [
            f"https://raw.githubusercontent.com/{owner}/{repo}/main/Triple_V_Config.json",
            f"https://raw.githubusercontent.com/{owner}/{repo}/master/Triple_V_Config.json",
            f"https://github.com/{owner}/{repo}/raw/main/Triple_V_Config.json",
            f"https://github.com/{owner}/{repo}/blob/main/Triple_V_Config.json?raw=true"
        ]
        
        for config_url in config_urls:
            try:
                print(f"Trying to fetch config from: {config_url}")
                response = requests.get(config_url, timeout=10)
                if response.status_code == 200:
                    # Try to parse as JSON
                    try:
                        return response.json()
                    except json.JSONDecodeError:
                        # If it's HTML (GitHub page), skip to next URL
                        if "<!DOCTYPE html>" in response.text:
                            continue
                        print(f"Invalid JSON from {config_url}")
            except requests.exceptions.RequestException as e:
                print(f"Request error for {config_url}: {e}")
            except Exception as e:
                print(f"Error fetching config from {config_url}: {e}")
        
        print(f"Could not fetch config from any URL for {owner}/{repo}")
        return None
        
    def get_download_url(self, github_url):
        """Get the download URL for the zipped tool"""
        owner, repo = self.parse_github_url(github_url)
        if not owner or not repo:
            return None
        
        # Common patterns for zip file names
        possible_zip_names = [
            f"{repo}.zip",
            f"{repo.replace('-', '_')}.zip",
            f"{repo.replace('_', '-')}.zip",
            f"{repo.lower()}.zip",
            f"{repo.replace('-', ' ')}.zip"  # Handle spaces
        ]
        
        # Try different URL patterns
        for zip_name in possible_zip_names:
            # URL encode the filename to handle spaces
            from urllib.parse import quote
            encoded_name = quote(zip_name)
            
            download_urls = [
                f"https://raw.githubusercontent.com/{owner}/{repo}/main/{encoded_name}",
                f"https://github.com/{owner}/{repo}/raw/main/{encoded_name}",
                f"https://github.com/{owner}/{repo}/blob/main/{encoded_name}?raw=true",
                # Also try without encoding for backwards compatibility
                f"https://raw.githubusercontent.com/{owner}/{repo}/main/{zip_name}",
            ]
            
            # Test each URL
            for url in download_urls:
                try:
                    print(f"Checking if zip exists at: {url}")
                    response = requests.head(url, timeout=5, allow_redirects=True)
                    if response.status_code == 200:
                        # Verify it's actually a zip file by checking content type
                        content_type = response.headers.get('content-type', '')
                        if 'application/zip' in content_type or 'application/octet-stream' in content_type or url.endswith('.zip'):
                            print(f"Found zip file at: {url}")
                            return url
                except Exception as e:
                    print(f"Error checking {url}: {e}")
        
        print(f"Could not find zip file for {owner}/{repo}")
        return None
        
    def download_tool(self, github_url, tool_name, parent_widget=None):
        """Download and install a tool"""
        # Fetch tool config
        config = self.fetch_tool_config(github_url)
        if not config:
            QMessageBox.warning(parent_widget, "Error", 
                              "Could not fetch tool configuration from GitHub.\n"
                              "Please ensure Triple_V_Config.json exists in the repository.")
            return False
        
        # Validate config has required fields
        if "version" not in config:
            QMessageBox.warning(parent_widget, "Error", 
                              "Invalid Triple_V_Config.json: missing 'version' field.")
            return False
            
        # Get download URL
        download_url = self.get_download_url(github_url)
        if not download_url:
            QMessageBox.warning(parent_widget, "Error", 
                              "Could not find download URL for this tool.\n"
                              "Please ensure the zip file exists in the repository.")
            return False
            
        # Create progress dialog
        progress = QProgressDialog("Downloading tool...", "Cancel", 0, 100, parent_widget)
        progress.setWindowModality(Qt.WindowModal)
        progress.setAutoClose(True)
        
        try:
            # Download the file
            print(f"Downloading from: {download_url}")
            response = requests.get(download_url, stream=True, timeout=30)
            
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: Could not download file")
                
            total_size = int(response.headers.get('content-length', 0))
            
            tool_dir = self.downloads_dir / tool_name
            tool_dir.mkdir(exist_ok=True)
            
            zip_path = tool_dir / f"{tool_name}.zip"
            
            downloaded = 0
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if progress.wasCanceled():
                        return False
                    if chunk:  # filter out keep-alive chunks
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress.setValue(int(downloaded * 100 / total_size))
                        
            # Verify it's a valid zip file
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    # Extract the zip
                    zip_ref.extractall(tool_dir)
                    print(f"Extracted files: {zip_ref.namelist()}")
            except zipfile.BadZipFile:
                raise Exception("Downloaded file is not a valid zip archive")
                
            # Save config file
            config_path = tool_dir / "Triple_V_Config.json"
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
                
            # Update installed tools registry
            self.installed_tools[tool_name] = {
                "version": config["version"],
                "path": str(tool_dir),
                "github_url": github_url
            }
            self.save_installed_tools()
            
            # Clean up zip file
            zip_path.unlink()
            
            progress.close()
            QMessageBox.information(parent_widget, "Success", 
                                  f"{tool_name} has been successfully downloaded!")
            return True
            
        except Exception as e:
            progress.close()
            print(f"Download error: {str(e)}")
            QMessageBox.critical(parent_widget, "Error", 
                               f"Failed to download tool: {str(e)}")
            return False
            
    def check_tool_update(self, github_url, current_version):
        """Check if a tool has an update available"""
        config = self.fetch_tool_config(github_url)
        if not config:
            return False, None
            
        latest_version = config.get("version", "0.0.0")
        
        try:
            if version.parse(latest_version) > version.parse(current_version):
                return True, latest_version
        except Exception as e:
            print(f"Error comparing versions: {e}")
            
        return False, None
        
    def update_tool(self, github_url, tool_name, parent_widget=None):
        """Update an existing tool"""
        if tool_name not in self.installed_tools:
            return False
            
        tool_info = self.installed_tools[tool_name]
        old_version = tool_info["version"]
        
        # Check for update
        has_update, new_version = self.check_tool_update(github_url, old_version)
        if not has_update:
            QMessageBox.information(parent_widget, "No Update", 
                                  "This tool is already up to date.")
            return False
            
        # Confirm update
        reply = QMessageBox.question(parent_widget, "Update Available",
                                   f"Update {tool_name} from v{old_version} to v{new_version}?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Remove old version
            tool_dir = Path(tool_info["path"])
            if tool_dir.exists():
                shutil.rmtree(tool_dir)
                
            # Download new version
            return self.download_tool(github_url, tool_name, parent_widget)
            
        return False