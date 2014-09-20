from flask import current_app
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

from qpython import qconnection
from qpython.qconnection import QConnectionException


def get_kdb(mode='c'):
    """Get an instance of kdb.

    This function will return a ``qpython.qconnection`` instance.
    It does this by finding the qpython object associated with
    the current flask app (using ``flask.current_app``).

    """
    return current_app.extensions['kdb'].connection()


class _KDB(object):
    default_config = (
        ('host', 'localhost'),
        ('port', 5000),
        ('timeout', None),
        # ('username', None),
        # ('passowrd', None),
    )

    config_prefix = 'KDB'

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initialize the flask app.
        """
        # Store default config to application
        for key, value in self.default_config:
            config_key = '_'.join((self.config_prefix, key.upper()))
            app.config.setdefault(config_key, value)

        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

        app.extensions['kdb'] = self

    def config(self, key):
        """
        Read actual configuration from Flask application config.

        :param key: Lowercase config key from :attr:`default_config` tuple
        """
        return self.app.config['_'.join((self.config_prefix, key.upper()))]

    def connect(self):
        host = self.config('HOST')
        port = self.config('PORT')
        timeout = self.config('TIMEOUT')
        q = qconnection.QConnection(host, port, timeout=timeout)
        try:
            q.open()
        except QConnectionException:
            raise RuntimeError("KDB connection cannot be establish! {}:{}".format(self._host, self._port))

        return q

    @property
    def connection(self):
        """
        Attempt to open the kdb interface.

        :return: QConnection object in the open state
        :raises RuntimeError: If the connection cannot be made
        """
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'kdb'):
                ctx.kdb = self.connect()
            return ctx.kdb

    @staticmethod
    def teardown(self, *args, **kwargs):
        ctx = stack.top
        if ctx is not None:
            if hasattr(ctx, 'kdb'):
                ctx.kdb.close()
