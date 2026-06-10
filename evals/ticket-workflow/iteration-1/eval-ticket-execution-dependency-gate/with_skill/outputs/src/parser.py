"""csvtool: minimal CSV row parsing helpers."""

DELIM = ","


def validate_row(fields, expected_count):
    """Return fields unchanged; raise ValueError if the field count differs."""
    if len(fields) != expected_count:
        raise ValueError(
            f"row has {len(fields)} fields, expected {expected_count}"
        )
    return fields


def parse_row(line, expected_count=None):
    """Split one CSV line into stripped fields (no quoting support yet).

    When expected_count is given, the parsed fields are validated with
    validate_row before being returned.
    """
    fields = [field.strip() for field in line.rstrip("\n").split(DELIM)]
    if expected_count is not None:
        return validate_row(fields, expected_count)
    return fields
