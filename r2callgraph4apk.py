import networkx as nx

from utils.logger import get_logger

LOGGER = get_logger(__name__)

class R2CallGraph4APK:
    def __init__(self, apk: str = ""):
        """
        """
        self.nxg = nx.DiGraph()


    def load(self):
        """
        # load the results processed from an apk.
        """

    # --------------------------------------------------------------------------
    def process(self):
        """
        Process the apk using a Pipeline of operations.
        """
        print(f'\n\n-------------------- PROCESSING {len(self.config["runs"])} SUPERGRAPHS --------------------\n\n')


    def request(self, action):
        """
        Handles general requests
        """
        _ACTIONS = ["init"]

        assert "name" in action
        assert action["name"] in _ACTIONS

        action_name = _ACTIONS["name"]

        if action_name == "init":
            pass