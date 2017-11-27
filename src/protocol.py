"""
This module provides the protocol class
"""

import time

class InvalidDateException(Exception):
    """raised in case an invalid date string was provided"""
    pass


class Protocol:
    """
    Provides the work time protocol for one month
    
    
    :param holidays_left: number of holidays left, 0 if omitted
    :param working_hours_account: credit of working hours, 0 if omitted
    :param month: integer of the form [[YY]YY]MM. Current time if omitted. Current year if only month is given. 20th century if first two digits are missing. 
        If only one digit is given it will be padded with a leading 0.
    :raises InvalidDateException: raised when the Date given is nonsense.
    """

    def __init__(self, holidays_left: int=0, working_hours_account: int=0, month: str=None):

        self.protocol = []
        self.holidays_left = holidays_left
        self.working_hours_account = working_hours_account
        
        if not month:
            t = time.localtime()
            self.year = t.tm_year
            self.month = t.tm_mon
        else:
            # first sanitize the string
            if len(month) == 1:
                # missing leading zero
                month = '0' + month
            if len(month) == 2:
                # no year given
                month = str(time.localtime().tm_year) + month
            elif len(month) == 4:
                # last two digits of year given
                month = '20' + month
            elif len(month) != 6:
                # something’s wrong with the string
                raise InvalidDateException("wrong length: %s" % month)

            try:
                self.year = int(month[:4])
                self.month = int(month[4:])
            except ValueError as e:
                raise InvalidDateException('Error parsing date: %r' % e)

        if self.month < 1 or self.month > 12:
            raise InvalidDateException('%d is not a valid month' % self.month)

# vim: ai sts=4 ts=4 sw=4 expandtab
