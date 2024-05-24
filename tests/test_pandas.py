from epyfun.pandas import sanitize_column_name
from epyfun.pandas import clean_names

import pytest

import os
import tempfile
import shutil

import pandas as pd
import numpy as np

import pandas.testing as pdt


def test_sanitize_column_name() -> None:
    assert sanitize_column_name("Any$§%_") == "any"
    assert sanitize_column_name("An$§y%_") == "an_y"


def test_clean_names() -> None:

    # from Pandas' docs https://pandas.pydata.org/docs/user_guide/advanced.html
    arrays = [
        ["bar", "bar", "baz", "baz", "foo", "foo", "qux", "qux"],
        ["one", "two", "one", "two", "one", "two", "one", "two"],
    ]
    tuples = list(zip(*arrays))
    index = pd.MultiIndex.from_tuples(tuples, names=["first", "second"])
    df = pd.DataFrame(np.random.randn(3, 8), index=["A", "B", "C"], columns=index)

    # one of the use cases of sanitize_column_name(), clean_names()
    # is to make nice column names for multi-index dataframes
    pdt.assert_index_equal(
        clean_names(df).columns,
        pd.Index(
            [
                "bar_one",
                "bar_two",
                "baz_one",
                "baz_two",
                "foo_one",
                "foo_two",
                "qux_one",
                "qux_two",
            ],
            dtype="object",
        ),
    )
