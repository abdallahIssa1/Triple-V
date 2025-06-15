from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from config.settings import Settings
import subprocess
import os
from pathlib import Path
import webbrowser

class MyToolCard(QFrame):
    def __init__(self, name, version, path, github_url):
        super().__init__()
        self.name = name
        self.version = version
        self.tool_path = Path(path)
        self.github_url = github_url
        self.init_ui()
        
    def init_ui(self):
        self.setFixedSize(300, 200)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 12px;
            }}
            QFrame:hover {{
                border-color: {Settings.PRIMARY_COLOR};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Name and version
        name_label = QLabel(self.name)
        name_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        name_label.setWordWrap(True)
        
        version_label = QLabel(f"Version: {self.version}")
        version_label.setFont(QFont("Segoe UI", 10))
        version_label.setStyleSheet("color: #aaa;")
        
        # Path info
        path_label = QLabel(f"📁 {self.tool_path.name}")
        path_label.setFont(QFont("Segoe UI", 9))
        path_label.setStyleSheet("color: #888;")
        path_label.setWordWrap(True)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # Run button
        self.run_btn = QPushButton("▶ Run")
        self.run_btn.setFixedHeight(35)
        self.run_btn.setCursor(Qt.PointingHandCursor)
        self.run_btn.clicked.connect(self.run_tool)
        self.run_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Settings.PRIMARY_COLOR};
                border: none;
                border-radius: 6px;
                color: {Settings.BACKGROUND_COLOR};
                font-weight: bold;
                padding: 0 15px;
            }}
            QPushButton:hover {{
                background-color: {Settings.SECONDARY_COLOR};
            }}
        """)
        
        # Open folder button
        folder_btn = QPushButton("📂")
        folder_btn.setFixedSize(35, 35)
        folder_btn.setCursor(Qt.PointingHandCursor)
        folder_btn.setToolTip("Open folder")
        folder_btn.clicked.connect(self.open_folder)
        folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #333;
                border: 1px solid #555;
                border-radius: 6px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #444;
            }
        """)
        
        # GitHub button
        github_btn = QPushButton("GitHub")
        github_btn.setFixedHeight(35)
        github_btn.setCursor(Qt.PointingHandCursor)
        github_btn.clicked.connect(lambda: webbrowser.open(self.github_url))
        github_btn.setStyleSheet("""
            QPushButton {
                background-color: #333;
                border: 1px solid #555;
                border-radius: 6px;
                color: white;
                font-weight: bold;
                padding: 0 15px;
            }
            QPushButton:hover {
                background-color: #444;
            }
        """)
        
        button_layout.addWidget(self.run_btn)
        button_layout.addWidget(folder_btn)
        button_layout.addWidget(github_btn)
        
        layout.addWidget(name_label)
        layout.addWidget(version_label)
        layout.addWidget(path_label)
        layout.addStretch()
        layout.addLayout(button_layout)
        
    def run_tool(self):
        """Run the tool executable"""
        try:
            # Find the exe file in the tool directory
            exe_files = list(self.tool_path.glob("*.exe"))
            if exe_files:
                exe_path = exe_files[0]  # Take the first exe found
                subprocess.Popen(str(exe_path), cwd=str(self.tool_path))
                QMessageBox.information(self, "Success", f"{self.name} started successfully!")
            else:
                QMessageBox.warning(self, "Error", "No executable file found in tool directory")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to run tool: {str(e)}")
            
    def open_folder(self):
        """Open the tool folder in explorer"""
        try:
            os.startfile(str(self.tool_path))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not open folder: {str(e)}")