from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QStackedWidget, QLabel, QGraphicsDropShadowEffect, QMessageBox)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal, QTimer, QThread
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
from ui.views.my_tools_view import MyToolsView

class UpdateCheckThread(QThread):
    update_available = pyqtSignal(str, dict)  # version, release_data
    
    def __init__(self, update_manager):
        super().__init__()
        self.update_manager = update_manager
        
    def run(self):
        try:
            has_update, latest_version, release_data = self.update_manager.check_app_update()
            if has_update:
                self.update_available.emit(latest_version, release_data)
        except Exception as e:
            print(f"Update check failed: {e}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.update_manager = UpdateManager()
        self.init_ui()
        # Start automatic update check after UI is ready
        QTimer.singleShot(2000, self.check_updates_automatically)
        
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
        # FIX: Connect the navigation signal to the handler
        self.sidebar.navigation_clicked.connect(self.on_navigation_clicked)
        main_layout.addWidget(self.sidebar)
        
        # Content area
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)
        
        # Views
        self.main_view = MainView()
        self.main_view.add_vault_clicked.connect(self.show_add_vault_dialog)
        self.main_view.about_clicked.connect(self.show_about_dialog)
        
        self.Classical_AUTOSAR = ToolsView("Classical AUTOSAR Tools", "Classical_AUTOSAR")
        self.Adaptive_AUTOSAR_view = ToolsView("Adaptive AUTOSAR Tools", "Adaptive_AUTOSAR")
        self.generic_view = ToolsView("Generic Tools", "generic")
        self.my_tools_view = MyToolsView()
        
        # Add views to stack
        self.content_stack.addWidget(self.main_view)
        self.content_stack.addWidget(self.Classical_AUTOSAR)
        self.content_stack.addWidget(self.Adaptive_AUTOSAR_view)
        self.content_stack.addWidget(self.generic_view)
        self.content_stack.addWidget(self.my_tools_view)
        
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
        print(f"Switching to view: {view_name}")  # Debug line
        if view_name == "main":
            self.content_stack.setCurrentWidget(self.main_view)
        elif view_name == "Classical_AUTOSAR":
            self.content_stack.setCurrentWidget(self.Classical_AUTOSAR)
        elif view_name == "Adaptive_AUTOSAR":
            self.content_stack.setCurrentWidget(self.Adaptive_AUTOSAR_view)
        elif view_name == "generic":
            self.content_stack.setCurrentWidget(self.generic_view)
        elif view_name == "My downloaded Tools":  # FIX: Match the nav_id from sidebar
            self.content_stack.setCurrentWidget(self.my_tools_view)
            if hasattr(self.my_tools_view, 'refresh_tools'):
                self.my_tools_view.refresh_tools()
            
    def show_add_vault_dialog(self):
        dialog = AddVaultDialog(self)
        dialog.exec_()
        
    def show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.exec_()
    
    def check_updates_automatically(self):
        """Check for updates automatically in background"""
        self.update_thread = UpdateCheckThread(self.update_manager)
        self.update_thread.update_available.connect(self.show_update_notification)
        self.update_thread.start()
        
    def show_update_notification(self, latest_version, release_data):
        """Show update notification only if update is available"""
        reply = QMessageBox.question(
            self, "Update Available", 
            f"Triple V v{latest_version} is available!\n\nWould you like to download and install it now?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.update_manager.show_update_dialog(self, latest_version, release_data)