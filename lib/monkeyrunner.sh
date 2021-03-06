#!/bin/bash
# monkeyrunner.sh

echo ADB AUTOMATION STEP2:
echo 		1. Put correct app name to get package name in python files
echo 		2. Extract package name only
echo 		3. Run MonkeyRunner
echo [START]

# NOTE
#	please change the list below corresponding to your setup
#	- variable desktop_path
#	- variable adb_path
#	- variable apk_path

desktop_path='/Users/mina/Desktop'
adb_path='/Users/mina/Library/Android/sdk/platform-tools'
cd $desktop_path

# app_name to obtain package name
app_name=$(python3 get_filename.py)
echo $app_name

cd $adb_path
package_name_str=$(./adb shell pm list packages | grep $app_name)
echo $package_name_str
 
package_name=$(echo $package_name_str | tr ":" "\n")

cd $adb_path
for pname in $package_name
do
	echo "1>$pname"
	if [ $pname != "package" ]
	then
		#remove white space
		temp1="$(echo -e "${pname}" | tr -d '[:space:]')"
		echo "2>$pname"
		./adb shell monkey -p $temp1 -v 1050 -s 42
	fi
done

echo [DONE STEP2]
