#!/bin/bash
set -e
cd "$(dirname "$0")"
host="${1:-127.0.0.1}"
port="${2:-8888}"
exec gunicorn --bind "$host:$port" app:app
