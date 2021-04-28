import os
import re
import csv
import pathlib 
import pandas as pd
import requests

from utils.utils import read_json

PWD = pathlib.Path(__file__).parent.parent.resolve()
DATA_DIR = os.path.join(PWD, "data")
API_KEY_FILE_NAME =  os.getenv("ANDROZOO_API_KEY", os.path.join(PWD, 'androzoo.az'))


class AndroZoo:
    def __init__(self):
        (self.api_key, self.input_file) = self._read_az(API_KEY_FILE_NAME)

    def _read_az(self, path):
        API_KEY_CONFIG_NAME = 'key'
        INPUT_FILE_CONFIG_NAME = 'input_file'
        SEPARATOR = '='

        api_key, input_file = None, None
        if os.path.exists(path):
            with open(path) as config:
                for line in config:
                    if SEPARATOR in line:
                        key, value = line.split(SEPARATOR)
                        if key == API_KEY_CONFIG_NAME:
                            api_key = value.strip()
                        elif key == INPUT_FILE_CONFIG_NAME:
                            input_file = value.strip()
        else:
            print("Key is not defined. Please, define configuration parameter 'key' in local or global config. Refer https://github.com/ArtemKushnerov/az/blob/master/README.md")
            raise ValueError
        return api_key, input_file

    @staticmethod
    def request_apk_andro(api_key: str, sha256: str, data_dir: str):
        """
        Request the AndroZoo API for the apk and write it to a directory
        
        params:
            api_key: Private key to the AndroZoo API
            sha256: sha256 of the apk
           data_dir: directory to save the file.
        """
        url = "https://androzoo.uni.lu/api/download?"

        packaged_url = url + 'apikey=' + api_key + '&sha256=' + sha256
        print(f"\tDownloading the apk: {sha256}")
        r = requests.get(packaged_url)

        filename = os.path.join(data_dir, sha256 + ".apk")
        with open(filename, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)

    def get_malicious_from_bank(self, b_sha256, save_dir):
        """
        Gets all malicious apks for a given benign apk.
        The benign and malicious apks are stored in `data/piggyback-all-pairs.csv`
        see columns, "ORIGINAL_APP" and "PIGGYBACKED_APP".
        
        params:
            b_sha256: benign apk's sha256
            save_dir: directory to save the file.
        """
        _apk_csv = os.path.join(DATA_DIR, 'piggyback-all-pairs.csv')

        _df = pd.read_csv(_apk_csv)

        malicious_sha_list = _df.loc[_df['ORIGINAL_APP'] == b_sha256]['PIGGYBACKED_APP']
        
        print(f"\tFound {len(malicious_sha_list)} malware(s)!!!")
        
        if len(malicious_sha_list) == 0:
            return []

        # TODO: Write util script to avoid creating if directory exists. 
        benign_folder_path = os.path.join(save_dir, "benign")

        if not os.path.isdir(benign_folder_path):
            os.makedirs(benign_folder_path)

        AndroZoo.request_apk_andro(self.api_key, str(b_sha256), benign_folder_path)
        print(f"\tSaved Benign apk in {os.path.join(benign_folder_path, b_sha256)}")

        malicious_folder_path = os.path.join(save_dir, "malicious")
        if not os.path.isdir(malicious_folder_path):
            os.makedirs(malicious_folder_path)

        for m_sha256 in malicious_sha_list:
            AndroZoo.request_apk_andro(self.api_key, str(m_sha256), malicious_folder_path)
            print(f"\tSaved Malicious apk in {os.path.join(malicious_folder_path, m_sha256)}")
            
        return malicious_sha_list

    @staticmethod
    def get_malware_labels(sha256: str) -> tuple:
        """
        Return the (name, type) of a given SHA256
        
        params:
          sha256: sha256 of a given app
        returns:
          (name, type): malware labels (predicted) from AndroZoo labels.
        """
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
    def get_malware_sha_by_name(malware_name):
        """
        Match the sha's malware name with the provided `malware_name`.
        params:
          malware_name: specific malware name to extract all the sha keys
          e.g., droidKungFu, basebrid and so on...
        
        returns:
          sha256: list of corresponding malware SHA key

        TODO: Reading line by line is expensive. Need to use `read_json` method.
        """

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
                match = re.match(malware_name, name)
                if match:
                    sha256.append(sha)

        f.close()
        return sha256

    @staticmethod
    def get_benign_apps(malware_sha256_list):
        """
        Note: proposed.json name file has some typo on malware names, such as 
        basebrid, which gives you 502 matching results, whereas, full name:
        basebridge, which gives you 438 matching results.
        
        params:
          malware_sha256_list: malware sha list obtained from get_malware_sha_with_name function above
        
        returns:
          benign_sha_list: list of corresponding piggybacked original SHA key
        """
        benign_sha_list = list()
        _apk_csv = os.path.join(DATA_DIR, 'piggyback-all-pairs.csv')
        with open(_apk_csv, 'r') as csv_file:
            reader = csv.reader(csv_file)
            piggy_org_dict = dict((rows[1], rows[0]) for rows in reader)

        for sha in malware_sha256_list:
            sha = sha.upper()
            if(piggy_org_dict.get(sha)):
                benign_sha_list.append(piggy_org_dict.get(sha))

        return benign_sha_list