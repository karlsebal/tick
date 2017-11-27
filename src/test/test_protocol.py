import unittest
from protocol import Protocol 
from protocol import InvalidDateException
import time

class TestProtocol(unittest.TestCase):
    
    def testInit(self):
        current_year = time.localtime().tm_year
        current_month = time.localtime().tm_mon

        invalid_datestrings = [
                            "00jj",
                            "jj",
                            "1144",
                            "0044",
                            "201713",
                            "123",
                            "201700",
                            "1700",
                            "1723",
                            '13',
                            '0',
                            '111'
                            ]

        for invalid_date in invalid_datestrings:
            print('test invalid date: %r' % invalid_date)
            self.assertRaises(InvalidDateException, Protocol, month=invalid_date)

        # without parameters year must be set to current
        self.assertEqual(Protocol().year, current_year)
        self.assertEqual(Protocol().month, current_month)

        p = Protocol(month='11')

        self.assertEqual(p.month, 11)
        self.assertEqual(p.year, current_year)

        p = Protocol(month='1')

        self.assertEqual(p.month, 1)
        self.assertEqual(p.year, current_year)

        p = Protocol(month='2012')

        self.assertEqual(p.month, 12)
        self.assertEqual(p.year, 2020)

# vim: ai sts=4 ts=4 sw=4 expandtab
