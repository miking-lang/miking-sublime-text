.PHONY: build

build:
	$(eval PWD := $(shell pwd -P))
	python3 src/gen.py mcore --dstdir=$(PWD)
