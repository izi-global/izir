"""tests/test_input_format.py.

Tests that izis built in introspection helper functions work as expected

Copyright (C) 2018 DiepDT-IZIGlobal

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

"""
import izi


def function_with_kwargs(argument1, **kwargs):
    pass


def function_with_args(argument1, *args):
    pass


def function_with_neither(argument1, argument2):
    pass


def function_with_both(argument1, argument2, argument3, *args, **kwargs):
    pass


def function_with_nothing():
    pass


class Object(object):

    def my_method(self):
        pass


def test_is_method():
    """Test to ensure izis introspection can correctly identify the difference between a function and method"""
    assert not izi.introspect.is_method(function_with_kwargs)
    assert izi.introspect.is_method(Object().my_method)


def test_arguments():
    """Test to ensure izi introspection can correctly pull out arguments from a function definition"""
    def function(argument1, argument2):
        pass

    assert tuple(izi.introspect.arguments(function_with_kwargs)) == ('argument1', )
    assert tuple(izi.introspect.arguments(function_with_args)) == ('argument1', )
    assert tuple(izi.introspect.arguments(function_with_neither)) == ('argument1', 'argument2')
    assert tuple(izi.introspect.arguments(function_with_both)) == ('argument1', 'argument2', 'argument3')


def test_takes_kwargs():
    """Test to ensure izi introspection can correctly identify when a function takes kwargs"""
    assert izi.introspect.takes_kwargs(function_with_kwargs)
    assert not izi.introspect.takes_kwargs(function_with_args)
    assert not izi.introspect.takes_kwargs(function_with_neither)
    assert izi.introspect.takes_kwargs(function_with_both)


def test_takes_args():
    """Test to ensure izi introspection can correctly identify when a function takes args"""
    assert not izi.introspect.takes_args(function_with_kwargs)
    assert izi.introspect.takes_args(function_with_args)
    assert not izi.introspect.takes_args(function_with_neither)
    assert izi.introspect.takes_args(function_with_both)


def test_takes_arguments():
    """Test to ensure izi introspection can correctly identify which arguments supplied a function will take"""
    assert izi.introspect.takes_arguments(function_with_kwargs, 'argument1', 'argument3') == set(('argument1', ))
    assert izi.introspect.takes_arguments(function_with_args, 'bacon') == set()
    assert izi.introspect.takes_arguments(function_with_neither,
                                          'argument1', 'argument2') == set(('argument1', 'argument2'))
    assert izi.introspect.takes_arguments(function_with_both, 'argument3', 'bacon') == set(('argument3', ))


def test_takes_all_arguments():
    """Test to ensure izi introspection can correctly identify if a function takes all specified arguments"""
    assert not izi.introspect.takes_all_arguments(function_with_kwargs, 'argument1', 'argument2', 'argument3')
    assert not izi.introspect.takes_all_arguments(function_with_args, 'argument1', 'argument2', 'argument3')
    assert not izi.introspect.takes_all_arguments(function_with_neither, 'argument1', 'argument2', 'argument3')
    assert izi.introspect.takes_all_arguments(function_with_both, 'argument1', 'argument2', 'argument3')


def test_generate_accepted_kwargs():
    """Test to ensure izi introspection can correctly dynamically filter out kwargs for only those accepted"""
    source_dictionary = {'argument1': 1, 'argument2': 2, 'hey': 'there', 'hi': 'hello'}

    kwargs = izi.introspect.generate_accepted_kwargs(function_with_kwargs, 'bacon', 'argument1')(source_dictionary)
    assert kwargs == source_dictionary

    kwargs = izi.introspect.generate_accepted_kwargs(function_with_args, 'bacon', 'argument1')(source_dictionary)
    assert kwargs == {'argument1': 1}

    kwargs = izi.introspect.generate_accepted_kwargs(function_with_neither, 'argument1', 'argument2')(source_dictionary)
    assert kwargs == {'argument1': 1, 'argument2': 2}

    kwargs = izi.introspect.generate_accepted_kwargs(function_with_both, 'argument1', 'argument2')(source_dictionary)
    assert kwargs == source_dictionary

    kwargs = izi.introspect.generate_accepted_kwargs(function_with_nothing)(source_dictionary)
    assert kwargs == {}
