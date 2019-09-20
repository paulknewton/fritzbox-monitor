from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import open
from future import standard_library
standard_library.install_aliases()
from builtins import object
import glob
import re
from datetime import datetime

import pandas as pd


class FritzStats(object):
    """
    Manages statistics for a FRITZ!Box router.
    """

    def __init__(self, log_dir, title):
        self.log_dir = log_dir + "/*"
        self.title = title

    def get_downtime(self):
        """
        Get the times when the router did not have an internet connection.
        :return: dataframe of the form timestamp, event (event is always 1)
        """
        return self._read_logs("Timeout during PPP negotiation")

    def _read_logs(self, pattern):

        log_files = glob.glob(self.log_dir)

        regex = re.compile("^(.*) %s.$" % pattern)

        # read each file in turn, scanning for the pattern
        timestamp_data = []
        print("log_files", log_files)
        for file in log_files:
            with open(file) as f:
                for line in f:
                    try:
                        ts_str = regex.search(line).group(1)  # timestamp when the event occurred
                        timestamp = datetime.strptime(ts_str, "%d.%m.%y %H:%M:%S")  # format "30.07.19 23:59:12"
                        timestamp_data.append(timestamp)
                    except AttributeError:
                        pass

        df = pd.DataFrame(timestamp_data, columns=["timestamp"]).drop_duplicates()
        if df.empty:
            return df

        df["event"] = 1
        df = df.set_index("timestamp")
        df.sort_index(inplace=True)

        return df
