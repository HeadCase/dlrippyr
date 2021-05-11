#!/usr/bin/env python
"""
File: features.py
Author: yourname
Email: yourname@email.com
Github: https://github.com/yourname
Description: Features implemented in command-line interface
"""

import subprocess

from dlrippyr.utils import find_vfiles, get_json, make_cmd, print_meta


def make_handbrake(input_path, output_path, preset, start, stop):
    files = find_vfiles(input_path)
    if output_path:
        for item in files:
            (input_file, _) = item
            cmd = make_cmd(input_file, output_path, preset, start,
                           stop).split()
            process = subprocess.Popen(cmd)
            while True:
                sout = process.communicate()[0]
                if process.poll() is not None:
                    break
                if sout:
                    print(sout)
    else:
        for item in files:
            (input_file, output_file) = item
            cmd = make_cmd(input_file, output_file, preset, start,
                           stop).split()
            process = subprocess.Popen(cmd)
            while True:
                sout = process.communicate()[0]
                if process.poll() is not None:
                    break
                if sout:
                    print(sout)


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
