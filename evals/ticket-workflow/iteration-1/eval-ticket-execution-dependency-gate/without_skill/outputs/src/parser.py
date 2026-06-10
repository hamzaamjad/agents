"""csvtool: minimal CSV row parsing helpers."""

DELIM = ","


def validate_row(fields, expected_count):
    """Return fields unchanged if the count matches, else raise ValueError."""
    if len(fields) != expected_count:
        raise ValueError(
            "expected %d fields, got %d" % (expected_count, len(fields))
        )
    return fields


def parse_row(line, expected_count=None):
    """Split one CSV line into stripped fields (no quoting support yet).

    When expected_count is given, the parsed fields are validated against
    it and a ValueError is raised on a mismatch.
    """
    fields = [field.strip() for field in line.rstrip("\n").split(DELIM)]
    if expected_count is not None:
        return validate_row(fields, expected_count)
    return fields
