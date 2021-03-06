# NOTE
#	Please follow the steps before running
# 	1. Please change adb_path, and code_path where all bash files are
#	2. Please check each bash file where to modify before run
#	3. Please put correct app number and package name in get_appnum.py and get_filename.py

adb_path='/Users/mina/Library/Android/sdk/platform-tools'
code_path='/Users/mina/Desktop'

# download simpleperf and benign apk
bash download_simpleperf_benignApk.sh
try=0

for i in {1..80}
do
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

	# run monkey runner and simpleperf
	# when 80 cycles are done, uninstall benign apk and install malicious apk
	cd $code_path
	bash monkeyrunner.sh &
	sleep 1
	bash simpleperf_benign.sh $i 15 &
	process_id="$process_id $!"
	echo PID: $process_id

	# check whether simpleperf failed
	# if so, try 10 more times
	for job in $process_id
	do
		wait $job || let "FAIL+=1"
		echo $job $FAIL
	done

	re='^[0-9]+$'
	if ! [[ $FAIL =~ $re ]] ; then
		try=0
	else
		if [ $FAIL -gt 0 ] ; then
			echo "FAIL! ($FAIL)"
			i=$i-1
			try=$((try+1))
			if [ $try -eq 10 ] ; then
				echo "Simpleperf Error"
				exit 1
			fi
		fi
	fi
done 

# start malicious app simpleperf monitoring (repeated process like above)
for i in {1..80}
do
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

	cd $code_path
	bash monkeyrunner.sh &
	sleep 1
	bash simpleperf_malicious.sh $i 15 &
	process_id="$process_id $!"
	echo PID: $process_id

	for job in $process_id
	do
		wait $job || let "FAIL+=1"
		echo $job $FAIL
	done

	re='^[0-9]+$'
	if ! [[ $FAIL =~ $re ]] ; then
		try=0
		#echo "PASS: Not a number" >&2;
	else
		if [ $FAIL -gt 0 ] ; then
			echo "FAIL! ($FAIL)"
			i=$i-1
			try=$((try+1))
			if [ $try -eq 10 ] ; then
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
