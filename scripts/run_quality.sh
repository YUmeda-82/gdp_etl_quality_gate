#!/bin/bash
set -e

echo "Importing dependencies..."

pip install ruff black mypy

echo "Staring CI pipe..."

ruff check etl/
black --check etl/
mypy etl/

echo "Quality gate passed!"