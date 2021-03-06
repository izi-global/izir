[![IZIR](https://raw.github.com/izi-global/izir/develop/artwork/logo.png)](http://izi.rest)
===================

[![PyPI version](https://badge.fury.io/py/izir.svg)](http://badge.fury.io/py/izir)
[![Build Status](https://travis-ci.org/izi-global/izi.svg?branch=master)](https://travis-ci.org/izi-global/izir)
[![Windows Build Status](https://ci.appveyor.com/api/projects/status/0h7ynsqrbaxs7hfm/branch/master?svg=true)](https://ci.appveyor.com/project/izi-global/izir)
[![Coverage Status](https://coveralls.io/repos/izi-global/izi/badge.svg?branch=master&service=github)](https://coveralls.io/github/izi-global/izi?branch=master)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/izi/)
[![Join the chat at https://gitter.im/izi-global/izi](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/izi-global/izi?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

NOTE: For more in-depth documentation visit [izi's website](http://www.izi.rest)

izi aims to make developing Python driven APIs as simple as possible, but no simpler. As a result, it drastically simplifies Python API development.

izi's Design Objectives:

- Make developing a Python driven API as succinct as a written definition.
- The framework should encourage code that self-documents.
- It should be fast. A developer should never feel the need to look somewhere else for performance reasons.
- Writing tests for APIs written on-top of izi should be easy and intuitive.
- Magic done once, in an API framework, is better than pushing the problem set to the user of the API framework.
- Be the basis for next generation Python APIs, embracing the latest technology.

As a result of these goals, izi is Python 3+ only and built upon [Falcon's](https://github.com/falconry/falcon) high performance HTTP library

[![IZIR Hello World Example](https://raw.github.com/izi-global/izir/develop/artwork/example.gif)](https://github.com/izi-global/izir/blob/develop/examples/hello_world.py)


Installing izi
===================

Installing izi is as simple as:

```bash
pip3 install izir --upgrade
```

Ideally, within a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/).


Getting Started
===================
Build an example API with a simple endpoint in just a few lines.

```py
# filename: happy_birthday.py
"""A basic (single function) API written using izi"""
import izi


@izi.get('/happy_birthday')
def happy_birthday(name, age:izi.types.number=1):
    """Says happy birthday to a user"""
    return "Happy {age} Birthday {name}!".format(**locals())
```

To run, from the command line type:

```bash
izi -f happy_birthday.py
```

You can access the example in your browser at:
`localhost:8000/happy_birthday?name=izi&age=1`. Then check out the
documentation for your API at `localhost:8000/documentation`

Parameters can also be encoded in the URL (check
out [`happy_birthday.py`](examples/happy_birthday.py) for the whole
example).

```py
@izi.get('/greet/{event}')
def greet(event: str):
    """Greets appropriately (from http://blog.ketchum.com/how-to-write-10-common-holiday-greetings/)  """
    greetings = "Happy"
    if event == "Christmas":
        greetings = "Merry"
    if event == "Kwanzaa":
        greetings = "Joyous"
    if event == "wishes":
        greetings = "Warm"

    return "{greetings} {event}!".format(**locals())
```

Which, once you are running the server as above, you can use this way:

```
curl http://localhost:8000/greet/wishes
"Warm wishes!"
```

Versioning with izi
===================

```py
# filename: versioning_example.py
"""A simple example of a izi API call with versioning"""
import izi

@izi.get('/echo', versions=1)
def echo(text):
    return text


@izi.get('/echo', versions=range(2, 5))
def echo(text):
    return "Echo: {text}".format(**locals())
```

To run the example:

```bash
izi -f versioning_example.py
```

Then you can access the example from `localhost:8000/v1/echo?text=Hi` / `localhost:8000/v2/echo?text=Hi` Or access the documentation for your API from `localhost:8000`

Note: versioning in izi automatically supports both the version header as well as direct URL based specification.


Testing izi APIs
===================

izi's `http` method decorators don't modify your original functions. This makes testing izi APIs as simple as testing any other Python functions. Additionally, this means interacting with your API functions in other Python code is as straight forward as calling Python only API functions. izi makes it easy to test the full Python stack of your API by using the `izi.test` module:

```python
import izi
import happy_birthday

izi.test.get(happy_birthday, 'happy_birthday', {'name': 'ViTuocGia', 'age': 25}) # Returns a Response object
```

You can use this `Response` object for test assertions (check
out [`test_happy_birthday.py`](examples/test_happy_birthday.py) ):

```python
def tests_happy_birthday():
    response = izi.test.get(happy_birthday, 'happy_birthday', {'name': 'ViTuocGia', 'age': 25})
    assert response.status == HTTP_200
    assert response.data is not None
``` 


Running izi with other WSGI based servers
===================

izi exposes a `__izi_wsgi__` magic method on every API module automatically. Running your izi based API on any standard wsgi server should be as simple as pointing it to `module_name`: `__izi_wsgi__`.

For Example:

```bash
uwsgi --http 0.0.0.0:8000 --wsgi-file examples/hello_world.py --callable __izi_wsgi__
```

To run the hello world izi example API.


Building Blocks of a izi API
===================

When building an API using the izi framework you'll use the following concepts:

**METHOD Decorators** `get`, `post`, `update`, etc HTTP method decorators that expose your Python function as an API while keeping your Python method unchanged

```py
@izi.get() # <- Is the izi METHOD decorator
def hello_world():
    return "Hello"
```

izi uses the structure of the function you decorate to automatically generate documentation for users of your API. izi always passes a request, response, and api_version variable to your function if they are defined params in your function definition.

**Type Annotations** functions that optionally are attached to your methods arguments to specify how the argument is validated and converted into a Python type

```py
@izi.get()
def math(number_1:int, number_2:int): #The :int after both arguments is the Type Annotation
    return number_1 + number_2
```

Type annotations also feed into `izi`'s automatic documentation
generation to let users of your API know what data to supply. 


**Directives** functions that get executed with the request / response data based on being requested as an argument in your api_function.
These apply as input parameters only, and can not be applied currently as output formats or transformations.

```py
@izi.get()
def test_time(izi_timer):
    return {'time_taken': float(izi_timer)}
```

Directives may be accessed via an argument with a `izi_` prefix, or by using Python 3 type annotations. The latter is the more modern approach, and is recommended. Directives declared in a module can be accessed by using their fully qualified name as the type annotation (ex: `module.directive_name`).

Aside from the obvious input transformation use case, directives can be used to pipe data into your API functions, even if they are not present in the request query string, POST body, etc. For an example of how to use directives in this way, see the authentication example in the examples folder.

Adding your own directives is straight forward:

```py
@izi.directive()
def square(value=1, **kwargs):
    '''Returns passed in parameter multiplied by itself'''
    return value * value

@izi.get()
@izi.local()
def tester(value: square=10):
    return value

tester() == 100
```

For completeness, here is an example of accessing the directive via the magic name approach:

```py
@izi.directive()
def multiply(value=1, **kwargs):
    '''Returns passed in parameter multiplied by itself'''
    return value * value

@izi.get()
@izi.local()
def tester(izi_multiply=10):
    return izi_multiply

tester() == 100
```

**Output Formatters** a function that takes the output of your API function and formats it for transport to the user of the API.

```py
@izi.default_output_format()
def my_output_formatter(data):
    return "STRING:{0}".format(data)

@izi.get(output=izi.output_format.json)
def hello():
    return {'hello': 'world'}
```

as shown, you can easily change the output format for both an entire API as well as an individual API call


**Input Formatters** a function that takes the body of data given from a user of your API and formats it for handling.

```py
@izi.default_input_format("application/json")
def my_input_formatter(data):
    return ('Results', izi.input_format.json(data))
```

Input formatters are mapped based on the `content_type` of the request data, and only perform basic parsing. More detailed parsing should be done by the Type Annotations present on your `api_function`


**Middleware** functions that get called for every request a izi API processes

```py
@izi.request_middleware()
def process_data(request, response):
    request.env['SERVER_NAME'] = 'changed'

@izi.response_middleware()
def process_data(request, response, resource):
    response.set_header('MyHeader', 'Value')
```

You can also easily add any Falcon style middleware using:

```py
__izi__.http.add_middleware(MiddlewareObject())
```


Splitting APIs over multiple files
===================

izi enables you to organize large projects in any manner you see fit. You can import any module that contains izi decorated functions (request handling, directives, type handlers, etc) and extend your base API with that module.

For example:

`something.py`

```py
import izi

@izi.get('/')
def say_hi():
    return 'hello from something'
```

Can be imported into the main API file:

`__init__.py`

```py
import izi
from . import something

@izi.get('/')
def say_hi():
    return "Hi from root"

@izi.extend_api('/something')
def something_api():
    return [something]
```

Or alternatively - for cases like this - where only one module is being included per a URL route:

```py
#alternatively
izi.API(__name__).extend(something, '/something')
```


Configuring izi 404
===================

By default, izi returns an auto generated API spec when a user tries to access an endpoint that isn't defined. If you would not like to return this spec you can turn off 404 documentation:

From the command line application:

```bash
izi -nd -f {file} #nd flag tells izi not to generate documentation on 404
```

Additionally, you can easily create a custom 404 handler using the `izi.not_found` decorator:

```py
@izi.not_found()
def not_found_handler():
    return "Not Found"
```

This decorator works in the same manner as the izi HTTP method decorators, and is even version aware:

```py
@izi.not_found(versions=1)
def not_found_handler():
    return ""

@izi.not_found(versions=2)
def not_found_handler():
    return "Not Found"
```


Asyncio support
===============

When using the `get` and `cli` method decorator on coroutines, izi will schedule
the execution of the coroutine.

Using asyncio coroutine decorator
```py
@izi.get()
@asyncio.coroutine
def hello_world():
    return "Hello"
```

Using Python 3.5 async keyword.
```py
@izi.get()
async def hello_world():
    return "Hello"
```

NOTE: IZIR is running on top Falcon which is not an asynchronous server. Even if using
asyncio, requests will still be processed synchronously.


Using Docker
===================
If you like to develop in Docker and keep your system clean, you can do that but you'll need to first install [Docker Compose](https://docs.docker.com/compose/install/).

Once you've done that, you'll need to `cd` into the `docker` directory and run the web server (Gunicorn) specified in `./docker/gunicorn/Dockerfile`, after which you can preview the output of your API in the browser on your host machine.

```bash
$ cd ./docker
# This will run Gunicorn on port 8000 of the Docker container.
$ docker-compose up gunicorn

# From the host machine, find your Dockers IP address.
# For Windows & Mac:
$ docker-machine ip default

# For Linux:
$ ifconfig docker0 | grep 'inet' | cut -d: -f2 | awk '{ print $1}' | head -n1
```

By default, the IP is 172.17.0.1. Assuming that's the IP you see, as well, you would then go to `http://172.17.0.1:8000/` in your browser to view your API.

You can also log into a Docker container that you can consider your work space. This workspace has Python and Pip installed so you can use those tools within Docker. If you need to test the CLI interface, for example, you would use this.

```bash
$ docker-compose run workspace bash
```

On your Docker `workspace` container, the `./docker/templates` directory on your host computer is mounted to `/src` in the Docker container. This is specified under `services` > `app` of `./docker/docker-compose.yml`.

```bash
bash-4.3# cd /src
bash-4.3# tree
.
├── __init__.py
└── handlers
    ├── birthday.py
    └── hello.py

1 directory, 3 files
```


Why izi?
===================

This represents the project's goal to help guide developers into creating well written and intuitive APIs.

--------------------------------------------

Thanks and I hope you find *this* izi helpful as you develop your next Python API!

~DiepDT
