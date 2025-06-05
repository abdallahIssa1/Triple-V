import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from ui.main_window import MainWindow
from utils.styles import load_stylesheet

def main():
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("Triple V")
    app.setOrganizationName("Triple V Platform")

    icon_path = os.path.join(os.path.dirname(__file__), "assets", "triple_v_logo.ico")
    app.setWindowIcon(QIcon(str(icon_path)))
    # Load stylesheet
    app.setStyleSheet(load_stylesheet())
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()