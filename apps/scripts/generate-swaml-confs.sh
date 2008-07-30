#!/bin/bash

# SWAML <http://swaml.berlios.de/>
# Semantic Web Archive of Mailing Lists
#
# Copyright (C) 2008 Sergio Fernández
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

USAGE="Usage: "$0" dir host baseuri"

if [ $# -ne 3 ]; then
    echo 1>&2 $USAGE
    exit -1
fi

DIR=$1
HOST=$2
BASEURI=$3

echo "Generating SWAML configurations for all mailboxes founded in "$DIR
cd $DIR

for X in `ls . | grep .mbox`
do
NAME=${X%.*}
FILE=$NAME.ini
touch $FILE
echo > $FILE
echo "[SWAML]" >> $FILE
echo "title = "$NAME" mailing list" >> $FILE
echo "description = "$NAME"" >> $FILE
echo "host = http://"$HOST"/" >> $FILE
echo "dir = archive/" >> $FILE
echo "base = "$BASEURI"/"$NAME"/archive/" >> $FILE
echo "mbox = "$NAME".mbox" >> $FILE
echo "post = YYYY-MMM/post-ID" >> $FILE
echo "to = "$NAME"@"$HOST"" >> $FILE
echo "kml = yes" >> $FILE
echo "search = swse" >> $FILE
echo "foaf = yes" >> $FILE
echo >> $FILE
echo "created config for "$NAME
done

