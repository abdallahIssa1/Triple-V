from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, 
                            QGridLayout, QLabel, QPushButton, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from config.settings import Settings
from ui.components.my_tool_card import MyToolCard
import json

class MyToolsView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("My Downloaded Tools")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setStyleSheet(f"color: {Settings.PRIMARY_COLOR};")
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setFixedSize(100, 40)
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.clicked.connect(self.refresh_tools)
        refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 2px solid {Settings.PRIMARY_COLOR};
                border-radius: 8px;
                color: {Settings.PRIMARY_COLOR};
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {Settings.PRIMARY_COLOR};
                color: {Settings.BACKGROUND_COLOR};
            }}
        """)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Scroll area for tools
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #40E0D0;
                border-radius: 5px;
                min-height: 20px;
            }
        """)
        
        self.tools_container = QWidget()
        self.tools_layout = QGridLayout(self.tools_container)
        self.tools_layout.setSpacing(20)
        
        scroll_area.setWidget(self.tools_container)
        layout.addWidget(scroll_area)
        
        # Load tools on init
        self.refresh_tools()
        
    def refresh_tools(self):
        # Clear existing widgets
        for i in reversed(range(self.tools_layout.count())): 
            self.tools_layout.itemAt(i).widget().setParent(None)
            
        # Load installed tools
        installed_tools_file = Settings.DOWNLOADS_DIR / "installed_tools.json"
        if installed_tools_file.exists():
            with open(installed_tools_file, 'r') as f:
                installed_tools = json.load(f)
                
            row = 0
            col = 0
            for tool_name, tool_info in installed_tools.items():
                tool_card = MyToolCard(
                    name=tool_name,
                    version=tool_info.get("version", "Unknown"),
                    path=tool_info.get("path", ""),
                    github_url=tool_info.get("github_url", "")
                )
                self.tools_layout.addWidget(tool_card, row, col)
                
                col += 1
                if col > 2:  # 3 columns
                    col = 0
                    row += 1