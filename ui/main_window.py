from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QStackedWidget, QLabel, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal, QTimer
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtSvg import QSvgWidget
from config.settings import Settings
from ui.sidebar import Sidebar
from ui.views.main_view import MainView
from ui.views.tools_view import ToolsView
from ui.dialogs.add_vault_dialog import AddVaultDialog
from ui.dialogs.about_dialog import AboutDialog
from utils.update_manager import UpdateManager
import webbrowser
from PyQt5.QtWidgets import QDesktopWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.update_manager = UpdateManager()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle(Settings.APP_NAME)

        # Get screen size for better adaptability
        screen = QDesktopWidget().screenGeometry()
        
        # Set window size to 80% of screen size
        width  = int(screen.width() * 0.8)
        height = int(screen.height() * 0.8)

        # Center the window
        x = (screen.width() - width) // 2
        y = (screen.height() - height) // 2

        self.setGeometry(x, y, width, height)
        self.setMinimumSize(800, 600)


        # Set dark palette
        self.set_dark_palette()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.navigation_clicked.connect(self.on_navigation_clicked)
        main_layout.addWidget(self.sidebar)
        
        # Content area
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)
        
        # Views
        self.main_view = MainView()
        self.main_view.add_vault_clicked.connect(self.show_add_vault_dialog)
        self.main_view.about_clicked.connect(self.show_about_dialog)
        self.main_view.check_updates_clicked.connect(self.check_for_updates)
        
        self.Classical_AUTOSAR = ToolsView("Classical AUTOSAR Tools", "Classical_AUTOSAR")
        self.Adaptive_AUTOSAR_view = ToolsView("Adaptive AUTOSAR Tools", "Adaptive_AUTOSAR")
        self.generic_view = ToolsView("Generic Tools", "generic")
        
        # Add views to stack
        self.content_stack.addWidget(self.main_view)
        self.content_stack.addWidget(self.Classical_AUTOSAR)
        self.content_stack.addWidget(self.Adaptive_AUTOSAR_view)
        self.content_stack.addWidget(self.generic_view)
        
        # Set initial view
        self.content_stack.setCurrentWidget(self.main_view)
        
    def set_dark_palette(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(26, 26, 26))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Base, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.AlternateBase, QColor(60, 60, 60))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Button, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.Link, QColor(0, 255, 136))
        dark_palette.setColor(QPalette.Highlight, QColor(0, 255, 136))
        dark_palette.setColor(QPalette.HighlightedText, QColor(26, 26, 26))
        self.setPalette(dark_palette)
        
    def on_navigation_clicked(self, view_name):
        if view_name == "main":
            self.content_stack.setCurrentWidget(self.main_view)
        elif view_name == "Classical_AUTOSAR":
            self.content_stack.setCurrentWidget(self.Classical_AUTOSAR)
        elif view_name == "Adaptive_AUTOSAR":
            self.content_stack.setCurrentWidget(self.Adaptive_AUTOSAR_view)
        elif view_name == "generic":
            self.content_stack.setCurrentWidget(self.generic_view)
            
    def show_add_vault_dialog(self):
        dialog = AddVaultDialog(self)
        dialog.exec_()
        
    def show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.exec_()
        
    def check_for_updates(self):
        # Check for Triple V updates
        has_update, latest_version, update_data = self.update_manager.check_app_update()
        if has_update:
            self.update_manager.show_update_dialog(self, latest_version, update_data)
        else:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(self, "No Updates", 
                                  f"Triple V is up to date (v{Settings.APP_VERSION})")