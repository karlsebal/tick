#!/usr/bin/python3
"""
Parser for :program:`tick`
"""

from protocol import Month, Year
from typing import Union

def parse_csv_protocol(protocol: Union[list, tuple]) -> dict:
    """
    parse a list of `csv` protocol entries into year. return year.

    :param protocol: protocol to parse
    """

    sorted_protocol = {}

    for entry in protocol:

        year = entry.pop(1)
        if year not in sorted_protocol:
            sorted_protocol[year] = {}

        month = entry.pop(1)
        if month not in sorted_protocol[year]:
            sorted_protocol[year][month] = []

        sorted_protocol[year][month].append(entry)

    sorted_years = {}
    former = None

    for year in sorted_protocol:
        for month in sorted_protocol[year]:
            if not year in sorted_years:
                sorted_years[year] = {}
            if not month in sorted_years[year]:
                sorted_years[year][month] = former.get_next() if former else Month(month=int(month))
            sorted_years[year][month].append_protocol(sorted_protocol[year][month])
            former = sorted_years[year][month]
    
    return sorted_years
            

if __name__ == '__main__':
    raise NotImplementedError

# vim: ai sts=4 ts=4 sw=4 expandtab
