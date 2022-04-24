#!/usr/bin/env python
import subprocess
from pathlib import Path
from typing import List

# Pathlib recursive globbing cannot be coerced into case-insensitive search
EXTS = ['mkv', 'mp4', 'mov', 'wmv', 'avi', 'MKV', 'MP4', 'MOV', 'WMV', 'AVI']


def find_vfiles(arg: Path) -> list:
    """Find video files recursively within the supplied path argument """
    vfiles = []

    if arg.is_file():
        vfiles.append(arg)
    elif arg.is_dir():
        for ext in EXTS:
            globgen = arg.rglob(f'*{ext}')
            for f in globgen:
                vfiles.append(f)

    return vfiles


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
