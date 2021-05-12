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
    """bar!"""
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
        cmd_list = run_dry(input_path, output_path, preset, start, stop)
        for cmd in cmd_list:
            print(cmd)
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
    for cmd in cmd_list:
        process = subprocess.Popen(cmd)
        while True:
            sout = process.communicate()[0]
            if process.poll() is not None:
                break
            if sout:
                print(sout)


def run_dry(input_path, output_path, preset, start, stop):
    files = find_vfiles(input_path)
    cmd_list = []
    if output_path:
        for item in files:
            (input_path, _) = item
            cmd = make_cmd(input_path, output_path, preset, start, stop)
            cmd_list.append(cmd)
    else:
        for item in files:
            (input_path, output_path) = item
            cmd = make_cmd(input_path, output_path, preset, start, stop)
            cmd_list.append(cmd)
    return cmd_list


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
