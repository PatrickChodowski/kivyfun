import subprocess

url = 'https://www.youtube.com/watch?v=Mbsc-3T6o4M'


class Youtube:
    def __init__(self):
        pass

    def get_best_audio(self,
                       url: str,
                       destination_path: str = ''
                       ):
        """
        Get new access token and headers
        """
        destination_path = '~/Documents/project/kivyfun/downloads/'
        cmd = f"youtube-dl -o '{destination_path}' -f 'bestaudio[ext=m4a]' '{url}' "
        subprocess.run(cmd, shell=True)


yt = Youtube()
yt.get_best_audio(url)