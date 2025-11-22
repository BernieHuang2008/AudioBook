#!/bin/bash

SCRIPT_PATH="$(readlink -f "$0")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"

python3 "$SCRIPT_DIR/../server.py"

trap 'exit 0' SIGTERM