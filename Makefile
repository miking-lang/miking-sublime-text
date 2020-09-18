.PHONY: build

LANGUAGES=mcore

SYNTAX-HIGHLIGHTERS=$(foreach LANG,$(LANGUAGES),$(LANG).sublime-syntax)

build: $(SYNTAX-HIGHLIGHTERS)

%.sublime-syntax: FORCE
	$(eval PWD := $(shell pwd -P))
	$(eval LANG := $*)
	python3 src/gen.py $(LANG) --dstdir=$(PWD)
	./src/$(LANG)/replacements.sh $(LANG).sublime-syntax
FORCE:
