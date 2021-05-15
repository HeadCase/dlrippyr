#!/usr/bin/env python
from pathlib import Path

from dlrippyr import features, utils

TEST_FILE = Path('samples/Wentworth.mov')
DEFAULT_OUT = 'samples/Wentworth.mkv'
TEST_OUT = Path('samples/Wentworth.mp4')
PRESET = 'conf/x265-1080p-mkv.json'


def test_file_make_hb():
    dry_no_out = features.make_handbrake(TEST_FILE, '', PRESET, None, None)
    dry_out = features.make_handbrake(TEST_FILE, TEST_OUT, PRESET, None, None)

    cmd_no_out = utils.make_cmd(TEST_FILE, DEFAULT_OUT, PRESET, None, None)
    cmd_out = utils.make_cmd(TEST_FILE, TEST_OUT, PRESET, None, None)

    assert dry_no_out == [cmd_no_out]
    assert dry_out == [cmd_out]


def test_file_sample():
    dry_out = features.make_handbrake(TEST_FILE, '', PRESET, 0, 20)

    cmd_out = utils.make_cmd(TEST_FILE, DEFAULT_OUT, PRESET, 0, 20)

    assert dry_out == [cmd_out]


def test_file_get_info():
    pass
