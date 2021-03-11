# NOTE
#	Please follow the steps before running
# 	1. Place all the bashfiles in the same directory with this file
#   2. Follow these commands: 
# 			export ADB_PATH=/path/to/adb (/path/to/adb should be replaced with your directory path to adb)
#			export DESKTOP_PATH=/path/to/desktop (/path/to/desktop should be replaced with directory path to desktop)
#			export APK_PATH=/path/to/apk (/path/to/apk folder donwloaded by ./r2callgraph4apk.py )
#	3. put correct app number and package name as arguments when running collect_simpleperfData.sh

adb_path=$(echo $ADB_PATH)
desktop_path=$(echo $DESKTOP_PATH)
apk_path=$(echo $APK_PATH)
bashfile_path=$(pwd)
app_num=$1
app_name=$2

benign_apkFile_path=$apk_path/$app_num/benign
malicious_apkFile_path=$apk_path/$app_num/malicious

echo "desktop_path:" $desktop_path
echo "adb_path:" $adb_path
echo "bashfile_path:" $bashfile_path
echo "benign_apkFile_path:" $benign_apkFile_path
echo "malicious_apkFile_path:" $malicious_apkFile_path

cd $adb_path
# phone stays awake while plugged
echo **Stay Awake**
./adb shell settings put global stay_on_while_plugged_in 3

# STEP1: download simpleperf and benign apk
cd $bashfile_path
bash download_simpleperf_benignApk.sh $adb_path $benign_apkFile_path

try=0
count=0

for (( i=1; i<=80; i++ ))
do
	echo "***ITERATION $i - benign***"
	cd $adb_path
	# wifi off
	echo **WIFI OFF**
	./adb shell su -c 'svc wifi disable'
	# need to find bluetooth off! (this does not seem to work, for further reference, look into the link below)
	# https://stackoverflow.com/questions/37259260/android-enable-disable-bluetooth-via-command-line
	echo **BLUETOOTH OFF**
	./adb shell settings get global bluetooth_on 0
	./adb shell am broadcast -a android.intent.action.BLUETOOTH_ENABLE --ez state true
	# location off
	echo **LOCATION OFF**
	./adb shell settings put secure location_providers_allowed -gps
	./adb shell settings put secure location_providers_allowed -network
	# nfc off
	echo **NFC OFF**
	./adb shell service call nfc 5
	# airplane mode off
	echo **AIRPLANE MODE OFF**
	./adb shell settings put global airplane_mode_on 0
	./adb shell am broadcast -a android.intent.action.AIRPLANE_MODE

	# STEP2(monkey run) & 3(simpleperf with benign): run monkey runner and simpleperf
	# when 80 cycles are done, uninstall benign apk and install malicious apk
	cd $bashfile_path
	bash monkeyrunner.sh $app_name $adb_path &
	sleep 1
	bash simpleperf_benign.sh $desktop_path $adb_path $malicious_apkFile_path $app_num $app_name $i 15 &
	process_id=$!
	# echo PID: $process_id

	# check whether simpleperf failed
	# if so, try 10 more times
	for job in $process_id
	do
		wait $job || let "FAIL+=1"
		# echo $job $FAIL
	done

	re='^[0-9]+$'
	if ! [[ $FAIL =~ $re ]] || [[ $FAIL -eq 0 ]] ; then
		# echo "Simpleperf Recovered"
		# reset variables
		try=0
		count=0
		
	else
		if [[ $FAIL -gt 0 ]] ; then
			FAIL=0
			count=$((count+1))
			echo "FAIL! ($count/10)"
			i=$((i-1))
			try=$((try+1))
			if [[ $try -eq 10 ]] ; then
				echo "Simpleperf Error"
				exit 1
			fi
		fi
	fi
done 

# start malicious app simpleperf monitoring (repeated process like above)
# initialize
try=0
count=0
for (( i=1; i<=80; i++ ))
do
	echo "***ITERATION $i - malicious***"
	cd $adb_path
	# wifi off
	./adb shell su -c 'svc wifi disable'
	# need to find bluetooth off! (this does not seem to work)
	./adb shell settings get global bluetooth_on 0
	./adb shell am broadcast -a android.intent.action.BLUETOOTH_ENABLE --ez state true
	# location off
	./adb shell settings put secure location_providers_allowed -gps
	./adb shell settings put secure location_providers_allowed -network
	# nfc off
	./adb shell service call nfc 5
	# airplane mode off
	./adb shell settings put global airplane_mode_on 0
	./adb shell am broadcast -a android.intent.action.AIRPLANE_MODE

	# STEP2(monkey run) & 4(simpleperf with malicious): run monkey runner and simpleperf
	cd $bashfile_path
	bash monkeyrunner.sh $app_name $adb_path &
	sleep 1
	bash simpleperf_malicious.sh $i 15 $desktop_path $adb_path $app_num $app_name &
	process_id=$!
	# echo PID: $process_id

	for job in $process_id
	do
		wait $job || let "FAIL+=1"
		# echo $job $FAIL
	done

	re='^[0-9]+$'
	if ! [[ $FAIL =~ $re ]] || [[ $FAIL -eq 0 ]] ; then
		# echo "Simpleperf Recovered"
		# reset variables
		try=0
		count=0

	else
		if [[ $FAIL -gt 0 ]] ; then
			FAIL=0
			count=$((count+1))
			echo "FAIL! ($count/10)"
			i=$((i-1))
			try=$((try+1))
			if [[ $try -eq 10 ]] ; then
				echo "Simpleperf Error"
				exit 1
			fi
		fi
	fi
done 

# trigger the factory reset
# whether to do factory reset or not depends on user's choice
cd $adb_path
./adb reboot recovery
