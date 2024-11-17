#!/bin/bash

export AOC_SESSION=$(cat AOC_SESSION)
source ~/.virtualenvs/aoc24/bin/activate
export UV_PROJECT_ENVIRONMENT=$VIRTUAL_ENV

alias init="python aoc/init.py"

