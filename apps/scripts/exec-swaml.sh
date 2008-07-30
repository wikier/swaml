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

USAGE="Usage: "$0" dir"

if [ $# -ne 1 ]; then
    echo 1>&2 $USAGE
    exit -1
fi

DIR=$1
SWAML="/usr/bin/swaml"

#process each list
for X in `find $DIR -name "*.ini"`
do
NAME=${x%.*}
echo
echo "---------------------------------------------------------------------"
echo
echo "Running SWAML with "$X" configuration file"
echo
$SWAML $X
echo
done

