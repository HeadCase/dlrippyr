#!/usr/bin/env python
import json
import subprocess
from pathlib import Path

from dlrippyr import utils

# EXTS = ['mkv', 'mp4', 'mov', 'wmv', 'avi']


class Metadata:
    """doc"""
    def __init__(self, path):
        # Track the path of the source file
        if not isinstance(path, Path):
            self.path = utils.make_path(path)
        else:
            self.path = path

        self.format_name = None
        self.codec_name = None
        self.profile = None
        self.avg_frame_rate = None
        self.height = None
        self.width = None
        self.bit_rate = int()
        self.size = int()

        # call initialisation methods to populate attributes from json
        _json = self.get_json()
        self.parse_json(_json)

    def __repr__(self):
        return (f'{self.__class__.__name__}("{self.path}")')

    def __str__(self):
        f_bit_rate = f'{round(self.bit_rate, 1)} Mb/s'
        f_size = f'{round(self.size, 1)} MB'

        return (f'      File: {self.path}\n'
                f'    Format: {self.format_name:<12}\n'
                f'     Codec: {self.codec_name:<12}\n'
                f'   Profile: {self.profile:<12}\n'
                f'   Average: {self.avg_frame_rate:<12}\n'
                f'    Height: {self.height:<12}\n'
                f'     Width: {self.width:<12}\n'
                f'  Bit Rate: {f_bit_rate:<12}\n'
                f'      Size: {f_size:<12}\n')

    def get_json(self):
        r"""Execute ffprobe under subprocess to acquire json-formatted metadata

        ### Parameters
        1. video_file: str
            - Path name to a video file in the form of a str object. Passed to
              `ffprobe`

        ### Returns
        _json:  str
             Bulk/raw metadata of input video file as a string in JSON format
        """

        # ffprobe incantation to get metadata how we want it
        raw = subprocess.run([
            'ffprobe', '-hide_banner', '-v', 'panic', '-print_format', 'json',
            '-show_format', '-show_streams', '-select_streams', 'v:0',
            f'{self.path}'
        ],
                             stdout=subprocess.PIPE)
        _json = json.loads(raw.stdout)

        return _json

    def parse_json(self, _json):

        relevant_tags = {
            'streams':
            ['codec_name', 'profile', 'avg_frame_rate', 'height', 'width'],
            'format': ['format_name', 'bit_rate', 'size'],
        }

        # Parse the bulk metadata to get the relevant bits we want
        for k, v in relevant_tags.items():
            if k == 'streams':
                for field in v:
                    setattr(self, field, _json[k][0][field])
            else:
                for field in v:
                    if field == 'bit_rate':
                        # Convert the bit rate to Mb/s
                        _json[k][field] = (int(_json[k][field]) / 1000**2)
                    elif field == 'size':
                        # Convert the video file size to MBs
                        _json[k][field] = (int(_json[k][field]) / 1024**2)
                    setattr(self, field, _json[k][field])


# def make_path(arg: str) -> Path:
#     """ Convert user input argument in the form of a string to a pathlib.Path
#     object
#     """

#     vpath = Path(arg).resolve()

#     return vpath

# def find_vfiles(user_arg: str) -> set:
#     """Find video files subject to the supplied path argument

#     ### Paramters
#     1. user_arg: str
#         - A str representing either a file or directory

#     ### Returns
#     - vfiles: set
#         - A set of the absolute paths for all discovered video files
#     """
#     vfiles = set()
#     vpath = make_path(user_arg)

#     if vpath.is_file():
#         vfiles.add(vpath)
#     elif vpath.is_dir():
#         cwd = Path(vpath)
#         glob = list()
#         # Build up the paths list with tuples of (input, output)
#         for ext in EXTS:
#             glob.extend(cwd.rglob(f'*{ext}'))
#             glob.extend(cwd.rglob(f'*{ext.upper()}'))
#             for path in glob:
#                 vfiles.add(path)

#     return vfiles
