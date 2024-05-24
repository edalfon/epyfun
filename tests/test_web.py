from epyfun.web import download_file

import pytest

import os
import tempfile
import shutil


def test_download_file() -> None:
    temp_dir = tempfile.mkdtemp()

    try:
        # succeed saving a a file destination
        destination = download_file(
            "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018/2018-09-18/us-airports.csv",
            temp_dir + "file.txt",
        )
        assert os.path.getsize(temp_dir + "file.txt") == 886165

        # succeed saving a a file destination
        destination = download_file(
            "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018/2018-09-18/us-airports.csv"
        )
        assert os.path.getsize(destination) == 886165
        os.remove(destination)

        # cannot download, should fail with an Exception
        with pytest.raises(Exception, match="Failed to download file"):
            destination = download_file(
                "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018/2018-09-18/us-airports"
            )

    finally:
        shutil.rmtree(temp_dir)
