import glob
import re
import pandas as pd
from datetime import datetime


class FritzStats:

    def __init__(self, log_dir, title):
        self.log_dir = log_dir + "/*"
        self.title = title

    def get_downtime(self):
        return self._read_logs(self.log_dir, "Timeout during PPP negotiation")

    def _read_logs(self, filter, pattern):

        log_files = glob.glob(filter)

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
                    except AttributeError as e:
                        pass

        df = pd.DataFrame(timestamp_data, columns=["timestamp"]).drop_duplicates()
        if df.empty:
            return df

        df["event"] = 1
        df = df.set_index("timestamp")
        #df.sort_index(inplace=True)

        return df
