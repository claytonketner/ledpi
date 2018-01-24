TARGET=clayton@ledpi.local
DIR=~/ledpi


.PHONY: all
all: push remote restart

.PHONY: push
push:
	rsync -rt * $(TARGET):$(DIR)

.PHONY: remote
remote: push
	ssh $(TARGET) 'cd $(DIR) && make -f RemoteMakefile'

.PHONY: daemon
daemon: push
	ssh -t $(TARGET) 'cd $(DIR) && make -f RemoteMakefile $@'

.PHONY: restart
restart:
	ssh -t $(TARGET) 'cd $(DIR) && make -f RemoteMakefile $@'
