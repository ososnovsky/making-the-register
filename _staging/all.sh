#!/bin/bash
cd "$(dirname "$0")"
export PYTHONIOENCODING=utf-8 PYTHONUTF8=1
for f in cand/*.txt; do c=$(basename $f .txt); python build.py $f >/dev/null && python geocode.py cand/$c.yaml cand/$c.geo.yaml | grep -E "^OPEN" | sed "s/^/[$c] /"; done
python merge.py && python ../validate_sources.py | grep -E "ERROR|VALID|entries\."
