#!/usr/bin/env python
import subprocess
from pathlib import Path
from typing import List

EXTS = ['mkv', 'mp4', 'mov', 'wmv', 'avi']


def make_path(arg: str) -> Path:
    """ Convert user input argument in the form of a string to a pathlib.Path
    object
    """
    vpath = Path(arg)  #.resolve()

    return vpath


def find_vfiles(arg: str) -> set:
    """Find video files recursively within the supplied path argument """
    vfiles = set()
    vpath = make_path(arg)

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


# TODO: This needs to be *much* smarter
def output_name_from_input(input: Path) -> Path:
    """Produce a default output name given a supplied input video file name """

    return Path(f"{input.stem}_x265.mp4")


def run_handbrake(cmd: List[str]) -> None:
    process = subprocess.Popen(cmd)
    # Regurgitate HandBrakeCLI back to stdout after it is gobbled up by
    # subprocess
    while True:
        sout = process.communicate()[0]
        if process.poll() is not None:
            break
        if sout:
            print(sout)
