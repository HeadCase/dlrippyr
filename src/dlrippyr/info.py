#!/usr/bin/env python

from pathlib import Path

import click

from dlrippyr.classes import Metadata
from dlrippyr.utils import find_vfiles


class ArgumentError(Exception):
    """Exception for erroneous command-line argument(s)"""


@click.command()
@click.argument('args', nargs=-1)
def info(args, print=True):
    # set() ensures we don't pickup unforeseen duplicates

    if not args:
        raise ArgumentError(
            'At least one video file must be supplied as argument')
    # TODO: Add rich comparison to Metadata to allow sorting
    f_list = {Metadata(f) for arg in args for f in find_vfiles(Path(arg))}

    # for item in sorted(f_list):
    if print:
        for item in f_list:
            click.echo(item)

    return f_list
