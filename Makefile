SHELL:=/usr/bin/env bash

.PHONY: unit
unit:
	pytest

test: unit
