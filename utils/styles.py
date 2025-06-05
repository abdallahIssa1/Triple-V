from config.settings import Settings

def load_stylesheet():
    """Load the global stylesheet for the application"""
    return f"""
        /* Global styles */
        QWidget {{
            background-color: {Settings.BACKGROUND_COLOR};
            color: {Settings.TEXT_COLOR};
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
        
        QScrollBar:vertical {{
            background-color: {Settings.SURFACE_COLOR};
            width: 10px;
            border-radius: 5px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {Settings.PRIMARY_COLOR};
            border-radius: 5px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {Settings.SECONDARY_COLOR};
        }}
        
        QToolTip {{
            background-color: {Settings.SURFACE_COLOR};
            color: {Settings.TEXT_COLOR};
            border: 1px solid {Settings.PRIMARY_COLOR};
            padding: 5px;
            border-radius: 4px;
        }}
    """