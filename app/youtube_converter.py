import subprocess


class Youtube:
    def __init__(self, destination_path: str = './downloads'):
        self.destination_path = destination_path

        # on android it cant be mp3, it can only be ogg or wav

    def get_m4a_audio(self,
                       url: str):
        """
        Get new access token and headers
        """

        cmd = f"youtube-dl -o '{self.destination_path}/%(title)s.%(ext)s' -f 'bestaudio[ext=m4a]' '{url}'"
        subprocess.run(cmd, shell=True)

    def get_mp3_audio(self,
                       url: str):
        """
        Get new access token and headers
        """
        cmd = f"youtube-dl -o '{self.destination_path}/%(title)s.%(ext)s' -x --audio-format mp3 '{url}'"
        subprocess.run(cmd, shell=True)

    # def get_ogg_audio(self,
    #                    url: str):
    #     """
    #     Get new access token and headers
    #     """
    #     cmd = f"youtube-dl -o '{self.destination_path}/%(title)s.%(ext)s' -x --audio-format mp3 '{url}'"
    #     subprocess.run(cmd, shell=True)

    def get_audio(self, url: str, output_format: str) -> None:
        """
        Get new access token and headers

        :param url: URL of youtube video
        :param output_format: MP3 for desktop, WAV or OGG for android
        """
        if output_format in ['mp3', 'wav', 'ogg']:
            cmd = f"youtube-dl -o '{self.destination_path}/%(title)s.%(ext)s' -x --audio-format {output_format} '{url}'"
            subprocess.run(cmd, shell=True)

