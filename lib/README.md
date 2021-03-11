r2callgraph4apk/lib:
    include bash files to run Simpleperf on apk files

Purpose:
    to help collect massive data automatically with Simpleperf

Requirements:
    1. A rooted phone - required to run Simpleperf
    2. Correct version of Simpleperf from ndk given by Android - check with your API version
        To test whether the current version of Simpleperf runs or not:
            The steps above should prompt the messages about how to use simpleperf
            1) ./adb push simpleperf_directory destination_folder_in_your_phone
            2) su ./simpleperf
    3. apk files to test

Usage:
    * collect_simpleperfData.sh runs all the other bash files (download_simpleperf_benignApk.sh, monkeyrunner.sh, simpleperf_benign.sh, simpleperf_malicious.sh)

    Please follow the steps below
        1. Follow these commands in your terminal: 
                - export ADB_PATH=/path/to/adb (/path/to/adb should be replaced with your directory path to adb)
                - export DESKTOP_PATH=/path/to/desktop (/path/to/desktop should be replaced with directory path to desktop)
                - export APK_PATH=/path/to/apk (/path/to/apk folder donwloaded by ./r2callgraph4apk.py )
        2. type "bash collect_simpleperfData.sh app_number pakcage_name" in the terminal

        Note:   App_number is folder name that has apk file donwloaded followed by Download pipeline in main README.md file.
                Package_name can be obtained from androguard. Check out the details: https://androguard.readthedocs.io/en/latest/intro/gettingstarted.html