#!/bin/bash

echo "STEP 4:"
echo "		1. Extract pid using ps command"
echo "		2. Run Simpleperf with malicious app"
echo "[START]"

event_group[0]='branch-load-misses,branch-loads,dTLB-loads,dTLB-stores'
event_group[1]='iTLB-loads,iTLB-stores,L1-dcache-load-misses,L1-dcache-store-misses'
event_group[2]='L1-dcache-stores,L1-icache-load-misses,L1-icache-store-misses,node-loads'
event_group[3]='node-stores,branch-instructions,branch-misses,instructions'

desktop_path=$3
adb_path=$4
app_num=$5
app_name=$6

# set up the directory for output csv files
output_dir="$desktop_path/malicious_output/$app_num$app_name"

# get one row table format result with ps command, and extract pid to use simpleperf
is_number=0
trial=0
while [ $is_number -eq 0 ]
do
	cd $adb_path
	pid_str=$(./adb shell "su -c 'ps | grep $app_name'")
	echo $pid_str
	 
	pid=$(echo $pid_str | awk '{print $2}')

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

cycle=$1
duration=$2

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

	echo "[***ALL COMPLETED***]"
	echo "...Completed Malicious Apkfile Testing and Dat Collection"
	echo "...Please factory reset the phone"
fi