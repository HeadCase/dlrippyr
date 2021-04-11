#!/usr/bin/env python
"""
File: main.py
Author: G. Headley
Email: gheadley27@gmail.com
Github: https://github.com/headcase
Description: A CLI utility for encoding video files
"""
import click


@click.command()
@click.argument('name')
def cli(name):
    """
    A tool for video encoding using HandBrakeCLI. Accepts an input file to be
    reencoded
    """
    click.echo('Hello, {}!'.format(name))
