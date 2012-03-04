# -*- coding: utf-8 -*-

"""
flask-googlefed
~~~~~~~~~~~~~~~

This module contains the Google Federated Authentication extension for Flask.
"""

import os
from functools import wraps

from flask import (
    Blueprint, session, request, _request_ctx_stack, redirect,
    url_for, g)

from flaskext.openid import OpenID

# Just a little context.
current_dir = os.path.dirname(__file__)


class GoogleAuth(object):
    """Google Federated Authentication manager.

    If ``install==True`` (default), it is automatically installed into the
    given Flask application.
    """

    def __init__(self, app, install=True, prefix=None, name='GoogleAuth'):
        self.app = app
        self.app.config.setdefault('GOOGLE_DOMAIN', None)

        self.oid = OpenID(self.app)
        self.url_prefix = prefix

        self.name = name
        self.blueprint = self._get_blueprint(self.name)
        self.domain = self.app.config.get('GOOGLE_DOMAIN')

        self._login = self.oid.loginhandler(self.__login)
        self._create_or_login = self.oid.after_login(self.__create_or_login)

        if install:
            self.install()


    def _check_auth(self):
        """Returns True if authentication is valid."""
        return ('openid' in session) if self.domain else True

    def __login(self):
        return self.oid.try_login('https://www.google.com/accounts/o8/site-xrds?hd=%s' % self.domain)

    def _before_request(self):
        g.user = None

    def __create_or_login(self, resp):
        """This is called when login with OpenID succeeded and it's not
        necessary to figure out if this is the users's first login or not.
        This function has to redirect otherwise the user will be presented
        with a terrible URL which we certainly don't want.
        """
        session['openid'] = resp.identity_url
        return redirect(self.oid.get_next_url())

    def _logout(self):
        session.pop('openid', None)
        return redirect(self.oid.get_next_url())

    def _get_blueprint(self, name):
          return Blueprint(
            name,
            __name__,
            static_folder=os.path.join(current_dir, 'static'),
            template_folder=os.path.join(current_dir, 'templates'),
        )

    def _configure_routes(self):
        self.blueprint.route('/login/', methods=['GET', 'POST'])(self._login)
        self.blueprint.route('/logout/', methods=['GET', 'POST'])(self._logout)

    def _register_blueprint(self, **kwargs):
        self.app.register_blueprint(
            self.blueprint,
            url_prefix=self.url_prefix,
            **kwargs
        )

    def install(self):
        """Installs the Blueprint into the app."""

        self.app.before_request(self._before_request)
        self._configure_routes()
        self._register_blueprint()

    def required(self, f):
        """Request decorator. Forces authentication."""

        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not self._check_auth():
                return redirect(url_for('%s.__login' % self.blueprint.name, next=request.url))
            return f(*args, **kwargs)
        return decorated

