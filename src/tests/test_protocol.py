import unittest
from protocol import Month as Protocol
from protocol import Month
from protocol import InvalidDateException
from protocol import ConfusingDataException
import time

class TestProtocol(unittest.TestCase):

    def testInit(self):
        current_year = time.localtime().tm_year
        current_month = time.localtime().tm_mon

        invalid_dates = [
                            1144,
                            44,
                            201713,
                            123,
                            201700,
                            1700,
                            1723,
                            13,
                            111
                            ]

        for invalid_date in invalid_dates:
            self.assertRaises(InvalidDateException, Protocol, month=invalid_date)

        # without parameters year must be set to current
        self.assertEqual(Protocol().year, current_year)
        self.assertEqual(Protocol().month, current_month)

        p = Protocol(month=11)

        self.assertEqual(p.month, 11)
        self.assertEqual(p.year, current_year)

        p = Protocol(month=1)

        self.assertEqual(p.month, 1)
        self.assertEqual(p.year, current_year)

        p = Protocol(year=20, month=12)

        self.assertEqual(p.month, 12)
        self.assertEqual(p.year, 20)

        p = Protocol(year=0, month=12)

        self.assertEqual(p.month, 12)
        self.assertEqual(p.year, current_year)

    def test_init_and_string(self):
        self.assertEqual(Protocol(2012, 9, 12, 12, 4).__str__(), 'Year: 2012, Month: 9, HolidaysLeftBeginMonth: 12d, HolidaysLeft: 12d, WorkingHoursAccountBeginMonth: 12s, WorkingHoursAccount: 12s, MonthlyTarget: 86.6h, WorkingHoursBalance: -86.6h, Protocol: []')

    def test_append(self):
        # although calculating in unixtime we use small numbers for testing

        epoc = int(time.time())
        hour = 3600

        test_entries = [
                    ['e', 12, 4 * hour, None, None, 'testtätigkeit'],   # duration given 
                    ['e', 13, None, epoc , epoc + 3 * hour, 'testtätigkeit'], # fromto given
                    ['e', 14, 3600, 100 , 3700, 'testtätigkeit'], # both given
                    ['e', 15, 100 * hour, 0, 0, 'long run'],
                    ['h', 16],
                    ['h', 17],
                    ['i', 18]
        ]
    
        month = Month(0, 0, 10, 0, 4)

        for entry in test_entries:
            month.append(*entry)
            print(50 * '*', '\n', month, '\n', 50 * '#')
            print(month.get_dict(), 50 * '*', '\n')


        # only from or to given
        self.assertRaises(ConfusingDataException, month.append, *['e', 2, None, 12, None, 'desc'])
        self.assertRaises(ConfusingDataException, month.append, *['e', 2, None, None, 12, 'desc'])

        # no duration given in a normal entry should use hours_worth_workday
        month.append('e', 2, None, None, None, 'desc')
        self.assertEqual(month.protocol.pop()['duration'], 4 * hour)

        # duration not matching fromto
        self.assertRaises(ConfusingDataException, month.append, *['e', 2, 2, 0, 10, 'desc'])

        # year 12 had a 29th
        month = Month(12,2,0,0)
        month.append('e', 29, 1, 0, 0, 'test')

        month = Month(13,2,0,0)

        # invalid date
        self.assertRaises(InvalidDateException, month.append, *['e', 29, 12, 0, 0, 'desc'])

        # check counting
        m = Month(0,0,20,0,4)
        self.assertEqual(m.holidays_left, 20)

        m.append('h',1)
        self.assertEqual(m.holidays_left, 19)
        self.assertEqual(m.working_hours_account, 4 * 3600)
        
        m.append('h',1,3 * 3600)
        self.assertEqual(m.holidays_left, 18)
        self.assertEqual(m.working_hours_account, 7 * 3600)

        # check target
        m = Month(hours_worth_working_day=6)
        self.assertEqual(m.monthly_target, 129.9)

        m = Month(hours_worth_working_day=8)
        self.assertEqual(m.monthly_target, 173.2)


# vim: ai sts=4 ts=4 sw=4 expandtab
