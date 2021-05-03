#!/usr/bin/env python
"""
File: main.py
Author: G. Headley
Email: gheadley27@gmail.com
Github: https://github.com/headcase
Description: A CLI utility for encoding video files
"""

import re
import subprocess
from pathlib import Path

import click

from tools import find_vfiles, get_info, make_cmd

DEFAULT_PRESET = 'x265-1080p-mkv.json'


@click.command()
@click.argument('input-file', type=click.Path(exists=True))
@click.option('-o', '--output-file', default='')
@click.option('-i', '--info', is_flag=True, default=False)
@click.option('-s', '--sample', is_flag=True, default=False)
@click.option('-d', '--dry-run', is_flag=True, default=False)
@click.option('-p', '--preset', default=DEFAULT_PRESET)
@click.version_option()
@click.option('--start', 'start', default=None)
@click.option('--stop', 'stop', default=None)
def cli(input_file, output_file, start, stop, info, sample, preset, dry_run):
    """
    A tool for video encoding using HandBrakeCLI. Accepts an input file to be
    reencoded
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
        if sample:
            start = 0
            stop = 20
        cmd = make_cmd(input_file, output_file, preset, start, stop).split()
        process = subprocess.Popen(cmd,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        print(process.communicate())
        # process = subprocess.Popen(, stdout=subprocess.PIPE,
        #                            stderr=subprocess.STDOUT)
        # print(process)
        # out, err = process.communicate()
        # print(out, err)
        # while True:
        #     out_out = process.stdout.readline()
        #     # out_err = process.stderr.readline()
        #     if out_out == '' and process.poll() is not None:
        #         break
        #     # if out_err == '' and process.poll() is not None:
        #         # break
        #     if out_out:
        #         print(out_out.strip(), flush=True)
        #     # if out_err:
        #         # print(out_err.strip(), flush=True)

        # process.poll()
        # process = subprocess.Popen(cmd,
        #                            shell=True,
        #                            stderr=subprocess.PIPE,
        #                            stdout=subprocess.PIPE)
        # for line in iter(process.stdout.readline, b''):

        #     # regex match for % complete and ETA
        #     matches = re.match(r'.*(\d+\.\d+)\s%.*ETA\s(\d+)h(\d+)m(\d+)s',
        #                        line.decode('utf-8'))

        #     if matches:
        #         print(matches.group())

        #     print(line)

        # process.stderr.close()
        # process.stdout.close()
        # process.wait()
        # result = subprocess.run(cmd, shell=True, capture_output=True)
        # print(result)


# ffprobe can be used to acquire video file metadata. The following
# incantation returns JSON formatted metadata for the video stream of a given
# file
# ffprobe -hide_banner -print_format json -show_streams -select_streams v samples/shotgun.mkv
