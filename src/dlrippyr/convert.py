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

from dlrippyr.classes import DryRunJob, HandBrakeJob, Metadata, SampleJob
from dlrippyr.utils import find_vfiles

# TODO: Break these out into a config file
DEFAULT_PRESET = 'conf/x265-1080p-mkv.json'
EXTS = ['mkv', 'mp4', 'mov', 'wmv', 'avi']


class OutputOptionError(Exception):
    pass


class InputError(Exception):
    pass


class SourceFileNotFoundError(Exception):
    pass


class IncompatibleOptionsError(Exception):
    pass


# TODO: sample default does not work as intended
@click.command()
@click.version_option()
@click.argument('srcs', nargs=-1, type=click.Path())
@click.option(
    '-o',
    '--output',
    is_flag=True,
    default=False,
    help='Optional flag indicating you want to name the output file. '
    'This option is only valid when used with a single input file and '
    'the value *must* be the final argument of the command string. '
    'Default: False')
@click.option('-s',
              '--sample',
              nargs=2,
              default=(10, 20),
              show_default=True,
              help='Convert only a sample, between the two supplied timecodes,'
              ' which are given as a space separated pair in total seconds.')
@click.option('-d',
              '--dry-run',
              is_flag=True,
              default=False,
              help='Execute a dry run of the supplied arguments. A dry run'
              ' prints to screen what would have been run otherwise')
@click.option('-p',
              '--preset',
              default=DEFAULT_PRESET,
              show_default=True,
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
    #############
    # Constants #
    #############

    job_list = []
    flist = set()
    skips = list()
    out = None
    start_tm, end_tm = sample
    srcs = list(srcs)

    ######################
    # Exception handling #
    ######################

    # TODO: Enforce output file to be last in command string?
    if not srcs:
        raise InputError('You must supply at least one source file or '
                         'directory, not none')

    if output:
        if len(srcs) > 1 or Path(srcs[0]).is_dir():
            raise OutputOptionError(
                'The output option (-o) is only valid with a single source '
                'file, not multiple files nor directories')
        out = srcs.pop(-1)

    if dry_run and sample:
        raise IncompatibleOptionsError(
            'Dry run (-d) and sample (-s) flags are incompatible')

    #############
    # Main loop #
    #############

    # Support for user supplying a mixture of one or many files and/or
    # directories
    for src in srcs:
        flist = flist.union(find_vfiles(src))

    for file in flist:
        meta = Metadata(file)
        if meta.codec_name == 'hevc' and not force:
            skips.append(file)
        elif dry_run:
            job_list.append(DryRunJob(file, preset=preset, output=out))
        elif sample:
            job_list.append(
                SampleJob(file,
                          preset=preset,
                          output=out,
                          start_tm=start_tm,
                          end_tm=end_tm))
        else:
            job_list.append(HandBrakeJob(file, preset=preset, output=out))

    if not job_list:
        raise SourceFileNotFoundError('No processable media files were found.')

    for job in job_list:
        job.run_handbrake()

    if skips:
        click.echo('The following files were skipped as they are already'
                   ' encoded in HEVC:')
        for file in skips:
            click.echo(f'     {file}')
        click.echo('You can force their encoding with -f/--force')
