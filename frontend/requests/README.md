# Requests

This is an attempt at emulating `Requests` a `Python` library for HTTP requests,
but with only a few select features.

## Goals

- Emulate [Requests](https://github.com/psf/requests)
- Support HTTP and HTTPs
- Support sending and recieving `JSON` payloads

## Documentation

### requests.request

```python
import requests
# Import Method for ease of use
from requests import Method

response: requests.Response = requests.requests("https://www.google.com", Method.GET)
```

Main entry point into library, as a generic way to make `HTTP` requests, but
used sparingly preferring `requests.get()`, `requests.put()`, `requests.post()`,
and `requests.delete()`. All of which are solely wrappers around `requests.request()`.

### Method

| Variant | Corresponding HTTP Request |
| ------- | -------------------------- |
| GET     | "GET"                      |
| PUT     | "PUT"                      |
| POST    | "POST                      |
| DELETE  | "DELETE"                   |
| HEAD    | **unsupported**            |
| PATCH   | **unsupported**            |

### requests.Response

Returned from every entry point to `requests`, behaves very closely to [Requests](https://github.com/psf/requests)

| Attribute    | Type           | Purpose                                                                                                                      |
| ------------ | -------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| status_code  | StatusCode     | Tuple[int, str] that describes the status                                                                                    |
| http_version | str            | Version of HTTP Response usually `HTTP/1.1` or `HTTP/2`                                                                      |
| header       | Dict[str, str] | The header parsed into it's corresponding values, note arrays aren't parsed as such but as `str` for the sake of performance |
| json         | Dict[Any, Any] | Payload of `Response` parsed as `JSON`                                                                                       |

### requests.StatusCode

A Tuple representing the status of an `HTTP` request, for instance

```python
(200, "OK")
```

In order to get the actual status code integer it must be unpacked

```python
import requests

response: requests.StatusCode = requests.get("https://www.google.com")

status_code = response.status_code
(code, reason) = status_code.value
```

Majority of the time though, the actual code isn't necessary so there are
methods part of `requests.Response` that handle error checking

```python
import requests

response: requests.Response = requests.get("https://www.google.com")

# If the error isn't a 200 or 100 it will raise an HTTPError
# NOTE: HTTPError has a reference to the requests.Response that caused it
try:
    response.raise_for_status()
except HTTPError as http_error:
    # use http_error
```

If you'd rather raise your own `Exception` then you can do an if check

```python
import requests

response: requests.Response = requests.get("https://www.google.com")

# If the error isn't a 200 or 100 it will raise YourOwnException
if response.is_error():
    raise YourOwnException("reason")
```

## Performance Issues

| Issue                                                       | Rationale                                     | Severity   |
| ----------------------------------------------------------- | --------------------------------------------- | ---------- |
| Parses entire response for every Request                    | Seemed like the most straightforward approach | **High**   |
| Completely Synchronous                                      | Easier than async alternative                 | **High**   |
| `Recv` bytes is a constant integer value and doesn't change | Naive implementation                          | **Medium** |
