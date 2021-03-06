echo ADB AUTOMATION STEP4:
echo 		1. Put correct app name in python file to get pid, and change app_num
echo 		2. Extract pid using ps command
echo		3. Run Simpleperf with malicious app
echo [START]

# NOTE
#	please change the list below corresponding to your setup
#	- variable desktop_path
#	- variable adb_path
#	- variable apk_path
#	- variable output_dir (folder to have all csv files collected by Simpleperf)

event_group[0]='branch-load-misses,branch-loads,dTLB-loads,dTLB-stores'
event_group[1]='iTLB-loads,iTLB-stores,L1-dcache-load-misses,L1-dcache-store-misses'
event_group[2]='L1-dcache-stores,L1-icache-load-misses,L1-icache-store-misses,node-loads'
event_group[3]='node-stores,branch-instructions,branch-misses,instructions'

desktop_path='/Users/mina/Desktop'
adb_path='/Users/mina/Library/Android/sdk/platform-tools'

cd $desktop_path
app_num=$(python3 get_appnum.py)
echo $app_num
app_name=$(python3 get_filename.py)
echo $app_name

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
	 
	cd $desktop_path
	pid=$(python3 extract_pid.py $pid_str)
	echo $pid

	# check if pid is extracted (try 10 times)
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

	echo [***DONE Malicious Testing***]
	echo ...Please factory reset the phone
fi
