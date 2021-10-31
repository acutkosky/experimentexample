#!/bin/bash

# get the current time
TIMESTAMP=$(date +%m-%d-%Y_%H-%M-%S)

# First argument provided by the user is a "TAG" value
# to help identify the experiment later.
TAG=${1:-MISSINGTAG}


# make a directory to hold the data.
# The -p argument tells mkdir to create any directories it needs along the path
# to the desired directory.
OUTDIR=runs/$TAG/$TIMESTAMP
mkdir -p $OUTDIR

#copy code over (could also use a git hash or something)
cp coin.py $OUTDIR
echo "python coin.py -o $OUTDIR" > $OUTDIR/commands.txt

python coin.py -o $OUTDIR

#keep most recent run in a special place
mkdir -p runs/recent/
cp -r $OUTDIR/* runs/recent/
echo $OUTDIR > runs/recent/location.txt