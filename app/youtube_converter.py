import logging
import os
import youtube_dl


class Youtube:
    def __init__(self,
                 logger: logging.Logger,
                 output_format: str,
                 destination_path: str = './downloads'
                 ):
        self.logger = logger
        self.destination_path = destination_path

        if output_format in ['mp3', 'wav', 'm4a']:
            self.ydl = youtube_dl.YoutubeDL({'outtmpl': f'{self.destination_path}/%(title)s.%(ext)s',
                                             'format': output_format})
        elif output_format == 'ogg':
            self.ydl = youtube_dl.YoutubeDL({'outtmpl': f'{self.destination_path}/%(title)s.%(ext)s',
                                             'format': 'vorbis'})
        else:
            self.ydl = None


        # on android it cant be mp3, it can only be ogg or wav


    def get_audio(self, url: str) -> None:
        """
        Get new access token and headers

        :param url: URL of youtube video
        """
        with self.ydl as ydl:
            ydl.download([url])


    def get_audio_cmd(self, url: str, output_format: str) -> None:
        """
        Get new access token and headers

        :param url: URL of youtube video
        :param output_format: MP3 for desktop, WAV or OGG for android
        """
        if output_format in ['mp3', 'wav', 'm4a']:
            cmd = f"youtube-dl -o '{self.destination_path}/%(title)s.%(ext)s' -x --audio-format {output_format} '{url}'"
        elif output_format == 'ogg':
            cmd = f"youtube-dl -o '{self.destination_path}/%(title)s.%(ext)s' -x --audio-format vorbis '{url}'"
        else:
            cmd = ''
        self.logger.info(f'DOWNLOAD CMD: {cmd}')
        os.system(cmd)

