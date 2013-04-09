#!/bin/bash
# This script is just for simple input in the form
# run.sh cnf.dimacs N SEED
# We recommend that you use the sosat command directly

if [ "$2" == "0" ]; then
    ALGO="genetic"
else
    ALGO="ant"
fi

sosat $1 -a $ALGO -s $3