import threading
import traceback
import youtube_dl
import logging
STATUS_IN_PROGRESS = 1
STATUS_DONE = 2
STATUS_ERROR = 3

# copied solution from youtube-dl-kivy repository, cant make it work otherwise on android
# https://github.com/odrevet/youtube-dl-kivy


class DownloaderThread(threading.Thread):
    def __init__(self, url,
                 ydl: youtube_dl.YoutubeDL,
                 logger: logging.Logger,
                 datum: dict = None):
        threading.Thread.__init__(self)
        self.url = url
        self.ydl = ydl
        self.datum = datum
        self.logger = logger

    def run(self):
        try:
            with self.ydl as ydl:
                ret_code = ydl.download([self.url])
                self.logger.info(f'Finished with retcode {ret_code}')
                self.datum['status'] = STATUS_DONE if ret_code == 0 else STATUS_ERROR
        except SystemExit:
            self.logger.info(f'System Exit')
            self.datum['status'] = STATUS_ERROR
            pass
        except Exception as e:
            self.logger.info(e)
            self.logger.error(traceback.format_exc())
            self.datum['status'] = STATUS_ERROR
            pass
