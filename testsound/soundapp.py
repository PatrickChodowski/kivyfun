import os
os.environ['KIVY_AUDIO'] = 'ffpyplayer'

from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from app.youtube_converter import Youtube
from kivy.uix.screenmanager import ScreenManager
from app.selected_song import SelectedSong



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


class SongPlayerScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SongPlayerScreen, self).__init__(**kwargs)

        filename = '../app/downloads/AC_DC - BACK IN BLACK MUSIC WITH LYRICS.mp3'
        #self.current_sound = SoundLoader.load(filename)
        self.current_sound = SelectedSong(filename=filename)

    def selected(self, filename):
        try:
            if self.current_sound:
                #print(type(self.current_sound)) #<class 'kivy.core.audio.audio_sdl2.SoundSDL2'>
                self.current_sound.play()
        except:
            pass

    def play(self):
        self.current_sound.play()

    def play_pos(self):
        self.current_sound.play_pos(60)

    def stop(self):
        self.current_sound.stop()

class Screens(ScreenManager):
    pass


class SoundApp(MDApp):
    def build(self):
        kv = Builder.load_file('soundapp.kv')
        return kv


if __name__ == "__main__":
    SoundApp().run()