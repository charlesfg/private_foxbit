import unittest
from unittest import TestCase

from utils import uts_from_timestr, dt_str_to_uts


class TestUts_from_timestr(TestCase):


    def test_positive_second(self):

        tt  = '2017-03-09 12:38:00'
        u = uts_from_timestr('+40s', tt)
        uts_from_str = dt_str_to_uts("2017-03-09 12:38:40")

        self.assertEqual(u, uts_from_str)

    def test_positive_without_second(self):

        tt  = '2017-03-09 12:38:00'
        u = uts_from_timestr('+40', tt)
        uts_from_str = dt_str_to_uts("2017-03-09 12:38:40")

        self.assertEqual(u, uts_from_str)

    def test_negative_second(self):

        tt  = '2017-03-09 12:38:40'
        u = uts_from_timestr('-40s', tt)
        uts_from_str = dt_str_to_uts("2017-03-09 12:38:00")

        self.assertEqual(u, uts_from_str)

    def test_negative_without_second(self):

        tt  = '2017-03-09 12:38:40'
        u = uts_from_timestr('-40', tt)
        uts_from_str = dt_str_to_uts("2017-03-09 12:38:00")

        self.assertEqual(u, uts_from_str)

    def test_negative_minutes(self):

        tt  = '2017-03-09 00:40:00'
        u = uts_from_timestr('-40m', tt)
        uts_from_str = dt_str_to_uts("2017-03-09 00:00:00")

        self.assertEqual(u, uts_from_str)

    def test_negative_hours(self):

        tt  = '2017-03-09 04:40:00'
        u = uts_from_timestr('-4h', tt)
        uts_from_str = dt_str_to_uts("2017-03-09 00:40:00")

        self.assertEqual(u, uts_from_str)

    def test_negative_days(self):
        tt = '2017-03-09 04:40:00'
        u = uts_from_timestr('-8d', tt)
        uts_from_str = dt_str_to_uts("2017-03-01 04:40:00")

        self.assertEqual(u, uts_from_str)

    def test_positive_minutes(self):

        tt  = '2017-03-09 00:00:00'
        u = uts_from_timestr('120m', tt)
        uts_from_str = dt_str_to_uts("2017-03-09 02:00:00")

        self.assertEqual(u, uts_from_str)

    def test_positive_hours(self):

        tt  = '2017-03-09 04:40:00'
        u = uts_from_timestr('+40h', tt)
        uts_from_str = dt_str_to_uts("2017-03-10 20:40:00")

        self.assertEqual(u, uts_from_str)

    def test_positive_days(self):
        tt = "2017-03-09 04:40:00"
        u = uts_from_timestr('364d', tt)
        uts_from_str = dt_str_to_uts('2018-03-08 04:40:00')

        self.assertEqual(u, uts_from_str)


if __name__ == '__main__':
    unittest.main()