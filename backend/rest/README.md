# Rest

Attempt to emulate `Flask` a `Python` Web App Framework

## Goals

- Emulate [Flask](https://github.com/pallets/flask)
- Support JSON Responses
- Allow `GET`, `PUT`, `POST` and `DELETE` Requests
- Support `404` and `200` status codes
- Asynchronous to allow for many clients
- Use configuration file to allow for designating port and host url

## Examples

```python
from typing import Dict, Any

from rest import Rest, Method


rest: Rest = Rest("./path_to_config_file")

@rest.route("/", Method.GET)
def hello_world() -> Dict[Any, Any]:
    return {"response": "Hello, World"}

# int:age dictates the type, otherwise type is assumed to be str
@rest.route("/<name>/<int:age>", Method.GET)
def name_age(name: str, age: int) -> Dict[Any, Any]:
    return {"response": f"Hello, {name} you are {age} years old"}

# POST and PUT requests pass in a payload which is just a Python Dict
@rest.route("/", Method.POST)
def add_one(payload: Dict[Any, Any]) -> Dict[Any, Any]:
    # payload #=> { "number": 6 }
    return {"response": f"you entered {payload['number'] + 1}"}

@rest.route("/<str:name>", Method.PUT)
def create_user(name: str, payload: Dict[Any, Any]) -> Dict[Any, Any]:
    user = User(name, payload["age"], payload["address"])
    # Convert object to Dict to ensure JSON Serializable
    return user.__dict__

# Run event loop
rest.run()
```

## Config

Configuration file to be passed into `Rest(here)` to establish the environment.
Fields are listed below with their domain of values

### host

IP address to be used to host server

### port

Port number to be used, generally for debugging `5000+` is suggested

### mode

| Value        | Explanation                             |
| ------------ | --------------------------------------- |
| "debug"      | Prints to the console and to a log file |
| "production" | Logs only to specified file             |

### log_file

`Path` to file to log to

### secret

Super secret passcode that should not be shared, provided to `JWT`

### websocket_port

This is a hack, as a result of writing a custom HTTP Requests server, in order
to use the same port and IP address it would require writing my own `Websocket`
implementation as well, only way to get around that and use a library, such as
`websockets` is to use a different port

### Example

```json
{
  "host": "127.0.0.1",
  "port": 8888,
  "mode": "debug",
  "log_file": "log_file.txt",
  "secret": "super_secret_passcodes",
  "websocket_port": 8889
}
```

## Stretch Goals

- Allow for `HTTPs` support via something similar to `Flask` 'adhoc' argument
