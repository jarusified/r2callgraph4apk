import os
import networkx as nx
import pathlib
from networkx.readwrite import json_graph
from pyinstrument import Profiler

from utils.logger import get_logger
from utils.utils import get_apks_from_path, get_filename_from_path
from droidPerf.androzoo import AndroZoo
from droidPerf.androguard import AndroGuard

LOGGER = get_logger(__name__)

PWD = pathlib.Path(__file__).parent.resolve()
DATA_DIR = os.path.join(PWD, "data")

MALWARE_NAMES = [] # TODO: Add all andorid malware types.

class R2CallGraph4APK:
    def __init__(self, malware_name: str, save_dir: str):
        """
        R2CallGraph4APK class.

        params:
            b_apk: benign_apk provided by the user
        """
        self.nxg = {} # map of nxg  {sha: <nx.DiGraph>}
        self.malware_name = malware_name
        self.save_dir = save_dir

        b_dir = os.path.join(self.save_dir, "benign")
        m_dir = os.path.join(self.save_dir, "malicious")

        self.b_sha_paths = get_apks_from_path(b_dir)
        self.m_sha_paths = get_apks_from_path(m_dir)

        self.b_shas = [get_filename_from_path(path) for path in self.b_sha_paths]
        self.m_shas = [get_filename_from_path(path) for path in self.m_sha_paths]

        self.b_ag = self._init_androguard(b_dir, self.b_sha_paths)
        self.m_ag = self._init_androguard(m_dir, self.m_sha_paths)
    
    def _init_androguard(self, directory, shas):
        ret = {}
        for sha in shas:
            path = os.path.join(directory, sha)
            ret[get_filename_from_path(sha)] = AndroGuard(sha, path)
        return ret
    
    def analyze(self):
        """
        Load the results processed from an apk.
        """
        for apk in self.b_ag:
            ag = self.b_ag[apk]
            self.nxg[ag.sha] = ag.read_cg()

        for apk in self.m_ag:
            ag = self.m_ag[apk]
            self.nxg[ag.sha] = ag.read_cg()

    def process(self):
        """
        Process pipeline for dumping call graphs, 
        """

        for b_sha in self.b_shas:
            self.b_ag[b_sha].save_cg()
        
        for m_sha in self.m_shas:
            self.m_ag[m_sha].save_cg()

    def download(self, save_dir):
        """
        Process the apk using a Pipeline of operations.
        """
        profiler = Profiler()
        profiler.start()

        az = AndroZoo()

        malicious_sha256_list = az.get_malware_sha_by_name(self.malware_name)
        
        print(f"1. Identified {len(malicious_sha256_list)} {self.malware_name} apk files")
        
        benign_sha256_list = az.get_benign_apps(malicious_sha256_list)
    
        print(f"2. R2CallGraph4APK could find only {len(benign_sha256_list)} benign versions.")
        
        print(f"3. Downloading {len(benign_sha256_list)} Benign and Malicious APKs")
        
        for idx, b_sha256 in enumerate(benign_sha256_list):
            save_path = os.path.join(save_dir, str(idx))
            m_sha256_list = az.get_malicious_from_bank(b_sha256, save_path)

            for m_sha256 in m_sha256_list:
                print("\t----------- Malware Chacterization -------------")
                (_name, _type) = az.get_malware_labels(m_sha256)
                print(f"\tBenign apk: {b_sha256}")
                print(f"\tMalware apk: {m_sha256}")
                print(f"\tMalware name: {_name}")
                print(f"\tMalware type: {_type}")
                print("\t------------------------------------------------")

        profiler.stop()
        print(profiler.output_text(unicode=True, color=True))

    def request(self, action):
        """
        Handles requests to an action from the client

        params:
            action: Action triggered by the server request.
        
        return:
            results in the valid JSON format.
        """
        _ACTIONS = ["cg", "init"]

        assert "name" in action
        assert action["name"] in _ACTIONS

        action_name = action["name"]

        if action_name == "init":
            return {
                "b_sha": self.b_shas,
                "m_sha": self.m_shas
            }

        if action_name == "cg":
            _nxg = self.nxg[action["sha"]]
            return json_graph.node_link_data(_nxg)

        # elif action_name == "metadata":
        #     return self.

