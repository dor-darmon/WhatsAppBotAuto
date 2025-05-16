import pywhatkit
import datetime
import time

class WhatsAppBot:
    def __init__(self, phone, message, start_hour, start_minute, interval, duration):
        self.phone = phone
        self.message = message
        self.start_hour = start_hour
        self.start_minute = start_minute
        self.interval = interval
        self.duration = duration
        self.sent_once = False

    def send_message(self):
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute + 1
        try:
            pywhatkit.sendwhatmsg(self.phone, self.message, hour, minute, wait_time=10, tab_close=True)
            print(f"Message sent at {hour:02d}:{minute:02d}")
        except Exception as e:
            print(f"Error sending message: {e}")

    def wait_until_start(self):
        print(f"Waiting for start time: {self.start_hour:02d}:{self.start_minute:02d}")
        while True:
            now = datetime.datetime.now()
            if now.hour > self.start_hour or (now.hour == self.start_hour and now.minute >= self.start_minute):
                break
            time.sleep(10)

    def run(self):
        self.wait_until_start()
        start_time = time.time()

        while True:
            if self.interval == 0 and not self.sent_once:
                self.send_message()
                self.sent_once = True
                break
            elif self.interval > 0:
                self.send_message()
                time.sleep(self.interval * 60)

            if (time.time() - start_time) >= self.duration * 60:
                break

        print("✅ Bot finished.")
