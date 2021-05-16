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
import snoop

from dlrippyr.features import parse_user_input
from dlrippyr.utils import find_vfiles, probe_meta

DEFAULT_PRESET = 'conf/x265-1080p-mkv.json'


@click.command()
@click.argument('args', nargs=-1, type=click.Path(exists=True))
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
@click.option('-f',
              '--force',
              is_flag=True,
              default=False,
              help='Force encoding of HEVC input file')
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
# @snoop
def cli(args, output_path, start, stop, info, sample, preset, dry_run, force):
    """
    A tool for encoding AVC (H264) video files to the more space-efficient
    HEVC (H265) codec using HandBrakeCLI. Accepts a single input video file or
    a directory or tree
    """
    # List of skipped files to report back to user at the end
    skips = []

    for input_file in args:
        input_path = Path(input_file)
        # Output does not need to be converted to a Path as it is only ever
        # supplied as a string to HandBrakeCLI

        # Currently bundling command-line opts/args into a dict for parsing.
        # What is the smarter way to do this?
        user_input = {
            'input': input_path,
            'output': output_path,
            'start': start,
            'stop': stop,
            'info': info,
            'sample': sample,
            'preset': preset,
            'dry run': dry_run,
            'test': False
        }
        # User can supply a directory, which we then parse for any video files
        if input_path.is_dir():
            if output_path:
                raise RuntimeError('Supplying an output file is not supported '
                                   'for directories')
            else:
                files = find_vfiles(input_path)
                for (input_file, output_file) in files:
                    # check metadata before processing
                    meta_check = probe_meta(input_file)
                    if (meta_check['codec_name'] == 'hevc') and not force:
                        print('This file is already encoded in HEVC and will'
                              ' be skipped: '
                              f'{input_file}')
                        skips.append(input_file)
                    else:
                        user_input['input'] = input_file
                        user_input['output'] = output_file
                        parse_user_input(user_input)

        # User can supply single video file, which we process directly
        else:
            # Since we already know it is a file and not a dir, we can called
            # find_vfiles and pull the zero index to extract the only tuple
            (input_file, output_file) = find_vfiles(input_path)[0]

            meta_check = probe_meta(input_file)
            if (meta_check['codec_name'] == 'hevc') and not force:
                print('This file is already encoded in HEVC and will be'
                      ' skipped: '
                      f'{input_file}')
                skips.append(input_file)
            # If the user has not supplied an output file, we'll use the
            # automatic one from find_vfiles
            else:
                if not output_path:
                    user_input['output'] = output_file
                user_input['input'] = input_file
                parse_user_input(user_input)
    if skips:
        print('The following files were skipped as they are already encoded'
              ' in HEVC:')
        for file in skips:
            print(file)
        print('You can force their encoding with --force')
