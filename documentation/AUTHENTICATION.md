Authentication in *izi*
=====================

IZIR supports a number of authentication methods which handle the http headers for you and lets you very simply link them with your own authentication logic.

To use izi's authentication, when defining an interface, you add a `requires` keyword argument to your `@get` (or other http verb) decorator. The argument to `requires` is a *function*, which returns either `False`, if the authentication fails, or a python object which represents the user. The function is wrapped by a wrapper from the `izi.authentication.*` module which handles the http header fields.

That python object can be anything. In very simple cases it could be a string containing the user's username. If your application is using a database with an ORM such as [peewee](http://docs.peewee-orm.com/en/latest/), then this object can be more complex and map to a row in a database table.

To access the user object, you need to use the `izi.directives.user` directive in your declaration.

    @izi.get(requires=)
    def handler(user: izi.directives.user)

This directive supplies the user object. IZIR will have already handled the authentication, and rejected any requests with bad credentials with a 401 code, so you can just assume that the user is valid in your logic.


Type of Authentication | IZIR Authenticator Wrapper | Header Name | Header Content | Arguments to wrapped verification function
----------------------------|----------------------------------|-----------------|-------------------------|------------
Basic Authentication | `izi.authenticaton.basic` | Authorization | "Basic XXXX" where XXXX is username:password encoded in Base64| username, password
Token Authentication | `izi.authentication.token` | Authorization | the token as a string| token
API Key Authentication | `izi.authentication.api_key` | X-Api-Key | the API key as a string | api-key
