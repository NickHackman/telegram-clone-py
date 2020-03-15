# Requests

This is an attempt at emulating `Requests` a `Python` library for HTTP requests,
but with only a few select features.

## Goals

- Emulate [Requests](https://github.com/psf/requests)
- Support HTTP and HTTPs
- Support sending and recieving `JSON` payloads
- Performant, but mainly satisifies project goals

## Files

### Client

- Directly utilizes the socket to send a recieve data from it
- Constructs Header (to send) and Response (when recieving)

### Header

- Fields necessary to send data to a server

### ResponseParser

Parses the servers Response into necessary fields

- Header
- JSON
- Status Code
- HTTP Version

### Response

an HTTP Response sent from the server

#### StatusCode

An `Enum` representing the Status Code as a Tuple[int, str]

#### Header

A python `Dict[str, str]` that stores all key value pairs in the Respone's
header section. Doesn't include the first line of Header, those are separate fields.

#### HTTP Version

Version of HTTP used by Server _usually_ `HTTP/1.1`

#### JSON

Payload of response is expected to be `JSON` and therefore is loaded from the
`Python str`

### Example

```python
import requests

# GET, PUT, POST and DELETE all have their own methods
# If they don't satisfy your needs then use the bare `request`
response: requests.Response = requests.get("www.google.com")

# Error handling
response.raise_for_status() # Either throws an exception or does nothing

if response.is_error():
    (code, reason) = response.status_code.value # unpack the StatusCode
    raise Exception(f"Error: {reason}")
```

## Performance Issues

| Issue                                                       | Rationale                                     | Severity   |
| ----------------------------------------------------------- | --------------------------------------------- | ---------- |
| Parses entire response for every Request                    | Seemed like the most straightforward approach | **High**   |
| Completely Synchronous                                      | Easier than async alternative                 | **High**   |
| `Recv` bytes is a constant integer value and doesn't change | Naive implementation                          | **Medium** |
