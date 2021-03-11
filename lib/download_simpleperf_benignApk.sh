# download_simpleperf_benignApk.sh
@echo off
echo "STEP1:"
echo "		1. Push simpleperf via adb"
echo "		2. Install benign apk to smartphone"
echo "[START]"

adb_path=$1
benign_apk_path=$2
echo "adb_path:" $adb_path
echo "benign_apk_path:" $benign_apk_path

# push simpleperf into the phone (corresponding ndk version needed)
cd $adb_path
./adb push ../ndk/20.1.5948944/simpleperf/bin/android/arm/simpleperf /sdcard/Download
   
cd $benign_apk_path
apk_filename=$(ls)
benign_apk_path=$benign_apk_path/$apk_filename
 
cd $adb_path
./adb install $benign_apk_path

echo "[DONE STEP1]"
