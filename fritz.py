#!/usr/bin/env python3

from fritzconnection import fritzconnection
import argparse
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from monitor import FritzMonitor
from statistics import FritzStats


def _get_cli_arguments():
    parser = argparse.ArgumentParser(description='FritzBox Monitor')
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
    parser.add_argument("--logdir", default="logs", help="folder where logs are stored")
    parser.add_argument("--title", default="Fritbox", help="pattern used for log filename")
    parser.add_argument("action", type=str, choices=["log", "stats"], help="action to perform")
    args = parser.parse_args()
    return args


def main():
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
        #print(downtime_df.tail(1000))
        if not (downtime_df is None or downtime_df.empty):

            sns.set(style="dark")

            # pd.set_option('display.max_rows', len(downtime))
            # print(df)
            # pd.reset_option('display.max_rows')

            hour_df = downtime_df.groupby(
                [downtime_df.index.year, downtime_df.index.month, downtime_df.index.day, downtime_df.index.hour]).count()
            hour_df.plot.bar()
            plt.ylabel("# failures")
            plt.xlabel("time")
            plt.title("%s failures (by hour)" % args.title)
            plt.legend()
            plt.savefig("docs/fig_hourly.png", bbox_inches='tight')

            day_df = downtime_df.groupby([downtime_df.index.year, downtime_df.index.month, downtime_df.index.day]).count()
            day_df.plot.bar()
            plt.ylabel("# failures")
            plt.xlabel("time")
            plt.title("%s failures (by hour)" % args.title)
            plt.legend()
            plt.savefig("docs/fig_daily.png", bbox_inches='tight')


if __name__ == '__main__':
    main()
