

from inputs import input_columns, captures
from difflib import get_close_matches


inputs_normalized = [i.lower() for i in input_columns]
captures_normalized = [i.lower() for i in captures]

def input_matcher(field, cutoff=0.8) -> str|None:
    "Returns the field name if it matches the input from the spec"
    field_normalized = field.lower()
    if (match := get_close_matches(field_normalized, inputs_normalized, 1, cutoff=cutoff)):
        match_index = inputs_normalized.index(match[0])
        input_name = input_columns[match_index]
        return input_name
    return None

def capture_matcher(field, cutoff=0.8) -> str|None:
    "Returns the field name if it matches the capture from the spec"
    field_normalized = field.lower()
    if (match := get_close_matches(field_normalized, captures_normalized, 1, cutoff=cutoff)):
        match_index = captures_normalized.index(match[0])
        capture_name = captures[match_index]
        return capture_name
    return None