import os, random, threading, requests, certifi
os.environ["SSL_CERT_FILE"] = certifi.where()  # lets HTTPS images load on Android
from kivy.app import App
from kivy.clock import mainthread
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label

class XkcdApp(App):
    title = "XKCD Comic Generator"
    icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png")
    latest = None  # newest comic number, fetched once and reused

    def build(self):
        root = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))
        self.img = AsyncImage(fit_mode="contain", size_hint=(1, 0.5))
        self.info = Label(halign="center", valign="top", font_size="14sp", size_hint=(1, 0.35))
        self.info.bind(size=lambda w, s: setattr(w, "text_size", (s[0], s[1])))  # wrap text
        self.btn = Button(text="Get A Random Comic", size_hint=(1, 0.15))
        self.btn.bind(on_press=self.start)
        for w in (self.img, self.info, self.btn):
            root.add_widget(w)
        return root

    def start(self, _):
        self.btn.disabled = True  # prevent double taps while loading
        self.info.text = "Loading..."
        threading.Thread(target=self.fetch, daemon=True).start()

    def fetch(self):  # runs in a background thread: never touch widgets here
        try:
            if not self.latest:
                self.latest = requests.get("https://xkcd.com/info.0.json", timeout=10).json()["num"]
            num = 404
            while num == 404:  # #404 doesn't exist (joke)
                num = random.randint(1, self.latest)
            c = requests.get(f"https://xkcd.com/{num}/info.0.json", timeout=10).json()
            self.show(c["img"], f"#{c['num']}: {c['title']}\n{c['year']}-{c['month']}-{c['day']}\n\n{c['alt']}")
        except Exception as e:
            self.show("", f"Error: {e}")

    @mainthread
    def show(self, img_url, text):
        self.img.source = img_url
        self.info.text = text
        self.btn.disabled = False

    def on_pause(self):
        return True  # keeps the app alive when you switch away on Android

if __name__ == "__main__":
    XkcdApp().run()