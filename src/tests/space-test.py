import unittest

import space as s


class TestSpace(unittest.TestCase):
    """Test space functions."""

    def testsPoint(self) -> None:
        """Test functions using Point."""
        p: s.Point = s.Point(0, 0)
        self.assertEqual(s.offset_to_point_in_region(p, s.Point(1, 5), 11), s.Point(1, 5))
        self.assertEqual(s.offset_to_point_in_region(p, s.Point(1, 5), 8), s.Point(1, 2))
        self.assertEqual(s.area(s.Point(0, 0), s.Point(3, 5)), 4 * 6)


if __name__ == '__main__':
    unittest.main()
