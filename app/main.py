import os
os.environ['KIVY_AUDIO'] = 'ffpyplayer'
from selected_song import SelectedSong
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from youtube_converter import Youtube
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
        resume_position = ObjectProperty(None)

        self.resume_position = resume_position
        self.song = None
        self.filename = None


    def selected(self, filename):
        filename = filename[0]
        print(f'new filename: {filename}')
        try:
            if (self.filename != filename) & (self.filename is not None):
                print('new filename')
                self.song.stop()
                self.song = None

                self.song = SelectedSong(filename=filename)
                self.filename = filename
                if self.song:
                    self.song.play()

            elif (self.filename == filename) & (self.filename is not None):
                print('same filename')
                self.song.stop()
                self.song.play()

            elif self.filename is None:
                print('current filename is empty')
                self.song = SelectedSong(filename=filename)
                self.song.play()
                self.filename = filename

        except Exception as e:
            print(e)

    def play(self):
        self.song.play()

    def stop(self):
        self.song.stop()

    def play_pos(self):
        if (self.resume_position.text is None) | (self.resume_position.text == ''):
            # if no argument provided, then use paused time
            print(f"starting from {self.song.paused_time}")
            self.song.play_pos(self.song.paused_time)
        elif (self.resume_position.text is not None) & (self.resume_position.text != ''):
            # if argument provided, play from the position provided
            start_pos = int(self.resume_position.text)

            if start_pos > self.song.length:
                start_pos = self.song.length-2

            print(f"starting from {start_pos}")
            self.song.play_pos(start_pos)

    def volume_up(self):
        self.song.volume_up(0.1)

    def volume_down(self):
        self.song.volume_down(0.1)




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
