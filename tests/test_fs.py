# pytest -s tests/ --cov=epyfun

import pytest

from epyfun.fs import get_latest_file
from epyfun.fs import create_dir
from epyfun.fs import convert_to_utf8

import tempfile
import shutil
import os
import hashlib


def test_get_latest_file() -> None:
    # test that given these two files, it correctly identifys README as the latest
    temp_dir = tempfile.mkdtemp()
    try:
        file1_content = "This is file 1."
        file2_content = "This is file 2."
        file1_path = os.path.join(temp_dir, "README.md")
        file2_path = os.path.join(temp_dir, "all.txt")
        with open(file1_path, "w") as file1:
            file1.write(file1_content)
        with open(file2_path, "w") as file2:
            file2.write(file2_content)

        assert os.path.basename(get_latest_file(temp_dir)) == "README.md"
    finally:
        shutil.rmtree(temp_dir)


def test_create_dir() -> None:
    temp_dir = tempfile.mkdtemp()

    try:
        # Success creating a new dir
        dir_path = temp_dir + "sdf"
        assert not os.path.exists(dir_path)
        create_dir(dir_path)
        assert os.path.exists(dir_path)

        # Success creating a new dir
        dir_path = temp_dir + "/sdf"
        assert not os.path.exists(dir_path)
        create_dir(dir_path)
        assert os.path.exists(dir_path)

        # Success creating a new dir, where many intermediate dirs do not exist
        dir_path = temp_dir + "/foo/bar/toy/no"
        assert not os.path.exists(dir_path)
        create_dir(dir_path)
        assert os.path.exists(dir_path)

        # Success creating a parent dir for a file path (i.e. path with extension)
        dir_path = temp_dir + "/foo/bar/playground/readme.txt"
        assert not os.path.exists(dir_path)
        create_dir(dir_path)
        assert not os.path.exists(dir_path)
        assert os.path.exists(os.path.dirname(dir_path))

        # Do not fail if the directory already exists
        dir_path = temp_dir + "/foo"
        assert os.path.exists(dir_path)  # should exist now, it was created above
        create_dir(dir_path)
        assert os.path.exists(dir_path)

    finally:
        shutil.rmtree(temp_dir)


def test_convert_to_utf8() -> None:
    test_file = "tests/tests_resources/TU_Stundenwerte_Beschreibung_Stationen.txt"

    # it should fail trying to read this file
    with pytest.raises(Exception, match="codec can't decode byte"):
        with open(test_file, "r", encoding="utf-8") as file:
            file_contents = file.read()

    temp_dir = tempfile.mkdtemp()
    temp_file = temp_dir + "/test.txt"
    try:
        # after calling convert_to_utf8, you now should be able to read the contents
        # of the file, saved in a new location
        convert_to_utf8(test_file, temp_file)
        with open(temp_file, "r", encoding="utf-8") as file:
            file_contents = file.read().replace("\n", "").replace("\r", "")
            assert (
                hashlib.sha256(file_contents.encode("utf-8")).hexdigest()
                == "ae1c4e8e19525385fe4b15b42f28c27a6d6966a9824e0ebeaf10758a9d173068"
            )

        # and it should also work by just replacing the file (not passing a value
        # for the outputfile_path argument). So let's first copy the file to a new location
        new_test_file = temp_dir + "/nonutf8.txt"
        shutil.copy2(test_file, new_test_file)

        # first, test again that the file in the new location cannot be read with utf-8
        with pytest.raises(Exception, match="codec can't decode byte"):
            with open(new_test_file, "r", encoding="utf-8") as file:
                file_contents = file.read()

        # now test that it can convert the encoding and replace the file
        convert_to_utf8(new_test_file)
        with open(new_test_file, "r", encoding="utf-8") as file:
            file_contents = file.read().replace("\n", "").replace("\r", "")
            assert (
                hashlib.sha256(file_contents.encode("utf-8")).hexdigest()
                == "ae1c4e8e19525385fe4b15b42f28c27a6d6966a9824e0ebeaf10758a9d173068"
            )
    finally:
        shutil.rmtree(temp_dir)
