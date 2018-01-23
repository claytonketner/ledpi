TARGET=clayton@ledpi.local
DIR=~/ledpi/
VIRTUAL_ENV?=venv

.PHONY: all push requirements

all: push

push:
	rsync -r --exclude={$(VIRTUAL_ENV),Makefile} * $(TARGET):$(DIR)

requirements: push
	ssh $(TARGET) 'cd $(DIR) && source $(VENV)/bin/activate && pip install -r requirements.txt'
