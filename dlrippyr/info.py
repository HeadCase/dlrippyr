#!/usr/bin/env python

import click

from dlrippyr.classes import Metadata
from dlrippyr.utils import find_vfiles


@click.command()
@click.argument('args', nargs=-1)
def info(args, print=True):
    # set() ensures we don't pickup unforeseen duplicates
    flist = set()
    objs = []

    # Arguments come in from command
    # line as a tuple, even singletons
    for val in args:
        flist = find_vfiles(val)

    for item in sorted(flist):
        meta = Metadata(item)
        objs.append(meta)
        if print:
            click.echo(meta)

    return objs
