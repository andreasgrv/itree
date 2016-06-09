NAME= $(shell python setup.py --name)
VERSION= $(shell python setup.py --version)

all: clean test install

clean:
	@echo ">> Cleaning..."
	@find . -name \*.pyc -exec rm -rf {} +

test:
	@echo ">> Testing..."
	py.test -v

install:
	@echo ">> Installing..."
	pip install -e .
