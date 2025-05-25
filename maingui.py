import tkinter as tk
from tkinter import ttk, messagebox
import requests
import sys
import subprocess
import webbrowser
from functools import partial

# Check and install missing modules
def install_module(module):
    try:
        __import__(module)
    except ImportError:
        print(f"Installing {module}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])
        
required_modules = ['requests']
for module in required_modules:
    install_module(module)

class KKR_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("KKR - Secure Access")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)  # Make window stay on top
        
        # Current theme (0=grey, 1=black, 2=white)
        self.current_theme = 0  
        
        # Password verification flag
        self.authenticated = False
        
        # Configure styles
        self.setup_styles()
        
        # Show login screen first
        self.show_login_screen()
    
    def setup_styles(self):
        """Configure the visual styles for the application"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Set color scheme based on current theme
        if self.current_theme == 0:  # Grey theme (default)
            self.bg_color = "#f0f0f0"
            self.fg_color = "#333333"
            self.accent_color = "#666666"
            self.dark_accent = "#444444"
            self.light_accent = "#e0e0e0"
            self.button_fg = "white"
        elif self.current_theme == 1:  # Black theme
            self.bg_color = "#121212"
            self.fg_color = "#ffffff"
            self.accent_color = "#333333"
            self.dark_accent = "#222222"
            self.light_accent = "#444444"
            self.button_fg = "white"
        else:  # White theme
            self.bg_color = "#ffffff"
            self.fg_color = "#000000"
            self.accent_color = "#e0e0e0"
            self.dark_accent = "#d0d0d0"
            self.light_accent = "#f0f0f0"
            self.button_fg = "black"
        
        # Base styles
        self.style.configure('.', 
                           background=self.bg_color, 
                           foreground=self.fg_color,
                           font=('Helvetica', 10))
        
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color)
        self.style.configure('TEntry', 
                           fieldbackground="white",
                           foreground=self.fg_color,
                           padding=5)
        
        # Button styles
        self.style.configure('TButton', 
                           background=self.accent_color, 
                           foreground=self.button_fg,
                           borderwidth=0,
                           relief="flat",
                           padding=8)
        
        self.style.map('TButton',
                     background=[('active', self.dark_accent), 
                               ('pressed', self.fg_color)])
        
        # Rounded button style
        self.style.configure('Rounded.TButton',
                           borderwidth=0,
                           relief="flat",
                           background=self.accent_color,
                           foreground=self.button_fg,
                           padding=10)
        
        # Menu button style
        self.style.configure('Menu.TButton',
                           background=self.light_accent,
                           foreground=self.fg_color,
                           padding=8,
                           font=('Helvetica', 9))
        
        self.style.map('Menu.TButton',
                     background=[('active', self.accent_color), 
                               ('pressed', self.dark_accent),
                               ('selected', self.dark_accent)])
        
        # Theme selector buttons
        self.style.configure('GreyTheme.TButton', background='#666666')
        self.style.configure('BlackTheme.TButton', background='#121212')
        self.style.configure('WhiteTheme.TButton', background='#ffffff')
    
    def show_login_screen(self):
        """Display the login/password screen"""
        self.clear_window()
        
        login_frame = ttk.Frame(self.root, padding=20)
        login_frame.pack(expand=True, fill=tk.BOTH)
        
        ttk.Label(login_frame, 
                 text="KKR Secure Access", 
                 font=('Helvetica', 18, 'bold'),
                 foreground=self.accent_color).pack(pady=20)
        
        ttk.Label(login_frame, text="Enter Password:").pack(pady=(20, 5))
        
        self.password_entry = ttk.Entry(login_frame, show="•")
        self.password_entry.pack(pady=5, ipady=5, fill=tk.X)
        self.password_entry.bind('<Return>', lambda e: self.verify_password())
        
        ttk.Button(login_frame, 
                  text="Login", 
                  style='Rounded.TButton',
                  command=self.verify_password).pack(pady=20)
        
        self.status_label = ttk.Label(login_frame, text="", foreground="red")
        self.status_label.pack()
    
    def verify_password(self):
        """Verify the password against the GitHub stored passwords"""
        entered_password = self.password_entry.get()
        
        if not entered_password:
            self.status_label.config(text="Please enter a password")
            return
        
        try:
            # Fetch passwords from GitHub
            url = "https://raw.githubusercontent.com/STORAGERKIR/keys/main/passwords.txt"
            response = requests.get(url)
            response.raise_for_status()
            
            valid_passwords = response.text.splitlines()
            
            if entered_password in valid_passwords:
                self.authenticated = True
                self.show_main_interface()
            else:
                self.status_label.config(text="Invalid password")
        except requests.RequestException as e:
            self.status_label.config(text=f"Connection error: {str(e)}")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
    
    def show_main_interface(self):
        """Show the main application interface after successful login"""
        self.clear_window()
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, 
                 text="KKR", 
                 font=('Helvetica', 20, 'bold'),
                 foreground=self.accent_color).pack()
        
        # Menu categories - centered
        self.setup_menu_categories(main_frame)
        
        # Content area
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Default content
        self.show_category_content("Dashboard")
    
    def setup_menu_categories(self, parent):
        """Create the centered category menu buttons"""
        categories = ["Dashboard", "Settings", "Tools", "Help"]
        
        menu_frame = ttk.Frame(parent)
        menu_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Container to center the buttons
        center_frame = ttk.Frame(menu_frame)
        center_frame.pack()
        
        for category in categories:
            ttk.Button(center_frame, 
                      text=category,
                      style='Menu.TButton',
                      command=partial(self.show_category_content, category)).pack(side=tk.LEFT, padx=2)
    
    def show_category_content(self, category):
        """Show content for the selected category"""
        # Clear previous content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Add category-specific content
        if category == "Dashboard":
            self.create_dashboard_content()
        elif category == "Settings":
            self.create_settings_content()
        elif category == "Tools":
            self.create_tools_content()
        elif category == "Help":
            self.create_help_content()
    
    def create_dashboard_content(self):
        """Content for Dashboard category"""
        frame = ttk.Frame(self.content_frame)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Separator(frame).pack(fill=tk.X, pady=5)
        
        # GitHub item
        item_frame = ttk.Frame(frame)
        item_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(item_frame, text="GitHub").pack(side=tk.LEFT)
        ttk.Button(item_frame, 
                 text="VIEW", 
                 style='TButton',
                 command=lambda: webbrowser.open("https://github.com/STORAGERKIR")).pack(side=tk.RIGHT)
    
    def create_settings_content(self):
        """Content for Settings category"""
        frame = ttk.Frame(self.content_frame)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(frame, text="Application Settings").pack(pady=10)
        ttk.Separator(frame).pack(fill=tk.X, pady=5)
        
        # Theme selector
        theme_frame = ttk.Frame(frame)
        theme_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT)
        
        # Theme buttons
        btn_frame = ttk.Frame(theme_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(btn_frame, 
                 style='GreyTheme.TButton',
                 width=2,
                 command=lambda: self.change_theme(0)).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, 
                 style='BlackTheme.TButton',
                 width=2,
                 command=lambda: self.change_theme(1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, 
                 style='WhiteTheme.TButton',
                 width=2,
                 command=lambda: self.change_theme(2)).pack(side=tk.LEFT, padx=2)
        
        # Updates button
        ttk.Button(frame, 
                  text="Check for Updates", 
                  style='TButton',
                  command=lambda: webbrowser.open("https://github.com/STORAGERKIR/GUI")).pack(fill=tk.X, pady=10)
    
    def change_theme(self, theme_num):
        """Change the application theme"""
        self.current_theme = theme_num
        self.setup_styles()
        self.show_main_interface()  # Refresh the UI
    
    def create_tools_content(self):
        """Content for Tools category"""
        frame = ttk.Frame(self.content_frame)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(frame, text="Available Tools").pack(pady=10)
        ttk.Separator(frame).pack(fill=tk.X, pady=5)
        
        # Sample tools
        tools = ["Analyzer", "Converter", "Generator", "Debugger"]
        for tool in tools:
            ttk.Button(frame, 
                      text=tool, 
                      style='Rounded.TButton').pack(fill=tk.X, pady=5)
    
    def create_help_content(self):
        """Content for Help category"""
        frame = ttk.Frame(self.content_frame)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(frame, text="Help and Support").pack(pady=10)
        ttk.Separator(frame).pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="Contact: salolagang@gmail.com").pack(pady=5)
        ttk.Label(frame, text="Version 1.0").pack(pady=5)
        
        # Buttons frame
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, 
                  text="Discord", 
                  style='Rounded.TButton',
                  command=lambda: webbrowser.open("https://discord.gg/neT5PhnnWw")).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(btn_frame, 
                  text="Logout", 
                  style='Rounded.TButton',
                  command=self.logout).pack(side=tk.LEFT, padx=10)
    
    def logout(self):
        """Log out and return to login screen"""
        self.authenticated = False
        self.show_login_screen()
    
    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = KKR_GUI(root)
    root.mainloop()
