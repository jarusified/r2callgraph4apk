# r2callgraph4apk

## Data.
- download the label list from this link - https://androzoo.uni.lu/labels
- unzip the labels.tar.gz to `data` folder

# Install

```
pip install androguard
```

## Usage

Add this directory to your PYTHONPATH

```sh
export PYTHONPATH=$(pwd):$PYTHONPATH
```

The current functionality lets the user download all malicious apk files for a
given benign apk file, if it exists in the bank.

```
python main.py --apk {sha256} --save_dir {/path/to/save/apk}
```