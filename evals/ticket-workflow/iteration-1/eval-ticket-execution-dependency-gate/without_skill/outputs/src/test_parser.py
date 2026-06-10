import unittest

from parser import parse_row, validate_row


class TestParseRow(unittest.TestCase):
    def test_basic_split(self):
        self.assertEqual(parse_row("a,b,c\n"), ["a", "b", "c"])

    def test_strips_whitespace(self):
        self.assertEqual(parse_row(" a , b ,c"), ["a", "b", "c"])

    def test_expected_count_match(self):
        self.assertEqual(parse_row("a,b", expected_count=2), ["a", "b"])

    def test_expected_count_mismatch(self):
        with self.assertRaises(ValueError):
            parse_row("a,b", expected_count=3)


class TestValidateRow(unittest.TestCase):
    def test_returns_fields_unchanged(self):
        fields = ["a", "b", "c"]
        self.assertIs(validate_row(fields, 3), fields)

    def test_mismatch_raises_with_both_counts(self):
        with self.assertRaises(ValueError) as ctx:
            validate_row(["a", "b"], 3)
        message = str(ctx.exception)
        self.assertIn("3", message)
        self.assertIn("2", message)


if __name__ == "__main__":
    unittest.main()
