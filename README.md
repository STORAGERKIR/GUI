# KKR - Secure Access GUI

A secure, password-protected GUI application with various tools and utilities.

![KKR GUI Screenshot](https://via.placeholder.com/600x500)  <!-- Replace with actual screenshot -->

## Features

### Authentication System
- Password-protected login
- Remote password verification from GitHub
- Secure logging (only first character of password attempts logged)

### Main Interface
- Dashboard with quick links
- Settings panel
- Tools section
- Help and support section

### Available Tools
1. **Solara** - Downloads and runs BootstrapperNew.exe
2. **UNDETEK cs2** - Downloads undetek-v9.9.7.zip and opens official website
3. **Meteor Client 1.21.4** - Downloads and extracts Minecraft mods
4. **FilterKeys (Delay Fixer)** - Downloads and runs FilterKeysSetter.exe

### Settings
- Theme selection (Grey, Black, White)
- Update checker
- FilterKeys utility download

### Logging System
- Automatic log file creation on desktop (`loggs.KKR/loggs.txt`)
- Timestamped actions
- Error logging

## Functions

### Core Functions
- `setup_logging()` - Initializes logging system
- `log_action(action)` - Logs actions with timestamp
- `verify_password()` - Checks password against remote repository
- `change_theme(theme_num)` - Changes application theme

### Download Utilities
- `download_and_run_filterkeys()` - Downloads FilterKeysSetter.exe
- `download_meteor_client()` - Downloads Minecraft Meteor Client
- `download_and_run_bootstrapper()` - Downloads BootstrapperNew.exe
- `download_undetek_and_open_site()` - Downloads UNDETEK and opens website

### UI Management
- `show_login_screen()` - Displays authentication screen
- `show_main_interface()` - Shows main application interface
- `show_category_content(category)` - Displays content for selected category
- `clear_window()` - Clears all widgets from root window

## Requirements
- Python 3.x
- Required packages:
