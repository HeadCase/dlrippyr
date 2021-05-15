#!/usr/bin/env python
from pathlib import Path

from dlrippyr import features, utils

TEST_FILE = Path('samples/Wentworth.mov')
TEST_OUT = Path('samples/Wentworth.mp4')
PRESET = 'conf/x265-1080p-mkv.json'
CMD_DICT = {
    'input': TEST_FILE,
    'output': '',
    'start': None,
    'stop': None,
    'info': False,
    'sample': False,
    'preset': PRESET,
    'dry run': False,
    'test': True
}


def test_file_dry_run():
    """Test for dry run flag on a single video file"""
    CMD_DICT['dry run'] = True
    expect_no_out = [[
        'HandBrakeCLI', '--preset-import-file', 'conf/x265-1080p-mkv.json',
        '-Z', 'x265-1080p-mkv', '-i', 'samples/Wentworth.mov', '-o',
        'samples/Wentworth.mkv'
    ]]

    expect_out = [[
        'HandBrakeCLI', '--preset-import-file', 'conf/x265-1080p-mkv.json',
        '-Z', 'x265-1080p-mkv', '-i', 'samples/Wentworth.mov', '-o',
        'samples/Wentworth.mp4'
    ]]

    dry_no_out = features.parse_user_input(CMD_DICT)
    CMD_DICT['output'] = TEST_OUT
    dry_out = features.parse_user_input(CMD_DICT)

    assert dry_no_out == expect_no_out
    assert dry_out == expect_out

    CMD_DICT['dry run'] = False


def test_file_sample():
    """Test for sample flag on a single video file"""
    CMD_DICT['sample'] = True
    expect = [[
        'HandBrakeCLI', '--preset-import-file', 'conf/x265-1080p-mkv.json',
        '-Z', 'x265-1080p-mkv', '-i', 'samples/Wentworth.mov', '--start-at',
        'seconds:0', '--stop-at', 'seconds:20', '-o', 'samples/Wentworth.mp4'
    ]]

    assert features.parse_user_input(CMD_DICT) == expect

    CMD_DICT['sample'] = False


def test_file_get_info():
    """Test for get info flag on single video file"""
    CMD_DICT['info'] = True
    expect = [
        'Metadata for samples/Wentworth.mov',
        '       format_name: mov,mp4,m4a,3gp,3g2,mj2',
        '        codec_name: hevc', '           profile: Main',
        '    avg_frame_rate: 24/1', '            height: 2160',
        '             width: 3840', '          bit_rate: 28.5 Mb/s',
        '              size: 349.0 MB', ''
    ]

    assert features.parse_user_input(CMD_DICT) == expect

    CMD_DICT['info'] = False
