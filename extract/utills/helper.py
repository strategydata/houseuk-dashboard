from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def update_param(url, param_name, new_value):
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    query_params[param_name] = [str(new_value)]
    new_query = urlencode(query_params, doseq=True)
    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))
