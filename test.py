
from app.synchronizer import Synchronizer
from app.utils import get_logger
logger = get_logger('songz')
s = Synchronizer(source_dir='/home/patrick/Music',
                 audio_format='m4a',
                 logger=logger,
                 config_path='./app/config.json')

