#!/usr/bin/env python3
# coding=utf8

# Converts a KiCad Footprint Position (.pos) File into JLCPCB compatible CPL file
# Copyright (C) 2019, Uri Shaked. Released under the MIT license.

import sys
import csv
from collections import OrderedDict
import kicad_netlist_reader

net = kicad_netlist_reader.netlist(sys.argv[1])

with open(sys.argv[2], 'r') as in_file, open(sys.argv[3], 'w', newline='') as out_file:

    reader = csv.DictReader(in_file)
    ordered_fieldnames = OrderedDict([('Designator',None),('Mid X',None),('Mid Y',None),('Layer',None),('Rotation',None)])
    writer = csv.DictWriter(out_file, fieldnames=ordered_fieldnames)
    writer.writeheader()

    for row in reader:
        # For each component, get the rotation field from the schematic, and add it to the rotation
        done = False
        rot = int(float(row['Rot']))
        for group in net.groupComponents():
            for component in group:
                if component.getRef() == row['Ref']:
                    if component.getField('JLCPCB Rotation'):
                        rot = rot + int(float(component.getField('JLCPCB Rotation')))
                    done = True
                if done:
                    break
            if done:
                break
        assert done
        writer.writerow({
            'Designator': row['Ref'], 
            'Mid X': row['PosX'] + 'mm', 
            'Mid Y': row['PosY'] + 'mm', 
            'Layer': row['Side'].capitalize(), 
            'Rotation': rot
        })
