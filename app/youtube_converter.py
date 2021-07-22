import logging
import os
import youtube_dl
import json
from dataclasses import dataclass, asdict
from downloader_thread import DownloaderThread
import traceback
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
                 ydl_logger: YdlLogger,
                 destination_path: str = './downloads',
                 source_path: str = './downloads'
                 ):
        self.output_format = output_format
        self.logger = logger
        self.destination_path = destination_path
        self.source_path = source_path
        self.ydl_logger = ydl_logger

        if self.output_format in ['mp3', 'wav', 'm4a']:
            self.ydl = youtube_dl.YoutubeDL({'outtmpl': f'{self.destination_path}/%(title)s.%(ext)s',
                                             'format': self.output_format,
                                             'logger': self.logger})
        elif self.output_format == 'ogg':
            self.ydl = youtube_dl.YoutubeDL({'outtmpl': f'{self.destination_path}/%(title)s.%(ext)s',
                                             'format': 'vorbis',
                                             'logger': self.logger})
        else:
            self.ydl = None

    def set_ydl_logger(self, ydl_logger):
        self.ydl = youtube_dl.YoutubeDL({'outtmpl': f'{self.destination_path}/%(title)s.%(ext)s',
                                         'format': self.output_format,
                                         'logger': ydl_logger})


    def get_meta(self, url: str) -> YoutubeMeta:
        self.logger.info(f"Getting metadata for url {url}")
        song_meta = dict()
        try:
            with self.ydl as ydl:
                self.logger.info("STARTING SONG META EXTRACTION")
                song_meta = ydl.extract_info(url, download=False)
                self.logger.info("SONG META EXTRACTED")
        except Exception as inst:
            print(inst)
            tb = traceback.format_exc()
            print(tb)
            pass


        th_url = ''
        if 'thumbnails' in song_meta:
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

        with open(f"{self.destination_path}/meta/{song_meta['id']}.json", 'w', encoding='utf-8') as fp:
            json.dump(asdict(y_song_meta), fp, ensure_ascii=False)

        return y_song_meta


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
        self.logger.info(f'DOWNLOAD URL: {url}')
        # self.get_meta(url)
        # Run youtube-dl in a thread so the UI do not freeze
        t = DownloaderThread(url=url,
                             ydl=self.ydl,
                             datum=dict(),
                             logger=self.logger
                             )
        t.start()
        self.logger.info(f'DOWNLOAD THREAD STARTED')
