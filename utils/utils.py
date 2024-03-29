import numpy as np
import pandas as pd
from scipy import stats
from pathlib import Path 

# ------------------------------------------------------------------------------
# statistics utils
# ------------------------------------------------------------------------------
def median(arr: list):
    """
    Returns the median and its index in the array.
    """
    indices = []

    list_size = len(arr)
    median = 0
    if list_size % 2 == 0:
        indices.append(int(list_size / 2) - 1)  # -1 because index starts from 0
        indices.append(int(list_size / 2))
        median = (arr[indices[0]] + arr[indices[1]]) / 2
    else:
        indices.append(int(list_size / 2))
        median = arr[indices[0]]

    return median, indices


def avg(arr: list):
    """
    Returns the average of the array.
    Uses floating-point division.
    """
    return sum(arr) / float(len(arr))

def histogram(data, data_range=None, bins=20):

    assert isinstance(data, (pd.Series, np.ndarray))
    if len(data) == 0:
        return np.array([]), np.array([])

    if data_range is None:
        data_range = [data.min(), data.max()]
    else:
        assert isinstance(data_range, (list, np.ndarray))
        assert len(data_range) == 2
    h, b = np.histogram(data, range=data_range, bins=bins)
    return 0.5 * (b[1:] + b[:-1]), h


def freedman_diaconis_bins(arr):
    """Calculate number of hist bins using Freedman-Diaconis rule."""
    # From https://stats.stackexchange.com/questions/798/

    n = len(arr)
    if n < 2:
        return 1

    # Calculate the iqr ranges.
    iqr = [stats.scoreatpercentile(arr, _) for _ in [25, 75]]

    # Calculate the h
    h = 2 * (iqr[1] - iqr[0]) / (n ** (1 / 3))

    # fall back to sqrt(a) bins if iqr is 0
    if h == 0:
        return int(np.sqrt(arr.size))

    else:
        return int(np.ceil((arr.max() - arr.min()) / h))


def outliers(data, scale=1.5, side='both'):

    assert isinstance(data, (pd.Series, np.ndarray))
    assert len(data.shape) == 1
    assert isinstance(scale, float)
    assert side in ['gt', 'lt', 'both']

    d_q13 = np.percentile(data, [25., 75.])
    iqr_distance = np.multiply(stats.iqr(data), scale)

    if side in ["gt", "both"]:
        upper_range = d_q13[1] + iqr_distance
        upper_outlier = np.greater(data - upper_range.reshape(1), 0)

    if side in ["lt", "both"]:
        lower_range = d_q13[0] - iqr_distance
        lower_outlier = np.less(data - lower_range.reshape(1), 0)

    if side == "gt":
        return upper_outlier
    if side == "lt":
        return lower_outlier
    if side == "both":
        return np.logical_or(upper_outlier, lower_outlier)


def kde(data, gridsize=10, fft=True,
        kernel="gau", bw="scott", cut=3, clip=(-np.inf, np.inf)):
    assert isinstance(data, (pd.Series, np.ndarray))

    if bw == "scott":
        bw = stats.gaussian_kde(data).scotts_factor() * data.std(ddof=1)

    kde = smnp.KDEUnivariate(data)

    # create the grid to fit the estimation.
    support_min = min(max(data.min() - bw * cut, clip[0]), 0)
    support_max = min(data.max() + bw * cut, clip[1])
    x = np.linspace(support_min, support_max, gridsize)

    kde.fit("gau", bw, fft, gridsize=gridsize, cut=cut, clip=clip)
    y = kde.density
    return x, y

# ------------------------------------------------------------------------------
# JSON utilities
# ------------------------------------------------------------------------------
import json
import jsonschema

def jsonify_string(string: str) -> any:
    """
    Convert a string input to a json object.

    :param string: String to be converted to JSON.
    :return JSON object
    """
    assert isinstance(string, str)
    _ = json.loads(string, object_hook=byteify)
    return byteify(_, ignore_dicts=True)


def byteify(data: str, ignore_dicts: bool=False) -> any:
    """
    Byteify a string into a JSON-valid object.

    :param data: data as string
    :param ignore_dicts: True will ignore dictionaries in deeper levels (used in recursive strategy)
    :return: JSON object
    """
    # if this is a unicode string, return its string representation
    if isinstance(data, bytes):
        return data.encode("utf-8")

    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [byteify(item, ignore_dicts=True) for item in data]

    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            byteify(key, ignore_dicts=True): byteify(value, ignore_dicts=True)
            for key, value in data.items()
        }
    # if it's anything else, return it in its original form
    return data

