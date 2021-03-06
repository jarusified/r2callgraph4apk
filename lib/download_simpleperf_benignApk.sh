# download_simpleperf_benignApk.sh
@echo off
echo ADB AUTOMATION STEP1:
echo 		1. Push simpleperf via adb
echo 		2. Install benign apk to smartphone
echo [START]

# NOTE
#	please change the list below corresponding to your setup
#	- variable desktop_path
#	- variable adb_path
#	- variable apk_path
#	- ndk version 

desktop_path='/Users/mina/Desktop'
adb_path='/Users/mina/Library/Android/sdk/platform-tools'
cd $desktop_path

# app number to get apk file
# when downloading apps from AndroZoo, apks are saved /number/benign or /number/malicious
app_num=$(python3 get_appnum.py)
#echo $app_num

# apk path
apk_path="/Users/mina/Desktop/Mina/Graduate_School/Research/malware/AndroZoo/droidkungfu_w_benign/$app_num/benign"
echo $apk_path

# push simpleperf into the phone (corresponding ndk version needed)
cd $adb_path
./adb push ../ndk/20.1.5948944/simpleperf/bin/android/arm/simpleperf /sdcard/Download
   
cd $apk_path
apk_filename=$(ls)
apk_path=$apk_path/$apk_filename
 
cd $adb_path
./adb install $apk_path

echo [DONE STEP1]
echo ...Benign app is ready to run
echo ...Please, start running STEP2
