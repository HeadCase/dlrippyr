#!/usr/bin/env python

import click
import snoop

from dlrippyr.file import find_vfiles, print_metadata, probe_meta


@click.command()
@click.argument('args', nargs=-1)
def info(args):
    info_list = list()

    for val in args:
        flist = find_vfiles(val)
        for path in flist:
            info_list.append(path)

    for item in sorted(info_list):
        metadata = probe_meta(item)
        print_metadata(metadata)


# def get_info(input_path):
#     r"""Acquire metadata, using ffprobe, for the supplied file/dir

#     Parameters
#     ----------
#     input_path: str
#         Path name to a single video file in the form of a str object.
#         Alternatively, directory which is parsed recursively to discover video
#         files. Video file(s) are passed to `ffparse`

#     Returns
#     -------
#     printout: list
#         A printout in the form of a list, which each string element
#         representing a line to be printed
#     """
#     printout = []
#     if input_path.is_dir():
#         files = find_vfiles(input_path)
#         for item in files:
#             (file, _) = item
#             printout.append(f'Metadata for {file}')
#             metadata = probe_meta(file)  # returns dictionary
#             for k, v in metadata.items():
#                 printout.append('{:>18}: {}'.format(k, v))
#             # Tack on a carriage return
#             printout.append('')

#     else:
#         printout.append(f'Metadata for {input_path}')
#         metadata = probe_meta(input_path)
#         for k, v in metadata.items():
#             printout.append('{:>18}: {}'.format(k, v))
#         # Tack on a carriage return
#         printout.append('')

#     return printout
