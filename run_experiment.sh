#!/bin/bash

# get the current time
TIMESTAMP=$(date +%m-%d-%Y_%H-%M-%S)

# First argument provided by the user is a "TAG" value
# to help identify the experiment later.
# Defaults to MISSINGTAG if no tag is supplied.
TAG=${1:-MISSINGTAG}


# make a directory to hold the data.
# The -p argument tells mkdir to create any directories it needs along the path
# to the desired directory.
OUTDIR=runs/$TAG/$TIMESTAMP
mkdir -p $OUTDIR

#copy code over (could also use a git hash or something)
cp primeplot.py $OUTDIR
# Store command in variable so that output to commands.txt matches actual command always
COMMAND="python primeplot.py -o $OUTDIR"
echo $COMMAND > $OUTDIR/commands.txt
$COMMAND

#keep most recent run in a special place for easier access (only reasonable if you don't produce a ton of data)
mkdir -p runs/recent/
cp -r $OUTDIR/* runs/recent/
#output permanent location of most recent run's data in location.txt
echo $OUTDIR > runs/recent/location.txt