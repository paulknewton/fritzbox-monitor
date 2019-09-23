[![travis-ci](https://travis-ci.org/paulknewton/fritz-monitor.svg?branch=master)](https://travis-ci.org/paulknewton/fritz-monitor)
[![codecov](https://codecov.io/gh/paulknewton/fritz-monitor/branch/master/graph/badge.svg)](https://codecov.io/gh/paulknewton/fritz-monitor)

[![DeepSource](https://static.deepsource.io/deepsource-badge-light.svg)](https://deepsource.io/gh/paulknewton/fritz-monitor/?ref=repository-badge)

# fritz-monitor
Monitor the internet health of a Fritz!Box router and plot graphs of errors

![Daily](docs/fritz7530_daily.png)

![Hourly](docs/fritz7530_hourly.png)

## How does it work?

The tools use the [fritzconnection](https://github.com/kbr/fritzconnection) libraries.
System logs are downloaded from the Fritz!Box on a periodic basis and stored on a local filesystem.
When the program is executed in 'statistics' mode, it reads all of the logs, and searches for key strings that indicate errors. These errors are used to populate a pandas Dataframe which are then converted to pretty graphs via matplotlib.

The tools support different command-line arguments for accessing the router (user, password etc) or when storing the graphs (log directory, output folder, graphs titles etc).

## Installation

The code is compatible with both python 2 and python 3.

All library dependencies are listed in `requirements.txt`, so on many platforms you can install everything via `pip`. For example, for python 3:
```
pip3 install -r requirements.txt
```

If you are using a virtualenv, then you can run the above command as a normal user.
If you are installing the libraries machine-wide then you will likely need to run as super-user instead:

```
sudo pip3 install -r requirements.txt
```

### Notes on installing on a Raspberry Pi
I run this code on a Raspberry Pi.
If you install everything using ```pip```as above then it will likely need to re-build some libraries from source.
The large scientific libraries such as sci-py, numpy and pandas will take an age (if they succeed at all). It is strongly recommended to install the large, complex python libraries first using the apt package manager and only use the ```pip``` installation for the remaining libaries.

A user also notified me that numpy requires you to install the libatlas-base-dev package as well.

```
sudo apt-get install python3-scipy python3-numpy python3-pandas libatlas-base-dev
sudo pip3 install -r requirements.txt
```

## Usage

Just run the `fritz.py` program. The `-h` flag lists all the possible arguments:

```
./fritz.py -h

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

The tool supports 2 operating modes:
* log - extract a log from the router
* stats - build graphs from the log files

e.g.
```
./fritz.py log -p somepass > logs/fritz.log
```

will dump out the last system log from the router to the `fritz.log` file (in the `logs` folder).

```
./fritz.py stats -title "Errors in my router" --logdir logs --output docs
```

will create some graphs from any log files found in the `logs` folder, and store the graphs in the `docs` folder.

## Running on a schedule

On my FRITZ!Box the system event logs are truncated so you will need to run the program in ````log```` mode on a regular basis.
The code is designed to discard duplicate entries occurring in different log extracts so you can run the program as often as you like and save the log files in a directory.
I run this on as a ```cron``` schedule each night.

```
0 0 * * * (cd /home/pi/fritz-monitor; python3 fritz.py -p your_pwd log > logs.fritz7530/fritz.`/bin/date "+\%Y\%m\%d-\%H\%M"`.txt)
30 0 * * * (cd /home/pi/fritz-monitor; ./build-graphs.sh)
```