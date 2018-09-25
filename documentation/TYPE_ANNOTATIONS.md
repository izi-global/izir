Type annotations in izi
=======================

izi leverages Python3 type annotations for validation and API specification. Within the context of izi, annotations should be set to one of 4 things:

 - A cast function, built-in, or your own (str, int, etc) that takes a value casts it and then returns it, raising an exception if it is not in a format that can be cast into the desired type
 - A izi type (izi.types.text, izi.types.number, etc.). These are essentially built-in cast functions that provide more contextual information, and good default error messages
 - A [marshmallow](https://marshmallow.readthedocs.org/en/latest/) type and/or schema. In izi 2.0.0 Marshmallow is a first class citizen in izi, and all fields and schemas defined with it can be used in izi as type annotations
 - A string. When a basic Python string is set as the type annotation it is used by izi to generate documentation, but does not get applied during the validation phase

For example:

    import izi


    @izi.get()
    def hello(first_name: izi.types.text, last_name: 'Family Name', age: int):
        print("Hi {0} {1}!".format(first_name, last_name)

is a valid izi endpoint.

Any time a type annotation raises an exception during casting of a type, it is seen as a failure. Otherwise the cast is assumed successful with the returned type replacing the passed-in parameter. By default, all errors are collected in an errors dictionary and returned as the output of the endpoint before the routed function ever gets called. To change how errors are returned you can transform them via the `on_invalid` route option, and specify a specific output format for errors by specifying the `output_invalid` route option. Or, if you prefer, you can keep izi from handling the validation errors at all by passing in `raise_on_invalid=True` to the route.

Built in izi types
==================

izi provides several built-in types for common API use cases:

 - `number`: Validates that a whole number was passed in
 - `float_number`: Validates that a valid floating point number was passed in
 - `decimal`: Validates and converts the provided value into a Python Decimal object
 - `uuid`: Validates that the provided value is a valid UUID
 - `text`: Validates that the provided value is a single string parameter
 - `multiple`: Ensures the parameter is passed in as a list (even if only one value is passed in)
 - `boolean`: A basic naive HTTP style boolean where no value passed in is seen as `False` and any value passed in (even if its `false`) is seen as `True`
 - `smart_boolean`: A smarter, but more computentionally expensive, boolean that checks the content of the value for common true / false formats (true, True, t, 1) or (false, False, f, 0)
 - `delimited_list(delimiter)`: splits up the passed in value based on the provided delimiter and then passes it to the function as a list
 - `one_of(values)`: Validates that the passed in value is one of those specified
 - `mapping(dict_of_passed_in_to_desired_values)`: Like `one_of`, but with a dictionary of acceptable values, to converted value.
 - `multi(types)`: Allows passing in multiple acceptable types for a parameter, short circuiting on the first acceptable one
 - `in_range(lower, upper, convert=number)`: Accepts a number within a lower and upper bound of acceptable values
 - `less_than(limit, convert=number)`: Accepts a number within a lower and upper bound of acceptable values
 - `greater_than(minimum, convert=number)`: Accepts a value above a given minimum
 - `length(lower, upper, convert=text)`: Accepts a a value that is within a specific length limit
 - `shorter_than(limit, convert=text)`: Accepts a text value shorter than the specified length limit
 - `longer_than(limit, convert=text)`: Accepts a value up to the specified limit
 - `cut_off(limit, convert=text)`: Cuts off the provided value at the specified index

Extending and creating new izi types
====================================

The most obvious way to extend a izi type is to simply inherit from the base type defined in `izi.types` and then override `__call__` to override how the cast function, or override `__init__` to override what parameters the type takes:

    import izi


    class TheAnswer(izi.types.number):
        """My new documentation"""

        def __call__(self, value):
            value = super().__call__(value)
            if value != 42:
                raise ValueError('Value is not the answer to everything.')
            return value

If you simply want to perform additional conversion after a base type is finished, or modify its documentation, the most succinct way is the `izi.type` decorator:

    import izi


    @izi.type(extend=izi.types.number)
    def the_answer(value):
        """My new documentation"""
        if value != 42:
            raise ValueError('Value is not the answer to everything.')
        return value


Marshmallow integration
=======================

[Marshmallow](https://marshmallow.readthedocs.org/en/latest/) is an advanced serialization, deserialization, and validation library. IZIR supports using marshmallow fields and schemas as input types.

Here is a simple example of an API that does datetime addition.


    import datetime as dt

    import izi
    from marshmallow import fields
    from marshmallow.validate import Range


    @izi.get('/dateadd', examples="value=1973-04-10&addend=63")
    def dateadd(value: fields.DateTime(),
                addend: fields.Int(validate=Range(min=1))):
        """Add a value to a date."""
        delta = dt.timedelta(days=addend)
        result = value + delta
        return {'result': result}
