"""
This module provides the Month and Year classes
"""

import pdb
from typing import Union
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
    :param working_hours_account: credit of working hours in *seconds*, 0 if omitted
    :param yearmonth: integer of the form [[YY]YY]MM. Current time if omitted. Current year if only month is given. 20th century if first two digits are missing. 
    :param hours_worth_working_day: number of hours a working day is worth
        If only one digit is given it will be padded with a leading 0.
    :raises InvalidDateException: raised when the Date given is nonsense.
    """

    AVERAGE_WEEKS_PER_MONTH = 4.33
    

    monthly_target = property(
            lambda self: 5 * self.hours_worth_working_day * Month.AVERAGE_WEEKS_PER_MONTH)

    working_hours_balance = property(
            lambda self: self.working_hours_account - self.monthly_target * 3600)

    working_hours = property(
            lambda self: self.working_hours_account - self.working_hours_account_begin)


    def __init__(self, year:int=0, month:int=0, 
                    holidays_left:int=0, working_hours_account:int=0, 
                    hours_worth_working_day:int=4):

        self.protocol = []
        self.holidays_left_begin = holidays_left
        self.holidays_left = self.holidays_left_begin
        self.working_hours_account_begin = working_hours_account
        self.hours_worth_working_day = hours_worth_working_day
        self.working_hours_account = working_hours_account 

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


    def get_next(self, year=None, month=None) -> 'Month':
        """
        return the next Month derived from the current

        holidays left are transferred, working hours account
        is adjusted.

        :param month: you can give a different month. If omitted next
            month is assumed.
        
        """

        return Month(year if year else self.year if self.month < 12 else self.year + 1, 
                    month if month else self.month + 1 if self.month < 12 else 1,
                    self.holidays_left, 
                    self.working_hours_account - self.monthly_target * 3600, 
                    self.hours_worth_working_day)


    def append(self, tag:str, day:int, duration:int=0, from_unixtime:int=0, to_unixtime:int=0, description:str=None) -> 'Month':
        """
        append an entry to the protocol

        :param tag: tag
        :param duration: duration of work in seconds
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

        # a whole day if no duration is given
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


        self.protocol.append({
                            'tag':tag, 
                            'day':day, 
                            'duration':duration, 
                            'from_unixtime':from_unixtime, 
                            'to_unixtime':to_unixtime, 
                            'description':description
                            })


        self.working_hours_account += duration

        if tag == 'h':
            self.holidays_left -= 1

        return self

    def append_protocol(self, protocol: Union[list, tuple]) -> 'Month':
        """
        add a list or tuple of entries to the protocol
        """

        for entry in protocol:
            self.append(*entry)


    def dump(self) -> dict:
        """return a dict with all values"""

        return {
            'year': self.year,
            'month': self.month,
            'holidays_left_begin': self.holidays_left_begin,
            'holidays_left': self.holidays_left,
            'working_hours_account_begin': self.working_hours_account_begin,
            'working_hours_account': self.working_hours_account,
            'monthly_target': self.monthly_target,
            'working_hours': self.working_hours,
            'protocol': self.protocol
        }



    def pretty(self) -> str:
        """return object as pretty string"""

        # protocol first

        protocol = ''

        for entry in self.protocol:
            # pretty fromto
            if entry['from_unixtime']:
                from_time = time.gmtime(entry['from_unixtime'])  
                from_hour = from_time.tm_hour
                from_minute = from_time.tm_min
            else:
                from_hour = 0
                from_minute = 0

            if entry['to_unixtime']:
                to_time = time.gmtime(entry['to_unixtime'])  
                to_hour = to_time.tm_hour
                to_minute = to_time.tm_min
            else:
                to_time = time.gmtime(entry['to_unixtime']) 
                to_hour = 0
                to_minute = 0

            # add entry
            protocol += '%d.%d %.2fh (%02d:%02d-%02d:%02d): %s\n' % (
                entry['day'],
                self.month,
                entry['duration'] / 3600,
                from_hour, from_minute,
                to_hour, to_minute,
                entry['description']
                )

        decorator = 25 * '*'

        # and all together now

        return (
            '%s %04d-%02d %s'
            '\nHolidaysLeftBeginMonth: %dd'
            '\nHolidaysLeft: %dd'
            '\nMonthlyTarget: %.1fh'
            '\nWorkingHoursAccountBeginMonth: %+.1fh (%ds)'
            '\nWorkingHoursAccount: %.1fh (%ds)'
            '\nWorkingHours: %.1fh (%ds)'
            '\nWorkingHoursBalance: %+.1fh'
            '\n%s Protocol %s' 
            '\n%s' % (
                decorator, self.year, self.month, decorator,
                self.holidays_left_begin,
                self.holidays_left,
                self.monthly_target,
                self.working_hours_account_begin / 3600, self.working_hours_account_begin,
                self.working_hours_account / 3600, self.working_hours_account,
                self.working_hours /3600, self.working_hours,
                self.working_hours_balance / 3600 ,
                decorator, decorator,
                protocol
            ) + 
            '\n' + 60 * '~'
        )


    def __str__(self):
        return (
            'Year: %d, '
            'Month: %d, '
            'HolidaysLeftBeginMonth: %dd, '
            'HolidaysLeft: %dd, '
            'WorkingHoursAccountBeginMonth: %ds, '
            'WorkingHoursAccount: %ds, '
            'MonthlyTarget: %.1fh, '
            'WorkingHours: %+.1fh, '
            'WorkingHoursBalance: %+.1fh, '
            'Protocol: %r' % (
                self.year,
                self.month,
                self.holidays_left_begin,
                self.holidays_left,
                self.working_hours_account_begin,
                self.working_hours_account,
                self.monthly_target,
                self.working_hours,
                self.working_hours_balance / 3600,
                self.protocol
            )
        )


class Season:
    """
    contains a chain of Months
    """

    def __init__(self, t = 0, working_hours_account = 0):
        self.months = []

    def add_month(self, month:Month) -> 'Season':
        """
        add a protocol
        :param protocol: protocol to add.
        self.protocols[protocol.month] = protocol
        """

        self.months.append(month)
        return self


    def validate(self) -> 'Season':
        """ 
        validate the chain of months 

        :raises ValueError: when validation fails
        :returns: self
        """

        former = None

        for month in self.months:
            current = self.months[month]

            if not former:
                former = current
            else:
                if former.working_hours_balance != current.working_hours_account_begin:
                    raise ValueError('working_hours_balance from %d is %d and does not'
                                    'match working_hours_account_begin from %d which is %d' % (
                                        former.month, former.working_hours_balance, 
                                        current.month, current.working_hours_account_begin))

                if former.holidays_left != current.holidays_left_begin:
                    raise ValueError('holidays_left from %d does not'
                                    'match holidays_left_begin from %d' % (
                                        former.month, current.month))

        return self

# vim: ai sts=4 ts=4 sw=4 expandtab
