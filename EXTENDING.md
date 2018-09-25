Building izi extensions
=========
Want to extend izi to tackle new problems? Integrate a new form of authentication? Add new useful types?
Awesome! Here are some guidlines to help you get going and make a world class izi extension
that you will be proud to have showcased to all izi users.

How are extensions built?
=========
izi extensions should be built like any other python project and uploaded to PYPI. What makes a izi extension a *izi* extension is simply it's name and the fact it contains within its Python code utilities and classes that extend izis capabilties.

Naming your extension
=========
All izi extensions should be prefixed with `izi_` for easy disscovery on PYPI. Additionally, there are a few more exact prefixes that can be optionally be added to help steer users to what your extensions accomplishes:

- `izi_types_` should be used if your extensions is used primarily to add new types to izi (for example: izi_types_numpy).
- `izi_authentication_` if your extension is used primarily to add a new authentication type to izi (for example: izi_authentication_oath2)
- `izi_output_format_` if your extension is used primarily to add a new output format to izi (for example: izi_output_format_svg)
- `izi_input_format_` if your extension is used primarily to add a new input format to izi (for example: izi_input_format_html)
- `izi_validate_` if your extension is used primarily to add a new overall validator to izi (for example: izi_validate_no_null).
- `izi_transform_` if your extension is used primarily to add a new izi transformer (for example: izi_transform_add_time)
- `izi_middleware_` if your extension is used primarily to add a middleware to izi (for example: izi_middleware_redis_session)

For any more complex or general use case that doesn't fit into these predefined categories or combines many of them, it
is perfectly suitable to simply prefix your extension with `izi_`. For example: izi_geo could combine izi types, izi input formats, and izi output formats making it a good use case for a simply prefixed extension.

Building Recommendations
=========
Ideally, izi extensions should be built in the same manner as izi itself. This means 100% test coverage using pytest, decent performance, pep8 compliance, and built in optional compiling with Cython. None of this is strictly required, but will help give users of your extension faith that it wont slow things down or break their setup unexpectedly.

Registering your extension
=========
Once you have finished developing and testing your extension, you can help increase others ability to discover it by registering it. The first place an extension should be registered is on PYPI, just like any other Python Package. In addition to that you can add your extension to the list of extensions on izi's [github wiki](https://github.com/izi-global/izir/wiki/IZIR-Extensions).

Thank you
=========
A sincere thanks to anyone that takes the time to develop and register an extension for izi. You are helping to make izi a more complete eco-system for everyuser out there, and paving the way for a solid foundation into the future.

Thanks!

~Timothy Crosley
