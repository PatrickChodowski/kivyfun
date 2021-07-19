import logging
import os


def get_logger(logger_name: str) -> logging.Logger:
    """
    Setup of the logger for the function
    :param logger_name: name of the logger
    :return: logging.Logger that will work for this function
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def list_music(logger: logging.Logger) -> list:
    song_list = list()
    for file in os.listdir('./downloads'):
        if file.endswith(".mp3"):
            song_list.append('./downloads/'+file)
        logger.info(song_list)
    return song_list
