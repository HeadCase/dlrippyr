#!/usr/bin/env python
import json
import subprocess
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional

from loguru import logger

from dlrippyr import utils

logger.add(sys.stderr,
           format="{time} {level} {message}",
           filter="my_module",
           level="INFO")


class Metadata:
    """doc"""
    path: Path
    format_name: str
    codec_name: str
    profile: str
    avg_frame_rate: str
    height: str
    width: str
    bit_rate: int
    size: int

    def __init__(self, path: Path) -> None:
        # Track the path of the source file
        self.path = path

        # call initialisation methods to populate attributes from json
        _json = self.get_json()
        self.parse_json(_json)
        logger.info(f'{self.__repr__}')

    def __repr__(self) -> str:
        return (f'{self.__class__.__name__}("{self.path}")')

    def __str__(self) -> str:
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

    def get_json(self) -> Dict:
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

    def parse_json(self, _json: Dict) -> None:

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


class BasicJob(ABC):
    input: Path
    output: Optional[Path]
    preset: str
    cmd: List[str]

    def __init__(self, input, output=None) -> None:
        self.input = input
        self.output = output

    @abstractmethod
    def make_cmd(self):
        pass


class DryRunJob(BasicJob):
    def __init__(self,
                 input: Path,
                 preset: str = 'x265',
                 output: Optional[Path] = None) -> None:
        self.input = input
        if not output:
            self.output = utils.output_name_from_input(self.input)
        else:
            self.output = output
        self.preset = preset
        self.cmd = self.make_cmd()

    def __str__(self) -> str:
        return ' '.join(self.cmd)

    def make_cmd(self) -> List[str]:
        """Makes a fully qualified HandBrakeCLI (with nicing) as required to be
        run by subprocess module"""

        # Presets are being stored in conf dir, which needs to be stripped, along
        # with json extension
        preset_name = self.preset.split('/')[1].strip('.json')
        cmd = 'nice -n 10 HandBrakeCLI '.split()
        _preset = f'--preset-import-file {self.preset} -Z {preset_name} '.split(
        )
        _in = ['-i', str(self.input)]
        _out = ['-o', str(self.output)]
        cmd.extend(_preset + _in + _out)
        return cmd


class SampleJob(BasicJob):
    start_tm: int
    end_tm: int

    def __init__(self,
                 input: Path,
                 preset: str = 'x265',
                 output: Optional[Path] = None,
                 start_tm: int = 10,
                 end_tm: int = 20) -> None:
        self.input = input
        if not output:
            self.output = utils.output_name_from_input(self.input)
        else:
            self.output = output
        self.preset = preset
        self.start_tm = start_tm
        self.end_tm = end_tm
        self.cmd = self.make_cmd()

    def __str__(self) -> str:
        return ' '.join(self.cmd)

    def make_cmd(self) -> List[str]:
        """SampleJob convert """

        # Presets are being stored in conf dir, which needs to be stripped, along
        # with json extension
        preset_name = self.preset.split('/')[1].strip('.json')
        cmd = 'nice -n 10 HandBrakeCLI '.split()
        _preset = f'--preset-import-file {self.preset} -Z {preset_name} '.split(
        )
        start_tm = f'--start-at seconds:{self.start_tm} '.split()
        end_tm = f'--stop-at seconds:{self.end_tm} '.split()
        _in = ['-i', str(self.input)]
        _out = ['-o', str(self.output)]
        cmd.extend(_preset + start_tm + end_tm + _in + _out)
        return cmd

    def run(self) -> None:
        utils.run_handbrake(self.cmd)


class HandBrakeJob(BasicJob):
    def __init__(self,
                 input: Path,
                 preset: str = 'x265',
                 output: Optional[Path] = None):
        self.input = input
        if not output:
            self.output = utils.output_name_from_input(self.input)
        else:
            self.output = output
        self.preset = preset
        self.cmd = self.make_cmd()

    def __str__(self) -> str:
        return ' '.join(self.cmd)

    def make_cmd(self) -> List[str]:
        """SampleJob convert """

        # Presets are being stored in conf dir, which needs to be stripped,
        # along with json extension
        preset_name = self.preset.split('/')[1].strip('.json')
        cmd = 'nice -n 10 HandBrakeCLI '.split()
        _preset = f'--preset-import-file {self.preset} -Z {preset_name} '.split(
        )
        _in = ['-i', str(self.input)]
        _out = ['-o', str(self.output)]
        cmd.extend(_preset + _in + _out)
        return cmd

    def run(self) -> None:
        utils.run_handbrake(self.cmd)
