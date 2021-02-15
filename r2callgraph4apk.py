import os
import re
import csv
import networkx as nx
import pandas as pd
import requests
import pathlib

from utils.logger import get_logger
from utils.utils import read_json

LOGGER = get_logger(__name__)

PWD = pathlib.Path(__file__).parent.resolve()
DATA_DIR = os.path.join(PWD, "data")
API_KEY = open(os.path.join(PWD, 'ANDROZOO_API_KEY.txt'), "r").read()


class R2CallGraph4APK:
    def __init__(self, b_apk: str = ""):
        """
        R2CallGraph4APK class.

        params:
            b_apk: benign_apk provided by the user
        """
        self.nxg = nx.DiGraph()
        self.b_apk = b_apk

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
        print(f"Downloading the apk: {sha256}")
        r = requests.get(packaged_url)

        filename = os.path.join(data_dir, sha256 + ".apk")
        with open(filename, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)

    @staticmethod
    def get_malicious_from_bank(b_sha256, save_dir):
        # Gets all malicious apks for a given benign apk.
        # The benign and malicious apks are stored in `data/piggyback-all-pairs.csv`
        # see columns, "ORIGINAL_APP" and "PIGGYBACKED_APP".
        #
        # params:
        #     b_sha256: benign apk's sha256
        #     save_dir: directory to save the file.
        _apk_csv = os.path.join(DATA_DIR, 'piggyback-all-pairs.csv')

        _df = pd.read_csv(_apk_csv)

        malicious_sha_list = _df.loc[_df['ORIGINAL_APP'] == b_sha256]['PIGGYBACKED_APP']
        
        print(f"Found {len(malicious_sha_list)} malware(s)!!!")
        
        if len(malicious_sha_list) == 0:
            return []

        # TODO: Write util script to avoid creating if directory exists. 
        benign_folder_path = os.path.join(save_dir, "benign")

        if not os.path.isdir(benign_folder_path):
            os.makedirs(benign_folder_path)

        R2CallGraph4APK.request_apk_andro(API_KEY, str(b_sha256), benign_folder_path)
        print(f"Saved Benign apk in {os.path.join(benign_folder_path, b_sha256)}")

        malicious_folder_path = os.path.join(save_dir, "malicious")
        if not os.path.isdir(malicious_folder_path):
            os.makedirs(malicious_folder_path)

        for m_sha256 in malicious_sha_list:
            R2CallGraph4APK.request_apk_andro(API_KEY, str(m_sha256), malicious_folder_path)
            print(f"Saved Malicious apk in {os.path.join(malicious_folder_path, m_sha256)}")
            
        return malicious_sha_list

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

    @staticmethod
    def get_malware_sha_with_name(malware_name):
        # params:
        #   malware_name: specific malware name to extract all the sha keys
        #       * proposed.json name file has some typo on malware names, such as basebrid, which gives you 502 matching results,
        #           whereas, full name: basebridge, which gives you 438 matching results.
        # returns:
        #   sha256: list of corresponding malware SHA key

        name = ''
        sha = ''
        sha256 = []
        l = []

        _PROPOSED_NAME_FILE = os.path.join(DATA_DIR, 'labels/names/proposed.json')
        f = open(_PROPOSED_NAME_FILE, "r")

        for line in f:
            l = line.split(':')
            if len(l) > 1:
                sha = l[0]
                name = l[1]

                sha = sha[3:-2]
                name = name[2:-3]
                match = re.match(pattern, name)
                if match:
                    sha256.append(sha)

        f.close()
        return sha256

    @staticmethod
    def get_piggybacked_apps(malware_sha256_list):
        # params:
        #   malware_sha256_list: malware sha list obtained from get_malware_sha_with_name function above
        #
        # returns:
        #   piggybaked_original_sha_list: list of corresponding piggybacked original SHA key

        piggybaked_original_sha_list = list()
        _apk_csv = os.path.join(DATA_DIR, 'piggyback-all-pairs.csv')
        with open(_apk_csv, 'r') as csv_file:
            reader = csv.reader(csv_file)
            piggy_org_dict = dict((rows[1], rows[0]) for rows in reader)

        for sha in sha256:
            sha = sha.upper()
            if(piggy_org_dict.get(sha)):
                piggybaked_original_sha_list.append(piggy_org_dict.get(sha))

        return piggybaked_original_sha_list

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
