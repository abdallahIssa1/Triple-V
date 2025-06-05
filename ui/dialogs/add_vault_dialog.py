from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QCheckBox, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from PyQt5.QtGui import QFont, QPainter, QColor
from config.settings import Settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class AddVaultDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add to Vault")
        self.setFixedSize(500, 600)
        self.setModal(True)
        self.init_ui()
        
    def init_ui(self):
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {Settings.SURFACE_COLOR};
                border: 2px solid {Settings.PRIMARY_COLOR};
                border-radius: 16px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("Add to Vault")
        header.setFont(QFont("Segoe UI", 24, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(f"color: {Settings.PRIMARY_COLOR};")
        layout.addWidget(header)
        
        # Checkboxes
        self.checkboxes = []
        checkbox_texts = [
            "I have tested the tool",
            "I have checked There're no compatibility or portability Issues",
            "I have provided a guide for the end user"
        ]
        
        for text in checkbox_texts:
            checkbox_container = QHBoxLayout()
            checkbox = QCheckBox(text)
            checkbox.setFont(QFont("Segoe UI", 11))
            checkbox.stateChanged.connect(self.check_form_complete)
            checkbox.setStyleSheet(f"""
                QCheckBox {{
                    color: {Settings.TEXT_COLOR};
                    spacing: 10px;
                }}
                QCheckBox::indicator {{
                    width: 24px;
                    height: 24px;
                    border: 2px solid {Settings.PRIMARY_COLOR};
                    border-radius: 4px;
                    background-color: transparent;
                }}
                QCheckBox::indicator:checked {{
                    background-color: {Settings.PRIMARY_COLOR};
                    image: url(triple_v_logo.png);
                }}
            """)
            self.checkboxes.append(checkbox)
            checkbox_container.addWidget(checkbox)
            layout.addLayout(checkbox_container)
            
        # Input fields
        self.inputs = {}
        input_fields = [
            ("Which category", "Which category", "Enter in which category the tool should be in"),
            ("Your email", "Your email", "Enter Your Vehiclevo email"),
            ("GitHub Repo Link", "GitHub Repo Link", "Enter GitHub Repo Link")
        ]
        
        for field_id, label_text, placeholder in input_fields:
            label = QLabel(label_text)
            label.setFont(QFont("Segoe UI", 12, QFont.Bold))
            label.setStyleSheet(f"color: {Settings.PRIMARY_COLOR};")
            
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(placeholder)
            line_edit.setFont(QFont("Segoe UI", 11))
            line_edit.textChanged.connect(self.check_form_complete)
            line_edit.setStyleSheet(f"""
                QLineEdit {{
                    background-color: rgba(255, 255, 255, 0.05);
                    border: 2px solid #444;
                    border-radius: 8px;
                    padding: 10px;
                    color: {Settings.TEXT_COLOR};
                    font-size: 14px;
                }}
                QLineEdit:focus {{
                    border-color: {Settings.PRIMARY_COLOR};
                    background-color: rgba(0, 255, 136, 0.05);
                }}
            """)
            
            self.inputs[field_id] = line_edit
            layout.addWidget(label)
            layout.addWidget(line_edit)
            
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.submit_btn = QPushButton("Submit to Vault")
        self.submit_btn.setFixedHeight(50)
        self.submit_btn.setEnabled(False)
        self.submit_btn.setCursor(Qt.PointingHandCursor)
        self.submit_btn.clicked.connect(self.submit_form)
        self.update_submit_button_style()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(40)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet(f"""
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
        
        button_layout.addWidget(self.submit_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
    def update_submit_button_style(self):
        if self.submit_btn.isEnabled():
            self.submit_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Settings.PRIMARY_COLOR};
                    border: none;
                    border-radius: 8px;
                    color: {Settings.BACKGROUND_COLOR};
                    font-size: 16px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {Settings.SECONDARY_COLOR};
                }}
            """)
        else:
            self.submit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #444;
                    border: none;
                    border-radius: 8px;
                    color: #888;
                    font-size: 16px;
                    font-weight: bold;
                }
            """)
            
    def check_form_complete(self):
        all_checked = all(cb.isChecked() for cb in self.checkboxes)
        all_filled = all(le.text().strip() for le in self.inputs.values())
        
        self.submit_btn.setEnabled(all_checked and all_filled)
        self.update_submit_button_style()
        
    def submit_form(self):
        # Show success message
        self.show_success_splash()
        
        # Send email (implement your email logic here)
        # self.send_email()
        
        # Close dialog after delay
        QTimer.singleShot(2000, self.accept)
        
    def show_success_splash(self):
        splash = QLabel("✓ Successfully Added to Vault!", self)
        splash.setAlignment(Qt.AlignCenter)
        splash.setFont(QFont("Segoe UI", 20, QFont.Bold))
        splash.setStyleSheet(f"""
            QLabel {{
                background-color: {Settings.PRIMARY_COLOR};
                color: {Settings.BACKGROUND_COLOR};
                padding: 40px 60px;
                border-radius: 16px;
            }}
        """)
        
        # Position at center
        splash.resize(400, 100)
        splash.move(50, 250)
        splash.show()
        splash.raise_()