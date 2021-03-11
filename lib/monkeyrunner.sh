#!/bin/bash
# monkeyrunner.sh

echo "STEP2:"
echo "		1. Extract package name from 'pm list packages' command"
echo "		2. Run MonkeyRunner with the package name"
echo "[START]"

app_name=$1
adb_path=$2

cd $adb_path
package_name_str=$(./adb shell pm list packages | grep $app_name)
# echo $package_name_str
 
package_name=$(echo $package_name_str | tr ":" "\n")

cd $adb_path
for pname in $package_name
do
	# echo "1>$pname"
	if [ $pname != "package" ]
	then
		#remove white space
		temp1="$(echo -e "${pname}" | tr -d '[:space:]')"
		echo "2>$pname"
		./adb shell monkey -p $temp1 -v 1050 -s 42
	fi
done
