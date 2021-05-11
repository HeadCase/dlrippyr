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

from tools import get_info, make_handbrake, run_dry

DEFAULT_PRESET = 'conf/x265-1080p-mkv.json'


@click.command()
@click.argument('input-file', type=click.Path(exists=True))
@click.version_option()
@click.option('-o',
              '--output-path',
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
def cli(input_file, output_path, start, stop, info, sample, preset, dry_run):
    """
    A tool for encoding AVC (H264) video files to the more space-efficient
    HEVC (H265) codec using HandBrakeCLI. Accepts a single input video file or
    a directory or tree
    """
    input_path = Path(input_file)
    if input_path.is_dir():
        if output_path:
            raise RuntimeError('Supplying an output file is not supported '
                               'for directories')
        else:
            if info:
                get_info(input_path)
            elif dry_run:
                run_dry(input_path, output_path, preset, start, stop)
            elif sample:
                make_handbrake(input_path,
                               output_path,
                               preset,
                               start=0,
                               stop=20)
            else:
                make_handbrake(input_path, output_path, preset, start, stop)
    else:
        if info:
            get_info(input_path)
        elif dry_run:
            run_dry(input_path, output_path, preset, start, stop)
        elif sample:
            make_handbrake(input_path, output_path, preset, start=0, stop=20)
        else:
            make_handbrake(input_path, output_path, preset, start, stop)
