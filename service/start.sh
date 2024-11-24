#!/bin/bash

python3 ../server.py

trap 'exit 0' SIGTERM