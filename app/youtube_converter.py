import subprocess
import logging


class Youtube:
    def __init__(self,
                 destination_path: str = './downloads',
                 logger: logging.Logger):
        self.logger = logger
        self.destination_path = destination_path

        # on android it cant be mp3, it can only be ogg or wav

    def get_m4a_audio(self,
                       url: str):
        """
        Get new access token and headers
        """

        cmd = f"youtube-dl -o '{self.destination_path}/%(title)s.%(ext)s' -f 'bestaudio[ext=m4a]' '{url}'"
        self.logger.info(f'DOWNLOAD CMD: {cmd}')
        subprocess.run(cmd, shell=True)

    def get_mp3_audio(self,
                       url: str):
        """
        Get new access token and headers
        """
        cmd = f"youtube-dl -o '{self.destination_path}/%(title)s.%(ext)s' -x --audio-format mp3 '{url}'"
        self.logger.info(f'DOWNLOAD CMD: {cmd}')
        subprocess.run(cmd, shell=True)

    def get_ogg_audio(self,
                       url: str):
        """
        Get new access token and headers
        """
        cmd = f"youtube-dl -o '{self.destination_path}/%(title)s.%(ext)s' -x --audio-format vorbis '{url}'"
        self.logger.info(f'DOWNLOAD CMD: {cmd}')
        subprocess.run(cmd, shell=True)

    def get_audio(self, url: str, output_format: str) -> None:
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
        subprocess.run(cmd, shell=True)

