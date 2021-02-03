import os
import networkx as nx
import pandas as pd
import requests

from utils.logger import get_logger
from utils.utils import read_json

LOGGER = get_logger(__name__)

PWD = os.path.abspath(".")
DATA_DIR = os.path.join(PWD, "data")
API_KEY = open(os.path.join(PWD, 'ANDROZOO_API_KEY.txt'), "r").read()


class R2CallGraph4APK:
    def __init__(self, apk: str = ""):
        """
        """
        self.nxg = nx.DiGraph()
        self.apk = apk

    def load(self):
        """
        # load the results processed from an apk.
        """

    def process(self):
        """
        Process the apk using a Pipeline of operations.
        """
        print(f'\n\n-------------------- PROCESSING  --------------------\n\n')

    @staticmethod
    def request_apk_andro(api_key: str, sha256: str, data_dir: str):
        # Request the AndroZoo API for the apk and write it to a directory
        #
        # params:
        #     api_key: Private key to the AndroZoo API
        #     sha256: sha256 of the apk
        #    data_dir: directory to save the file.
        url = "https://androzoo.uni.lu/api/download?"

        packaged_url = url + 'apikey=' + api_key + '&sha256=' + sha256
        print("Requesting", packaged_url)
        r = requests.get(packaged_url)

        filename = os.path.join(data_dir, sha256 + ".apk")
        with open(filename, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)

    @staticmethod
    def get_malicious_from_piggyback(b_sha256, data_dir):
        # Gets all malicious apks for a given benign apk.
        # The benign and malicious apks are stored in `data/piggyback-all-pairs.csv`
        # see columns, "ORIGINAL_APP" and "PIGGYBACKED_APP".
        #
        # params:
        #     b_sha256: benign apk's sha256
        #     data_dir: directory to save the file.
        _apk_csv = os.path.join(DATA_DIR, 'piggyback-all-pairs.csv')

        _df = pd.read_csv(_apk_csv)

        malicious_sha_list = _df.loc[_df['ORIGINAL_APP'] == b_sha256]['PIGGYBACKED_APP']

        benign_folder_path = os.path.join(data_dir, "benign")
        print(benign_folder_path)

        if not os.path.isdir(benign_folder_path):
            os.makedirs(benign_folder_path)

        R2CallGraph4APK.request_apk_andro(API_KEY, str(b_sha256), benign_folder_path)

        malicious_folder_path = os.path.join(data_dir, "malicious")
        print(malicious_folder_path)
        if not os.path.isdir(malicious_folder_path):
            os.makedirs(malicious_folder_path)

        for malicious_sha256 in malicious_sha_list:
            R2CallGraph4APK.request_apk_andro(API_KEY, str(malicious_sha256), malicious_folder_path)

    @staticmethod
    def get_malware_labels(sha256: str) -> tuple:
        # Return the (name, type) of a given SHA256
        #
        # params:
        #   sha256: sha256 of a given app
        # returns:
        #   (name, type): malware labels (predicted) from AndroZoo labels.

        # TODO: We might need to move the reading to process, if we want to use this functionality.
        _PROPOSED_NAME_FILE = os.path.join(DATA_DIR, 'labels/names/proposed.json')
        _PROPOSED_TYPE_FILE = os.path.join(DATA_DIR, 'labels/types/proposed.json')

        _name_dict = read_json(_PROPOSED_NAME_FILE)
        _type_dict = read_json(_PROPOSED_TYPE_FILE)

        if sha256 in _name_dict:
            _name = _name_dict[sha256]
        else:
            _name = None

        if sha256 in _type_dict:
            _type = _type_dict[sha256]
        else:
            _type = None

        return (_name, _type)

    def request(self, action):
        """
        Handles requests to an action from the client
        """
        _ACTIONS = ["init"]

        assert "name" in action
        assert action["name"] in _ACTIONS

        action_name = action["name"]

        if action_name == "init":
            pass
