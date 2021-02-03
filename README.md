# r2callgraph4apk

## r2callgraph4apk.py
Since we have to bypass size restriction on uploads to GitHub,
please follow one of the two methods below to use search_malware_name_and_type function:

[method 1]

    1) download the label list from this link - https://androzoo.uni.lu/labels
    2) unzip the labels.tar.gz to your {desired directory}, then you will see 'labels' folder
    3) change the filename
        proposed.json file in {desired directory}/labels/names folder -> proposed_name.json
        proposed.json file in {desired directory}/labels/types folder -> proposed_type.json
    4) move or copy proposed_name.json file and proposed_type.json file to {directory where you pulled the repository}/r2callgraph4apk/data/

[method 2]

    1) download the label list from this link - https://androzoo.uni.lu/labels
    2) unzip the labels.tar.gz to your {desired directory}, you will see 'labels' folder
    3) modify the r2callgraph4apk.py source code like below:

        [original version]
        @staticmethod
        def search_malware_name_and_type(malicious_sha256):
            # call this function to get name and type through malicious sha256
            name_file = open(DATA_DIR + '/proposed_name.json', 'r')
            type_file = open(DATA_DIR + '/proposed_type.json', 'r')

        [modified version]
        @staticmethod
        def search_malware_name_and_type(malicious_sha256):
            # call this function to get name and type through malicious sha256
            name_file = open('{directory where you have 'labels' folder}/labels/names/proposed.json', 'r')
            type_file = open('{directory where you have 'labels' folder}/labels/types/proposed.json', 'r')

        [example - let's say we saved upzipped 'labels' folder in /User/anonymous/Desktop/]
        @staticmethod
        def search_malware_name_and_type(malicious_sha256):
            # call this function to get name and type through malicious sha256
            name_file = open('/User/anonymous/Desktop/labels/names/proposed.json', 'r')
            type_file = open('/User/anonymous/Desktop/labels/types/proposed.json', 'r')
