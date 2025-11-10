dev:
	pymon src/app.py -i "*"

install:
	pip install -r requirement.txt

init:
	python3 -m venv ./.venv
