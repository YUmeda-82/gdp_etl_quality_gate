quality:
	bash scripts/run_quality.sh

run:
	python3 main.py

build:
	docker build -t gdp-etl .

all: build quality run