#!/bin/bash
# usage: ./run.sh <category>  -> build, geocode, assemble, validate
cd "$(dirname "$0")"
export PYTHONIOENCODING=utf-8 PYTHONUTF8=1
python build.py cand/$1.txt && python geocode.py cand/$1.yaml cand/$1.geo.yaml | grep -v "^OK" ; python merge.py && python ../validate_sources.py | grep -E "ERROR|VALID|entries" | head -20
