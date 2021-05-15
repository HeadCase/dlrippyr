#!/usr/bin/env python
import json
import subprocess
from collections import deque
from pathlib import Path


def probe_meta(video_file):
    r"""Acquires relevant metadata from supplied video file

    Parameters
    ----------
    video_file: str
        Path name to a video file in the form of a str object. Passed on to
        get_json

    Returns
    -------
    relevant_data:  dict
         Dictionary of relevant metadata; keys for category (e.g. bit rate or
         file size) and values for values (e.g. 3.6 Mbps or 25MB)
    """
    # Define the metadata we actually want back
    relevant_tags = {
        'format_name': 'format',
        'codec_name': 'streams',
        'profile': 'streams',
        'avg_frame_rate': 'streams',
        'height': 'streams',
        'width': 'streams',
        'bit_rate': 'format',
        'size': 'format',
    }
    relevant_data = {}

    # json-formatted 'bulk' metadata
    raw_meta = get_json(video_file)

    # Parse the bulk metadata to get the relevant bits we want
    for k, v in relevant_tags.items():
        if v == 'streams':
            relevant_data[k] = raw_meta[v][0][k]
        else:
            relevant_data[k] = raw_meta[v][k]
    # Tinker with units and formatting
    rate_mb = (int(relevant_data['bit_rate']) / 1000**2)
    size_mb = int(relevant_data['size']) / 1024**2
    relevant_data['bit_rate'] = '{} Mb/s'.format(round(rate_mb, 1))
    relevant_data['size'] = '{} MB'.format(round(size_mb, 1))

    return relevant_data


def get_json(video_file):
    r"""Execute ffprobe under subprocess to acquire json-formatted metadata

    Parameters
    ----------
    video_file: str
        Path name to a video file in the form of a str object. Passed to
        `ffprobe`

    Returns
    -------
    _json:  str
         Bulk/raw metadata of input video file as a string in JSON format
    """

    # ffprobe incantation to get metadata how we want it
    raw = subprocess.run([
        'ffprobe', '-hide_banner', '-v', 'panic', '-print_format', 'json',
        '-show_format', '-show_streams', '-select_streams', 'v:0',
        '{}'.format(video_file)
    ],
                         stdout=subprocess.PIPE)
    _json = json.loads(raw.stdout)

    return _json

    # ffprobe incantation for posterity:
    # ffprobe -hide_banner -print_format json -show_streams -select_streams v
    # samples/shotgun.mkv


def make_cmd(video_in, video_out, preset, start=None, stop=None):
    """Builds a HandBrakeCLI command from supplied arguments

    Parameters
    ----------
    input_path: Path or str
         pathname of the input video file to be encoded
    output_path: str
         path of the output file to be created by encoding
    preset: str
         path of the preset file to be used for encoding
    start: int
         the start (in seconds) from which to output the encoding
    stop: int
         the end (in seconds) from which to no longer output the encoding

    Returns
    -------
    cmd: str
         Fully qualified handbrake command, passable to subprocess
    """

    # Presets are being stored in conf dir, which needs to be stripped, along
    # with json extension
    preset_name = preset.split('/')[1].strip('.json')
    cmd = 'nice -n 10 HandBrakeCLI '
    _in = f'-i {video_in} '
    _out = f'-o {video_out}'
    _preset = f'--preset-import-file {preset} -Z {preset_name} '
    _start = ''
    _stop = ''
    if start != None:
        _start = f'--start-at seconds:{start} '
    if stop != None:
        _stop = f'--stop-at seconds:{stop} '
    if (_start or _stop):
        cmd = cmd + _preset + _in + _start + _stop + _out
    else:
        cmd = cmd + _preset + _in + _out
    # Subprocess likes each bit split into a separate string
    return cmd.split()


def find_vfiles(input_path):
    r"""Find video files recursively, or parse individually supplied file

    Parameters
    ----------
    input_path: Path
        pathlib.Path object to recursively parse for video files. If a lone
        file is supplied, it is parsed as such

    Returns
    -------
    paths:  list (of tuples)
        list of tuple pairs representing input and output file paths
    """
    paths = []

    # If we encounter merely one file, parse it
    if input_path.is_file():
        # Set the output path to be the same as the input, except with mkv
        # extension
        output_path = str(input_path).rsplit('.', 1)[0] + '.mkv'
        in_out = (input_path, output_path)
        paths.append(in_out)
    # If we encounter a directory, parse it recursively (using glob) to find
    # video files
    if input_path.is_dir():
        queue = deque(['mkv', 'mp4', 'mov', 'wmv', 'avi'])
        exts = []
        while queue:
            ext = queue.pop()
            exts.append(ext)
            exts.append(ext.upper())

        cwd = Path(f"{input_path}")
        # Build up the paths list with tuples of (input, output)
        for ext in exts:
            glob = cwd.rglob(f'*{ext}')
            for path in glob:
                # Set the output path to be the same as the input, except with
                # mkv extension
                output_path = str(path).rsplit('.', 1)[0] + '.mkv'
                in_out = (path, output_path)
                paths.append(in_out)

    return paths
