#!/usr/bin/env bash
set -e

virtualenv -p python3 venv
venv/bin/pip install --upgrade pip
venv/bin/pip install -I -r requirements.txt
