#!/usr/bin/env python
"""
File: main.py
Author: G. Headley
Email: gheadley27@gmail.com
Github: https://github.com/headcase
Description: A CLI utility for encoding video files
"""

import click

from dlrippyr.classes import DryRunJob, HandBrakeJob, Metadata, SampleJob
from dlrippyr.utils import find_vfiles

DEFAULT_PRESET = 'conf/x265-1080p-mkv.json'


@click.command()
@click.version_option()
@click.argument('srcs', nargs=-1, type=click.Path())
@click.option('-o',
              '--output',
              is_flag=True,
              default=False,
              help='Optional flag indicating you want to name the output file.'
              ' This *must* be the final argument of the command string.')
@click.option('-s',
              '--sample',
              nargs=2,
              type=int,
              default=(10, 20),
              help='Convert only a sample, between the two supplied timecodes,'
              ' which are given in total seconds')
@click.option('-d',
              '--dry-run',
              is_flag=True,
              default=False,
              help='Execute a dry run of the supplied arguments. A dry run'
              ' prints to screen what would have been run otherwise')
@click.option('-p',
              '--preset',
              default=DEFAULT_PRESET,
              help='Conversion preset as created using the HandBrake GUI.'
              'JSON format.')
@click.option('-f',
              '--force',
              is_flag=True,
              default=False,
              help='Optional flag to force (re)encoding of an HEVC file')
def convert(srcs, output, preset, force, dry_run, sample):
    """
    A tool for encoding AVC (H264) video files to the more space-efficient
    HEVC (H265) codec using HandBrakeCLI. Accepts any number (or mix) of video
    files and/or directories to parse. Directories are searched recursively
    for video files, which are then processed.
    """
    v_files = set()
    skips = list()
    dst = None
    start_tm, end_tm = sample
    srcs = list(srcs)
    # If the user has chosen to specify an output, it must be the last argument
    # at command-line
    # TODO: Enforce output file to be last in command string?
    if output:
        dst = srcs.pop(-1)

    for src in srcs:
        v_files = v_files.union(find_vfiles(src))

    for file in v_files:
        meta = Metadata(file)
        if meta.codec_name == 'hevc' and not force:
            skips.append(file)
        elif dry_run:
            run = DryRunJob(file, preset=preset, output=dst)
            click.echo(run)
        elif sample:
            job = SampleJob(file,
                            preset=preset,
                            output=dst,
                            start_tm=start_tm,
                            end_tm=end_tm)
            job.run()
        else:
            job = HandBrakeJob(file, preset=preset, output=dst)
            job.run()
            

    if skips:
        click.echo('The following files were skipped as they are already'
                   ' encoded in HEVC:')
        for file in skips:
            click.echo(f'     {file}')
        click.echo('You can force their encoding with -f/--force')
