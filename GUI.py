#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:36:58 2021
Refactored on Dec 2025 for Modern UI & AI Integration & Advanced Features

"""

# import all the required modules
import threading
import select
from tkinter import *
import winsound # Windows Sound
import ast # For parsing user list
import customtkinter as ctk # Modern UI
from chat_utils import *
import json
import ai_utils # AI Helper
import time
import re # RegEx for message parsing
from datetime import datetime
import emoji # pip install emoji
from PIL import Image, ImageTk # pip install Pillow
import base64
import io
from tkinter import filedialog
import traceback

# Setup CustomTkinter Theme to match "shadcn" (Dark, Blue/Slate)
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = ctk.CTk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""
        
        # AI Handler
        self.ai = ai_utils.AIHandler()
        
        # Advanced Features
        self.input_history = []
        self.history_index = 0
        self.online_users = []
        self.after_id = None # For polling
        self.commands = ["/time", "/who", "/quit", "/poem", "/connect", "/search", "/aipic", "/clear"]
        
        # State for Date Display
        self.last_print_date = None
        self.loaded_images = [] # Keep references to prevent GC

    def login(self):
        # login/signup window
        self.login_window = ctk.CTkToplevel()
        # set the title
        self.login_window.title("Welcome")
        self.login_window.geometry("400x450")
        self.login_window.resizable(width=False, height=False)

        # Center things a bit
        self.login_frame = ctk.CTkFrame(self.login_window)
        self.login_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # create a Label
        self.pls = ctk.CTkLabel(self.login_frame, 
                       text="Welcome to Chat System",
                       font=("Helvetica", 16, "bold"))
        self.pls.pack(pady=(30, 10))
        
        # Mode toggle (Login/Signup)
        self.auth_mode = "login"  # Default to login
        self.mode_label = ctk.CTkLabel(self.login_frame,
                               text="Login to your account",
                               font=("Helvetica", 12))
        self.mode_label.pack(pady=5)

        # create a Label
        self.labelName = ctk.CTkLabel(self.login_frame,
                               text="Username:",
                               font=("Helvetica", 12))
        self.labelName.pack(pady=5)

        # create a entry box for typing the username
        self.entryName = ctk.CTkEntry(self.login_frame, 
                             font=("Helvetica", 14),
                             width=250)
        self.entryName.pack(pady=10)
        # set the focus of the cursor
        self.entryName.focus()
        
        # Password label
        self.labelPassword = ctk.CTkLabel(self.login_frame,
                               text="Password:",
                               font=("Helvetica", 12))
        self.labelPassword.pack(pady=5)
        
        # Password entry (masked)
        self.entryPassword = ctk.CTkEntry(self.login_frame, 
                             font=("Helvetica", 14),
                             width=250,
                             show="*")
        self.entryPassword.pack(pady=10)
        self.entryPassword.bind("<Return>", lambda e: self.goAhead(self.entryName.get(), self.entryPassword.get()))

        # Status label for errors
        self.status_label = ctk.CTkLabel(self.login_frame,
                               text="",
                               font=("Helvetica", 10),
                               text_color="red")
        self.status_label.pack(pady=5)

        # create a Continue Button along with action
        self.go = ctk.CTkButton(self.login_frame,
                         text="LOGIN", 
                         font=("Helvetica", 14, "bold"), 
                         command=lambda: self.goAhead(self.entryName.get(), self.entryPassword.get()))
        self.go.pack(pady=10)
        
        # Toggle button
        self.toggle_btn = ctk.CTkButton(self.login_frame,
                         text="Don't have an account? Sign up",
                         font=("Helvetica", 11),
                         fg_color="transparent",
                         command=self.toggle_auth_mode)
        self.toggle_btn.pack(pady=10)
        
        self.Window.mainloop()
    
    def toggle_auth_mode(self):
        """Toggle between login and signup modes"""
        if self.auth_mode == "login":
            self.auth_mode = "signup"
            self.mode_label.configure(text="Create a new account")
            self.go.configure(text="SIGN UP")
            self.toggle_btn.configure(text="Already have an account? Login")
        else:
            self.auth_mode = "login"
            self.mode_label.configure(text="Login to your account")
            self.go.configure(text="LOGIN")
            self.toggle_btn.configure(text="Don't have an account? Sign up")
        self.status_label.configure(text="")

    def goAhead(self, name, password):
        if len(name) > 0 and len(password) > 0:
            action = self.auth_mode  # "login" or "signup"
            msg = json.dumps({"action": action, "name": name, "password": password})
            self.send(msg)
            response = json.loads(self.recv())
            
            if action == "signup":
                if response["status"] == 'ok':
                    self.status_label.configure(text="Signup successful! Please login.", text_color="green")
                    self.toggle_auth_mode()  # Switch to login mode
                    self.entryPassword.delete(0, END)
                else:
                    self.status_label.configure(text=response.get("message", "Signup failed"), text_color="red")
            
            elif action == "login":
                if response["status"] == 'ok':
                    self.login_window.destroy()
                    self.sm.set_state(S_LOGGEDIN)
                    self.sm.set_myname(name)
                    self.layout(name)
                    self.textCons.configure(state=NORMAL)
                    self.textCons.insert(END, "Welcome to the Chat!\n" + menu + "\n")
                    self.textCons.configure(state=DISABLED)
                    self.textCons.see(END)
                    
                    # Start the process thread
                    process = threading.Thread(target=self.proc)
                    process.daemon = True
                    process.start()
                    
                    # Start polling logic (Wait a bit for connection to settle)
                    self.Window.after(2000, self.update_user_list)
                else:
                    self.status_label.configure(text=response.get("message", "Login failed"), text_color="red")
        else:
            self.status_label.configure(text="Username and password required", text_color="red")

    # The main layout of the chat
    def layout(self, name):
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM - " + self.name)
        self.Window.geometry("950x640")
        self.Window.resizable(width=True, height=True)

        # Configure Grid Layout (Sidebar + Main Chat)
        self.Window.grid_columnconfigure(1, weight=1)
        self.Window.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR (AI & TOOLS) ---
        self.sidebar_frame = ctk.CTkFrame(self.Window, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text=f"User: {self.name}", font=ctk.CTkFont(size=18, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Quick Actions
        self.action_label = ctk.CTkLabel(self.sidebar_frame, text="Quick Actions", anchor="w")
        self.action_label.grid(row=1, column=0, padx=20, pady=(10, 0))

        self.btn_time = ctk.CTkButton(self.sidebar_frame, text="🕒 Time", command=lambda: self.sendButton("/time"))
        self.btn_time.grid(row=2, column=0, padx=20, pady=5)
        
        self.btn_who = ctk.CTkButton(self.sidebar_frame, text="👥 Who", command=lambda: self.sendButton("/who"))
        self.btn_who.grid(row=3, column=0, padx=20, pady=5)
        
        self.btn_poem = ctk.CTkButton(self.sidebar_frame, text="📜 Poem", command=lambda: self.sendButton("/poem 1")) # Shortcut to sonnet 1
        self.btn_poem.grid(row=4, column=0, padx=20, pady=5)

        # AI Tools
        self.ai_label = ctk.CTkLabel(self.sidebar_frame, text="AI Tools", anchor="w")
        self.ai_label.grid(row=5, column=0, padx=20, pady=(20, 0))

        self.btn_summary = ctk.CTkButton(self.sidebar_frame, text="📝 Summary", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.on_summary_click)
        self.btn_summary.grid(row=6, column=0, padx=20, pady=5)

        self.btn_keywords = ctk.CTkButton(self.sidebar_frame, text="🔑 Keywords", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.on_keywords_click)
        self.btn_keywords.grid(row=7, column=0, padx=20, pady=5)
        
        # User List (Discord Style)
        self.user_list_label = ctk.CTkLabel(self.sidebar_frame, text="Online Users", anchor="w", font=("Arial", 12, "bold"))
        self.user_list_label.grid(row=8, column=0, padx=20, pady=(20, 5), sticky="s") 
        
        self.user_list_frame = ctk.CTkScrollableFrame(self.sidebar_frame, width=180, height=150)
        self.user_list_frame.grid(row=9, column=0, padx=10, pady=10, sticky="nsew")


        # --- MAIN CHAT AREA ---
        self.chat_frame = ctk.CTkFrame(self.Window, corner_radius=10)
        self.chat_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.chat_frame.grid_rowconfigure(0, weight=1)
        self.chat_frame.grid_columnconfigure(0, weight=1)

        self.textCons = ctk.CTkTextbox(self.chat_frame, width=250, font=("Roboto Medium", 14))
        self.textCons.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.textCons.configure(state=DISABLED)
        # Configure Tags for Colors
        self.textCons.tag_config("me", foreground="#4ADE80") # Greenish
        self.textCons.tag_config("peer", foreground="#FFFFFF") # White
        self.textCons.tag_config("system", foreground="#FACC15") # Yellow
        self.textCons.tag_config("ai", foreground="#38BDF8") # Cyan

        # --- INPUT AREA ---
        self.entry_frame = ctk.CTkFrame(self.Window, corner_radius=0, height=80) 
        self.entry_frame.grid(row=1, column=1, sticky="ew", padx=20, pady=(0, 20))
        self.entry_frame.grid_columnconfigure(0, weight=1)
        
        # Hint Label
        self.hint_label = ctk.CTkLabel(self.entry_frame, text="", text_color="gray", font=("Arial", 10))
        self.hint_label.grid(row=0, column=0, sticky="w", padx=10)

        self.entryMsg = ctk.CTkEntry(self.entry_frame, placeholder_text="Type... (/cmds, @user, @ai query)", font=("Roboto Medium", 14))
        self.entryMsg.grid(row=1, column=0, padx=(10, 5), pady=(0, 10), sticky="ew")
        
        # BINDINGS
        self.entryMsg.bind("<Return>", lambda event: self.sendButton(self.entryMsg.get()))
        self.entryMsg.bind("<Up>", self.navigate_history_up)
        self.entryMsg.bind("<Down>", self.navigate_history_down)
        self.entryMsg.bind("<KeyRelease>", self.check_autocomplete)
        self.entryMsg.bind("<Tab>", self.do_autocomplete)

        # Send Button
        self.buttonMsg = ctk.CTkButton(self.entry_frame, text="Send", width=80, command=lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.grid(row=1, column=2, padx=(5, 10), pady=(0, 10))

        # Emoji Button
        self.btn_emoji = ctk.CTkButton(self.entry_frame, text="😊", width=40, height=30, fg_color="transparent", border_width=1, command=self.open_emoji_picker)
        self.btn_emoji.grid(row=1, column=1, padx=5, pady=(0, 10))
        
        # Image Button
        self.btn_image = ctk.CTkButton(self.entry_frame, text="📷", width=40, height=30, fg_color="transparent", border_width=1, command=self.send_image)
        self.btn_image.grid(row=1, column=3, padx=5, pady=(0, 10))
        
    def update_user_list(self):
        # Poll for user list every 10 seconds
        try:
            msg = json.dumps({"action": "list"})
            self.send(msg)
        except Exception as e:
            print(f"Error polling user list: {e}")
            # Continue anyway, will retry on next poll
        self.Window.after(10000, self.update_user_list)
        
    def navigate_history_up(self, event):
        if self.input_history:
            if self.history_index > 0:
                self.history_index -= 1
            
            # Show history item
            self.entryMsg.delete(0, END)
            self.entryMsg.insert(0, self.input_history[self.history_index])

    def navigate_history_down(self, event):
        if self.input_history:
            if self.history_index < len(self.input_history) - 1:
                self.history_index += 1
                self.entryMsg.delete(0, END)
                self.entryMsg.insert(0, self.input_history[self.history_index])
            else:
                self.history_index = len(self.input_history)
                self.entryMsg.delete(0, END)

    def check_autocomplete(self, event):
        text = self.entryMsg.get()
        if text.startswith("/") and " " not in text:
            # Command suggestion (no space yet)
            matches = [c for c in self.commands if c.startswith(text)]
            if matches:
                 self.hint_label.configure(text=f"Commands: {', '.join(matches)}")
            else:
                 self.hint_label.configure(text="")
        elif text.startswith("/connect "):
            # Autocomplete for connect command with online users
            partial = text.replace("/connect ", "")
            matches = [u for u in self.online_users if u.startswith(partial) and u != self.name]
            if matches:
                self.hint_label.configure(text=f"Users: {', '.join(matches)}")
            else:
                self.hint_label.configure(text="No matching users online")
        elif "@" in text:
             # Just a visual hint for now
             self.hint_label.configure(text="Tip: Use @ai <msg> to talk to bot, or @<User> to mention.")
        else:
             self.hint_label.configure(text="")


    def do_autocomplete(self, event):
        text = self.entryMsg.get()
        if text.startswith("/") and " " not in text:
             # Command autocomplete
             matches = [c for c in self.commands if c.startswith(text)]
             if len(matches) == 1:
                 self.entryMsg.delete(0, END)
                 self.entryMsg.insert(0, matches[0] + " ")
                 return "break" # Stop default tab behavior
             elif len(matches) > 1:
                 # Show all matches in hint
                 self.hint_label.configure(text=f"Commands: {', '.join(matches)}")
                 return "break"
        elif text.startswith("/connect "):
             # Username autocomplete for connect
             partial = text.replace("/connect ", "")
             matches = [u for u in self.online_users if u.startswith(partial) and u != self.name]
             if len(matches) == 1:
                 self.entryMsg.delete(0, END)
                 self.entryMsg.insert(0, f"/connect {matches[0]}")
                 return "break"
             elif len(matches) > 1:
                 # Show all matches in hint
                 self.hint_label.configure(text=f"Users: {', '.join(matches)}")
                 return "break"

    def open_emoji_picker(self):
        try:
            if self.emoji_toplevel and self.emoji_toplevel.winfo_exists():
                self.emoji_toplevel.lift()
                return
        except:
            pass
            
        self.emoji_toplevel = ctk.CTkToplevel(self.Window)
        self.emoji_toplevel.title("Emoji Picker")
        self.emoji_toplevel.geometry("400x500")
        self.emoji_toplevel.attributes("-topmost", True)
        
        # Tab View for filtering
        self.emoji_tabs = ctk.CTkTabview(self.emoji_toplevel)
        self.emoji_tabs.pack(fill="both", expand=True, padx=10, pady=10)
        
        categories = {"Smileys": "😊", "Space": "🚀", "Food": "🍔", "Animals": "🐶", "Hearts": "❤️"}
        
        for cat, icon in categories.items():
            self.emoji_tabs.add(cat)
            
            # Scrollable frame for each tab
            scroll = ctk.CTkScrollableFrame(self.emoji_tabs.tab(cat))
            scroll.pack(fill="both", expand=True)
            
            # Populate with some common emojis (Full list is too huge, let's pick subsets or generated ranges)
            # For demonstration, we'll use a curated list or a quick generator. 
            # Real full implementation of ALL emojis requires parsing emoji.EMOJI_DATA
            
            self._populate_emojis(scroll, cat)

    def _populate_emojis(self, parent, category):
        # Basic Curated Lists (To avoid freezing UI with 5000+ items)
        emojis_sets = {
            "Smileys": ["😀","😃","😄","😁","😆","😅","🤣","😂","🙂","🙃","😉","😊","😇","🥰","😍","🤩","😘","😗","😚","😙","😋","😛","😜","🤪","😝","🤑","🤗","🤭","🤫","🤔","🤐","🤨","😐","😑","😶","😏","😒","🙄","😬","🤥","😌","😔","😪","🤤","😴","😷","🤒","🤕","🤢","🤮","🤧","🥵","🥶","🥴","😵","🤯","🤠","🥳","😎","🤓","🧐","😕","😟","🙁","☹️","😮","😯","😲","😳","🥺","😦","😧","😨","😰","😥","😢","😭","😱","😖","😣","😞","😓","😩","😫","🥱","😤","😡","😠","🤬","😈","👿","💀","☠️"],
            "Space": ["🚀","🛸","🌌","🌑","🌒","🌓","🌔","🌕","🌖","🌗","🌘","🌙","🌚","🌛","🌜","☀️","🌝","🌞","⭐","🌟","🌠","☁️","⛅","⛈️","🌤️","🌥️","🌦️","🌧️","🌨️","🌩️","🌪️","🌫️","🌬️","🌀","🌈","🌂","☂️","⚡","❄️","☃️","⛄","☄️","🔥","💧","🌊"],
            "Food": ["🍏","🍎","🍐","🍊","🍋","🍌","🍉","🍇","🍓","🍈","🍒","🍑","🥭","🍍","🥥","🥝","🍅","🍆","🥑","🥦","🥬","🥒","🌶️","🌽","🥕","🧄","🧅","🥔","🍠","🥐","🥯","🍞","🥖","🥨","🧀","🥚","🍳","🧈","🥞","🧇","🥓","🥩","🍗","🍖","🦴","🌭","🍔","🍟","🍕","🥪","🥙","🧆","🌮","🌯","🥗","🥘","🥫","🍝","🍜","🍲","🍛","🍣","🍱","🥟","🦪","🍤","🍙","🍚","🍘","🍥","🥠","🍢","🍡","🍧","🍨","🍦","🥧","🧁","🍰","🎂","🍮","🍭","🍬","🍫","🍿","🍩","🍪","🌰","🥜","🍯","🥛","🍼","☕","🍵","🧃","🥤","🍶","🍺","🍻","🥂","🍷","🥃","🍸","🍹","🧉","🍾","🧊","🥄","🍴","🍽️","🥣","🥡","🥢","🧂"],
            "Animals": ["🐶","🐕","🦮","🐕‍🦺","🐩","🐺","🦊","🦝","🐱","🐈","🐈‍⬛","🦁","🐯","🐅","🐆","🐴","🐎","🦄","🦓","🦌","🦬","🐮","🐂","🐃","🐄","🐷","🐖","🐗","🐽","🐏","🐑","🐐","🐪","🐫","🦙","🦒","🐘","🦣","🦏","🦛","🐭","🐁","🐀","🐹","🐰","🐇","🐿️","🦫","🦔","🦇","🐻","🐻‍❄️","🐨","🐼","🦥","🦦","🦨","🦘","🦡","🐾","🦃","🐔","🐓","🐣","🐤","🐥","🐦","🐧","🕊️","🦅","🦆","🦢","🦉","🦩","🦚","🦜","🐸","🐊","🐢","🦎","🐍","🐲","🐉","🦕","🦖","🐳","🐋","🐬","🦭","🐟","🐠","🐡","🦈","🐙","🐚","🐌","🦋","🐛","🐜","🐝","🐞","🦗","🕷️","🕸️","🦂","🦟","🦠","💐","🌸","💮","🏵️","🌹","🥀","🌺","🌻","🌼","🌷","🌱","🌲","🌳","🌴","🌵","🌾","🌿","☘️","🍀","🍁","🍂","🍃"],
            "Hearts": ["❤️","🧡","💛","💚","💙","💜","🖤","🤍","🤎","💔","❣️","💕","💞","💓","💗","💖","💘","💝","💟","☮️","✝️","☪️","🕉️","☸️","✡️","🔯","🕎","☯️","☦️","🛐","⛎","♈","♉","♊","♋","♌","♍","♎","♏","♐","♑","♒","♓","🆔","⚛️"]
            }
        
        # Grid them
        row = 0
        col = 0
        WIDTH = 6
        
        items = emojis_sets.get(category, [])
        for em in items:
            btn = ctk.CTkButton(parent, text=em, width=30, height=30, fg_color="transparent", command=lambda e=em: self.insert_emoji(e))
            btn.grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col >= WIDTH:
                col = 0
                row += 1

    def insert_emoji(self, emoji):
        self.entryMsg.insert(END, f"{emoji}")

    def send_image(self):
        # Support all common image formats
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("All Images", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.webp;*.tiff;*.tif;*.ico"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg;*.jpeg"),
                ("GIF", "*.gif"),
                ("BMP", "*.bmp"),
                ("WebP", "*.webp"),
                ("TIFF", "*.tiff;*.tif"),
                ("ICO", "*.ico"),
                ("All Files", "*.*")
            ]
        )
        
        if not file_path:
            return
            
        try:
             # Process Image with format validation
             try:
                 img = Image.open(file_path)
                 # Verify it's actually an image
                 img.verify()
                 # Reopen after verify (verify closes the file)
                 img = Image.open(file_path)
             except Exception as e:
                 self._display_system_message(f"Invalid image file: {str(e)[:50]}", "system")
                 return
             
             # Handle animated GIFs - take first frame
             if hasattr(img, 'is_animated') and img.is_animated:
                 img.seek(0)  # First frame
                 self._display_system_message("Sending first frame of animated image", "system")
             
             # Resize if too big (Max 300px width/height for better transmission)
             img.thumbnail((300, 300))  # Maintains aspect ratio
             
             # Handle different color modes for compatibility
             # Convert images with transparency or unusual modes
             if img.mode in ('RGBA', 'LA', 'P'):
                 # Create white background for formats that don't support transparency
                 background = Image.new('RGB', img.size, (255, 255, 255))
                 if img.mode == 'P':
                     img = img.convert('RGBA')
                 # Paste with alpha mask if available
                 if img.mode in ('RGBA', 'LA'):
                     background.paste(img, mask=img.split()[-1])
                 else:
                     background.paste(img)
                 img = background
             elif img.mode not in ('RGB', 'L'):
                 # Convert any other mode to RGB
                 img = img.convert('RGB')
             
             # Convert to Bytes - always use PNG for lossless transmission
             buffer = io.BytesIO()
             img.save(buffer, format="PNG")
             img_bytes = buffer.getvalue()
             
             # Check size (limit to ~2MB base64 for stability)
             if len(img_bytes) > 1500000:  # ~2MB base64
                 self._display_system_message("Image too large. Please use a smaller image (max ~1.5MB).", "system")
                 return
             
             # Encode to base64
             base64_str = base64.b64encode(img_bytes).decode('utf-8')
             
             # Send with error handling
             try:
                 msg = json.dumps({"action": "image", "from": self.name, "data": base64_str})
                 self.send(msg)
                 
                 # Local Echo with timestamp
                 self._display_image(img, self.name, is_me=True)
                 
             except Exception as send_err:
                 print(f"Send error: {send_err}")
                 traceback.print_exc()
                 self._display_system_message(f"Failed to send image: Connection error", "system")
             
        except FileNotFoundError:
            self._display_system_message("Image file not found", "system")
        except PermissionError:
            self._display_system_message("Permission denied to read image", "system")
        except Exception as e:
            print(f"Image Error: {e}")
            traceback.print_exc()
            self._display_system_message(f"Failed to process image: {str(e)[:50]}", "system")

    def _display_image(self, pil_image, user, is_me=False):
        if threading.current_thread() is not threading.main_thread():
             # We can't pass the PIL image effectively if we delay too long? 
             # Actually, passing objects to lambda in 'after' is fine.
             self.Window.after(0, lambda: self._display_image(pil_image, user, is_me))
             return

        try:
            # We need to convert PIL image to something Tkinter can display in a Text widget
            # CTkImage is for labels/buttons. Text widget uses tk.PhotoImage
            
            photo = ImageTk.PhotoImage(pil_image)
            self.loaded_images.append(photo) # Keep reference!
            
            # Add timestamp for consistency
            current_time = datetime.now().strftime("%H:%M")
            tag = "me" if is_me else "peer"
            
            self.textCons.configure(state=NORMAL)
            self.textCons.insert(END, f"[{current_time}] [{user} sent an image]:\n", tag)
            
            # Access underlying tk widget
            self.textCons._textbox.image_create(END, image=photo)
            self.textCons.insert(END, "\n")
            
            self.textCons.configure(state=DISABLED)
            self.textCons.see(END)
        except Exception as e:
            print("Display Image Error:", e)
            traceback.print_exc()

    def on_summary_click(self):
        # Grab last few lines of text
        full_text = self.textCons.get("1.0", END)
        if len(full_text) < 10:
            return
        
        # Run AI in thread so UI doesn't freeze
        t = threading.Thread(target=self._run_summary)
        t.start()
    
    def on_keywords_click(self):
        # Grab last few lines of text
        full_text = self.textCons.get("1.0", END)
        if len(full_text) < 10:
            return
        
        t = threading.Thread(target=self._run_keywords)
        t.start()
    
    def ask_ai_inline(self, query):
        # Send AI query to server for processing and broadcasting
        try:
            msg = json.dumps({"action":"ai_query", "query":query})
            self.send(msg)
        except Exception as e:
            print(f"Failed to send AI query: {e}")
            self._display_system_message(f"Failed to send AI query: {e}", "system")

    def _run_summary(self):
        full_text = self.textCons.get("1.0", END)
        history = full_text[-2000:]
        summary = self.ai.get_summary(history)
        
        # Broadcast summary via server (as AI query)
        summary_message = f"--- AI Summary ---\n{summary}\n------------------"
        try:
            # Send as regular exchange message
            msg = json.dumps({"action":"exchange", "from":"[AI Summary]", "message":summary_message})
            self.send(msg)
        except Exception as e:
            print(f"Failed to send AI summary: {e}")
            self._display_system_message(summary_message, "ai")  # Fallback to local

    def _run_keywords(self):
        full_text = self.textCons.get("1.0", END)
        history = full_text[-1000:]
        keywords = self.ai.extract_keywords(history)
        
        # Broadcast keywords to all users
        keywords_message = f"--- AI Keywords ---\n{keywords}\n-------------------"
        try:
            msg = json.dumps({"action":"exchange", "from":"[AI Keywords]", "message":keywords_message})
            self.send(msg)
        except Exception as e:
            print(f"Failed to send AI keywords: {e}")
            self._display_system_message(keywords_message, "ai")  # Fallback to local

    def _display_system_message(self, text, tag=None):
        if threading.current_thread() is not threading.main_thread():
             self.Window.after(0, lambda: self._display_system_message(text, tag))
             return

        self.textCons.configure(state=NORMAL)
        # Check tag based on content if not provided
        if not tag:
            if "[Me]" in text: tag = "me"
            elif "AI:" in text: tag = "ai"
            else: tag = "peer"
        
        self.textCons.insert(END, text + "\n", tag) # Reduced newline gap
        self.textCons.configure(state=DISABLED)
        self.textCons.see(END)
        self.system_msg = "" # STRICT BUG FIX

    def sendButton(self, msg):
        self.textCons.configure(state=DISABLED)
        self.my_msg = msg
        self.entryMsg.delete(0, END)
        self.hint_label.configure(text="") # Clear hints
        
        # Add to history
        if msg.strip():
             self.input_history.append(msg)
             self.history_index = len(self.input_history) 
        
        # --- LOCAL ECHO (User Request: See what I typed) ---
        if msg.strip():
             # Custom Time Format for Local Echo
             current_date = datetime.now().strftime("%d-%m-%Y")
             current_time = datetime.now().strftime("%H:%M")
             
             # Date Header Check
             if self.last_print_date != current_date:
                 self.last_print_date = current_date
                 self._display_system_message(f"--------- {current_date} ---------", "system")
             
             display_txt = f"[{current_time}] [Me] {msg}"
             self._display_system_message(display_txt, "me")
             
             # Sound Check (Send)
             try:
                 winsound.MessageBeep(winsound.MB_ICONASTERISK)
             except:
                 pass

        # COMMAND MAPPING LOGIC
        if msg.startswith("/connect"):
            parts = msg.split(" ", 1)
            if len(parts) > 1:
                self.my_msg = f"c {parts[1]}"
            else:
                 self._display_system_message("Usage: /connect <username>", "system")
                 self.my_msg = "" # don't send

        elif msg.startswith("/search"):
            parts = msg.split(" ", 1)
            if len(parts) > 1:
                self.my_msg = f"? {parts[1]}"
            else:
                 self._display_system_message("Usage: /search <term>", "system")
                 self.my_msg = ""

        elif msg.startswith("/poem"):
            parts = msg.split(" ", 1)
            if len(parts) > 1 and parts[1].strip().isdigit():
                self.my_msg = f"p{parts[1].strip()}"
            else:
                self.my_msg = "p1"  # Default to sonnet #1 

        elif msg.startswith("/quit"):
            self.my_msg = "q"
            
        elif msg.startswith("/who"): 
            self.my_msg = "who"
        elif msg.startswith("/time"): 
            self.my_msg = "time"
        
        elif msg.startswith("/clear"):
            # Clear the chat screen for this user only
            self.textCons.configure(state=NORMAL)
            self.textCons.delete("1.0", END)
            self.textCons.insert(END, "Chat cleared!\n" + menu + "\n")
            self.textCons.configure(state=DISABLED)
            self.textCons.see(END)
            self.my_msg = ""  # Don't send to server
            return  # Exit early


        # @AI IN-CHAT TRIGGER
        if "@ai" in msg.lower():
            try:
                parts = msg.lower().split("@ai", 1)
                if len(parts) > 1 and parts[1].strip():
                    query = parts[1].strip()
                    threading.Thread(target=lambda: self.ask_ai_inline(query)).start()
            except Exception as e:
                print(f"AI trigger error: {e}")


        # Check for AI commands / image gen
        if msg.startswith("/aipic"):
            try:
                # Extract prompt after /aipic or /aipic:
                if msg.startswith("/aipic:"):
                    prompt = msg.replace("/aipic:", "").strip()
                elif msg.startswith("/aipic "):
                    prompt = msg.replace("/aipic ", "").strip()
                else:
                    self._display_system_message("Usage: /aipic <prompt> or /aipic: <prompt>", "system")
                    return
                
                if prompt:
                    self._display_system_message(f"[Generating Image for: {prompt} ...]", "system")
                    # Send to server for processing and broadcasting
                    threading.Thread(target=lambda: self._generate_image_server(prompt)).start()
                else:
                    self._display_system_message("Please provide a prompt for image generation", "system")
            except Exception as e:
                print(f"AI image gen error: {e}")
                self._display_system_message("Failed to generate image", "system")
        

    def _generate_image_server(self, prompt):
        """Send image generation request to server for broadcasting"""
        try:
            msg = json.dumps({"action":"ai_image", "prompt":prompt})
            self.send(msg)
        except Exception as e:
            print(f"Failed to send image generation request: {e}")
            self._display_system_message(f"Failed to generate image: {e}", "system")
    
    def _generate_image(self, prompt):
        """Legacy local image generation (kept for backward compatibility)"""
        url = self.ai.generate_image(prompt)
        self._display_system_message(f"--- AI Image ---\n[Image Generated]: {url}\n(Click or copy usage depends on standard terminal unsupported in GUI for now)\n----------------", "ai")

    def proc(self):
        while True:
            try:
                read, write, error = select.select([self.socket], [], [], 0)
            except Exception as e:
                print(f"Select error: {e}")
                time.sleep(0.1)
                continue
                
            peer_msg = []
            if self.socket in read:
                try:
                    peer_msg = self.recv()
                except (ConnectionAbortedError, ConnectionResetError, ConnectionError) as e:
                    print(f"Connection error in recv: {e}")
                    self._display_system_message("Connection interrupted. Please check your network.", "system")
                    time.sleep(1)  # Brief pause before retry
                    continue
                except Exception as e:
                    print(f"Unexpected error in recv: {e}")
                    traceback.print_exc()
                    time.sleep(0.5)
                    continue
            
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                # Handle Sidebar Updates (Silently)
                if len(peer_msg) > 0:
                    try:
                        pm_json = json.loads(peer_msg)
                        
                        # --- IMAGE HANDLING ---
                        if pm_json.get("action") == "image":
                             try:
                                 sender = pm_json.get("from", "Unknown")
                                 b64_data = pm_json.get("data", "")
                                 
                                 if b64_data:
                                     # Decode
                                     img_bytes = base64.b64decode(b64_data)
                                     img = Image.open(io.BytesIO(img_bytes))
                                     self._display_image(img, sender, is_me=False)
                                     
                                     # Sound
                                     try: winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                                     except: pass
                             except Exception as e:
                                 print(f"Image Reception Error: {e}")
                                 traceback.print_exc()
                                 self._display_system_message("Failed to receive image", "system")
                                 
                             continue # Skip normal text processing
                        
                        if pm_json.get("action") == "list":
                            # Parse User List
                            raw_res = pm_json["results"]
                            start = raw_res.find("{")
                            end = raw_res.find("}") + 1
                            if start != -1 and end != -1:
                                users_dict = ast.literal_eval(raw_res[start:end])
                                self.online_users = list(users_dict.keys())
                                # Update Sidebar UI
                                for widget in self.user_list_frame.winfo_children():
                                    widget.destroy()
                                for u in self.online_users:
                                    status = "🟢" 
                                    if u == self.name: status = "👤"
                                    u_btn = ctk.CTkLabel(self.user_list_frame, text=f"{status} {u}", anchor="w", font=("Arial", 12))
                                    u_btn.pack(fill="x", pady=2)
                            
                            continue
                    except:
                        pass
                
                # Normal Processing
                new_text = self.sm.proc(self.my_msg, peer_msg)
                
                # Regex Parse Server Message: (dd.mm.yy,HH:MM) user : message
                # Pattern: (07.12.25,19:12) user : hello
                
                match = re.search(r"^\((\d{2}\.\d{2}\.\d{2}),(\d{2}:\d{2})\) (.*?) : (.*)$", new_text)
                
                final_msg = new_text # Fallback
                tag = "peer"
                
                if match:
                    date_str, time_str, user, content = match.groups()
                    
                    if self.last_print_date != date_str:
                         self.last_print_date = date_str
                         self._display_system_message(f"--------- {date_str} ---------", "system")
                    
                    final_msg = f"[{time_str}] [{user}] {content}"
                    
                    if user == "System": tag = "system"
                
                else:
                    if "joined" in new_text: 
                        tag = "system"
                        final_msg = f"[System] {new_text}"
                
                self.system_msg = final_msg 
                
                # SOUNDS
                if len(peer_msg) > 0:
                     try:
                         # Play sound for incoming message
                         winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                     except:
                         pass

                # AI Enhancement: Analyze sentiment
                if match:
                     try:
                        content = match.group(4)
                        sentiment = self.ai.analyze_sentiment(content)
                        if sentiment:
                            self.system_msg = final_msg + f"  {sentiment}"
                     except Exception as e:
                         print(f"Sentiment Analysis Error: {e}")
                
                self.my_msg = "" # Reset my message
                
                # Update GUI - ONLY if there is actual content to display
                if self.system_msg.strip():
                    self.textCons.configure(state=NORMAL)
                    # Strip trailing whitespace/newlines, then add exactly one newline
                    clean_msg = self.system_msg.rstrip() + "\n"
                    self.textCons.insert(END, clean_msg, tag)
                    self.textCons.configure(state=DISABLED)
                    self.textCons.see(END)
                
                self.system_msg = "" # STRICT BUG FIX

    def run(self):
        self.login()
# create a GUI class object
if __name__ == "__main__": 
    # Just for testing the GUI without the full client wrapper if needed
    pass 