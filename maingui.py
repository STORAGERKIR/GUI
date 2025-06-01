import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
import webbrowser
from functools import partial
from urllib.request import urlretrieve
import subprocess
import sys
import zipfile

class KKR_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("KKR - Secure Access")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        
        # Theme and authentication
        self.current_theme = 0
        self.authenticated = False
        self.setup_styles()
        self.show_login_screen()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.root.destroy()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        if self.current_theme == 0:  # Grey
            self.bg_color = "#f0f0f0"
            self.fg_color = "#333333"
            self.accent_color = "#666666"
            self.button_fg = "white"
        elif self.current_theme == 1:  # Black
            self.bg_color = "#121212"
            self.fg_color = "#ffffff"
            self.accent_color = "#333333"
            self.button_fg = "white"
        else:  # White
            self.bg_color = "#ffffff"
            self.fg_color = "#000000"
            self.accent_color = "#e0e0e0"
            self.button_fg = "black"
            
        self.style.configure('.', 
            background=self.bg_color, 
            foreground=self.fg_color,
            font=('Helvetica', 10))
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color)
        self.style.configure('TButton', 
            background=self.accent_color, 
            foreground=self.button_fg,
            padding=8)
        self.style.map('TButton',
            background=[('active', '#888888'), ('pressed', '#555555')])

    def show_login_screen(self):
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
            style='TButton',
            command=self.verify_password).pack(pady=20)
        
        self.status_label = ttk.Label(login_frame, text="", foreground="red")
        self.status_label.pack()

    def verify_password(self):
        entered_password = self.password_entry.get()
        if not entered_password:
            self.status_label.config(text="Please enter a password")
            return
        
        try:
            url = "https://raw.githubusercontent.com/STORAGERKIR/keys/main/passwords.txt"
            response = requests.get(url)
            response.raise_for_status()
            
            if entered_password in response.text.splitlines():
                self.authenticated = True
                self.show_main_interface()
            else:
                self.status_label.config(text="Invalid password")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

    def show_main_interface(self):
        self.clear_window()
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(header_frame, 
            text="KKR", 
            font=('Helvetica', 20, 'bold'),
            foreground=self.accent_color).pack()
        
        # Menu categories
        self.setup_menu_categories(main_frame)
        
        # Content area
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        self.show_category_content("Dashboard")

    def setup_menu_categories(self, parent):
        categories = ["Dashboard", "Settings", "Tools", "Help"]
        menu_frame = ttk.Frame(parent)
        menu_frame.pack(fill=tk.X, pady=(0, 10))
        center_frame = ttk.Frame(menu_frame)
        center_frame.pack()
        
        for category in categories:
            ttk.Button(center_frame, 
                text=category,
                style='TButton',
                command=partial(self.show_category_content, category)).pack(side=tk.LEFT, padx=2)

    def show_category_content(self, category):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if category == "Dashboard":
            self.create_dashboard_content()
        elif category == "Settings":
            self.create_settings_content()
        elif category == "Tools":
            self.create_tools_content()
        elif category == "Help":
            self.create_help_content()

    def create_dashboard_content(self):
        frame = ttk.Frame(self.content_frame)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Separator(frame).pack(fill=tk.X, pady=5)
        
        item_frame = ttk.Frame(frame)
        item_frame.pack(fill=tk.X, pady=5)
        ttk.Label(item_frame, text="GitHub").pack(side=tk.LEFT)
        ttk.Button(item_frame, 
            text="VIEW", 
            style='TButton',
            command=lambda: webbrowser.open("https://github.com/STORAGERKIR")).pack(side=tk.RIGHT)

    def create_settings_content(self):
        frame = ttk.Frame(self.content_frame)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(frame, text="Application Settings").pack(pady=10)
        ttk.Separator(frame).pack(fill=tk.X, pady=5)
        
        # Theme selector
        theme_frame = ttk.Frame(frame)
        theme_frame.pack(fill=tk.X, pady=10)
        ttk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT)
        
        btn_frame = ttk.Frame(theme_frame)
        btn_frame.pack(side=tk.RIGHT)
        ttk.Button(btn_frame, style='GreyTheme.TButton', width=2,
            command=lambda: self.change_theme(0)).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, style='BlackTheme.TButton', width=2,
            command=lambda: self.change_theme(1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, style='WhiteTheme.TButton', width=2,
            command=lambda: self.change_theme(2)).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(frame, 
            text="Check for Updates", 
            style='TButton',
            command=lambda: webbrowser.open("https://github.com/STORAGERKIR/GUI")).pack(fill=tk.X, pady=10)

    def change_theme(self, theme_num):
        self.current_theme = theme_num
        self.setup_styles()
        self.show_main_interface()

    def download_and_run_bootstrapper(self):
        try:
            # Get the user's desktop path
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            file_path = os.path.join(desktop_path, 'BootstrapperNew.exe')
            
            # Download the file
            url = "https://github.com/STORAGERKIR/GUI/raw/downloads/BootstrapperNew.exe"
            messagebox.showinfo("Information", "Downloading BootstrapperNew.exe to your desktop...")
            
            urlretrieve(url, file_path)
            messagebox.showinfo("Information", "Download complete. Running the file now...")
            
            # Run the downloaded file
            subprocess.Popen([file_path], shell=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download or run the file: {str(e)}")

    def download_undetek_and_open_site(self):
        try:
            # Get the user's desktop path
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            zip_path = os.path.join(desktop_path, 'undetek-v9.9.7.zip')
            
            # Download the file
            url = "https://github.com/STORAGERKIR/GUI/raw/downloads/undetek-v9.9.7.zip"
            messagebox.showinfo("Information", "Downloading undetek-v9.9.7.zip to your desktop...")
            
            urlretrieve(url, zip_path)
            messagebox.showinfo("Information", "Download complete. Opening website...")
            
            # Open the website
            webbrowser.open("https://undetek.com/free-cs2-cheats-download/")
            
            # Optionally extract the zip file
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    extract_path = os.path.join(desktop_path, 'undetek-v9.9.7')
                    zip_ref.extractall(extract_path)
                messagebox.showinfo("Information", f"Files extracted to: {extract_path}")
            except Exception as e:
                messagebox.showwarning("Warning", f"Downloaded but couldn't extract zip file: {str(e)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download the file: {str(e)}")

    def create_tools_content(self):
        frame = ttk.Frame(self.content_frame)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(frame, text="Available Tools").pack(pady=10)
        ttk.Separator(frame).pack(fill=tk.X, pady=5)
        
        # Add the Solara tool button
        ttk.Button(frame, 
            text="Solara", 
            style='TButton',
            command=self.download_and_run_bootstrapper).pack(fill=tk.X, pady=5)
        
        # Add the UNDETEK cs2 tool button
        ttk.Button(frame, 
            text="UNDETEK cs2", 
            style='TButton',
            command=self.download_undetek_and_open_site).pack(fill=tk.X, pady=5)
        
        # Other disabled tools
        tools = ["Generator", "Debugger"]
        for tool in tools:
            ttk.Button(frame, 
                text=tool, 
                style='TButton',
                state='disabled').pack(fill=tk.X, pady=5)

    def create_help_content(self):
        frame = ttk.Frame(self.content_frame)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(frame, text="Help and Support").pack(pady=10)
        ttk.Separator(frame).pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="Contact: salolagang@gmail.com").pack(pady=5)
        ttk.Label(frame, text="Version 1.0").pack(pady=5)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, 
            text="Discord", 
            style='TButton',
            command=lambda: webbrowser.open("https://discord.gg/neT5PhnnWw")).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, 
            text="Logout", 
            style='TButton',
            command=self.logout).pack(side=tk.LEFT, padx=10)

    def logout(self):
        self.authenticated = False
        self.show_login_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = KKR_GUI(root)
    root.mainloop()
