#!/bin/bash
set -e
cd "$(dirname "$0")"
exec gunicorn --bind 127.0.0.1:8888 app:app
