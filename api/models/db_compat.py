"""Database compatibility utilities for MySQL and PostgreSQL"""

import os
import sqlalchemy as sa
from sqlalchemy import String, Text
from sqlalchemy.dialects import mysql, postgresql
from sqlalchemy.sql import func

from .engine import get_current_db_type, get_current_db_version

def get_uuid_default():
    """Get appropriate UUID default value based on database type and version"""
    scheme = get_current_db_type()
    if 'mysql' in scheme:
        mysql_version = get_current_db_version()
        if mysql_version >= (8, 0):
            # MySQL 8.0+ supports UUID() as default value
            return sa.text("(UUID())")
        else:
            # MySQL < 8.0 doesn't support function calls as default values
            # Use a trigger or application-level UUID generation instead
            return None  # Will be handled by application code
    else:
        # PostgreSQL uses uuid_generate_v4()
        return sa.text("uuid_generate_v4()")


def get_array_column(item_type, **kwargs):
    """Get appropriate array column type based on database type"""
    scheme = get_current_db_type()
    if 'mysql' in scheme:
        # MySQL doesn't have native array type, use JSON
        return sa.JSON
    else:
        # PostgreSQL has native ARRAY type
        return sa.ARRAY(item_type)


def get_current_timestamp():
    """Get appropriate current timestamp function based on database type"""
    scheme = get_current_db_type()
    if 'mysql' in scheme:
        return sa.text("CURRENT_TIMESTAMP")
    else:
        return func.current_timestamp()


def get_boolean_default(value: bool):
    """Get appropriate boolean default based on database type"""
    scheme = get_current_db_type()
    if 'mysql' in scheme:
        return sa.text("1" if value else "0")
    else:
        return sa.text("true" if value else "false")


def get_varchar_default(value: str):
    """Get appropriate varchar default based on database type"""
    scheme = get_current_db_type()
    if 'mysql' in scheme:
        return sa.text(f"'{value}'")
    else:
        return sa.text(f"'{value}'::character varying")