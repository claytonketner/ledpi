TARGET=clayton@ledpi.local
DIR=~/ledpi

.PHONY: all push remote

all: push remote

push:
	rsync -rt * $(TARGET):$(DIR)

remote: push
	ssh $(TARGET) 'cd $(DIR) && make -f RemoteMakefile'
