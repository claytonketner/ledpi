# Config stuff for debian init.d daemons

TARGET=clayton@clockpi.local
SUDO_TARGET=root@clockpi.local

all:
	rsync bin/* $(TARGET):/usr/local/bin/
	rsync init.d/* $(SUDO_TARGET):/etc/init.d/
	# TODO hardcoded
	ssh -t $(TARGET) 'sudo update-rc.d clockpi defaults && sudo touch /var/log/clockpi.log'
