# LightDriod - DroidPerf/VIS
LightDriod is an light-weight malware detection tool for Android platform.
LightDriod uses Hardware Performance Couters (HPCs) to detect malicious
applications based on low-level hardware features. 

Note: This repository is under development still. Expect things to change!! 
## Requirements:
Python >=3.7
Nodejs >= v12.16.2
Yarn >= 1.21.1

## Androzoo: Malicious/Benign APKs  (Optional)
Data/APKs that we have tested our app as case studies can be found
(here)[https://drive.google.com/file/d/1A8bOhEN2zvAwiuBMerF1FwhAuMzQH933/view?usp=sharing]
(10 DroidKungFu apks) as zip file. If you would like to get new data, read on.

Androzoo is a dataset of Android APKs that have been tagged as "malware" by
several online platforms like VirusTotal, Anti Virus software. They provide a
nice interface to download malwares for research applications. 

1. ** APK Labels **. The data repository provides a convenient API interface to download as `.apk`
   files. Each `.apk` is tagged by its `sha256` hash to uniquely identify the
   required APK file. This list can be found (here)[https://androzoo.uni.lu/labels].
   Unzip the labels.tar.gz in the `data` folder. This will take a few minutes as
   the file named `latest.csv` which is quite large ~3.5 GB. 

2. ** Androzoo API Key **. An API key is required to androzoo is required to get download the apk files. Please find more
information (here)[https://androzoo.uni.lu/access] on how to get the API_KEY.

Once you have the API_KEY, place your API_KEY into a `.az` file.

Your `.az` file must contain

```
key=%API_KEY%  
input_file=%PATH_TO_INPUT_FILE%
```

Next, export the file to $ANDROZOO_API_KEY using, 
```
export ANDROZOO_API_KEY = {path/to/API_KEY_FILE.az}
```
   
4. ** Downloading **. One can either use `curl`, (`az`)[https://github.com/ArtemKushnerov/az], or
   use `main.py --download` to get access to malwares.

   via `curl`:

   ```
    curl -O --remote-header-name -G -d apikey=${APIKEY} -d sha256=${SHA256} https://androzoo.uni.lu/api/download
   ```

   via `az`. `az` provides several features to filter out apk files by size,
   time, platform and so on. Please refer az's github for more information. 

   ```
    az -n 10 -d 2015-12-11: -s :3000000 -m play.google.com,appchina
   ```

   via `main.py --download`. In our experiments, we particularly focused on
   piggybacked applications. A list of piggybacked applications can be found at
   `data/piggyback-all-pairs.csv`. 

    For listing the support malware_names, use the following `awk` command to
    return the number malware apk for the malware name.

    ```
    awk -F ':' '{print $2}' data/labels/names/proposed.json | sort | uniq -c
    ```

    To download the apks, use
    ```
    python3 main.py --malware {malware_name} --save_dir {/path/to/save/apk} --download
    ```

    The above script will collect all the malwares of that particular type.
# DroidPerf - Performance Data Collection
DroidPerf is a HPC data collector that uses Intel VTune's Performance toolkit
and Android's monkeyrunner tool to collect 16 critical HPCs from the application
at runtime by simulation.

See [here](droidPerf/README.md)

# LightDriod-app
LightDriod-app is a React-native based mobile application that provides
explainability into when our classification algorithm tags a malware. This app
can be used on an Android device and automatic reports will be sent and user can
also attribute the HPCs to a particular malicious behavior.

## Setup

### React-Native
To get started with the development environment, please visit
https://reactnative.dev/docs/environment-setup and follow the steps
there to install react-native.

Steps below show what exact versions of each tool were installed when I was setting up the environment. We want everybody in the team to use the same versions.

Highly recommend that you use `nvm` to install `node`, as it can easily control what node version you can use.

```
brew install nvm
```

We'll be using Node LTS v12.16.2 along with `yarn` package manager v1.12.1.

```
nvm install 12.16.2
```

We'll then install `watchman`, which is a tool to watch changes in the filesystem. It can help speed up the debugger process later in React Native by showing the changes in you app without needing to reinstall the app.
```
brew install watchman
```
### Cocoapods
Cocoapods is a package manager for Xcode. You can install it with the following command
```
sudo gem install cocoapods
```

We can then use `pod` to install ios platform-specific packages that are supporting the higher level react-native modules.
```
cd ios
pod install
```
### Android
To set up the development environment to build for Android, please follow the guide here https://reactnative.dev/docs/environment-setup. It supports building in MacOS, Windows, and Linux.

Please ignore the "Creating a new application" section.

## Installation

To install required packages used by the React-native application,
```
yarn install
```

## Running the Application
It is a React Native builtin command line inteface. Rather than installing it
globally, you can run the current version of it with `npx`. The below command
wil spawn a client-server that will render the application. 

```
yarn start --reset-cache
```

To run the simulator on your system,
```
yarn run-android
```

To run on a physical device, 
```
yarn run-android --simulator "Device Name" 
```

### Simulator
If you want to launch your app in a Android emulator, please run the following command.
```
npx react-native run-android
```
You can also run it directly from within Android Studio by choosing the emulator as the device you want to run on.

### Android Device
In Android studio, please open the project by choosing the `android` directory. You can then run the application by choosing your connected device.



## Static Feature Visualizations - Web application
This web-application provides a perspective into 
### Installation
1. Ensure you have yarn and nodejs installed in your machine.
```
cd app # Go into app folder
yarn install  # Install all required packages
```

### Running

To run the server,
```
python3 main.py --save_dir {path/to/save/apk} --analyze
```

To run the client,
```
cd app
vite # vite launches a web client on localhost:3000 by default.
```

