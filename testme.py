
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
filename = 'downloads/AC_DC - BACK IN BLACK MUSIC WITH LYRICS.mp3'
current_sound = SoundLoader.load(filename)
if self.current_sound:
    print("Sound found at %s" % self.current_sound.source)
    print("Sound is %.3f seconds" % self.current_sound.length)
    print(type(self.current_sound))  # <class 'kivy.core.audio.audio_sdl2.SoundSDL2'>
    self.current_sound.play()