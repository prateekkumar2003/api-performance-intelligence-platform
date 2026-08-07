import re


def normalize_query(query):

    # Replace numbers
    query = re.sub(r'\b\d+\b', '?', query)

    # Replace quoted strings
    query = re.sub(r"'[^']*'", "?", query)

    return query.strip()