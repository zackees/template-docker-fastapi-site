#!/bin/bash
set -e
function abs_path {
  (cd "$(dirname '$1')" &>/dev/null && printf "%s/%s" "$PWD" "${1##*/}")
}
if command -v python3 &>/dev/null; then
  alias python=python3
fi
if command -v pip3 &>/dev/null; then
    alias pip=pip3
fi
# if make_venv dir is not present, then make it
if [ ! -d "venv" ]; then
  python make_venv.py
fi
# if IN_ACTIVATED_ENV is set, then we are already in the venv
if [ -n "$IN_ACTIVATED_ENV" ]; then
  exit 0
fi
. $( dirname $(abs_path ${BASH_SOURCE[0]}))/venv/bin/activate
export PATH=$( dirname $(abs_path ${BASH_SOURCE[0]}))/:$PATH
export IN_ACTIVATED_ENV="1"
