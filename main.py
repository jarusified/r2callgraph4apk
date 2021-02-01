import os
import sys

from version import  __version__
from utils.logger import init_logger
from utils.argparser import ArgParser
from r2callgraph4apk import R2CallGraph4APK

def main():
    # --------------------------------------------------------------------------
    print(f' ----------------- r2callgraph4apk {__version__} -----------------')

    # Start logging.
    log_level = 1 if '--verbose' in sys.argv else 2
    init_logger(level=log_level)

    args = ArgParser(sys.argv)
    apk = args.args['apk']

    assert os.path.splitext(apk)[-1].lower() == ".apk"

    r2callgraph = R2CallGraph4APK(apk=apk)




if __name__ == '__main__':
    main()
