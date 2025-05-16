import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import threading
import datetime

from whatsapp_bot import WhatsAppBot
from config_manager import ConfigManager
from database_manager import DatabaseManager


class BotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp Auto Sender with Contacts & DB")
        self.root.geometry("450x600")
        self.db = DatabaseManager()
        self.create_widgets()
        self.load_previous_settings()

    def create_widgets(self):
        # Contact selection
        tk.Label(self.root, text="👤 Select Contact or enter manually:").pack()
        self.contact_combo = ttk.Combobox(self.root, width=40)
        self.contact_combo.pack()
        self.load_contacts()

        tk.Button(self.root, text="➕ Add Contact", command=self.add_contact_popup).pack()

        tk.Label(self.root, text="📞 Phone Number (optional if selected):").pack()
        self.phone_entry = tk.Entry(self.root, width=40)
        self.phone_entry.pack()

        # Message selection
        tk.Label(self.root, text="💬 Select Message or enter manually:").pack()
        self.message_combo = ttk.Combobox(self.root, width=40)
        self.message_combo.pack()
        self.load_messages()

        tk.Button(self.root, text="➕ Add Message", command=self.add_message_popup).pack()

        tk.Label(self.root, text="✏️ Message Content (optional if selected):").pack()
        self.message_entry = tk.Entry(self.root, width=40)
        self.message_entry.pack()

        # Date and time
        tk.Label(self.root, text="📅 Select Date:").pack()
        self.date_entry = DateEntry(self.root, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.pack()

        tk.Label(self.root, text="⏰ Hour (0-23):").pack()
        self.hour_spin = tk.Spinbox(self.root, from_=0, to=23, width=5)
        self.hour_spin.pack()

        tk.Label(self.root, text="⏱ Minute (0-59):").pack()
        self.minute_spin = tk.Spinbox(self.root, from_=0, to=59, width=5)
        self.minute_spin.pack()

        # Interval and duration
        tk.Label(self.root, text="🔁 Interval between messages (0 = once):").pack()
        self.interval_entry = tk.Entry(self.root, width=10)
        self.interval_entry.pack()

        tk.Label(self.root, text="⌛ Total duration (in minutes):").pack()
        self.duration_entry = tk.Entry(self.root, width=10)
        self.duration_entry.pack()

        self.save_var = tk.IntVar()
        tk.Checkbutton(self.root, text="💾 Save settings", variable=self.save_var).pack()

        tk.Button(self.root, text="🚀 Start Bot", command=self.start_bot_thread).pack(pady=10)

    def load_contacts(self):
        contacts = self.db.get_contacts()
        contact_names = [f"{name} ({phone})" for name, phone in contacts]
        self.contact_combo["values"] = contact_names

    def load_messages(self):
        messages = self.db.get_messages()
        titles = [f"{title} - {content[:30]}" for title, content in messages]
        self.message_combo["values"] = titles

    def add_contact_popup(self):
        win = tk.Toplevel(self.root)
        win.title("Add Contact")

        tk.Label(win, text="Name:").pack()
        name_entry = tk.Entry(win)
        name_entry.pack()
        tk.Label(win, text="Phone:").pack()
        phone_entry = tk.Entry(win)
        phone_entry.pack()

        def save():
            self.db.add_contact(name_entry.get(), phone_entry.get())
            self.load_contacts()
            win.destroy()

        tk.Button(win, text="Save", command=save).pack()

    def add_message_popup(self):
        win = tk.Toplevel(self.root)
        win.title("Add Message")

        tk.Label(win, text="Title:").pack()
        title_entry = tk.Entry(win)
        title_entry.pack()
        tk.Label(win, text="Content:").pack()
        content_entry = tk.Entry(win)
        content_entry.pack()

        def save():
            self.db.add_message(title_entry.get(), content_entry.get())
            self.load_messages()
            win.destroy()

        tk.Button(win, text="Save", command=save).pack()

    def load_previous_settings(self):
        config = ConfigManager.load_config()
        if config:
            self.phone_entry.insert(0, config["phone"])
            self.message_entry.insert(0, config["message"])
            self.hour_spin.delete(0, tk.END)
            self.hour_spin.insert(0, config["start_hour"])
            self.minute_spin.delete(0, tk.END)
            self.minute_spin.insert(0, config["start_minute"])
            self.interval_entry.insert(0, config["interval"])
            self.duration_entry.insert(0, config["duration"])

    def start_bot_thread(self):
        threading.Thread(target=self.start_bot).start()

    def start_bot(self):
        try:
            phone = self.phone_entry.get().strip()
            if not phone and self.contact_combo.get():
                phone = self.contact_combo.get().split("(")[-1].strip(")")

            message = self.message_entry.get().strip()
            if not message and self.message_combo.get():
                message = self.message_combo.get().split(" - ", 1)[-1]

            date = self.date_entry.get_date()
            hour = int(self.hour_spin.get())
            minute = int(self.minute_spin.get())
            interval = int(self.interval_entry.get())
            duration = int(self.duration_entry.get())

            # Save config
            config = {
                "phone": phone,
                "message": message,
                "start_hour": hour,
                "start_minute": minute,
                "interval": interval,
                "duration": duration
            }

            if self.save_var.get():
                ConfigManager.save_config(config)

            bot = WhatsAppBot(phone, message, hour, minute, interval, duration)
            messagebox.showinfo("WhatsApp Bot", f"The bot will start on {date} at {hour:02d}:{minute:02d}")
            bot.run()
            messagebox.showinfo("WhatsApp Bot", "Bot finished successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))
