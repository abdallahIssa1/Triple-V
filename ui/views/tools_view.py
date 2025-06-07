from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, 
                            QGridLayout, QLabel, QPushButton, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from config.settings import Settings
from ui.components.tool_card import ToolCard
import webbrowser

class ToolsView(QWidget):
    back_clicked = pyqtSignal()
    
    def __init__(self, title, category):
        super().__init__()
        self.title = title
        self.category = category
        self.init_ui()
        self.load_tools()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel(self.title)
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setStyleSheet(f"color: {Settings.PRIMARY_COLOR};")
        
        back_btn = QPushButton("← Back")
        back_btn.setFixedSize(100, 40)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(self.go_back)
        back_btn.setStyleSheet(f"""
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
        header_layout.addWidget(back_btn)
        
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
        
        # Tools container
        self.tools_container = QWidget()
        self.tools_layout = QGridLayout(self.tools_container)
        self.tools_layout.setSpacing(20)
        
        scroll_area.setWidget(self.tools_container)
        layout.addWidget(scroll_area)
        
    def load_tools(self):
        tools_config = Settings.load_tools_config()
        tools = tools_config.get(self.category, [])
        
        row = 0
        col = 0
        for tool in tools:
            tool_card = ToolCard(
                tool["name"],
                tool["description"],
                tool["github_url"],
                tool.get("icon", "🔧")
            )
            self.tools_layout.addWidget(tool_card, row, col)
            
            col += 1
            if col > 2:  # 3 columns
                col = 0
                row += 1
                
    def go_back(self):
        main_window = self.window()
        main_window.on_navigation_clicked("main")
        # Update sidebar active state
        main_window.sidebar.nav_buttons[0].setChecked(True)
        for i in range(1, len(main_window.sidebar.nav_buttons)):
            main_window.sidebar.nav_buttons[i].setChecked(False)