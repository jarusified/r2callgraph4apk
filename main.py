import os
import sys
from pyinstrument import Profiler


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
    save_dir = args.args['save_dir']

    # assert os.path.splitext(apk)[-1].lower() == ".apk"

    r2callgraph = R2CallGraph4APK(b_apk=apk)

    # profiler = Profiler()
    # profiler.start()
    m_apks = r2callgraph.get_malicious_from_bank(apk, save_dir)

    if len(m_apks) == 0:
        print("No Malware apks found in the bank")
        print("See ya, Bye :(")
        exit()

    for m_apk in m_apks:
        (_name, _type) = r2callgraph.get_malware_labels(m_apk)
        print("------------------------------------------------")
        print(f"Malware apk: {m_apk}")
        print(f"Malware name: {_name}")
        print(f"Malware type: {_type}")
        print("------------------------------------------------")

    # profiler.stop()
    # print(profiler.output_text(unicode=True, color=True))
    
if __name__ == '__main__':
    main()
