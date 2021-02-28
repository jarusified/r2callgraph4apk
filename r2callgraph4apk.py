from lib.androguard import AndroGuard
import os
import networkx as nx
import pathlib
from networkx.readwrite import json_graph
from pyinstrument import Profiler

from utils.logger import get_logger
from lib.androzoo import AndroZoo

LOGGER = get_logger(__name__)

PWD = pathlib.Path(__file__).parent.resolve()
DATA_DIR = os.path.join(PWD, "data")
API_KEY_FILE_NAME =  os.getenv("ANDROZOO_API_KEY", os.path.join(PWD, 'androzoo.az'))

MALWARE_NAMES = [] # TODO: Add all andorid malware types.

class R2CallGraph4APK:
    def __init__(self, malware_name: str = ""):
        """
        R2CallGraph4APK class.

        params:
            b_apk: benign_apk provided by the user
        """
        self.nxg = nx.DiGraph()
        self.malware_name = malware_name
        self.save_dir = None
    
    def analyze(self, save_dir):
        """
        # load the results processed from an apk.
        """
        # TODO: Generate the cg here.
        self.save_dir = save_dir

        b_dir = os.path.join(self.save_dir, "benign")
        m_dir = os.path.join(self.save_dir, "malicious")

        # TODO: Remove the assumption that there can be only one apk per type.
        self.b_sha = os.listdir(b_dir)[0]
        self.m_sha = os.listdir(m_dir)[0]

        self.b_ag = AndroGuard(os.path.join(b_dir, self.b_sha))
        self.m_ag = AndroGuard(os.path.join(m_dir, self.m_sha))

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
        _ACTIONS = ["cg"]

        assert "name" in action
        assert action["name"] in _ACTIONS

        action_name = action["name"]

        

        if action_name == "cg":
            # b_path = os.path.join(self.save_dir, 'cg/benign.gml')
            # m_path = os.path.join(self.save_dir, 'cg/malicious.gml')

            # if os.path.isfile(b_path):
            #     b_nxg = nx.read_gml(b_path)
            # else:
            #     b_nxg = nx.DiGraph()

            # if os.path.isfile(m_path):
            #     m_nxg = nx.read_gml(m_path)
            # else:
            #     m_nxg = nx.DiGraph()

            # return {
            #     "b_g": json_graph.node_link_data(b_nxg),
            #     "m_g": json_graph.node_link_data(m_nxg)
            # }

            return {
                "b_g": json_graph.node_link_data(self.b_ag.get_cg()),
                "m_g": json_graph.node_link_data(self.m_ag.get_cg())
            }

