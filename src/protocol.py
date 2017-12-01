"""
This module provides the protocol class
"""

import time
import datetime

class InvalidDateException(Exception):
    pass

class ConfusingDataException(Exception):
    pass


class Month:
    """
    Provides the work time protocol for one month
    
    
    :param holidays_left: number of holidays left, 0 if omitted
    :param working_hours_account: credit of working hours in seconds, 0 if omitted
    :param yearmonth: integer of the form [[YY]YY]MM. Current time if omitted. Current year if only month is given. 20th century if first two digits are missing. 
    :param hours_worth_working_day: number of hours a working day is worth
        If only one digit is given it will be padded with a leading 0.
    :raises InvalidDateException: raised when the Date given is nonsense.
    """

    AVERAGE_WEEKS_PER_MONTH = 4.33

    def __init__(self, year:int=0, month:int=0, holidays_left:int=0, working_hours_account:int=0, hours_worth_working_day:int=4):

        self.protocol = []
        self.holidays_left_begin = holidays_left
        self.holidays_left = self.holidays_left_begin
        self.working_hours_account_begin = working_hours_account
        self.working_hours_account = self.working_hours_account_begin
        self.hours_worth_working_day = hours_worth_working_day
        self.monthly_target = 5 * hours_worth_working_day * Month.AVERAGE_WEEKS_PER_MONTH

        t = time.localtime()

        if not month:
            self.month = t.tm_mon
        else:
            self.month = month

        if not year:
            self.year = t.tm_year
        else:
            self.year = year

        if self.month < 1 or self.month > 12:
            raise InvalidDateException('%d is not a valid month' % self.month)

    def append(self, tag:str, day:int, duration:int=0, from_unixtime:int=0, to_unixtime:int=0, description:str=None) -> 'Month':
        """
        append an entry to the protocol

        :param tag: tag
        :param duration: duration of work
        :param from_unixtime: beginning of work in epoch
        :param to_unixtime: ending of work in epoch
        :param description: description
        :raises ConfusingData: when duration and from/to do are both given and do not match

        """
        # validate and set duration
        if from_unixtime and not to_unixtime or to_unixtime and not from_unixtime:
            raise ConfusingDataException('from and to must be given both')

        if duration and from_unixtime:
            if duration != (to_unixtime - from_unixtime):
                raise ConfusingDataException('duration given and calculated do not match')

        if not duration and not from_unixtime:
            duration = self.hours_worth_working_day * 3600

        # we should be safe now
        if not duration:
            duration = to_unixtime - from_unixtime

        # validate date
        try:
            datetime.date(self.year, self.month, day)
        except ValueError as e:
            raise InvalidDateException('%s' % str(e))


        self.protocol.append({'tag':tag, 'day':day, 'duration':duration, 
                                'from_unixtime':from_unixtime, 'to_unixtime':to_unixtime, 'description':description})


        self.working_hours_account += duration

        if tag == 'h':
            self.holidays_left -= 1

        return self



    def get_dict(self) -> dict:
        """return a dict with all values"""

        return {
            'year': self.year,
            'month': self.month,
            'holidays_left_begin': self.holidays_left_begin,
            'holidays_left': self.holidays_left,
            'working_hours_account_begin': self.working_hours_account_begin,
            'working_hours_account': self.working_hours_account,
            'monthly_target': self.monthly_target,
            'working_hours_balance': self.working_hours_account/3600 - self.monthly_target,
            'protocol': self.protocol
        }



    def __str__(self):
        return (
            'Year: %d, '
            'Month: %d, '
            'HolidaysLeftBeginMonth: %dd, '
            'HolidaysLeft: %dd, '
            'WorkingHoursAccountBeginMonth: %ds, '
            'WorkingHoursAccount: %ds, '
            'MonthlyTarget: %.1fh, '
            'WorkingHoursBalance: %+.1fh, '
            'Protocol: %r' % (
                self.year,
                self.month,
                self.holidays_left_begin,
                self.holidays_left,
                self.working_hours_account_begin,
                self.working_hours_account,
                self.monthly_target,
                self.working_hours_account/3600 - self.monthly_target,
                self.protocol
            )
        )


class Year:
    def __init__(self, year:int=None):
        if not year:
            self.year = time.localtime().tm_year
        else:
            self.year = year

        self.months = {}

    def add_month(self, month:Month) -> 'Year':
        """
        add a protocol to :var:`self.protocols`
        :param protocol: protocol to add.
        self.protocols[protocol.month] = protocol
        """
        raise NotImplementedError

        return self

# vim: ai sts=4 ts=4 sw=4 expandtab
