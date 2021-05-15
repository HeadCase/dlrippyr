#!/usr/bin/env python
"""
File: features.py
Author: yourname
Email: yourname@email.com
Github: https://github.com/yourname
Description: Features implemented in command-line interface
"""

import subprocess

import snoop
from loguru import logger

from dlrippyr.utils import find_vfiles, make_cmd, probe_meta


def parse_user_input(user_input: dict):
    """Parses arguments and options supplied by user at command line

    Parameters
    ----------
    user_input: dict
         User supplied options and arguments which have been bundled in a
         dictionary. Dict keys like 'info' or 'sample' drive what to execute;
         others like 'start' or 'preset' provide values to pass to follow-up
         functions

    Returns
    -------
    None.
    """
    info = user_input['info']
    dry_run = user_input['dry run']
    sample = user_input['sample']
    input_path = user_input['input']
    output_path = user_input['output']
    preset = user_input['preset']
    start = user_input['start']
    stop = user_input['stop']
    if info:
        metadata = get_info(input_path)
        for line in metadata:
            print(line)
    elif dry_run:
        cmd_list = make_handbrake(input_path, output_path, preset, start, stop)
        for cmd in cmd_list:
            print(' '.join(cmd))
    elif sample:
        cmd_list = make_handbrake(input_path,
                                  output_path,
                                  preset,
                                  start=0,
                                  stop=20)
        run_handbrake(cmd_list)
    else:
        cmd_list = make_handbrake(input_path, output_path, preset, start, stop)
        run_handbrake(cmd_list)


def make_handbrake(input_path, output_path, preset, start, stop):
    """Makes a list of strings representing HandBrakeCLI command(s) to run

    Parameters
    ----------
    input_path: Path
         pathlib.Path object specifying the pathname of the input video file
         to be encoded
    output_path: str
         string representing the path of the output file to be created by
         encoding
    preset: str
         string representing the path of the preset file to be used for
         encoding
    start: int
         integer indicating the start (in seconds) from which to output the
         encoding
    stop: int
         integer indicating the end (in seconds) from which to no longer
         output the encoding

    Returns
    -------
    cmd_list: list
         List of handbrake command(s), each element being a string
    """
    # find_vfiles will give us back a list of tuples of (input, output) for
    # supplied file or directory
    files = find_vfiles(input_path)
    cmd_list = []
    if output_path:
        for item in files:
            (input_path, _) = item
            cmd = make_cmd(input_path, output_path, preset, start,
                           stop).split()
            cmd_list.append(cmd)
    else:
        for item in files:
            (input_path, output_path) = item
            cmd = make_cmd(input_path, output_path, preset, start,
                           stop).split()
            cmd_list.append(cmd)
    return cmd_list


def run_handbrake(cmd_list):
    """Parses and executes HandBrakeCLI commands under a system subprocess

    Parameters
    ----------
    cmd_list: list
         List of handbrake command(s), each element being a string

    Returns
    -------
    None.
    """
    for cmd in cmd_list:
        process = subprocess.Popen(cmd)
        # Regurgitate HandBrakeCLI back to stdout after it is gobbled up by
        # subprocess
        while True:
            sout = process.communicate()[0]
            if process.poll() is not None:
                break
            if sout:
                print(sout)


def get_info(input_path):
    r"""Acquire metadata, using ffprobe, for the supplied file/dir

    Parameters
    ----------
    input_path: str
        Path name to a single video file in the form of a str object.
        Alternatively, directory which is parsed recursively to discover video
        files. Video file(s) are passed to `ffparse`

    Returns
    -------
    printout: list
        A printout in the form of a list, which each string element
        representing a line to be printed
    """
    printout = []
    if input_path.is_dir():
        files = find_vfiles(input_path)
        for item in files:
            (file, _) = item
            printout.append(f'Metadata for {file}')
            metadata = probe_meta(file)  # returns dictionary
            for k, v in metadata.items():
                printout.append('{:>18}: {}'.format(k, v))
            # Tack on a carriage return
            printout.append('')

    else:
        printout.append(f'Metadata for {input_path}')
        metadata = probe_meta(input_path)
        for k, v in metadata.items():
            printout.append('{:>18}: {}'.format(k, v))
        # Tack on a carriage return
        printout.append('')

    return printout
