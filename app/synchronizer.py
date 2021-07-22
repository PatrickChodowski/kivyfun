
import logging
import os
import json
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import AuthError
import sys


class Synchronizer:
    def __init__(self,
                 source_dir: str,
                 audio_format: str,
                 logger: logging.Logger,
                 config_path: str = 'config.json'):

        self.audio_format = audio_format
        self.source_dir = source_dir
        self.logger = logger
        self.config_path = config_path

        self.song_list = list()
        self.key_list = dict()
        self.local_library = dict()
        self.master_library = dict()
        self.config = self._read_config()

    def _read_config(self) -> dict:
        with open(self.config_path) as config_file:
            config_dict = json.load(config_file)
        return config_dict

    def get_local_songs(self) -> list:
        self.song_list = list()
        for file in os.listdir(self.source_dir):
            if file.endswith(f".{self.audio_format}"):
                self.song_list.append(f'{self.source_dir}/{file}')
            self.logger.info(self.song_list)
        return self.song_list


    def get_local_meta(self) -> list:
        self.key_list = list()
        for file in os.listdir(f'{self.source_dir}/meta'):
            if file.endswith(f".json"):
                key = file.replace('.json', '')
                self.key_list.append(key)
                # with open(f'{self.source_dir}/meta/{file}') as json_file:
                #     data = json.load(json_file)
                # self.json_dict[key] = data
            self.logger.info("Local meta listed:")
            self.logger.info(self.key_list)
        return self.key_list

    def build_local_library(self):
        self.logger.info("Building local library first")
        all_songs = self.get_local_meta()
        with open(f'{self.source_dir}/meta/library/local_library.json', 'w', encoding='utf-8') as outfile:
            json.dump(all_songs, outfile, ensure_ascii=False)
        self.logger.info("meta/library/local_library.json rebuilt")

    def read_library(self, name: str) -> list:
        self.logger.info(f"Reading library {name}")
        with open(f'{self.source_dir}/meta/library/{name}_library.json') as library_file:
            loaded_string = json.load(library_file)
            self.logger.info(f"Read library {name} as string: {loaded_string}")

            self.logger.info(f"type of the library string: {type(loaded_string)}")
            if not isinstance(loaded_string, list):
                library = eval(loaded_string)
                return library
            else:
                return loaded_string

    def compare_local_with_master(self) -> (list, list):
        local_library = self.read_library('local')
        self.logger.info("Read local library finished")
        master_library = self.read_library('master')
        self.logger.info("Read master library finished")

        local_only = list(set(local_library) - set(master_library))
        master_only = list(set(master_library) - set(local_library))
        #in_both = set(local_library.keys()).intersection(set(master_library.keys()))
        self.logger.info(f"local only files: {local_only}")
        self.logger.info(f"master only files: {master_only}")

        # delete local_only
        # download master_only
        return local_only, master_only


    def upload_master_library_dropbox(self):
        with dropbox.Dropbox(self.config['TOKEN']) as dbx:
            try:
                dbx.users_get_current_account()
            except AuthError:
                sys.exit("ERROR: Invalid access token; try re-generating an "
                         "access token from the app console on the web.")
            with open(f"{self.source_dir}/meta/library/master_library.json", 'rb') as f:
                dbx.files_upload(f.read(), '/master_library.json', mode=WriteMode('overwrite'))

    def download_master_to_local_master_copy_library_dropbox(self):
        with dropbox.Dropbox(self.config['TOKEN']) as dbx:
            try:
                dbx.users_get_current_account()
            except AuthError:
                sys.exit("ERROR: Invalid access token; try re-generating an "
                         "access token from the app console on the web.")

            md, response = dbx.files_download('/master_library.json')
            file_contents = response.content.decode("utf-8")
            self.logger.info("Just read contents of dropbox master library:")
            self.logger.info(file_contents)

            with open(f'{self.source_dir}/meta/library/master_library.json', 'w', encoding='utf-8') as outfile:
                json.dump(file_contents, outfile, ensure_ascii=False)
            self.logger.info("Sync down finished")



    def upload_local_as_master_library_dropbox(self):
        with dropbox.Dropbox(self.config['TOKEN']) as dbx:
            try:
                dbx.users_get_current_account()
            except AuthError:
                sys.exit("ERROR: Invalid access token; try re-generating an "
                         "access token from the app console on the web.")

            with open(f"{self.source_dir}/meta/library/local_library.json", 'rb') as f:
                self.logger.info("Overwriting master library on dropbox")
                dbx.files_upload(f.read(), '/master_library.json', mode=WriteMode('overwrite'))

    def delete_songs_local(self, list_local_only: list):
        if list_local_only.__len__() > 0:
            for lfo in list_local_only:
                filename = f'{self.source_dir}/meta/{lfo}.json'
                if os.path.isfile(filename):
                    self.logger.info(f"{filename} exists!")
                    with open(filename) as meta_file:
                        song_meta = json.load(meta_file)
                        title = song_meta['title']
                        song_path = f'{self.source_dir}/{title}.{self.audio_format}'
                        self.logger.info(f"song path to delete: {song_path}")
                        if os.path.isfile(song_path):
                            self.logger.info(f"{song_path} exists...")
                            os.remove(song_path)
                            self.logger.info(f"...not anymore")
