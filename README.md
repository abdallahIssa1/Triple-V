# Triple V - Vehiclevo Versatile Vault 🗃️🛒

<div align="center">
  <img src="assets/triple_v_logo.png" alt="Triple V Logo" width="200"/>
  
  [![Version](https://img.shields.io/badge/version-4.0.0-green.svg)](https://github.com/abdallahIssa1/Triple-V/releases)
  [![License](https://img.shields.io/badge/license-Proprietary-blue.svg)](LICENSE)
  [![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
  
  **A comprehensive tool management platform for Vehiclevo**
</div>

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [For Developers](#for-developers)
- [Tool Categories](#tool-categories)
- [Contributing](#contributing)
- [Support](#support)
- [License](#License)

## 🎯 Overview

**Triple V (Vehiclevo Versatile Vault)** Vehiclevo Versatile Vault is a comprehensive tool management platform designed to be a unified Hub for all Vehiclevo tools.

### Why Triple V?

- **Vehiclevo**: Built only for Vehiclevo.
- **Versatile**: Supporting tools across the entire automotive development spectrum.
- **Vault**: A versioned repository where every tool is documented and easily discoverable.

## ✨ Features

### 🔧 Core Features

- **Smart Tool Management**
  - One-click download and installation.
  - Automatic version checking and updates.
  - Organized categorization (Classical AUTOSAR, Adaptive AUTOSAR, Generic).
- **Modern UI/UX**
  - Dark theme with the fancy vehiclevo turquoise color.
  - Animated sidebar navigation.
  - Responsive design for all screen sizes.
- **Seamless Updates**
  - Self-updating mechanism for Triple V Application itself.
  - Individual tool update mechanism.
  - Version-aware executable naming (e.g., `TripleV_v4.0.0.exe`)
- **Community-Driven**
  - "Add to Vault" feature for tool submissions.
  - Email-based contribution workflow.
  - Quality assurance through review process.


## 💾 Installation

### System Requirements

- **OS**: Windows 10/11 (64-bit).
- **Storage**: 50MB for Triple V App exe + additional space for downloaded tools.

### Quick Start

1. **Download the latest release**
   https://github.com/abdallahIssa1/Triple-V/releases/latest  
2. **Extract and run**  
   - Extract `TripleV_v4.0.0.zip`  
   - Run `TripleV_v4.0.0.exe`  
3. **First launch**
   - Triple V will create necessary directories.
   - Check for updates automatically.
   - Ready to download tools!

## 📖 Usage Guide

## 🧑‍🤝‍🧑 For End Users

#### 1. Navigating the Interface

- **Sidebar Navigation**: Click the hamburger menu to expand/collapse  
- 🏠 Home: Main dashboard with core actions  
- 🌱 Classical AUTOSAR: Traditional AUTOSAR tools  
- 🐧 Adaptive AUTOSAR: Modern AUTOSAR tools  
- 🧩 Generic Tools: Cross-domain utilities  

#### 2. Downloading Tools

1. Navigate to the desired category.
2. Browse available tools.
3. Click "Download" on any tool card.
4. Monitor progress in the dialog.
5. Find downloaded tools in `My Downloaded Tools` folder.

#### 3. Updating Tools

- Tools automatically check for updates on startup.
- Orange "Update" button appears when updates are available.
- Click to update with one click.

#### 4. Checking for Triple V Updates

1. Click "Check for Updates" on the home screen.
2. If an update is available, follow the prompts.
3. Triple V will update itself and restart.

#### 5. Contributing Tools

1. Click "Add to Vault" on the home screen.
2. Fill in all required information:
   - Check all required boxes.
   - Select appropriate category.
   - Enter your Vehiclevo email.
   - Provide GitHub repository URL.
3. Submit for review.

## 👩‍💻 For Developers

### ✍️ Adding Your Tool to Triple V

#### Prerequisites

1. GitHub repository for your tool.
2. Working executable (`.exe`).
3. Version management strategy.

#### Step 1: Prepare Your Repository

***Ensure YourTool.zip is in the main branch***

```
your-tool-repo/
├── YourTool.zip # Contains your .exe file
├── Triple_V_Config.json # Version metadata
└── README.md # Tool documentation
```

#### Step 2: Create Triple_V_Config.json

***Ensure Triple_V_Config.json is in the main branch***

```json
{
  "version": "1.0.0",
  "tool_name": "Your Tool Name",
  "description": "Brief description of your tool"
}
```

### 🔨 Building Triple V from Source

#### Requirements
```bash
pip install -r triple-v-requirements.txt
```


#### Project Structure
```
Triple-V/
├── main.py              # Entry point
├── config/              # Configuration files
│   ├── settings.py      # Application settings
│   └── tools_registry.json
├── ui/                  # User interface
│   ├── main_window.py
│   ├── sidebar.py
│   ├── views/
│   ├── components/
│   └── dialogs/
├── utils/               # Utilities
│   ├── download_manager.py
│   └── update_manager.py
└── assets/              # Resources
    ├── triple_v_logo.png
    ├── triple_v_logo.ico
    └── triple_v_pulse.gif
```
#### Building Executable
```
pyinstaller --name="TripleV_v4.0.0" \
            --onefile \
            --windowed \
            --icon=assets/icon.ico \
            --add-data="assets;assets" \
            --add-data="config;config" \
            main.py
```

## 📚 Tool Categories

- 🌱 Classical AUTOSAR Tools
- 🐧 Adaptive AUTOSAR Tools
- 🧩 Generic Tools

## 🤝 Contributing

We welcome contributions from all Vehiclevo engineers!

### How to Contribute

1. Develop your tool.
2. Test thoroughly.
3. Document usage.
4. Submit via "Add to Vault".

### Contribution Guidelines

- ✅ Tools must be stable and tested.
- ✅ Include comprehensive documentation.
- ✅ Follow semantic versioning (SemVer).
- ✅ Ensure Windows compatibility.
- ✅ No malicious code.

### Review Process

1. Submission received via email.
2. Technical and stability review by the Reviewers (mainly abdallah.issa and ahmed.Dawoud).
3. Integration into tools registry.

## 🆘 Support

### Getting Help
- Documentation: Check this README and usage PDF.
- Issues: Contact the development team.
- Email: abdallah.issa@vehiclevo.com -> (TODO: to be replaced by triplev@vehiclevo.com or something like).

## 📜 License
Copyright © 2024 Vehiclevo. All rights reserved.
This software is proprietary to Vehiclevo and for internal use only.

<div align="center">
  <b>Triple V</b>
  <br>
  Made with ❤️ to Vehiclevo
</div>
