from kivy.core.audio import SoundLoader
import logging
import time


class SelectedSong:
    def __init__(self, filename: str, logger: logging.Logger):
        """
        Class to manipulate with selected song
        """
        self.logger = logger
        self.logger.info(f"Creating SelectedSong instance from {filename}")

        self.song = SoundLoader.load(filename)
        self.length = self.song.length
        self.logger.info(f"Current SelectedSong length: {self.length}")

        self.paused_time = 0

    def play(self) -> int:
        if self.song:
            if self.song.state == 'stop':
                self.song.play()
                self.song.seek(0)

                time.sleep(1)
                start_position = round(self.song.get_pos())
                self.logger.info(f"start position: {start_position}" )
                return start_position
            else:
                self.logger.info("song is not in stop state")
                return 0
        else:
            self.logger.info("song didnt load")
            return 0

    def stop(self) -> int:
        if self.song:
            if self.song.state == 'play':
                stopped_pos = round(self.song.get_pos())
                self.logger.info(f"stopped position: {stopped_pos}")
                self.paused_time = stopped_pos
                self.song.stop()
                return stopped_pos
            else:
                self.logger.info("song is not in play state")
                return 0
        else:
            self.logger.info("song didnt load")
            return 0

    def play_pos(self, position: int):
        if self.song:
            if self.song.state == 'stop':
                self.song.play()
                self.song.seek(position)
            else:
                self.logger.info("song is not in stop state")
        else:
            self.logger.info("song didnt load")

    def volume_up(self, increment: float):
        if self.song.volume <= 1.0:
            self.song.volume += increment

    def volume_down(self, increment: float):
        if self.song.volume >= 0.0:
            self.song.volume -= increment
