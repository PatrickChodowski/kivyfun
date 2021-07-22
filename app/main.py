import os
import certifi
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from youtube_converter import Youtube
from utils import get_logger
from ydl_logger import YdlLogger
from kivy.uix.label import Label
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from synchronizer import Synchronizer

__version__ = '0.4.2'

if platform in ['linux', 'win']:
    AUDIO_OUTPUT = 'm4a'
    OUTPUT_DIR = '/home/patrick/Music'
    SOURCE_DIR = '/home/patrick/Music'
elif platform in ['android']:
    AUDIO_OUTPUT = 'm4a'
    OUTPUT_DIR = os.getenv('EXTERNAL_STORAGE')
    OUTPUT_DIR += '/Music'
    SOURCE_DIR = OUTPUT_DIR
elif platform in ['macosx']:
    AUDIO_OUTPUT = 'm4a'
    OUTPUT_DIR = '/Users/patrick/Music'
    SOURCE_DIR = '/Users/patrick/Music'
elif platform in ['ios']:
    AUDIO_OUTPUT = 'wav'
    OUTPUT_DIR = './downloads'
    SOURCE_DIR = './downloads'

STATUS_IN_PROGRESS = 1
STATUS_DONE = 2
STATUS_ERROR = 3

logger = get_logger('songz')

if platform == 'android':
    from android.permissions import request_permissions, Permission, check_permission
    from android.storage import primary_external_storage_path
    os.environ['SSL_CERT_FILE'] = certifi.where()


logger.info(f"PLATFORM NAME name: {platform}")
logger.info(f"AUDIO OUTPUT name: {AUDIO_OUTPUT}")
logger.info(f"OUTPUT DIR name: {OUTPUT_DIR}")
logger.info(f"SOURCE DIR name: {SOURCE_DIR}")

y = Youtube(logger=logger,
            output_format=AUDIO_OUTPUT,
            ydl_logger=YdlLogger(rv=dict(), index=0),
            destination_path=OUTPUT_DIR)

s = Synchronizer(source_dir=SOURCE_DIR, audio_format=AUDIO_OUTPUT, logger=logger)



class RV(RecycleView):
    pass


class DownloadStatusBar(BoxLayout):
    url = StringProperty('')
    status = NumericProperty(STATUS_IN_PROGRESS)
    log = StringProperty('')
    index = NumericProperty()
    status_icon = StringProperty('./img/loader.png')
    title = StringProperty('')
    percent = NumericProperty(0)
    ETA = StringProperty('')
    speed = StringProperty('')
    file_size = StringProperty('')
    popup = None

    def on_status(self, instance, value):
        if value == STATUS_IN_PROGRESS:
            self.status_icon = './img/loader.png'
        elif value == STATUS_DONE:
            self.status_icon = './img/correct.png'
        elif value == STATUS_ERROR:
            self.status_icon = './img/cancel.png'


class DownloaderLayout(BoxLayout):
    youtube_link = ObjectProperty(None)

    def start_download(self):
        index = len(self.ids.rv.data)
        url = self.youtube_link.text
        meta = y.get_meta(url)
        # Add UI status bar for this download
        self.ids.rv.data.append({'url': url,
                                 'index': index,
                                 'log': '',
                                 'title': meta.title,
                                 'status': STATUS_IN_PROGRESS})

        y.set_ydl_logger(ydl_logger=YdlLogger(self.ids.rv, index))

        logger.info(f"link: {url}")
        if ('https://www.youtube.com/watch?v=' in url) | ('https://youtu.be/' in url):
            y.get_audio_with_thread(url)

    def start_download_from_url(self, url: str):
        index = len(self.ids.rv.data)
        meta = y.get_meta(url)
        # Add UI status bar for this download
        self.ids.rv.data.append({'url': url,
                                 'index': index,
                                 'log': '',
                                 'title': meta.title,
                                 'status': STATUS_IN_PROGRESS})

        y.set_ydl_logger(ydl_logger=YdlLogger(self.ids.rv, index))

        logger.info(f"link: {url}")
        if ('https://www.youtube.com/watch?v=' in url) | ('https://youtu.be/' in url):
            y.get_audio_with_thread(url)

    def syncronize_up(self):
        s.build_local_library()
        s.upload_local_as_master_library_dropbox()

    def syncronize_down(self):
        s.build_local_library()
        s.download_master_to_local_master_copy_library_dropbox()
        local_only, master_only = s.compare_local_with_master()

        # s.delete_songs_local(local_only)

        if master_only.__len__() > 0:
            for lmo in master_only:
                url_lmo = f"https://www.youtube.com/watch?v={lmo}"
                self.start_download_from_url(url_lmo)



class RootLayout(Label):
    pass


class StatusIcon(Label):
    status = NumericProperty(1)


class Songz(App):
    def build(self):
        if platform == 'android' and not check_permission('android.permission.WRITE_EXTERNAL_STORAGE'):
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE])

        kv = Builder.load_file('music.kv')
        return RootLayout()


if __name__ == '__main__':
    Songz().run()
