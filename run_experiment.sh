#!/bin/bash
## ^ specified that this is a bash script.
## only needed if you chmod +x and invoke as ./scriptname rather than bash scriptname

module load python3

# get the current time. $(command) will store the output of command as a variable
TIMESTAMP=$(date +%m-%d-%Y_%H-%M-%S)

# First argument provided by the user is a "TAG" value
# to help identify the experiment later.
# Defaults to MISSINGTAG if no tag is supplied.
TAG=${1:-MISSINGTAG}


# make a directory to hold the data.
# The -p argument tells mkdir to create any directories it needs along the path
# to the desired directory.
OUTDIR=runs/$TAG/$TIMESTAMP/


mkdir -p $OUTDIR
cp primeplot.py $OUTDIR
COMMAND="python3 primeplot.py -o $OUTDIR > $OUTDIR/output.txt"
echo "$COMMAND" > $OUTDIR/commands.txt
eval "$COMMAND" # this is poor security, but probably fine in this limited case.



#keep most recent run in a special place for easier access (only reasonable if you don't produce a ton of data)
mkdir -p runs/recent/
cp -r $OUTDIR/* runs/recent/
#output permanent location of most recent run's data in location.txt
echo $OUTDIR > runs/recent/location.txt
