import logging
import os
import youtube_dl
import json
from dataclasses import dataclass, asdict
from downloader_thread import DownloaderThread
from ydl_logger import YdlLogger


@dataclass
class YoutubeMeta:
    """Class for storing youtube meta"""
    id: str
    title: str
    duration: int
    webpage_url: str
    channel: str
    upload_date: int
    thumbnail_url: str




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

    def get_meta(self, url: str) -> None:
        with self.ydl as ydl:
            song_meta = ydl.extract_info(url, download=False)
            th_url = ''
            for th in song_meta['thumbnails']:
                if th['height'] == 94:
                    th_url = th['url']

            y_song_meta = YoutubeMeta(
                id=song_meta['id'],
                title=song_meta['title'],
                duration=song_meta['duration'],
                webpage_url=song_meta['webpage_url'],
                channel=song_meta['channel'],
                thumbnail_url=th_url,
                upload_date=song_meta['upload_date'],
            )
            self.logger.info(f"META - ID: {song_meta['id']}")
            self.logger.info(f"META - TITLE: {song_meta['title']}")
            self.logger.info(f"META - DURATION: {song_meta['duration']}")
            self.logger.info(f"META - URL: {song_meta['webpage_url']}")
            self.logger.info(f"META - CHANNEL: {song_meta['channel']}")
            self.logger.info(f"META - THUMBNAIL URL: {th_url}")
            self.logger.info(f"META - UPLOAD DATE: {song_meta['upload_date']}")

            with open(f"./meta/{song_meta['id']}.json", 'w', encoding='utf-8') as fp:
                json.dump(asdict(y_song_meta), fp, ensure_ascii=False)


    def get_audio(self, url: str) -> None:
        """
        Get new access token and headers

        :param url: URL of youtube video
        """
        self.logger.info(f'DOWNLOAD URL: {url}')
        self.get_meta(url)

        with self.ydl as ydl:
            ydl.download([url])


    def get_audio_cmd(self, url: str, output_format: str) -> None:
        """
        Get new access token and headers

        :param url: URL of youtube video
        :param output_format: MP3 for desktop, WAV or OGG for android
        """
        self.get_meta(url)

        if output_format in ['mp3', 'wav', 'm4a']:
            cmd = f"youtube-dl -o '{self.destination_path}/%(title)s.%(ext)s' -x --audio-format {output_format} '{url}'"
        elif output_format == 'ogg':
            cmd = f"youtube-dl -o '{self.destination_path}/%(title)s.%(ext)s' -x --audio-format vorbis '{url}'"
        else:
            cmd = ''
        self.logger.info(f'DOWNLOAD CMD: {cmd}')
        os.system(cmd)


    def get_audio_with_thread(self, url: str) -> None:
        ydl_logger = YdlLogger(rv=None, index=0)

        # Run youtube-dl in a thread so the UI do not freeze
        t = DownloaderThread(url=url,
                             ydl=self.ydl,
                             ydl_logger=ydl_logger,
                             datum=dict()
                             )
        t.start()
