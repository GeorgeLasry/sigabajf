# syslog.py: simule SYSLOG on Windows
# Ref: https://stackoverflow.com/questions/25537419/python-import-syslog-on-windows 
# version: 2.0
import sys
import datetime as dt

LOG_EMERG, LOG_ALERT, LOG_CRIT, LOG_ERR, LOG_WARNING, \
    LOG_NOTICE, LOG_INFO, LOG_DEBUG = range(8)
NAME = ["EMERG", "ALERT", "CRIT", "ERR", "WARN", "NOTICE", "INFO", "DEBUG"]

LOG_KERN, LOG_USER, LOG_MAIL, LOG_DAEMON, LOG_AUTH, \
    LOG_SYSLOG, LOG_LPR, LOG_NEWS, LOG_UUCP = range(0, 65, 8)

LOG_CRON = 120
LOG_LOCAL0 = 128
LOG_LOCAL1 = 136
LOG_LOCAL2 = 144
LOG_LOCAL3 = 152
LOG_LOCAL4 = 160
LOG_LOCAL5 = 168
LOG_LOCAL6 = 176
LOG_LOCAL7 = 184

LOG_PID = 1
LOG_CONS = 2
LOG_NDELAY = 8
LOG_NOWAIT = 16

# ------------------
LOGFILE = None
FACILITY = None


def syslog(priority, message):
    if LOGFILE is None:
        print("???");
        exit()
    # timestamp = dt.datetime.now()
    timestamp = (str(dt.datetime.now()))[-4:]
    print(f"{NAME[priority]} {priority} {timestamp}  {message}", file=LOGFILE)


def openlog(ident="LOG", logoption=0, facility=LOG_USER):
    global LOGFILE, FACILITY
    if ident == "LOG":
        LOGFILE = sys.stdout
    else:
        LOGFILE = open("LOGS/" + ident + "_log.txt", "a")
    FACILITY = facility
    syslog(LOG_DEBUG, "---Starting Logging----")
