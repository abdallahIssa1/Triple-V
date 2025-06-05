from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QScrollArea, QWidget, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from config.settings import Settings

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Triple V")
        # Make the dialog a bit smaller than before (e.g. 400×500)
        self.setFixedSize(400, 500)
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        # Overall dialog style
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {Settings.SURFACE_COLOR};
                border: 2px solid {Settings.PRIMARY_COLOR};
                border-radius: 16px;
            }}
        """)

        # --- STEP 1: Create a QVBoxLayout for the dialog itself ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # --- STEP 2: Create a QScrollArea and make it resize with the dialog ---
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        main_layout.addWidget(scroll)

        # --- STEP 3: Create a content QWidget that holds the original "About" layout ---
        content = QWidget()
        scroll.setWidget(content)

        # --- STEP 4: Move your old layout code inside this content widget ---
        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignTop)

        # Header
        header = QLabel("About Triple V")
        header.setFont(QFont("Segoe UI", 24, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(f"color: {Settings.PRIMARY_COLOR};")
        layout.addWidget(header)

        # Version info
        version_label = QLabel(f"Triple-V Platform - Version {Settings.APP_VERSION}")
        version_label.setFont(QFont("Segoe UI", 12))
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("color: #ddd;")
        layout.addWidget(version_label)

        # Developer info container
        dev_container = QVBoxLayout()
        dev_container.setSpacing(8)

        dev_header = QLabel("Development Team")
        dev_header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        dev_header.setAlignment(Qt.AlignCenter)
        dev_header.setStyleSheet(f"color: {Settings.PRIMARY_COLOR};")
        dev_container.addWidget(dev_header)

        developers = [
            ("Lead Developer", "Abdallah Issa"),
            ("UI/UX Designer", "Abdallah Issa"),
            ("Backend Engineer", "Abdallah Issa")
        ]
        for role, name in developers:
            dev_label = QLabel(f"<b>{role}:</b> {name}")
            dev_label.setFont(QFont("Segoe UI", 11))
            dev_label.setAlignment(Qt.AlignCenter)
            dev_label.setStyleSheet("color: #ccc;")
            dev_container.addWidget(dev_label)

        layout.addLayout(dev_container)

        # Description
        description = QLabel(
            "✨Triple V✨: Vehiclevo Versatile Vault is a comprehensive tool management platform "
            "designed to be a unified Hub for all Vehiclevo tools."
        )
        description.setFont(QFont("Segoe UI", 11))
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignCenter)
        description.setStyleSheet("color: #aaa; line-height: 1.5;")
        layout.addWidget(description)

        # Copyright
        copyright_label = QLabel("© 2024 Triple V Platform. All rights reserved.")
        copyright_label.setFont(QFont("Segoe UI", 10))
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet("color: #888;")
        layout.addWidget(copyright_label)

        layout.addStretch()

        # Close button
        close_btn = QPushButton("Close")
        close_btn.setFixedHeight(36)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 2px solid {Settings.PRIMARY_COLOR};
                border-radius: 8px;
                color: {Settings.PRIMARY_COLOR};
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {Settings.PRIMARY_COLOR};
                color: {Settings.BACKGROUND_COLOR};
            }}
        """)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)
