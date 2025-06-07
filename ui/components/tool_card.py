from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPainter, QColor
from config.settings import Settings
from utils.download_manager import DownloadManager
import webbrowser

class ToolCard(QFrame):
    def __init__(self, name, description, github_url, icon="🔧"):
        super().__init__()
        self.name = name
        self.description = description
        self.github_url = github_url
        self.icon = icon
        self.download_manager = DownloadManager()
        self.init_ui()
        # Delay the check to ensure UI is ready
        QTimer.singleShot(100, self.check_installed_status)

    def init_ui(self):
        self.setFixedSize(300, 250)  # Increased height
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
        
        # Icon and name
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(self.icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 32))
        icon_label.setStyleSheet(f"color: {Settings.PRIMARY_COLOR};")
        
        name_label = QLabel(self.name)
        name_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        name_label.setWordWrap(True)
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(name_label, 1)
        
        # Description
        desc_label = QLabel(self.description)
        desc_label.setFont(QFont("Segoe UI", 10))
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #aaa; line-height: 1.4;")
        desc_label.setMinimumHeight(60)  # Ensure minimum space
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.download_btn = QPushButton("Download")
        self.download_btn.setFixedHeight(35)
        self.download_btn.setCursor(Qt.PointingHandCursor)
        self.download_btn.clicked.connect(self.handle_download)
        self.style_download_button()
        
        self.github_btn = QPushButton("GitHub")
        self.github_btn.setFixedHeight(35)
        self.github_btn.setCursor(Qt.PointingHandCursor)
        self.github_btn.clicked.connect(lambda: webbrowser.open(self.github_url))
        self.github_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #333;
                border: 1px solid #555;
                border-radius: 6px;
                color: white;
                font-weight: bold;
                padding: 0 15px;
            }}
            QPushButton:hover {{
                background-color: #444;
                border-color: {Settings.PRIMARY_COLOR};
            }}
        """)
        
        button_layout.addWidget(self.download_btn)
        button_layout.addWidget(self.github_btn)
        
        layout.addLayout(header_layout)
        layout.addWidget(desc_label)
        layout.addStretch()
        layout.addLayout(button_layout)
        
    def style_download_button(self, is_update=False, enabled=True):
        if enabled:
            self.download_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Settings.PRIMARY_COLOR if not is_update else '#ff9900'};
                    border: none;
                    border-radius: 6px;
                    color: {Settings.BACKGROUND_COLOR};
                    font-weight: bold;
                    padding: 0 15px;
                }}
                QPushButton:hover {{
                    background-color: {Settings.SECONDARY_COLOR if not is_update else '#ffaa00'};
                }}
            """)
        else:
            self.download_btn.setStyleSheet("""
                QPushButton {
                    background-color: #444;
                    border: 1px solid #555;
                    border-radius: 6px;
                    color: #888;
                    font-weight: bold;
                    padding: 0 15px;
                }
            """)
            
    def check_installed_status(self):
        is_installed, installed_version = self.download_manager.is_tool_installed(self.name)
        
        if is_installed:
            # Check for updates
            has_update, latest_version = self.download_manager.check_tool_update(self.github_url, installed_version)
            
            if has_update:
                self.download_btn.setText("Update")
                self.download_btn.setEnabled(True)
                self.style_download_button(is_update=True, enabled=True)
            else:
                self.download_btn.setText("Update")
                self.download_btn.setEnabled(False)
                self.style_download_button(is_update=True, enabled=False)
        else:
            self.download_btn.setText("Download")
            self.download_btn.setEnabled(True)
            self.style_download_button(is_update=False, enabled=True)
            
    def handle_download(self):
        if self.download_btn.text() == "Download":
            success = self.download_manager.download_tool(self.github_url, self.name)
            if success:
                self.check_installed_status()
        else:
            success = self.download_manager.update_tool(self.github_url, self.name)
            if success:
                self.check_installed_status()