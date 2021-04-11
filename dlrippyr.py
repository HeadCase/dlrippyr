#!/usr/bin/env python
"""
File: main.py
Author: G. Headley
Email: gheadley27@gmail.com
Github: https://github.com/headcase
Description: A CLI utility for encoding video files
"""
import click


def handbrake_cmd(input_file, output_file, start=0, stop=0):
    cmd = ''
    in_ = '-i {} '.format(input_file)
    out_ = '-o {}'.format(output_file)
    start_ = ''
    stop_ = ''
    if start:
        start_ = '--start-at seconds:{} '.format(start)
    if stop:
        stop_ = '--start-at seconds:{} '.format(stop)
    if (start_ or stop_):
        cmd = in_ + start_ + stop_ + out_
    else:
        cmd = in_ + out_
    return cmd


@click.command()
@click.argument('input_file')
@click.option('-o', 'output_file', default='test.mkv')
@click.option('--start', 'start', default=0)
@click.option('--stop', 'stop', default=0)
def cli(input_file, output_file, start, stop):
    """
    A tool for video encoding using HandBrakeCLI. Accepts an input file to be
    reencoded
    """
    cmd = handbrake_cmd(input_file, output_file, start, stop)
    click.echo('Your handbrake dry run is:\nhandbrake {}'.format(cmd))
