.PHONY: build

build:
	$(eval PWD := $(shell pwd -P))
	./src/gen.py mcore --dstdir=$(PWD)
