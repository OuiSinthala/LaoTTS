#!/bin/bash
# MUST HAVE POETRY INSTALLED
poetry install
poetry lock --no-update
poetry install
poetry export --without-hashes --format=requirements.txt > requirements.txt