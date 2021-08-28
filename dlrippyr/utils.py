#!/usr/bin/env python
import json
import subprocess
from collections import deque
from pathlib import Path

import snoop

EXTS = ['mkv', 'mp4', 'mov', 'wmv', 'avi']


# TODO: Abstract this function out into a class
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
    cmd = 'nice -n 10 HandBrakeCLI '.split()
    # Calling string on a pathlib.Path sorts of things like spaces and OS
    # issues
    _in = ['-i', str(video_in)]
    _out = ['-o', str(video_out)]
    _preset = f'--preset-import-file {preset} -Z {preset_name} '.split()
    _start = ''
    _stop = ''
    if start is not None:
        _start = f'--start-at seconds:{start} '.split()
    if stop is not None:
        _stop = f'--stop-at seconds:{stop} '.split()
    if (_start or _stop):
        cmd.extend(_preset)
        cmd.extend(_in)
        cmd.extend(_start)
        cmd.extend(_stop)
        cmd.extend(_out)
    else:
        cmd.extend(_preset)
        cmd.extend(_in)
        cmd.extend(_out)
    # Subprocess likes each bit split into a separate string
    return cmd


def make_path(arg: str) -> Path:
    """ Convert user input argument in the form of a string to a pathlib.Path
    object
    """

    vpath = Path(arg).resolve()

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
