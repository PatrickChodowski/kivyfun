import threading
import traceback
import youtube_dl
from ydl_logger import YdlLogger

STATUS_IN_PROGRESS = 1
STATUS_DONE = 2
STATUS_ERROR = 3

# copied solution from youtube-dl-kivy repository, cant make it work otherwise on android
# https://github.com/odrevet/youtube-dl-kivy


class DownloaderThread(threading.Thread):
    def __init__(self, url, ydl: youtube_dl.YoutubeDL, ydl_logger: YdlLogger, datum: dict = None):
        threading.Thread.__init__(self)
        self.url = url
        self.ydl = ydl
        self.ydl_logger = ydl_logger
        self.datum = datum

    def run(self):
        try:
            with self.ydl as ydl:
                retcode = ydl.download([self.url])
                self.ydl_logger.debug(f'Finished with retcode {retcode}')
                self.datum['status'] = STATUS_DONE if retcode == 0 else STATUS_ERROR
        except SystemExit:
            self.ydl_logger.debug('System Exit')
            self.datum['status'] = STATUS_ERROR
            pass
        except Exception as inst:
            self.ydl_logger.error(inst)
            self.ydl_logger.error(traceback.format_exc())
            self.datum['status'] = STATUS_ERROR
            pass
