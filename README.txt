# WhatsAppBotAuto

This project allows you to automatically send scheduled WhatsApp messages using a graphical interface.

## 🛠 Requirements

- Python 3.x installed
- Internet connection
- WhatsApp Web login (first time only)

##  Installation

1. Extract the ZIP.
2. Open Command Prompt in the extracted folder.
3. Run:
    pip install pywhatkit tkcalendar

##  How to Use

1. Run `run_bot.bat` (or run `python main.py` manually).
2. Enter:
   - Phone number (e.g. +972501234567)
   - Message content
   - Start time (hour & minute)
   - Interval between messages (0 = once)
   - Total duration in minutes
3. Check "Save settings" to remember them.
4. Click **Start Bot**.
5. Keep WhatsApp Web open in your browser.

##  Files

- `main.py` – Main runner
- `bot_ui.py` – GUI logic
- `whatsapp_bot.py` – WhatsApp message handling
- `config_manager.py` – Config save/load logic
- `run_bot.bat` – Windows launcher
- `config.json` – Auto-generated if saved

## Notes

- The bot uses `pywhatkit`, which opens WhatsApp Web in your browser.
- Messages are scheduled 1 minute ahead (due to WhatsApp API constraints).
- Don't touch the mouse/keyboard while the message is being sent.

Enjoy 🤖
