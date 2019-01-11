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


def parse_csv_protocol(protocol: Union[list, tuple], state:str) -> dict:
    """
    parse a list of `csv` protocol entries into year. return year.

    The dict returned will contain a chain of Months in ascending order
    regardless of missing months. That means the working hour account is
    assigned to the next month found in protocol no matter how many months
    are missing in between.

    :param protocol: protocol to parse
    :param state: state based on which workdays are calculated by protocol
    :return: a dict containing years containing instances of protocol.Month

    """

    # first sort month and year, leafs are protocol lists
    # as they are found in the csv
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


    # now fill that into a dict with instances of
    # protocol.Month as leafs 
    sorted_years = {}
    former = None

    for year in sorted(sorted_protocol):
        for month in sorted(sorted_protocol[year]):
            if not year in sorted_years:
                sorted_years[year] = {}

            if not month in sorted_years[year]:
                sorted_years[year][month] = former.get_next(month=month, year=year) if former else Month(month=int(month), year=int(year), state=state)

            sorted_years[year][month].append_protocol(sorted_protocol[year][month])
            former = sorted_years[year][month]

    return sorted_years
            

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('usage: ' + sys.argv[0] + ' <protocol.csv> [<protocol.xlsx>] [<state>]')
        exit(-1)

    state = sys.argv[3] if len(sys.argv) >= 4 else None

    with open(sys.argv[1]) as file:
        reader = csv.reader(file)
        year = parse_csv_protocol(reader, state)

    xlsx_outfile = sys.argv[2] if len(sys.argv) >= 3 else 'protocol.xlsx'

    with xlsxwriter.Workbook(xlsx_outfile) as workbook:

        # reversed output (Kaufmännische Heftung)
        for y in reversed(sorted(year)):
            for m in reversed(sorted(year[y])):
                print(year[y][m].pretty())
                year[y][m].get_worksheet(workbook)

# vim: ai sts=4 ts=4 sw=4 expandtab
