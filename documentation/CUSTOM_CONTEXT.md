Context factory in izi
======================

There is a concept of a 'context' in falcon, which is a dict that lives through the whole request. It is used to integrate
for example SQLAlchemy library. However, in izi's case you would expect the context to work in each interface, not
only the http one based on falcon. That is why izi provides its own context, that can be used in all interfaces.
If you want to see the context in action, see the examples.

## Create context

By default, the izi creates also a simple dict object as the context. However, you are able to define your own context
by using the context_factory decorator.

```py
@izi.create_context()
def context_factory(*args, **kwargs):
    return dict()
```

Arguments that are provided to the factory are almost the same as the ones provided to the directive
(api, api_version, interface and interface specific arguments). For exact arguments, go to the interface definition.

## Delete context

After the call is finished, the context is deleted. If you want to do something else with the context at the end, you
can override the default behaviour by the delete_context decorator.

```py
@izi.delete_context()
def delete_context(context, exception=None, errors=None, lacks_requirement=None):
    pass
```

This function takes the context and some arguments that informs us about the result of the call's execution.
If the call missed the requirements, the reason will be in lacks_requirements, errors will contain the result of the
validation (None if call has passed the validation) and exception if there was any exception in the call.
Note that if you use cli interface, the errors will contain a string with the first not passed validation. Otherwise,
you will get a dict with errors.


Where can I use the context?
============================

The context can be used in the authentication, directives and validation. The function used as an api endpoint
should not get to the context directly, only using the directives.

## Authentication

To use the context in the authentication function, you need to add an additional argument as the context.
Using the context, you can for example check if the credentials meet the criteria basing on the connection with the
database.
Here are the examples:

```py
@izi.authentication.basic
def context_basic_authentication(username, password, context):
    if username == context['username'] and password == context['password']:
        return True

@izi.authentication.api_key
def context_api_key_authentication(api_key, context):
    if api_key == 'Bacon':
        return 'ViTuocGia'

@izi.authentication.token
def context_token_authentication(token, context):
    if token == precomptoken:
        return 'ViTuocGia'
```

## Directives

Here is an example of a directive that has access to the context:


```py
@izi.directive()
def custom_directive(context=None, **kwargs):
    return 'custom'
```

## Validation

### IZIR types

You can get the context by creating your own custom izi type. You can extend a regular izi type, as in example below:


```py
@izi.type(chain=True, extend=izi.types.number, accept_context=True)
def check_if_near_the_right_number(value, context):
    the_only_right_number = context['the_only_right_number']
    if value not in [
        the_only_right_number - 1,
        the_only_right_number,
        the_only_right_number + 1,
    ]:
        raise ValueError('Not near the right number')
    return value
```

You can also chain extend a custom izi type that you created before. Keep in mind that if you marked that
the type that you are extending is using the context, all the types that are extending it should also use the context.


```py
@izi.type(chain=True, extend=check_if_near_the_right_number, accept_context=True)
def check_if_the_only_right_number(value, context):
    if value != context['the_only_right_number']:
        raise ValueError('Not the right number')
    return value
```

It is possible to extend a izi type without the chain option, but still using the context:


```py
@izi.type(chain=False, extend=izi.types.number, accept_context=True)
def check_if_string_has_right_value(value, context):
    if str(context['the_only_right_number']) not in value:
        raise ValueError('The value does not contain the only right number')
    return value
```

### Marshmallow schema

Marshmallow library also have a concept of the context, so izi also populates the context here.


```py
class MarshmallowContextSchema(Schema):
    name = fields.String()

    @validates_schema
    def check_context(self, data):
        self.context['marshmallow'] += 1

@izi.get()
def made_up_hello(test: MarshmallowContextSchema()):
    return 'hi'
```

What can be a context?
======================

Basically, the answer is everything. For example you can keep all the necessary database sessions in the context
and also you can keep there all the resources that need to be dealt with after the execution of the endpoint.
In delete_context function you can resolve all the dependencies between the databases' management.
See the examples to see what can be achieved. Do not forget to add your own example if you find an another usage!
