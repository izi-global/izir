Routing in izi
==============

The most basic function of any framework meant to enable external interaction with an API, is routing how the external
interaction will correspond to internal function calls and business logic. izi provides flexible and powerful routers
that aim to scale intuitively from simple use-cases to complex.

To enable this all izi routers share 3 attributes:

 - Can be used directly as function decorators
 - Can be used separately from the function
 - Can be stored, modified, and chained before being used

And, while izi uses functions in most of its examples, it supports applying routes to methods and objects as well. All izi routers enforce type annotation
and enable automatic argument supplying via directives.

Using a router as a decorator
=============================

The most basic use case is to simply define the route directly above the function you need to expose as a decorator:

    import izi


    @izi.get('/home')
    def root():
        return 'Welcome home!'

This is clear, explicit, and obvious. As such, this is recommended for most basic APIs.

Declaring a router separate from a function
===========================================

Sometimes, in more complex use-cases, it's necessary to define routing separate from where the code itself is defined.
izi aims to make this as easy and intuitive as it can be:

Internal API:

    # internal.py


    def root():
        return 'Welcome home!'

External API:

    # external.py
    import izi

    import internal

    router = izi.route.API(__name__)
    router.get('/home')(internal.root)

Or, alternatively:

    # external.py
    import izi

    import internal

    api = izi.API(__name__)
    izi.get('/home', api=api)(internal.root)

Chaining routers for easy re-use
================================

A very common scenario when using izi routers, because they are so powerful, is duplication between routers.
For instance: if you decide you want every route to return the 404 page when a validation error occurs or you want to
require validation for a collection of routes. izi makes this extremely simple by allowing all routes to be chained
and reused:

    import izi

    api = izi.get(on_invalid=izi.redirect.not_found)


    @api.urls('/do-math', examples='number_1=1&number_2=2')
    def math(number_1: izi.types.number, number_2: izi.types.number):
        return number_1 + number_2


    @api
    def happy_birthday(name, age: izi.types.number):
        """Says happy birthday to a user"""
        return "Happy {age} Birthday {name}!".format(**locals())

It's important to note that to chain you simply call the argument you would normally pass in to the routers init function
as a method on the existing router. Then you pass in any additional parameters you would like to override as **kwargs - as
shown in the math example above.

Common router parameters
========================

There are a few parameters that are shared between all router types, as they are globally applicable to all currently supported interfaces:

 - `api`: The API to register the route with. You can always retrieve the API singleton for the current module by doing `izi.API(__name__)`
 - `transform`: A function to call on the the data returned by the function to transform it in some way specific to this interface
 - `output`: An output format to apply to the outputted data (after return and optional transformation)
 - `requires`: A list or single function that must all return `True` for the function to execute when called via this interface (commonly used for authentication)

HTTP Routers
============

in addition to `izi.http` izi includes convenience decorators for all common HTTP METHODS (`izi.connect`, `izi.delete`, `izi.get`, `izi.head`, `izi.options`, `izi.patch`, `izi.post`, `izi.put`, `izi.get_post`, `izi.put_post`, and `izi.trace`). These methods are functionally the same as calling `@izi.http(accept=(METHOD, ))` and are otherwise identical to the http router.

 - `urls`: A list of or a single URL that should be routed to the function. Supports defining variables within the URL that will automatically be passed to the function when `{}` notation is found in the URL: `/website/{page}`. Defaults to the name of the function being routed to.
 - `accept`: A list of or a single HTTP METHOD value to accept. Defaults to all common HTTP methods.
 - `examples`: A list of or a single example set of parameters in URL query param format. For example: `examples="argument_1=x&argument_2=y"`
 - `versions`: A list of or a single integer version of the API this endpoint supports. To support a range of versions the Python builtin range function can be used.
 - `suffixes`: A list of or a single suffix to add to the end of all URLs using this router.
 - `prefixes`: A list of or a single prefix to add before all URLs using this router.
 - `response_headers`: An optional dictionary of response headers to set automatically on every request to this endpoint.
  - `status`: An optional status code to automatically apply to the response on every request to this endpoint.
 - `parse_body`: If `True` and the format of the request body matches one known by izi, izi will run the specified input formatter on the request body before passing it as an argument to the routed function. Defaults to `True`.
 - `on_invalid`: A transformation function to run outputed data through, only if the request fails validation. Defaults to the endpoints specified general transform function, can be set to not run at all by setting to `None`.
 - `output_invalid`: Specifies an output format to attach to the endpoint only on the case that validation fails. Defaults to the endpoints specified output format.
 - `raise_on_invalid`: If set to true, instead of collecting validation errors in a dictionary, izi will simply raise them as they occur.


Handling for 404 Responses
===========

By default, IZIR will call `documentation_404()` if a user tries to access a nonexistant route when serving. If you want to specify something different, you can use the "sink" decorator, such as in the example below. The `@izi.sink()` decorator serves as a "catch all" for unassigned routes.

```Python 
import izi

@izi.sink('/all')
def my_sink(request):
    return request.path.replace('/all', '')
```

In this case, the server routes requests to anything that's no an assigned route to the landing page. To test the functionality of your sink decorator, serve your application locally, then attempt to access an unassigned route. Using this code, if you try to access `localhost:8000/this-route-is-invalid`, you will be rerouted to `localhost:8000`.


CLI Routing
===========

Any endpoint can also be exposed to the command line as well, using `@izi.cli`:

  - `name`: The name that should execute the command from the command line. Defaults to the name of the function being routed.
  - `version`: The optional version associated with this command line application.
  - `doc`: Documentation to provide to users of this command line tool. Defaults to the functions doc string.


Local Routing
=============

By default all izi APIs are already valid local APIs. However, sometimes it can be useful to apply type annotations and/or directives to local use as well. For these cases izi provides `@izi.local`:

 - `validate`: Apply type annotations to local use of the function. Defaults to `True`.
 - `directives`: Apply directives to local use of the function. Defaults to `True`.
 - `version`: Specify a version of the API for local use. If versions are being used, this generally should be the latest supported.
 - `on_invalid`: A transformation function to run outputed data through, only if the request fails validation. Defaults to the endpoints specified general transform function, can be set to not run at all by setting to `None`.
 - `output_invalid`: Specifies an output format to attach to the endpoint only on the case that validation fails. Defaults to the endpoints specified output format.
 - `raise_on_invalid`: If set to `True`, instead of collecting validation errors in a dictionary, izi will simply raise them as they occur.

NOTE: unlike all other routers, this modifies the function in-place
