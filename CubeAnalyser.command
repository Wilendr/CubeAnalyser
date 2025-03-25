#!/bin/bash
cd "$(dirname "$0")"

if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed."
    echo "Please install it from https://www.python.org/downloads/"
    exit 1
fi

python3 program/main.py
