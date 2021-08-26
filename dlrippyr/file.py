#!/usr/bin/env python
import json
import subprocess
from pathlib import Path

import click
import snoop

EXTS = ['mkv', 'mp4', 'mov', 'wmv', 'avi']


# TODO: Abstract into a metadata class
# BUG: get_json expects a string but we want to pass Path(s) to this function
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
    raw_meta = get_json(str(video_file))

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

    ### Parameters
    1. video_file: str
        - Path name to a video file in the form of a str object. Passed to
          `ffprobe`

    ### Returns
    _json:  str
         Bulk/raw metadata of input video file as a string in JSON format
    """

    # ffprobe incantation to get metadata how we want it
    raw = subprocess.run([
        'ffprobe', '-hide_banner', '-v', 'panic', '-print_format', 'json',
        '-show_format', '-show_streams', '-select_streams', 'v:0',
        f'{video_file}'
    ],
                         stdout=subprocess.PIPE)
    _json = json.loads(raw.stdout)

    return _json

    # ffprobe incantation for posterity:
    # ffprobe -hide_banner -print_format json -show_streams -select_streams v
    # samples/shotgun.mkv


def print_metadata(metadata: dict):
    """ Print metadata to stdout


    ### Parameters
    1. metadata: Path
        - Metadata for a recognised video file

    ### Returns
    1. None
        - Printout
    """
    for k, v in metadata.items():
        click.echo(f'{k:>18}: {v}')
    click.echo('')


def make_path(user_arg: str) -> Path:
    """ Convert user input argument in the form of a string to a pathlib.Path
    object
    """

    vpath = Path(user_arg).resolve()

    return vpath


def find_vfiles(user_arg: str) -> set:
    """Find video files subject to the supplied path argument

    ### Paramters
    1. user_arg: str
        - A str representing either a file or directory

    ### Returns 
    - vfiles: set 
        - A set of the absolute paths for all discovered video files
    """
    vfiles = set()
    vpath = make_path(user_arg)

    if vpath.is_file():
        vfiles.add(vpath)
    elif vpath.is_dir():
        cwd = Path(vpath)
        glob = list()
        # Build up the paths list with tuples of (input, output)
        for ext in EXTS:
            glob.extend(cwd.rglob(f'*{ext}'))
            glob.extend(cwd.rglob(f'*{ext.upper()}'))
            for path in glob:
                vfiles.add(path)

    return vfiles
