from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
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
            #y.get_best_audio(url=url)
            y.get_mp3_audio(url=url)


class SongPlayerScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SongPlayerScreen, self).__init__(**kwargs)

        self.current_sound = None

    def selected(self, filename):
        try:
            print(filename[0])
            self.current_sound = SoundLoader.load(filename[0])
            if self.current_sound:
                print("Sound found at %s" % self.current_sound.source)
                print("Sound is %.3f seconds" % self.current_sound.length)
                print(type(self.current_sound)) #<class 'kivy.core.audio.audio_sdl2.SoundSDL2'>
                self.current_sound.play()
        except:
            pass

    def play(self):
        self.current_sound.play()

    def stop(self):
        self.current_sound.stop()

    # def list_music(self) -> list:
    #     song_list = list()
    #     for file in os.listdir('./Downloads'):
    #         if file.endswith(".m4a"):
    #             song_list.append(file)
    #     print(song_list)
    #     return song_list


class Screens(ScreenManager):
    pass


class MusicApp(MDApp):
    def build(self):
        kv = Builder.load_file('music.kv')
        return kv


if __name__ == "__main__":
    MusicApp().run()
