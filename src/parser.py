#!/usr/bin/python3 
"""
parser for :program:`tick`
"""

import logging
import pdb

from typing import Union

import sys
import csv
from protocol import Month

import xlsxwriter


def parse_csv_protocol(protocol: Union[list, tuple]) -> dict:
    """
    parse a list of `csv` protocol entries into year. return year.

    :param protocol: protocol to parse

    """

    # first sort month and year, leafs are protocol lists
    sorted_protocol = {}

    for entry in protocol:

        # adjust types
        for i in range(1, 7):
            entry[i] = int(entry[i]) if entry[i] else None

        # year and month are at position 1 and 2
        # we don’t need them anymore after retrieval
        year = int(entry.pop(1))
        if year not in sorted_protocol:
            sorted_protocol[year] = {}

        month = int(entry.pop(1))
        if month not in sorted_protocol[year]:
            sorted_protocol[year][month] = []

        sorted_protocol[year][month].append(entry)

    # now fill that into a dict with Months as leafs 
    sorted_years = {}
    former = None

    for year in sorted_protocol:
        for month in sorted_protocol[year]:
            if not year in sorted_years:
                sorted_years[year] = {}

            if not month in sorted_years[year]:
                sorted_years[year][month] = former.get_next(month=month, year=year) if former else Month(month=int(month), year=int(year))

            sorted_years[year][month].append_protocol(sorted_protocol[year][month])
            former = sorted_years[year][month]

    return sorted_years
            

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('usage: ' + sys.argv[0] + ' <protocol.csv> [<protocol.xlsx>]')
        exit(-1)

    with open(sys.argv[1]) as file:
        reader = csv.reader(file)
        year = parse_csv_protocol(reader)

    xlsx_outfile = sys.argv[2] if len(sys.argv) >= 3 else 'protocol.xlsx'

    with xlsxwriter.Workbook(xlsx_outfile) as workbook:

        for y in year:
            for m in year[y]:
                print(year[y][m].pretty())
                year[y][m].get_worksheet(workbook)

# vim: ai sts=4 ts=4 sw=4 expandtab
