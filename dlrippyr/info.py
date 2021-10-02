#!/usr/bin/env python

import click

from dlrippyr.classes import Metadata
from dlrippyr.utils import find_vfiles


@click.command()
@click.argument('args', nargs=-1)
def info(args, print=True):
    # set() ensures we don't pickup unforeseen duplicates
    f_list = set()
    objs = []

    # click args come in as a tuple, even singletons
    for path in args:
        f_list = find_vfiles(path)

    for item in sorted(f_list):
        meta = Metadata(item)
        objs.append(meta)
        if print:
            click.echo(meta)

    return objs
