#!/usr/bin/env python

import click
import snoop

from dlrippyr.file import Metadata, find_vfiles


@click.command()
@click.argument('args', nargs=-1)
def info(args, print=True):
    # ensures we don't pickup unforeseen duplicates
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
