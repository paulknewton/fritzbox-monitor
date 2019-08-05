# fritz-monitor
Monitor internet health of a fritz box and plot graphs

![Daily](docs/fig_daily.png)

![Hourly](docs/fig_hourly.png)

## Installation

## Usage
```
usage: fritz.py [-h] [-i [ADDRESS]] [-u [USER]] [-p [PASSWORD]]
                [--port [PORT]] [--logdir LOGDIR] [--title TITLE]
                [--output OUTPUT] [--prefix PREFIX]
                {log,stats}

FritzBox Monitor

positional arguments:
  {log,stats}           action to perform

optional arguments:
  -h, --help            show this help message and exit
  -i [ADDRESS], --ip-address [ADDRESS]
                        ip-address of the FritzBox to connect to. Default:
                        169.254.1.1
  -u [USER], --user [USER]
                        Fritzbox authentication username
  -p [PASSWORD], --password [PASSWORD]
                        Fritzbox authentication password
  --port [PORT]         port of the FritzBox to connect to. Default: 49000
  --logdir LOGDIR       folder where logs are stored
  --title TITLE         title used on graphs
  --output OUTPUT       folder to store graphs
  --prefix PREFIX       prefix added to graph filenames
```
