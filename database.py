"""
Contains DB object, Which can be used at various places in application
"""

from peewee import PostgresqlDatabase

import config


DB = PostgresqlDatabase(
    database=config.DB_NAME,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    host=config.DB_HOST,
    port=config.DB_PORT
)
