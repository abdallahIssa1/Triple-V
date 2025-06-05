from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal, QRect
from PyQt5.QtGui import QPainter, QColor, QFont
from config.settings import Settings

class SidebarButton(QPushButton):
    def __init__(self, text, icon="", parent=None):
        super().__init__(parent)
        self.text_label = text
        self.icon = icon
        self.setFixedHeight(50)
        self.setCursor(Qt.PointingHandCursor)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background on hover/active
        if self.isChecked() or self.underMouse():
            painter.fillRect(self.rect(), QColor(0, 255, 136, 30))
            
        # Active indicator
        if self.isChecked():
            painter.fillRect(0, 0, 3, self.height(), QColor(Settings.PRIMARY_COLOR))
            
        # Icon
        if self.icon:
            painter.setFont(QFont("Segoe UI Emoji", 20))
            painter.setPen(QColor(Settings.PRIMARY_COLOR))
            icon_rect = QRect(10, 0, 40, self.height())
            painter.drawText(icon_rect, Qt.AlignCenter, self.icon)
            
        # Text (only when expanded)
        if self.width() > 100:
            painter.setFont(QFont("Segoe UI", 11))
            painter.setPen(QColor(Settings.TEXT_COLOR))
            text_rect = QRect(60, 0, self.width() - 70, self.height())
            painter.drawText(text_rect, Qt.AlignVCenter, self.text_label)

class Sidebar(QWidget):
    navigation_clicked = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.expanded = False
        self.init_ui()
        
    def init_ui(self):
        self.setFixedWidth(Settings.SIDEBAR_WIDTH)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #151515;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Toggle button
        self.toggle_btn = QPushButton()
        self.toggle_btn.setFixedSize(60, 60)
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)
        layout.addWidget(self.toggle_btn)
        
        # Navigation buttons
        self.nav_buttons = []
        
        nav_items = [
            ("main", "Home", "🏠"),
            ("autosar", "AUTOSAR-Related", "🌱"),
            ("non_autosar", "Non-AUTOSAR-Related", "💻"),
            ("mixed", "Mixed/Generic Tools", "🧩")
        ]
        
        for nav_id, text, icon in nav_items:
            btn = SidebarButton(text, icon)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, n=nav_id: self.on_nav_clicked(n))
            if nav_id == "main":
                btn.setChecked(True)
            layout.addWidget(btn)
            self.nav_buttons.append(btn)
            
        layout.addStretch()
        
        # Animation
        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(Settings.ANIMATION_DURATION)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        
    def toggle_sidebar(self):
        self.expanded = not self.expanded
        
        end_width = Settings.SIDEBAR_EXPANDED_WIDTH if self.expanded else Settings.SIDEBAR_WIDTH
        
        self.animation.setStartValue(self.width())
        self.animation.setEndValue(end_width)
        self.animation.start()
        
    def on_nav_clicked(self, nav_id):
        # Uncheck all buttons
        for btn in self.nav_buttons:
            btn.setChecked(False)
            
        # Check clicked button
        sender = self.sender()
        if sender:
            sender.setChecked(True)
            
        self.navigation_clicked.emit(nav_id)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#151515"))
        
        # Draw hamburger menu
        painter.setPen(QColor(Settings.PRIMARY_COLOR))
        painter.setBrush(QColor(Settings.PRIMARY_COLOR))
        
        x, y = 20, 25
        bar_height = 3
        bar_spacing = 7
        bar_width = 20
        
        if not self.expanded:
            # Normal hamburger
            for i in range(3):
                painter.drawRect(x, y + i * bar_spacing, bar_width, bar_height)
        else:
            # X shape
            painter.save()
            painter.translate(x + bar_width/2, y + bar_spacing)
            painter.rotate(45)
            painter.drawRect(int(-bar_width/2), int(-bar_height/2), int(bar_width), int(bar_height))
            painter.rotate(-90)
            painter.drawRect(int(-bar_width/2), int(-bar_height/2), int(bar_width), int(bar_height))
            painter.restore()