def read_json(filename: str) -> any:
    """
    Read a JSON file as text and convert to JSON format.

    :param filename: File's name to be read
    :return JSON formatted text.
    """
    f = open(filename, "r").read()
    json_data = jsonify_string(f)
    return json_data

def write_json(json_data, filename) -> None:
    """
    Write a JSON object into a file.

    :param json_data: JSON data to put in the file.
    :param filename: Filename to store the JSON object.
    :return: None
    """
    with open(filename, "w") as fp:
        fp.write(json.dumps(json_data, default=lambda o: o.__dict__, sort_keys=True, indent=2))

def is_valid_json(data: any) -> bool:
    """
    Check if data is a valid JSON object.
    """
    try:
        json.loads(data)
    except ValueError as err:
        print(err)
        return False
    return True

def is_valid_json_with_schema(data: any, schema: any) -> any:
    jsonschema.validate(instance=data, schema=schema)

# ------------------------------------------------------------------------------
# Directory utilities
# ------------------------------------------------------------------------------
def list_subdirs(path: str, exclude_subdirs: list=[]) -> list:
    """
    List the sub directories in path. This excludes the subdirs in exclude_names.

    :param path: Path to list sub directories.
    :param exclude_subdirs: Exclude array
    :return: list of sub directories in the given path
    """
    subdirs = [os.path.basename(f.path) for f in os.scandir(path)
               if f.is_dir()]
    return [_ for _ in subdirs if _ not in exclude_subdirs]


def list_files(path: str, include_file_extn: str, exclude_files: list=[]) -> list:
    """
    List files in path.

    :param path:
    :param include_file_extn:
    :param exclude_files:
    :return:
    """
    files = [os.path.basename(_) for _ in os.scandir(path)
             if os.path.splitext(_)[1] == include_file_extn]
    return [_ for _ in files if _ not in exclude_files]


# ------------------------------------------------------------------------------
# Subprocess utilities
# ------------------------------------------------------------------------------
import subprocess
import os

def execute_cmd(cmd: str) -> None:
    """
    cmd is expected to be something like "cd [place]"
    """
    cmd = cmd + " && pwd"
    p = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    out = p.stdout.read()
    err = p.stderr.read()

    if out != "":
        os.chdir(out[0 : len(out) - 1])
    if err != "":
        print(err)
    return


# ------------------------------------------------------------------------------
# File encoding utilities.
# ------------------------------------------------------------------------------
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


# --------------------------------------------------------------------------
# callflow.nxg utilities.
# --------------------------------------------------------------------------

def nx_add_prefix(graph, prefix):
    """
    Rename graph to obtain disjoint node labels
    """
    assert isinstance(graph, nx.DiGraph)
    if prefix is None:
        return graph

    def label(x):
        if isinstance(x, str):
            name = prefix + x
        else:
            name = prefix + repr(x)
        return name

    return nx.relabel_nodes(graph, label)

def nx_tailhead(edge):
    return (edge[0], edge[1])

def nx_tailheadDir(edge, edge_direction):
    return (str(edge[0]), str(edge[1]), edge_direction[edge])

def nx_leaves_below(nxg, node):
    assert isinstance(nxg, nx.DiGraph)
    return set(
        sum(
            (
                [vv for vv in v if nxg.out_degree(vv) == 0]
                for k, v in nx.dfs_successors(nxg, node).items()
            ),
            [],
        )
    )

# --------------------------------------------------------------------------
# r2callgraph4apk utilities.
# --------------------------------------------------------------------------

def get_apks_from_path(path):
    ALLOW_EXTENSIONS = [".apk"]

    allowed_files = []    
    for ext in ALLOW_EXTENSIONS:
        allowed_files.extend([
            str(file) for file in Path(path).iterdir() if file.name.endswith(".apk")
        ])
    return allowed_files 

def get_filename_from_path(filepath):
    """
    Truncates the parents and the extension from a filepath.
    """
    return filepath.split("/")[-1].split(".")[0]