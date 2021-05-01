#!/usr/bin/env python
import json
import subprocess


def get_info(video_file):
    r"""Print relevant metadata from supplied video file

    Parameters
    ----------
    video_file: str
        Path name to a video file in the form of a str object. Passed to
        `ffparse`

    Returns
    -------
    Prints to STDOUT
    """
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


def make_cmd(video_in, video_out, start=0, stop=0):
    cmd = ''
    _in = '-i {} '.format(video_in)
    _out = '-o {}'.format(video_out)
    _start = ''
    _stop = ''
    if start:
        _start = '--start-at seconds:{} '.format(start)
    if stop:
        _stop = '--start-at seconds:{} '.format(stop)
    if (_start or _stop):
        cmd = _in + _start + _stop + _out
    else:
        cmd = _in + _out
    return cmd
