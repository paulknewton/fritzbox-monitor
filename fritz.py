#!/usr/bin/env python3

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
import argparse

import matplotlib
from fritzconnection import FritzConnection

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from monitor import FritzMonitor
from statistics import FritzStats

# max number of bars to show on a graph (avoids overcrowding)
max_graph_size = 50


def _get_cli_arguments():
    parser = argparse.ArgumentParser(description='FritzBox Monitor')
    parser.add_argument("action", type=str, choices=["log", "stats"], help="action to perform")

    # used by action: log
    parser.add_argument('-i', '--ip-address',
                        nargs='?', default=None, const=None,
                        dest='address',
                        help='ip-address of the FritzBox to connect to. '
                             'Default: %s' % fritzconnection.FRITZ_IP_ADDRESS)
    parser.add_argument('-u', '--user',
                        nargs='?', default=None, const=None,
                        help='Fritzbox authentication username')
    parser.add_argument('-p', '--password',
                        nargs='?', default=None, const=None,
                        help='Fritzbox authentication password')
    parser.add_argument('--port',
                        nargs='?', default=None, const=None,
                        dest='port',
                        help='port of the FritzBox to connect to. '
                             'Default: %s' % fritzconnection.FRITZ_TCP_PORT)

    # used by action: stats
    parser.add_argument("--logdir", default="logs", help="folder where logs are stored")
    parser.add_argument("--title", default="FRITZ!Box", help="title used on graphs")
    parser.add_argument("--output", default="docs", help="folder to store graphs")
    parser.add_argument("--prefix", default="fig_fritz", help="prefix added to graph filenames")

    args = parser.parse_args()
    return args


def main():
    """
    Run the tool to either extract a new system log, or build graphs from existing logs.

    usage: fritz.py [-h] [-i [ADDRESS]] [-u [USER]] [-p [PASSWORD]]
                [--port [PORT]] [--logdir LOGDIR] [--title TITLE]
                [--output OUTPUT] [--prefix PREFIX]
                {log,stats}
    """
    args = _get_cli_arguments()
    print(args)

    if args.action == "log":
        fritz = FritzMonitor(
            address=args.address,
            port=args.port,
            user=args.user,
            password=args.password,
        )

        log = fritz.get_system_log()
        print(log)

    elif args.action == "stats":
        fritz = FritzStats(args.logdir, args.title)
        downtime_df = fritz.get_downtime()
        # downtime_df.to_pickle("df.pkl")
        if not (downtime_df is None or downtime_df.empty):
            sns.set(style="dark")

            # pd.set_option('display.max_rows', len(downtime))
            # print(df)
            # pd.reset_option('display.max_rows')

            hour_df = downtime_df.groupby(
                [downtime_df.index.year, downtime_df.index.month, downtime_df.index.day,
                 downtime_df.index.hour]).count()
            hour_df = hour_df.tail(max_graph_size)  # truncate

            hour_df.plot.bar(figsize=(10, 4))
            plt.ylabel("# failures")
            plt.xlabel("time")
            plt.title("%s failures (by hour)" % args.title)
            plt.legend()
            plt.savefig(args.output + "/" + args.prefix + "_hourly.png", bbox_inches='tight')

            day_df = downtime_df.groupby(
                [downtime_df.index.year, downtime_df.index.month, downtime_df.index.day]).count()
            day_df = day_df.tail(max_graph_size)  # truncate

            day_df.plot.bar(figsize=(10, 4))
            plt.ylabel("# failures")
            plt.xlabel("time")
            plt.title("%s failures (by day)" % args.title)
            plt.legend()
            plt.savefig(args.output + "/" + args.prefix + "_daily.png", bbox_inches='tight')


if __name__ == '__main__':
    main()
