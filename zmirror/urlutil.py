from urllib.parse import urlparse, parse_qsl, urlencode


def clean_and_sort_url(url):
    """Reduce a url to a stable cache key.

    Drops the scheme and host, sorts the query parameters so that orderings
    differing only by parameter order share a key, and discards 'q' because it
    carries the user's search terms rather than identifying the page.
    """
    parsed = urlparse(url)

    query_params = parse_qsl(parsed.query, keep_blank_values=True)
    filtered_sorted_params = sorted(
        [(k, v) for k, v in query_params if k != 'q']
    )

    new_query = urlencode(filtered_sorted_params)

    if new_query:
        return '{}?{}'.format(parsed.path, new_query)
    return parsed.path
