#!/bin/bash

echo "STEP 3:"
echo "		1. Extract pid using ps command"
echo "		2. Run Simpleperf with benign app"
echo "[START]"

event_group[0]='branch-load-misses,branch-loads,dTLB-loads,dTLB-stores'
event_group[1]='iTLB-loads,iTLB-stores,L1-dcache-load-misses,L1-dcache-store-misses'
event_group[2]='L1-dcache-stores,L1-icache-load-misses,L1-icache-store-misses,node-loads'
event_group[3]='node-stores,branch-instructions,branch-misses,instructions'

desktop_path=$1
adb_path=$2
apk_path=$3
app_num=$4
app_name=$5

echo "desktop_path:" $desktop_path
echo "adb_path:" $adb_path
echo "apk_path:" $apk_path
echo "desktop_path:" $app_num
echo "adb_path:" $app_name

# set up the directory for output csv files
output_dir="$desktop_path/benign_output/$app_num$app_name"

# get one row table format result with ps command, and extract pid to use simpleperf
is_number=0
trial=0
while [ $is_number -eq 0 ]
do
	cd $adb_path
	pid_str=$(./adb shell "su -c 'ps | grep $app_name'")
	echo $pid_str

	pid=$(echo $pid_str | awk '{print $2}')
	echo "pid:" $pid
	 
	# check if pid is extracted
	re='^[0-9]+$'
	if ! [[ $pid =~ $re ]] ; then
		echo "error: Not a number" >&2;
		trial=$((trial+1))
		if [ $trial -eq 10 ] ; then
			exit 1
		fi
	else
		is_number=1
	fi
done


cycle=$6
duration=$7

# event group automation based on the cycle #
divider=20
event_num=$((cycle/divider))
remainder=$((cycle%divider))

if [ $remainder -eq 0 ]
then
	event_num=$((event_num-1))
fi

# run simpleperf
cd $adb_path
./adb shell "su -c './sdcard/Download/simpleperf stat -p $pid -e ${event_group[$event_num]} --duration $duration --interval 10 -o /sdcard/Download/output$cycle.csv'"

# when reaching to 80th cycle, pull all output files into the output directory
if [ $cycle -eq 80 ]
then
	mkdir $output_dir
	for i in {1..80}
	do
		./adb pull /sdcard/Download/output$i.csv $output_dir
	done
	./adb shell rm -rf /sdcard/Download/benign
	./adb shell rm -rf /sdcard/Download/*.csv
	package_name_str=$(./adb shell pm list packages | grep $app_name)
	package_name=$(echo $package_name_str | tr ":" "\n")
	for pname in $package_name
	do
		if [ $pname != "package" ]
		then
			#remove white space
			temp1="$(echo -e "${pname}" | tr -d '[:space:]')"
			./adb uninstall $temp1
		fi
	done

	echo "[DONE STEP3]"
	echo "...Completed Benign Apkfile Testing and Data Collection"
	echo "...Completed benign data transfer"
	echo "...Installing malicious apk"
	  
	cd $apk_path
	apk_filename=$(ls $apk_path)
	apk_path=$apk_path/$apk_filename
	 
	cd $adb_path
	./adb install $apk_path

fi
