import os
import argparse

class ArgParser:
    """
    Argparser class decodes the arguments passed to
    """
    def __init__(self, args_string):

        assert isinstance(args_string, list)

        # Parse the arguments passed.
        self.parser = ArgParser._create_parser()
        self.args = vars(self.parser.parse_args())

        # Verify if only valid things are passed.
        self._verify_parser()


    def __str__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "<%s: {%s}> \n" % (self.__class__.__name__, ", ".join(items))

    def __repr__(self):
        return self.__str__()

    # --------------------------------------------------------------------------
    # Private methods.
    @staticmethod
    def _create_parser():
        """
        Parse the input arguments.
        """
        parser = argparse.ArgumentParser(prefix_chars="--")
        parser.add_argument("--malware", type=str,
                            help="APK file to be visualized.")
        parser.add_argument("--save_dir", type=str,
                            help="Save directory for the Benign APK")
        parser.add_argument("--download", action="store_true", 
                            help="Download benign and malicious versions of the malware type")
        parser.add_argument("--analyze", action="store_true",
                            help="Spawns a visualization tool to study and analyze benign and malicious apks")
        return parser

    def _verify_parser(self):
        """
        Verify the input arguments.

        Raises expections if something is not provided
        Check if the config file is provided and exists!

        :pargs : argparse.Namespace
            Arguments passed by the user.

        Returns
        -------
        """
        _has_malware_name = self.args["malware"] is not None
        _is_download = self.args["download"] is not None
        _is_analyze = self.args["analyze"] is not None

        if not _has_malware_name:
            s = "Malware name not provied"
            print(s)
            exit(1)

        if not _is_analyze and not _is_download:
            s = "Please provide the mode you want to run this script. Available modes are --download | --analyze"
            print(s)
            exit(1)
