#!/usr/bin/env python
import json
import subprocess
from collections import deque
from pathlib import Path

import snoop
from loguru import logger


# @snoop
# @logger.catch
def run_dry(input_path, output_path, preset, start, stop):
    files = find_vfiles(input_path)
    if output_path:
        for item in files:
            (input_file, _) = item
            print(make_cmd(input_file, output_path, preset, start, stop))
    else:
        for item in files:
            (input_file, output_file) = item
            print(make_cmd(input_file, output_file, preset, start, stop))


def get_info(input_path):
    r"""Print relevant metadata from supplied video file(s)

    Parameters
    ----------
    input_path: str
        Path name to a single video file in the form of a str object.
        Alternatively, directory which is parsed recursively to discover video
        files. Video file(s) are passed to `ffparse`

    Returns
    -------
    Prints to STDOUT
    """
    if input_path.is_dir():
        files = find_vfiles(input_path)
        for item in files:
            (file, _) = item
            print(f'Metadata for {file}')
            print_meta(file)
            print()  # Finish with a carriage return
    else:
        print(f'Metadata for {input_path}')
        print_meta(input_path)
        print()  # Finish with a carriage return


def print_meta(video_file):
    """foo!"""
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

    metadata = get_json(video_file)

    for k, v in relevant_tags.items():
        if v == 'streams':
            relevant_data[k] = metadata[v][0][k]
        else:
            relevant_data[k] = metadata[v][k]
    rate_mb = (int(relevant_data['bit_rate']) / 1000**2)
    size_mb = int(relevant_data['size']) / 1024**2
    relevant_data['bit_rate'] = '{} Mb/s'.format(round(rate_mb, 1))
    relevant_data['size'] = '{} MB'.format(round(size_mb, 1))

    for k, v in relevant_data.items():
        print('{:>18}: {}'.format(k, v))


def get_json(video_file):
    r"""Acquire metadata from a video file

    Parameters
    ----------
    video_file: str
        Path name to a video file in the form of a str object. Passed to
        `ffparse`

    Returns
    -------
    _json:  str
         Metadata of input video file as a string in JSON format
    """
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
    """foo!"""
    preset_name = preset.strip('.json')
    cmd = 'HandBrakeCLI '
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
    return cmd


def find_vfiles(input_path):
    r"""Acquire list of all video files recursively from supplied dir

    Parameters
    ----------
    input_path: a pathlib.Path object to recursively parse for video files. If
    a lone file is supplied, it is simply returned.

    Returns
    -------
    list: list of file paths
    """
    paths = []

    if input_path.is_file():
        output_path = str(input_path).rsplit('.', 1)[0] + '.mkv'
        in_out = (input_path, output_path)
        paths.append(in_out)
    if input_path.is_dir():
        queue = deque(['mkv', 'mp4', 'mov', 'wmv', 'avi'])
        exts = []
        while queue:
            ext = queue.pop()
            exts.append(ext)
            exts.append(ext.upper())

        cwd = Path(f"{input_path}")
        for ext in exts:
            glob = cwd.rglob(f'*{ext}')
            for path in glob:
                output_path = str(path).rsplit('.', 1)[0] + '.mkv'
                in_out = (path, output_path)
                paths.append(in_out)

    return paths
