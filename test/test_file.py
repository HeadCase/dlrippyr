#!/usr/bin/env python
from pathlib import Path

from dlrippyr import features

TEST_FILE = Path('samples/Wentworth.mov')
PRESET = 'conf/x265-1080p-mkv.json'


def test_file_dry_run(capsys):
    features.run_dry(TEST_FILE, '', PRESET, None, None)
    out, err = capsys.readouterr()
    assert out == 'HandBrakeCLI --preset-import-file conf/x265-1080p-mkv.json'\
    ' -Z conf/x265-1080p-mkv -i samples/Wentworth.mov -o'\
    ' samples/Wentworth.mkv\n'
    assert err == ''


def test_file_sample():
    pass


def test_file_get_info():
    pass
