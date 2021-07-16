import subprocess


class Youtube:
    def __init__(self):
        pass

    def get_m4a_audio(self,
                       url: str,
                       destination_path: str = '~/Documents/projects/kivyfun/downloads'
                       ):
        """
        Get new access token and headers
        """

        cmd = f"youtube-dl -o '{destination_path}/%(title)s.%(ext)s' -f 'bestaudio[ext=m4a]' '{url}'"
        subprocess.run(cmd, shell=True)

    def get_mp3_audio(self,
                       url: str,
                       destination_path: str = '~/Documents/projects/kivyfun/downloads'
                       ):
        """
        Get new access token and headers
        """
        cmd = f"youtube-dl -o '{destination_path}/%(title)s.%(ext)s' -x --audio-format mp3 '{url}'"
        subprocess.run(cmd, shell=True)

