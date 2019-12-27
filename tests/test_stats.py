from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()
from fritz import FritzStats
import pandas as pd


def test_missing_folder():
    fritz = FritzStats("missing_folder", "some_title")
    assert fritz.get_downtime().empty


def test_dataframes():
    fritz = FritzStats("tests/test_log_files", "some_title")
    downtime_df = fritz.get_downtime()

    # num rows
    assert downtime_df.shape[0] == 91

    expected_df = pd.read_pickle("tests/expected_df.pkl")
    print(downtime_df)
    print(expected_df)
    assert downtime_df.equals(expected_df)
