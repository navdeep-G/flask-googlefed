Google Federated Auth for Flask (and Humans)
============================================

Require an account from a given Google Apps domain for your Flask apps.

Great for internal apps on public-facing servers.


Usage
-----

Setup is super simple::

    from flask import Flask
    from flask_googlefed import GoogleAuth

    app = Flask(__name__)
    app.secret_key = 'random secret key'
    app.config['GOOGLE_DOMAIN'] = 'heroku.com'

    auth = GoogleAuth(app)

    @app.route('/')
    @auth.required
    def secret():
        return 'ssssshhhhh'


Install
-------

Installation is equally simple::

    $ pip install flask-googlefed


TODO
----

Be forewarned, there's work to be done:

- ``g.user`` is always ``None``
