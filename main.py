import os
import sys

from version import  __version__
from utils.logger import init_logger
from utils.argparser import ArgParser
from r2callgraph4apk import R2CallGraph4APK
from provider_api import APIProvider

R2CG_APP_HOST = os.getenv("CALLFLOW_APP_HOST", "127.0.0.1")
R2CG_APP_PORT = int(os.getenv("CALLFLOW_APP_PORT", 5000))


def main():
    """
    LightDroid && DroidPerf command utility. 
    """
    print(f' ----------------- r2callgraph4apk {__version__} -----------------')

    # Start logging.
    log_level = 1 if '--verbose' in sys.argv else 2
    init_logger(level=log_level)

    args = ArgParser(sys.argv)
    malware = args.args['malware']
    download = args.args['download']
    process = args.args['process']
    analyze = args.args["analyze"]
    save_dir = args.args['save_dir']

    assert isinstance(malware, str)

    if process:
        r2cg = R2CallGraph4APK(malware_name=malware, save_dir=save_dir)
        r2cg.process()        
    elif analyze:
        r2cg = APIProvider(malware_name=malware, save_dir=save_dir)
        r2cg.analyze()
        r2cg.start(host=R2CG_APP_HOST, port=R2CG_APP_PORT)
    elif download:
        r2cg = R2CallGraph4APK(malware_name=malware, save_dir=save_dir)
        r2cg.download()
        r2cg.process()        

if __name__ == '__main__':
    main()
