#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Takes a file containing a list of MPNs and outputs pasteable TSV-formatted specs."""

__author__ = 'Scott Johnston'
__version__ = '0.0.1'

import sys
import argparse
import csv
import scottopart

def main(input_file=False, output_file=False):
    """Main screen turn on."""

    # Read input part list.
    partlist = []
    reader = csv.reader(input_file)
    for row in reader:
        if len(row) > 0:
            partlist.append(row[0])

    # Process part numbers.
    s = scottopart.Scottopart()
    results = s.match_by_mpn(partlist)

    # Write output.
    writer = csv.DictWriter(output_file, dialect='excel-tab', extrasaction='ignore', fieldnames=scottopart.dblib_conventions.get_tablefields(results[0]['table_name']))
    writer.writeheader()
    for r in results:
        if r['success']:
            writer.writerow(r['table_row'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('infile', help="Input file", type=argparse.FileType('r'))
    parser.add_argument('-o', '--outfile', help="Output file",
                        default=sys.stdout, type=argparse.FileType('w'))
    args = parser.parse_args()

    main(args.infile, args.outfile)
