#!/usr/bin/env python
"""
File: main.py
Author: G. Headley
Email: gheadley27@gmail.com
Github: https://github.com/headcase
Description: A CLI utility for encoding video files
"""

import re
from pathlib import Path
from subprocess import PIPE, Popen

import click

from tools import find_vfiles, get_info, make_cmd

DEFAULT_PRESET = 'x265-1080p-mkv.json'


@click.command()
@click.argument('input-file', type=click.Path(exists=True))
@click.version_option()
@click.option('-o',
              '--output-file',
              default='',
              help='Output file/path, defaults to source name/path')
@click.option('-i',
              '--info',
              is_flag=True,
              default=False,
              help='Query supplied file for metadata')
@click.option('-s',
              '--sample',
              is_flag=True,
              default=False,
              help='Trigger encoding of just first 20 seconds of input file')
@click.option('-d',
              '--dry-run',
              is_flag=True,
              default=False,
              help='Print to screen command which would have been run')
@click.option('-p',
              '--preset',
              default=DEFAULT_PRESET,
              help='Preset file for encoding (JSON format)')
@click.option('--start',
              'start',
              default=None,
              help='Time at which to start encoding, default None')
@click.option('--stop',
              'stop',
              default=None,
              help='Time at which to stop encoding, default None')
def cli(input_file, output_file, start, stop, info, sample, preset, dry_run):
    """
    A tool for encoding AVC (H264) video files to the more space-efficient
    HEVC (H265) codec using HandBrakeCLI. Accepts a single input video file or
    a directory or tree
    """
    input_path = Path(input_file)

    if not output_file:
        # If no input is provided, use root of input file with mkv extension
        output_file = input_file.rsplit('.', 1)[0] + '.mkv'
    if info:
        if input_path.is_dir():
            files = find_vfiles(input_file)
            for file in files:
                click.echo(f"Here is the info for {file}:")
                get_info(file)
                click.echo('')
        else:
            click.echo(f"Here is the info for {input_path}:")
            get_info(input_file)
    elif dry_run:
        if input_path.is_dir():
            files = find_vfiles(input_file)
            for file in files:
                if sample:
                    start = 0
                    stop = 20
                cmd = make_cmd(file, output_file, preset, start, stop)
                click.echo(f'Your handbrake dry run is:\n{cmd}')
                click.echo('')
        else:
            if sample:
                start = 0
                stop = 20
            cmd = make_cmd(input_file, output_file, preset, start, stop)
            click.echo('Your handbrake dry run is:\n{}'.format(cmd))
    else:
        if input_path.is_dir():
            print('''
Directory support coming soon!
Use --dry-run flag to see files found for encoding
            ''')
        else:
            if sample:
                start = 0
                stop = 20
            cmd = make_cmd(input_file, output_file, preset, start,
                           stop).split()
            process = Popen(cmd)
            while True:
                sout = process.communicate()[0]
                if process.poll() is not None:
                    break
                if sout:
                    print(sout)


# ffprobe can be used to acquire video file metadata. The following
# incantation returns JSON formatted metadata for the video stream of a given
# file
# ffprobe -hide_banner -print_format json -show_streams -select_streams v samples/shotgun.mkv
