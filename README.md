# r2callgraph4apk
## Installation
### Requirements:
Access to androzoo. Place your API_KEY file in the root directory of the
project.  You can also set the Filename using

```
export ANDROZOO_API_KEY = {path/to/API_KEY_FILE}
```

Note: Ensure python 3.0 or greater is installed. 

### Data.
- download the label list from this link - https://androzoo.uni.lu/labels.
- unzip the labels.tar.gz to `data` folder.

## Download pipeline
This allows the user to download benign & malicious APKs by the malware name.
For listing the support malware_names, use the following `awk` command to return
the number malware apk for the malware name.

```
awk -F ':' '{print $2}' data/labels/names/proposed.json | sort | uniq -c
```

To download the apks, use
```
python3 main.py --malware {malware_name} --save_dir {/path/to/save/apk} --download
```

## Visual Analysis framework.

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
vite # vite launches a web client on localhost:3000 by default.
```

## Usage

Add this directory to your PYTHONPATH

```sh
export PYTHONPATH=$(pwd):$PYTHONPATH
```

Note: This repository is under development still.