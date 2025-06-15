from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QCheckBox, QPushButton, QMessageBox,
    QComboBox, QScrollArea, QWidget, QTextEdit
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from config.settings import Settings
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import keyring

class AddVaultDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add to Vault")
        # Make dialog responsive to screen size
        self.setMinimumSize(550, 500)
        self.resize(550, 650)
        self.setModal(True)

        # Email and URL validation regex
        self.mail_regex = r'\b[A-Za-z0-9._%+-]+@vehiclevo\.(com|de)\b'
        self.url_regex = r'^(https?:\/\/)?github\.com\/[A-Za-z0-9_.-]+(?:\/[A-Za-z0-9_.-]+)?$'

        self.init_ui()

        # Adjust size based on screen
        self.adjust_to_screen()

    def adjust_to_screen(self):
        """Adjust dialog size based on available screen space"""
        from PyQt5.QtWidgets import QDesktopWidget
        screen = QDesktopWidget().screenGeometry()

        # If screen height is less than 800px, make dialog smaller
        if screen.height() < 800:
            self.resize(550, min(screen.height() - 100, 600))
        else:
            self.resize(550, 650)



    def init_ui(self):
        # 1) Top‐level layout for the dialog itself
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  # We'll let inner widgets handle padding

        # 2) Create a QScrollArea (vertical scrollbar enabled by default)
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)  # Let the content widget expand to the width
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Always show scrollbar
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # No horizontal scroll
        scroll.setStyleSheet("""
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
        main_layout.addWidget(scroll)

        # 3) Create a separate QWidget to hold all form content
        content_widget = QWidget()
        scroll.setWidget(content_widget)

        # 4) Attach a VBoxLayout to content_widget, and move all existing widgets into it
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(50, 50, 50, 50)  # replicate your previous margins
        layout.setSpacing(20)

        # ----- HEADER -----
        header = QLabel("Add to Vault")
        header.setFont(QFont("Segoe UI", 28, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(f"color: {Settings.PRIMARY_COLOR};")
        layout.addWidget(header)

        # Add some vertical space after header
        layout.addSpacing(15)

        # ----- CHECKBOXES -----
        self.checkboxes = []
        checkbox_texts = [
            "I have tested the tool core functionality.",
            "I have checked there're no portability Issues.",
            "I have provided a guide for the enduser."
        ]
        for text in checkbox_texts:
            # Create a simpler, more familiar checkbox style:
            checkbox = QCheckBox(text)
            checkbox.setFont(QFont("Segoe UI", 11))
            checkbox.stateChanged.connect(self.check_form_complete)
            checkbox.setStyleSheet(f"""
                QCheckBox {{
                    color: {Settings.TEXT_COLOR};
                    spacing: 10px;
                    padding: 5px 0;
                }}
                /* Draw a light border so the user sees a checkbox box */
                QCheckBox::indicator {{
                    width: 18px;
                    height: 18px;
                    border: 2px solid {Settings.PRIMARY_COLOR};
                    border-radius: 3px;
                    background-color: {Settings.BACKGROUND_COLOR};
                }}
                /* When checked, let Qt draw the standard checkmark over the colored box */
                QCheckBox::indicator:checked {{
                    background-color: {Settings.PRIMARY_COLOR};
                }}
            """)
            self.checkboxes.append(checkbox)
            layout.addWidget(checkbox)
        layout.addSpacing(15)

        # ----- CATEGORY DROPDOWN -----
        category_label = QLabel("Which Category")
        category_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        category_label.setStyleSheet(f"color: {Settings.PRIMARY_COLOR};")
        layout.addWidget(category_label)

        self.category_combo = QComboBox()
        self.category_combo.addItems([
            "Classical AUTOSAR related tools",
            "Adaptive AUTOSAR related tools",
            "Generic Tools"
        ])
        self.category_combo.currentTextChanged.connect(self.check_form_complete)
        self.category_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: rgba(255, 255, 255, 0.05);
                border: 2px solid #444;
                border-radius: 8px;
                padding: 12px 15px;
                color: {Settings.TEXT_COLOR};
                font-size: 14px;
                min-height: 25px;
            }}
            QComboBox:focus {{
                border-color: {Settings.PRIMARY_COLOR};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {Settings.PRIMARY_COLOR};
                margin-right: 10px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {Settings.SURFACE_COLOR};
                border: 1px solid {Settings.PRIMARY_COLOR};
                selection-background-color: {Settings.PRIMARY_COLOR};
                color: {Settings.TEXT_COLOR};
            }}
        """)
        layout.addWidget(self.category_combo)
        layout.addSpacing(15)

        # ----- EMAIL INPUT -----
        email_label = QLabel("Your Email")
        email_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        email_label.setStyleSheet(f"color: {Settings.PRIMARY_COLOR};")
        layout.addWidget(email_label)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("your.name@vehiclevo.com or @vehiclevo.de")
        self.email_input.textChanged.connect(self.check_form_complete)
        self.email_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: rgba(255, 255, 255, 0.05);
                border: 2px solid #444;
                border-radius: 8px;
                padding: 12px 15px;
                color: {Settings.TEXT_COLOR};
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border-color: {Settings.PRIMARY_COLOR};
                background-color: rgba(0, 255, 136, 0.05);
            }}
        """)
        layout.addWidget(self.email_input)
        layout.addSpacing(15)

        # ----- GITHUB URL INPUT -----
        github_label = QLabel("Link to GitHub Repository")
        github_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        github_label.setStyleSheet(f"color: {Settings.PRIMARY_COLOR};")
        layout.addWidget(github_label)

        self.github_input = QLineEdit()
        self.github_input.setPlaceholderText("https://github.com/username/repository")
        self.github_input.textChanged.connect(self.check_form_complete)
        self.github_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: rgba(255, 255, 255, 0.05);
                border: 2px solid #444;
                border-radius: 8px;
                padding: 12px 15px;
                color: {Settings.TEXT_COLOR};
                font-size: 14px;
                min-height: 25px;
            }}
            QLineEdit:focus {{
                border-color: {Settings.PRIMARY_COLOR};
                background-color: rgba(0, 255, 136, 0.05);
            }}
        """)
        layout.addWidget(self.github_input)
        layout.addSpacing(15)

        # ----- ERROR LABEL -----
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #ff4444; font-size: 12px; padding: 5px 0;")
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        layout.addWidget(self.error_label)

        layout.addStretch()  # Push buttons to the bottom

        # ----- BUTTONS -----
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 20, 0, 0)  # Add top margin

        self.submit_btn = QPushButton("Submit to Vault")
        self.submit_btn.setFixedHeight(45)
        self.submit_btn.setFixedWidth(180)
        self.submit_btn.setEnabled(False)
        self.submit_btn.setCursor(Qt.PointingHandCursor)
        self.submit_btn.clicked.connect(self.submit_form)
        self.update_submit_button_style()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(45)
        cancel_btn.setFixedWidth(180)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 2px solid {Settings.PRIMARY_COLOR};
                border-radius: 8px;
                color: {Settings.PRIMARY_COLOR};
                font-weight: bold;
                font-size: 15px;
            }}
            QPushButton:hover {{
                background-color: {Settings.PRIMARY_COLOR};
                color: {Settings.BACKGROUND_COLOR};
            }}
        """)

        button_layout.addWidget(self.submit_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        # ----- TOOL ICON -----
        icon_label = QLabel("Tool Icon (Emoji)")
        icon_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        icon_label.setStyleSheet(f"color: {Settings.PRIMARY_COLOR};")
        layout.addWidget(icon_label)

        self.icon_input = QLineEdit()
        self.icon_input.setPlaceholderText("e.g., 🔧 or 📊 or 💻")
        self.icon_input.setMaxLength(2)  # Usually one emoji
        self.icon_input.textChanged.connect(self.check_form_complete)
        self.icon_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: rgba(255, 255, 255, 0.05);
                border: 2px solid #444;
                border-radius: 8px;
                padding: 12px 15px;
                color: {Settings.TEXT_COLOR};
                font-size: 20px;
                min-height: 25px;
            }}
            QLineEdit:focus {{
                border-color: {Settings.PRIMARY_COLOR};
                background-color: rgba(0, 255, 136, 0.05);
            }}
        """)
        layout.addWidget(self.icon_input)
        layout.addSpacing(15)

        # ----- TOOL DESCRIPTION -----
        desc_label = QLabel("Tool Description")
        desc_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        desc_label.setStyleSheet(f"color: {Settings.PRIMARY_COLOR};")
        layout.addWidget(desc_label)

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Brief description of what your tool does...")
        self.desc_input.setMaximumHeight(80)
        self.desc_input.textChanged.connect(self.check_form_complete)
        self.desc_input.setStyleSheet(f"""
            QTextEdit {{
                background-color: rgba(255, 255, 255, 0.05);
                border: 2px solid #444;
                border-radius: 8px;
                padding: 12px 15px;
                color: {Settings.TEXT_COLOR};
                font-size: 14px;
            }}
            QTextEdit:focus {{
                border-color: {Settings.PRIMARY_COLOR};
                background-color: rgba(0, 255, 136, 0.05);
            }}
        """)
        layout.addWidget(self.desc_input)
        layout.addSpacing(15)

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
        # Check that all checkboxes are checked
        all_checked = all(cb.isChecked() for cb in self.checkboxes)
        email = self.email_input.text().strip()
        github_url = self.github_input.text().strip()

        # Validate email
        email_valid = bool(re.match(self.mail_regex, email)) if email else False

        # Validate GitHub URL
        url_valid = bool(re.match(self.url_regex, github_url)) if github_url else False

        # Show validation errors if needed
        errors = []
        if not all_checked and any(cb.isChecked() for cb in self.checkboxes):
            errors.append("Please check all confirmation boxes")
        if email and not email_valid:
            errors.append("Email must be @vehiclevo.com or @vehiclevo.de")
        if github_url and not url_valid:
            errors.append("Must be a valid GitHub repository URL")

        if errors:
            self.error_label.setText(" • ".join(errors))
            self.error_label.show()
        else:
            self.error_label.hide()

        # Enable submit only if everything is filled and valid
        all_filled = bool(email and github_url and icon and description)
        all_valid = bool(email_valid and url_valid)
        self.submit_btn.setEnabled(all_checked and all_filled and all_valid)
        self.update_submit_button_style()

    def submit_form(self):
        # Collect form data
        form_data = {
            "category": self.category_combo.currentText(),
            "email": self.email_input.text().strip(),
            "github_url": self.github_input.text().strip(),
            "icon": self.icon_input.text().strip(),
            "description": self.desc_input.toPlainText().strip()

        }

        # Send email
        if self.send_email(form_data):
            # Show success label, then auto‐close
            self.show_success_splash()
            QTimer.singleShot(2000, self.accept)
        else:
            QMessageBox.warning(self, "Error", "Failed to send email. Please try again.")

    def send_email(self, form_data):
        """Send email with vault submission data."""
        try:
            # Email configuration (update with real SMTP settings)
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            sender_email = "abdallahissa9800@gmail.com"
            
            # sender_password = ""
            # I'll use library called Keyring here to not show my password in the code
            # -> needs additional tweaks in the future to be sent from my veh email (TODO: contact IT guys)
            
            # Get password from system keyring
            sender_password = keyring.get_password("Triple_V", sender_email)
            print(f"sender password: {sender_password}")
            if not sender_password:
                print("Email password not found in keyring")
                return False
            recipient_email = "abdallah.issa@vehiclevo.com"

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = f"New Tool Submission - {form_data['category']}"

            body = f"""
            New Tool Submission to Triple V Vault
            =====================================

            Submission Details:
            ------------------
            Category: {form_data['category']}
            Submitted By: {form_data['email']}
            GitHub Repository: {form_data['github_url']}
            Icon: {form_data['icon']}
            Description: {form_data['description']}
            Submission Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

            Action Required from the Reviewers:
            ----------------------------------
            1. Verify the tool meets quality standards.
            2. Add to tools_registry.json if approved.

            --
            Triple V Platform
            Automated Submission System
            """
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)

            print(f"Email sent successfully for: {form_data}")
            return True

        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

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
        splash.resize(400, 100)
        # Center the splash inside the dialog’s 550×600 area
        splash.move((550 - splash.width()) // 2, (600 - splash.height()) // 2)
        splash.show()
        splash.raise_()
