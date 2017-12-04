#!/usr/bin/python3
"""
Parser for :program:`tick`
"""

from protocol import Month, Year
from typing import Union

def read_csv(file: str) -> list:
    """
    Read a csv and parse it into a list

    :param file: csv file to parse
    :return: csv as list
    """
    raise NotImplementedError
    pass

def parse_csv_protocol_to_year(protocol: Union[list, tuple]) -> Year:
    """
    parse a list of `csv` protocol entries into year. return year.

    :param protocol: protocol to parse
    """

    year = Year(protocol[0][1])

    sorted_protocol = {}

    for entry in protocol:
        sorted_protocol[entry[2]] = entry

    raise NotImplementedError


def parse_csv_protocol_to_years(protocol: Union[list, tuple]) -> list:
    """
    parse a list of `csv` protocol entries of different years.
    return a list of years.
    """
    raise NotImplementedError




if __name__ == '__main__':
    raise NotImplementedError

# vim: ai sts=4 ts=4 sw=4 expandtab
