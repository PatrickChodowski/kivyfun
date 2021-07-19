import subprocess


class Youtube:
    def __init__(self, destination_path: str = './downloads'):
        self.destination_path = destination_path

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

