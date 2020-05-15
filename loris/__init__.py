"""
"""

import os

from loris.settings import Config
from loris.errors import LorisError

os.environ['DJ_SUPPORT_ADAPTED_TYPES'] = "TRUE"

config = Config.load()
conn = config.conn


from loris.database.users import (
    grantuser, grantprivileges, dropuser, change_password
)


class DataBase:

    def __init__(self, config):
        self.config = config

    def __getattr__(self, name):

        if (
            ('config' in vars(self))
            and ('schemata' in self.config)
            and (name in self.config['schemata'])
        ):
            return self.config['schemata'][name]
        else:
            raise AttributeError


db = DataBase(config)


__all__ = [
    'config',
    'conn',
    'Config',
    'LorisError',
    'df',
    'grantuser',
    'grantprivileges',
    'dropuser',
    'change_password',
    'db'
]
