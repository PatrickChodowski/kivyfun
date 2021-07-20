import os
os.environ['KIVY_AUDIO'] = 'ffpyplayer'

from kivy.utils import platform
from selected_song import SelectedSong
from kivymd.uix.screen import MDScreen
from kivy.uix.actionbar import ActionBar
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.recycleview import RecycleView
from kivy.core.window import Window
from youtube_converter import Youtube
from kivy.uix.screenmanager import ScreenManager, Screen
from utils import get_logger, list_music

__version__ = '0.1.5'

AUDIO_OUTPUT = 'm4a'
if platform in ['linux', 'macosx', 'win']:
    AUDIO_OUTPUT = 'm4a'
elif platform in ['android']:
    AUDIO_OUTPUT = 'ogg'
elif platform in ['ios']:
    AUDIO_OUTPUT = 'wav'

logger = get_logger('songz')

if platform == 'android':
    from android.permissions import request_permissions, Permission, check_permission
    from android.storage import primary_external_storage_path
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

logger.info(f"PLATFORM NAME name: {platform}")
logger.info(f"AUDIO OUTPUT name: {AUDIO_OUTPUT}")

y = Youtube(output_format=AUDIO_OUTPUT,
            destination_path='./downloads',
            logger=logger)

Builder.load_string('''
<FileChooserListView>:
    canvas.before:
        Color:
            rgba: 0,0.8,0.8,1
        Rectangle:
            size: self.size
''')


class RV(RecycleView):
    pass


class ActionBarMain(ActionBar):
    pass


class DownloadScreen(MDScreen):
    def __init__(self, **kwargs):
        super(DownloadScreen, self).__init__(**kwargs)
    youtube_link = ObjectProperty(None)

    def download_youtube_url(self) -> None:
        url = self.youtube_link.text
        logger.info(f"link: {url}")

        if ('https://www.youtube.com/watch?v=' in url) | ('https://youtu.be/' in url):
            #y.get_audio_cmd(url, AUDIO_OUTPUT)
            #y.get_audio_with_thread(url)
            y.get_audio(url)


class SongPlayerScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SongPlayerScreen, self).__init__(**kwargs)
        resume_position = ObjectProperty(None)

        self.resume_position = resume_position
        self.song = None
        self.filename = None


    def selected(self, filename):
        filename = filename[0]
        logger.info(f'new filename: {filename}')
        try:
            if (self.filename != filename) & (self.filename is not None):
                logger.info(f'previous filename: {self.filename}. Providing new one')
                self.song.stop()
                self.song = None

                self.song = SelectedSong(filename=filename, logger=logger)
                self.filename = filename
                if self.song:
                    self.song.play()

            elif (self.filename == filename) & (self.filename is not None):
                logger.info(f'previous filename: {self.filename}. Its the same')
                self.song.stop()
                self.song.play()

            elif self.filename is None:
                logger.info('current filename is empty')
                self.song = SelectedSong(filename=filename, logger=logger)
                self.song.play()
                self.filename = filename

        except Exception as e:
            logger.info(e)

    def play(self):
        if self.song is not None:
            self.song.play()
        else:
            # play the first from the list
            first_song = list_music(logger, AUDIO_OUTPUT)[0]
            self.song = SelectedSong(filename=first_song, logger=logger)
            self.filename = first_song
            if self.song:
                self.song.play()

    def stop(self):
        if self.song is not None:
            self.song.stop()

    def play_pos(self):
        if (self.resume_position.text is None) | (self.resume_position.text == ''):
            # if no argument provided, then use paused time
            logger.info(f"starting from {self.song.paused_time}")
            self.song.play_pos(self.song.paused_time)
        elif (self.resume_position.text is not None) & (self.resume_position.text != ''):
            # if argument provided, play from the position provided
            start_pos = int(self.resume_position.text)

            if start_pos > self.song.length:
                start_pos = self.song.length-2

            logger.info(f"starting from {start_pos}")
            self.song.play_pos(start_pos)

    def volume_up(self):
        self.song.volume_up(0.1)

    def volume_down(self):
        self.song.volume_down(0.1)


class Screens(ScreenManager):
    pass


class MusicApp(MDApp):
    def build(self):
        kv = Builder.load_file('music.kv')
        return kv


if __name__ == "__main__":
    MusicApp().run()
