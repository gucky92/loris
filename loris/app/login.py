"""Login classes
"""

from flask_login import UserMixin
import datajoint as dj
import warnings
import pymysql

from loris import config
from loris.errors import LorisError


class User(UserMixin):

    def __init__(self, user_name):
        print(config['connection'])
        self.table = config.user_table

        # skip mysql error
        try:
            if not len(self.table()):
                config.create_administrator()
        except pymysql.err.InterfaceError:
            warnings.warn('not creating administrator')

        self.user_name = user_name

        self.restriction = {config['user_name']: self.user_name}

        print(self.restriction)
        self.restricted_table = self.table & self.restriction
        self._user_exists = bool(len(self.restricted_table))

        if len(self.restricted_table) > 1:
            raise LorisError('More than a single user entry')

        self._entry = None
        self._is_authenticated = False

    @property
    def entry(self):

        if self._entry is None:
            if config['user_active'] is None:
                self._entry = self.restricted_table.proj(
                    config['user_name'],
                ).fetch1()

            else:
                self._entry = self.restricted_table.proj(
                    config['user_name'],
                    config['user_active'],
                ).fetch1()

        return self._entry

    @property
    def user_exists(self):
        return self._user_exists

    def get_id(self):
        return str(self.user_name)

    @property
    def is_active(self):
        if config['user_active'] is None:
            return True
        return bool(self.entry[config['user_active']])

    @property
    def is_authenticated(self):
        return self._is_authenticated

    def check_password(self, password):
        # check password in mysql database
        try:
            config.conn(
                user=self.user_name,
                password=password,
                reset=True
            )
            success = True
            self._is_authenticated = True
        except Exception:
            success = False
            self._is_authenticated = False
        config.conn(reset=True)
        return success
