from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from youtube_converter import Youtube
import os
from kivy.uix.screenmanager import ScreenManager, Screen

Window.size = (400, 500)
y = Youtube()

Builder.load_string('''
<FileChooserListView>:
    canvas.before:
        Color:
            rgba: 0,0.8,0.8,1
        Rectangle:
            size: self.size
''')


class DownloadScreen(MDScreen):
    def __init__(self, **kwargs):
        super(DownloadScreen, self).__init__(**kwargs)
    youtube_link = ObjectProperty(None)

    def download_youtube_url(self) -> None:
        url = self.youtube_link.text
        print(f"link: {url}")

        if 'https://www.youtube.com/watch?v=' in url:
            y.get_best_audio(url=url)


class SongPlayerScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SongPlayerScreen, self).__init__(**kwargs)

    def selected(self, filename):
        print(filename)

    def list_music(self) -> list:
        song_list = list()
        for file in os.listdir('./Downloads'):
            if file.endswith(".m4a"):
                song_list.append(file)
        print(song_list)
        return song_list


class Screens(ScreenManager):
    pass


class MusicApp(MDApp):
    def build(self):
        kv = Builder.load_file('music.kv')
        return kv
        #return PrimaryScreen()


if __name__ == "__main__":
    MusicApp().run()
