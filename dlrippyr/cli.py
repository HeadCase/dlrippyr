#!/usr/bin/env python
"""
File: main.py
Author: G. Headley
Email: gheadley27@gmail.com
Github: https://github.com/headcase
Description: A CLI utility for encoding video files
"""

import click

from dlrippyr import info

# from dlrippyr import convert, info, sample


@click.group()
@click.version_option()
def cli():
    pass


# cli.add_command(convert)
# cli.add_command(sample)
cli.add_command(info)
