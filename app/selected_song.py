from kivy.core.audio import SoundLoader
import time


class SelectedSong:
    def __init__(self, filename: str):
        """
        Class to manipulate with selected song
        """
        print(filename)
        self.song = SoundLoader.load(filename)
        self.length = self.song.length
        self.paused_time = 0

    def play(self) -> int:
        if self.song:
            if self.song.state == 'stop':
                self.song.play()
                self.song.seek(0)

                time.sleep(1)
                start_position = round(self.song.get_pos())
                print(f"start position: {start_position}" )
                return start_position
            else:
                print("song is not in stop state")
                return 0
        else:
            print("song didnt load")
            return 0

    def stop(self) -> int:
        if self.song:
            if self.song.state == 'play':
                stopped_pos = round(self.song.get_pos())
                print(f"stopped position: {stopped_pos}")
                self.paused_time = stopped_pos
                self.song.stop()
                return stopped_pos
            else:
                print("song is not in play state")
                return 0
        else:
            print("song didnt load")
            return 0

    def play_pos(self, position: int):
        if self.song:
            if self.song.state == 'stop':
                self.song.play()
                self.song.seek(position)
            else:
                print("song is not in stop state")
        else:
            print("song didnt load")

    def volume_up(self, increment: float):
        if self.song.volume <= 1.0:
            self.song.volume += increment

    def volume_down(self, increment: float):
        if self.song.volume >= 0.0:
            self.song.volume -= increment
