# -*- coding: utf-8 -*-
from peewee import SqliteDatabase


try:
    from settings_local import *
except ImportError as e:
    pass