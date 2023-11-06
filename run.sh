#!/bin/sh

export FLASK_APP=main.py
export FLASK_DEBUG=True

python -m flask run -p 5001 -h 0.0.0.0