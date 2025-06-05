# Triple V Desktop Application

✨Triple V✨: Vehiclevo Versatile Vault is a comprehensive tool management platform designed to be a unified Hub for all Vehiclevo tools.

## Project Structure

```
triple-v/
├── main.py                     # Application entry point
├── config/
│   ├── settings.py            # Application settings and constants
│   └── tools_registry.json    # Tools configuration file
├── ui/
│   ├── main_window.py         # Main application window
│   ├── sidebar.py             # Animated sidebar navigation
│   ├── views/
│   │   ├── main_view.py       # Main view with logo and buttons
│   │   └── tools_view.py      # Tools grid view
│   ├── components/
│   │   └── tool_card.py       # Individual tool card widget
│   └── dialogs/
│       ├── add_vault_dialog.py    # Add to vault dialog
│       └── about_dialog.py        # About dialog
├── utils/
│   ├── styles.py              # Global stylesheet
│   ├── download_manager.py    # Tool download/update logic
│   └── update_manager.py      # App update checker
├── downloads/                 # Downloaded tools directory
└── assets/
    └── logo.svg              # Triple V logo

```

## Features

### 1. **Modular Architecture**
- Clean separation of concerns
- Easy to extend with new tools
- Reusable components

### 2. **Tool Management System**
- **Download/Update Mechanism**: 
  - Each tool has a `Triple_V_Config.json` in its GitHub repo
  - Version comparison using SemVer
  - Automatic update detection
  - Progress dialog during downloads

### 3. **User Interface**
- **Animated Sidebar**: Smooth expand/collapse animation
- **Tool Cards**: Each tool displays with:
  - Tool name and description
  - Download/Update button (context-aware)
  - GitHub link button
- **Dark Theme**: Modern dark UI with green accents
- **Responsive Design**: Adapts to window resizing

### 4. **Update Strategy**
The update system works as follows:

1. **Tool Configuration**: Each tool repository must contain:
   ```
   repository/
   ├── Triple_V_Config.json    # Tool metadata
   └── tool_name.zip          # Zipped executable
   ```

2. **Triple_V_Config.json Structure**:
   ```json
   {
       "tool_name": "Tool Name",
       "version": "1.0.0"
   }
   ```

3. **Version Management**:
   - Uses semantic versioning (SemVer)
   - Compares installed vs. repository versions
   - Enables update button when newer version available

## Installation & Setup

### Requirements
```bash
pip install -r triple-v-requirements.txt
```

### Running the Application
```bash
python launch_triple_v.py
```

## Adding New Tools

### For Developers Adding Tools:

1. **Prepare Your Repository**:
   - Create `Triple_V_Config.json` with tool info
   - Create a zip file containing your executable
   - Push both to your GitHub repository

2. **Update tools_registry.json**:
   ```json
   {
       "name": "Your Tool Name",
       "description": "Brief description",
       "github_url": "https://github.com/username/repo",
       "icon": "🔧"
   }
   ```

3. **Categories**:
   - `autosar`: AUTOSAR-related tools
   - `non_autosar`: Non-AUTOSAR tools
   - `mixed`: Mixed/Generic tools

### For End Users:

1. **Download Tools**:
   - Navigate to tool category via sidebar
   - Click "Download" button on desired tool
   - Tool will be downloaded to `downloads/` directory

2. **Update Tools**:
   - Tools automatically check for updates on app start
   - "Update" button enables when new version available
   - Click to update to latest version

3. **Check for Triple V Updates**:
   - Click "Check for Updates" button on main screen
   - Downloads latest Triple V version if available

## Key Components

### Settings (config/settings.py)
- Centralized configuration
- Color scheme definitions
- Path management
- Default values

### Download Manager (utils/download_manager.py)
- Handles tool downloads from GitHub
- Version comparison logic
- Progress tracking
- Local tool registry management

### Tool Card (ui/components/tool_card.py)
- Self-contained tool widget
- Automatic status checking
- Download/Update state management
- GitHub link integration

## Customization

### Changing Colors
Edit color values in `config/settings.py`:
```python
PRIMARY_COLOR = "#00ff88"      # Green accent
SECONDARY_COLOR = "#00cc66"    # Darker green
BACKGROUND_COLOR = "#1a1a1a"   # Dark background
SURFACE_COLOR = "#2d2d2d"      # Card backgrounds
TEXT_COLOR = "#ffffff"         # White text
```

### Adding Tool Categories
1. Add new category to `tools_registry.json`
2. Create new view in `ui/views/`
3. Add navigation item in `ui/sidebar.py`
4. Connect in `ui/main_window.py`

## API Integration

The app expects tools to follow this GitHub structure:
- Latest release with zip asset, OR
- Direct file at `repo/main/tool_name.zip`
- `Triple_V_Config.json` in main branch.

## Future Enhancements

1. **Tool Search**: Add search functionality.
2. **Tool Ratings**: User ratings and reviews.

## Troubleshooting

### Common Issues:

1. **Tool won't download**:
   - Check GitHub URL is correct.
   - Ensure `Triple_V_Config.json` exists in the repo main path.
   - Verify zip file is accessible in the repo main path.

2. **Update not detected**:
   - Check version format (must be SemVer).
   - Ensure version in repo is higher.
   - Try restarting the application.

3. **UI scaling issues**:
   - Application supports high DPI displays
   - Adjust system DPI settings if needed

## License

© 2024 Triple V Platform. All rights reserved.

## Support

For issues or questions:
- Create an issue on GitHub
- Contact abdallah.issa@vehiclevo.com
- Check documentation at (TODO:will host the documentation soon somewhere)
