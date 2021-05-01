#!/usr/bin/env python
"""
File: main.py
Author: G. Headley
Email: gheadley27@gmail.com
Github: https://github.com/headcase
Description: A CLI utility for encoding video files
"""

from pathlib import Path

import click

from tools import find_vfiles, get_info, make_cmd


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', 'output_file', default='test.mkv')
@click.option('-i', 'info', is_flag=True)
@click.version_option()
@click.option('--start', 'start', default=0)
@click.option('--stop', 'stop', default=0)
def cli(input_file, output_file, start, stop, info):
    """
    A tool for video encoding using HandBrakeCLI. Accepts an input file to be
    reencoded
    """
    input_path = Path(input_file)
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
    else:
        if input_path.is_dir():
            files = find_vfiles(input_file)
            for file in files:
                cmd = make_cmd(file, output_file, start, stop)
                click.echo(f'Your handbrake dry run is:\nhandbrake {cmd}')
                click.echo('')
        else:
            cmd = make_cmd(input_file, output_file, start, stop)
            click.echo('Your handbrake dry run is:\nhandbrake {}'.format(cmd))


# ffprobe can be used to acquire video file metadata. The following
# incantation returns JSON formatted metadata for the video stream of a given
# file
# ffprobe -hide_banner -print_format json -show_streams -select_streams v samples/shotgun.mkv
