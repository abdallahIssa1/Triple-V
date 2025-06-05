from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QRect
from PyQt5.QtGui import QPainter, QColor, QLinearGradient, QFont
from PyQt5.QtSvg import QSvgWidget
from config.settings import Settings

class AnimatedLogo(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 200)
        self.angle = 0
        
        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)
        
        # Float animation
        self.float_animation = QPropertyAnimation(self, b"geometry")
        self.float_animation.setDuration(3000)
        self.float_animation.setLoopCount(-1)
        
    def update_animation(self):
        self.angle = (self.angle + 2) % 360
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background with gradient
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(Settings.PRIMARY_COLOR))
        gradient.setColorAt(1, QColor(Settings.SECONDARY_COLOR))
        
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 30, 30)
        
        # Draw VVV text
        painter.setPen(QColor(26, 26, 26))
        painter.setFont(QFont("Arial", 72, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, "V")
        
        # Animated shine effect
        painter.save()
        painter.translate(self.width()/2, self.height()/2)
        painter.rotate(self.angle)
        
        shine_gradient = QLinearGradient(-100, -100, 100, 100)
        shine_gradient.setColorAt(0, QColor(255, 255, 255, 0))
        shine_gradient.setColorAt(0.5, QColor(255, 255, 255, 30))
        shine_gradient.setColorAt(1, QColor(255, 255, 255, 0))
        
        painter.setBrush(shine_gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRect(-150, -10, 300, 20)
        painter.restore()

class StyledButton(QPushButton):
    def __init__(self, text, enabled=True):
        super().__init__(text)
        self.setEnabled(enabled)
        self.setFixedSize(200, 60)
        self.setCursor(Qt.PointingHandCursor if enabled else Qt.ForbiddenCursor)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Button background
        if self.isEnabled():
            gradient = QLinearGradient(0, 0, self.width(), self.height())
            gradient.setColorAt(0, QColor(42, 42, 42))
            gradient.setColorAt(1, QColor(58, 58, 58))
            painter.setBrush(gradient)
            
            if self.underMouse():
                painter.setPen(QColor(Settings.PRIMARY_COLOR))
            else:
                painter.setPen(QColor(Settings.PRIMARY_COLOR).darker())
        else:
            painter.setBrush(QColor(40, 40, 40))
            painter.setPen(QColor(100, 100, 100))
            
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 12, 12)
        
        # Button text
        painter.setPen(QColor(Settings.TEXT_COLOR) if self.isEnabled() else QColor(100, 100, 100))
        painter.setFont(QFont("Segoe UI", 14, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())

class MainView(QWidget):
    add_vault_clicked = pyqtSignal()
    about_clicked = pyqtSignal()
    check_updates_clicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(40)
        
        # Logo
        self.logo = AnimatedLogo()
        layout.addWidget(self.logo, alignment=Qt.AlignCenter)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(30)
        
        self.add_vault_btn = StyledButton("Add to Vault")
        self.add_vault_btn.clicked.connect(self.add_vault_clicked.emit)
        
        self.about_btn = StyledButton("About")
        self.about_btn.clicked.connect(self.about_clicked.emit)
        
        self.check_updates_btn = StyledButton("Check for Updates")
        self.check_updates_btn.clicked.connect(self.check_updates_clicked.emit)
        
        button_layout.addWidget(self.add_vault_btn)
        button_layout.addWidget(self.about_btn)
        button_layout.addWidget(self.check_updates_btn)
        
        layout.addLayout(button_layout)