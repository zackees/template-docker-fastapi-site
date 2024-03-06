#!/bin/bash
# cd to the directory of the script
cd "$(dirname "$0")"
find . -type f -name "*.css" -not -path "./node_modules/*" -print0 | xargs -0 -I {} -P $(nproc) npx stylelint --allow-empty-input --fix {}