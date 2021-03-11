# r2callgraph4apk/lib:
Bash files to run Simpleperf on apk files

## Purpose:
To help collect massive data automatically with Simpleperf

## Requirements:
1. A rooted phone - required to run Simpleperf
2. Apk files to test
3. Correct version of Simpleperf from ndk given by Android - check with your API version
   - To test whether the current version of Simpleperf runs, please follow the steps below
     - It should prompt the messages about how to use simpleperf
        ```
        a) ./adb push simpleperf_directory destination_folder_in_your_phone
        b) ./adb shell
        c) cd destination_folder_in_your_phone (type in adb shell)
        d) su ./simpleperf
        ```


## Usage:
Please follow the steps below</br>
- collect_simpleperfData.sh runs all the other bash files (download_simpleperf_benignApk.sh, monkeyrunner.sh, simpleperf_benign.sh, simpleperf_malicious.sh)
1. Follow these commands in your terminal
```
export ADB_PATH=/path/to/adb (/path/to/adb should be replaced with your directory path to adb)
export DESKTOP_PATH=/path/to/desktop (/path/to/desktop should be replaced with directory path to desktop)
export APK_PATH=/path/to/apk (/path/to/apk folder donwloaded by ./r2callgraph4apk.py )
```
2. Type
```
bash collect_simpleperfData.sh app_number pakcage_name
```

Note:</br>
- App_number is folder name that has apk file donwloaded followed by Download pipeline in main README.md file</br>
- Package_name can be obtained from androguard: <Referenced> https://androguard.readthedocs.io/en/latest/intro/gettingstarted.html
