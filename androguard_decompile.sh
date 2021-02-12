# To install androguard
pip install androguard

# To generate a Control Flow Graph for a APK. 
androguard decompile -o data/cfg/malicious.apk -f png {PATH/TO/APK}