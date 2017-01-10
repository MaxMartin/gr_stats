import unittest
from datetime import datetime

from gr_stats import data_builder

class GrStatsTest(unittest.TestCase):
    def test_month_hist_empty_list(self):
        self.assertEqual([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            data_builder.month_histogram([]))

    def test_month_hist_one_date(self):
        self.assertEqual([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            data_builder.month_histogram([(datetime(2000, 1, 1), 0)]))

    def test_month_hist_some_dates(self):
        dates = [(datetime(2000, 1, 1), 0),
                 (datetime(2000, 2, 1), 0),
                 (datetime(2000, 3, 1), 0),
                 (datetime(2000, 4, 1), 0),
                 (datetime(2000, 6, 1), 0),
                 (datetime(2000, 6, 2), 0),
                 (datetime(2000, 7, 1), 0),
                 (datetime(2000, 9, 1), 0),
                 (datetime(2000, 9, 3), 0),
                 (datetime(2000, 9, 6), 0)
                 ]
        self.assertEqual([1, 1, 1, 1, 0, 2, 1, 0, 3, 0, 0, 0],
            data_builder.month_histogram(dates))

    def test_month_hist_pages_zero_pages(self):
        dates = [(datetime(2000, 1, 1), 0),
                 (datetime(2000, 2, 1), 0),
                 (datetime(2000, 3, 1), 0),
                 (datetime(2000, 4, 1), 0),
                 (datetime(2000, 6, 1), 0),
                 (datetime(2000, 6, 2), 0),
                 (datetime(2000, 7, 1), 0),
                 (datetime(2000, 9, 1), 0),
                 (datetime(2000, 9, 3), 0),
                 (datetime(2000, 9, 6), 0)
                 ]
        self.assertEqual([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            data_builder.month_histogram(dates, pages=True))

    def test_month_hist_pages_nonzero_pages(self):
        dates = [(datetime(2000, 1, 1), 10),
                 (datetime(2000, 2, 1), 10),
                 (datetime(2000, 3, 1), 10),
                 (datetime(2000, 4, 1), 10),
                 (datetime(2000, 6, 1), 10),
                 (datetime(2000, 6, 2), 10),
                 (datetime(2000, 7, 1), 10),
                 (datetime(2000, 9, 1), 10),
                 (datetime(2000, 9, 3), 10),
                 (datetime(2000, 9, 6), 10)
                 ]
        self.assertEqual([10, 10, 10, 10, 0, 20, 10, 0, 30, 0, 0, 0],
            data_builder.month_histogram(dates, pages=True))

if __name__ == "__main__":
    unittest.main()
