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
from pathlib import Path


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
        print('usage: ' + sys.argv[0] + ' <protocol.csv> [<state>]')
        exit(-1)

    state = sys.argv[2] if len(sys.argv) == 3 else None

    path = Path(sys.argv[1]).expanduser()

    csv_infile = str(path)
    xlsx_outfile = str(path.with_suffix('.xlsx'))
    txt_outfile = path.with_suffix('.txt')


    # parse the csv
    with open(csv_infile) as infile:
        reader = csv.reader(infile)
        year = parse_csv_protocol(reader, state)

    # write the parsed protocol to excel and txt
    with xlsxwriter.Workbook(xlsx_outfile) as workbook, \
            txt_outfile.open('w') as txtfile:


        # reversed output (Kaufmännische Heftung)
        for y in reversed(sorted(year)):
            for m in reversed(sorted(year[y])):
                txtfile.writelines((year[y][m].pretty(), '\n'))
                year[y][m].get_worksheet(workbook)

    # some feedback
    print('\nWorkbook written to %s'
            '\nTextfile written to %s'
            '\nFollowing an output of the month on top.'
            '\n' % (xlsx_outfile, str(txt_outfile))
        )

    # finally give a printout of the month on top
    y = sorted(year)[-1]
    m = sorted(year[y])[-1]
    print(year[y][m].pretty())


# vim: ai sts=4 ts=4 sw=4 expandtab
