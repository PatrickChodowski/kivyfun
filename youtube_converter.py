import subprocess

class Youtube:
    def __init__(self):
        pass

    def get_best_audio(self,
                       url: str,
                       destination_path: str = '~/Documents/projects/kivyfun/downloads'
                       ):
        """
        Get new access token and headers
        """
        #cmd = "youtube-dl -f 'bestaudio[ext=m4a]' 'https://www.youtube.com/watch?v=Mbsc-3T6o4M'"
        cmd = f"youtube-dl -o '{destination_path}/%(title)s.%(ext)s' -f 'bestaudio[ext=m4a]' '{url}'"

        #cmd = f"youtube-dl -f 'bestaudio[ext=m4a]' '{url}'"

        #cmd = f"youtube-dl -x --audio-format mp3 'https://www.youtube.com/watch?v=Mbsc-3T6o4M'"
        subprocess.run(cmd, shell=True)

