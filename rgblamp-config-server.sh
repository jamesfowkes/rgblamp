#!/bin/sh

### BEGIN INIT INFO
# Provides:          rgblamp-config-server
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: RGB lamp configuration website
# Description:       Python Flask webserver with config views and API
### END INIT INFO

# Change the next 3 lines to suit where you install your script and what you want to call it
DIR=/home/pi/rgblamp/config-site
DAEMON=$DIR/run.py
DAEMON_NAME=rgblamp-config-server
LOGFILE=/var/log/rgblamp/config.log

# Source configuration options
[ -f /etc/default/rgblamp/config ] && . /etc/default/rgblamp/config

# Add any command line options for your daemon here
DAEMON_OPTS="$LOGFILE --public"

# This next line determines what user the script runs as.
# Root generally not recommended but necessary if you are using the Raspberry Pi GPIO from Python.
DAEMON_USER=pi

# The process ID of the script when it runs is stored here:
PIDFILE=/tmp/$DAEMON_NAME.pid

. /lib/lsb/init-functions

log_daemon_msg "Using config file $RGBLAMP_CONFIG_SERVER_CONFIG_PATH"

do_start () {
    log_daemon_msg "Starting system $DAEMON_NAME daemon"
    start-stop-daemon --start --background --pidfile $PIDFILE --make-pidfile --user $DAEMON_USER --chuid $DAEMON_USER --startas /bin/bash -- -c "exec $DAEMON $DAEMON_OPTS"
    log_end_msg $?
}
do_stop () {
    log_daemon_msg "Stopping system $DAEMON_NAME daemon"
    start-stop-daemon --stop --pidfile $PIDFILE --retry 10
    log_end_msg $?
}

case "$1" in

    start|stop)
        do_${1}
        ;;

    restart|reload|force-reload)
        do_stop
        do_start
        ;;

    status)
        status_of_proc "$DAEMON_NAME" "$DAEMON" && exit 0 || exit $?
        ;;

    *)
        echo "Usage: /etc/init.d/$DAEMON_NAME {start|stop|restart|status}"
        exit 1
        ;;

esac
exit 0
