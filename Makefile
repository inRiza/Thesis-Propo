.PHONY: all build proposal clean validate

all: clean build

build:
	mkdir -p dist
	mkdir -p build
	latexmk -pdf -bibtex -outdir=../../build -cd src/thesis/thesis.tex
	mv build/thesis.pdf dist

proposal:
	mkdir -p dist
	mkdir -p build
	latexmk -pdf -bibtex -outdir=../../build -cd src/proposal/proposal.tex
	cp build/proposal.pdf dist/proposal.pdf

validate:
	find src -name '*.tex' -print0 | xargs -0 chktex -l .chktexrc

clean:
	rm -f dist/* build/*
	find . -iname "*~" -exec rm '{}' ';'
