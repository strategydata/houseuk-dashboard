from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


def update_param(url, param_name, increment):
    """The function `update_param` updates a specified parameter in a URL by incrementing its value by a
    given amount.

    Parameters
    ----------
    url
        The `url` parameter is the URL string that you want to update by modifying or adding a query
    parameter.
    param_name
        param_name is the name of the parameter in the URL query string that you want to update or
    increment.
    increment
        The `increment` parameter is the value by which you want to increment the specified parameter in
    the URL.

    Returns
    -------
        The function `update_param` takes a URL, a parameter name, and an increment value as input, and
    updates the specified parameter in the URL by incrementing its value by the provided increment. It
    then returns the updated URL with the modified parameter.

    """
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    if "index" in query_params:
        try:
            current_value = int(query_params["index"][0])
        except (ValueError, IndexError):
            current_value = 0
        query_params[param_name] = [str(current_value + int(increment))]
    else:
        query_params[param_name] = [str(increment)]

    new_query = urlencode(query_params, doseq=True)
    return urlunparse(parsed._replace(query=new_query))
