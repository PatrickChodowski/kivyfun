from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.core.window import Window

Window.size = (400, 500)
Builder.load_file('music.kv')


class PrimaryScreen(MDScreen):
    def __init__(self, **kwargs):
        super(PrimaryScreen, self).__init__(**kwargs)
    youtube_link = ObjectProperty(None)

    def press_submit(self):
        print(f"link: {self.youtube_link.text}")


class MusicApp(MDApp):
    def build(self):
        return PrimaryScreen()


if __name__ == "__main__":
    MusicApp().run()
