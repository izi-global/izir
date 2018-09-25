izi directives (automatic argument injection)
===================

Oftentimes you'll find yourself needing something particular to an interface (say a header, a session, or content_type), but don't want to tie your function
to a single interface. To support this, izi introduces the concept of `directives`. In izi, directives are simply arguments that have been registered to automatically provide a parameter value based on knowledge known to the interface.

For example, this is the built-in session directive:


    @izi.directive()
    def session(context_name='session', request=None, **kwargs):
        """Returns the session associated with the current request"""
        return request and request.context.get(context_name, None) or None

Then, when using this directive in your code, you can either specify the directive via type annotation:

    @izi.get()
    def my_endpoint(session: izi.directives.session):
        session # is here automatically, without needing to be passed in

Or by prefixing the argument with `izi_`:

    @izi.get()
    def my_endpoint(izi_session):
        session # is here automatically, without needing to be passed in

You can then specify a different location for the izi session, simply by providing a default for the argument:

    @izi.get()
    def my_endpoint(izi_session='alternative_session_key'):
        session # is here automatically, without needing to be passed in

Built-in directives
===================

izi provides a handful of directives for commonly needed attributes:

 - izi.directives.Timer (izi_timer=precision): Stores the time the interface was initially called, returns how much time has passed since the function was called, if casted as a float. Automatically converts to the time taken when returned as part of a JSON structure. The default value specifies the float precision desired when keeping track of the time passed.
 - izi.directives.module (izi_module): Passes along the module that contains the API associated with this endpoint.
 - izi.directives.api (izi_api): Passes along the izi API singleton associated with this endpoint.
 - izi.directives.api_version (izi_api_version): Passes along the version of the API being called.
 - izi.directives.documentation (izi_documentation): Generates and passes along the entire set of documentation for the API that contains the endpoint.
 - izi.directives.session (izi_session=context_name): Passes along the session associated with the current request. The default value provides a different key whose value is stored on the request.context object.
 - izi.directives.user (izi_user): Passes along the user object associated with the request.
 - izi.directives.CurrentAPI (izi_current_api): Passes along a smart, version-aware API caller, to enable calling other functions within your API, with reassurance that the correct function is being called for the version of the API being requested.

Building custom directives
===================

izi provides the `@izi.directive()` to enable creation of new directives. It takes one argument: apply_globally, which defaults to False.
If you set this parameter to True, the izi directive will be automatically made available as a magic `izi_` argument on all endpoints outside of your defined API. This is not a concern if you're applying directives via type annotation.

The most basic directive will take an optional default value, as well as **kwargs:

    @izi.directive()
    def basic(default=False, **kwargs):
        return str(default) + ' there!'


This directive could then be used like this:

    @izi.local()
    def endpoint(izi_basic='hi'):
        return izi_basic

    assert endpoint() == 'hi there!'

It's important to always accept **kwargs for directive functions, as each interface gets to decide its own set of
keyword arguments to send to the directive, which can then be used to pull in information for the directive.

Common directive key word parameters
===================

Independent of interface, the following key word arguments will be passed to the directive:

 - `interface` - The interface that the directive is being run through. Useful for conditionally injecting data (via the decorator) depending on the interface it is being called through, as demonstrated at the bottom of this section.
 - `api` - The API singleton associated with this endpoint.

Interface Example:

    @directive()
    def my_directive(default=None, interface=None, **kwargs):
        if interface == izi.interface.CLI:
            return 'CLI specific'
        elif interface == izi.interface.HTTP:
            return 'HTTP specific'
        elif interface == izi.interface.Local:
            return 'Local'

        return 'unknown'

HTTP directive key word parameters
===================

Directives are passed the following additional keyword parameters when they are being run through an HTTP interface:

 - `response`: The HTTP response object that will be returned for this request.
 - `request`: The HTTP request object that caused this interface to be called.
 - `api_version`: The version of the endpoint being hit.

CLI directive key word parameters
===================

Directives get one additional argument when they are run through a command line interface:

 - `argparse`: The argparse instance created to parse command line arguments.
