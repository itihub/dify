import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Database-agnostic naming convention
INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

metadata = MetaData(naming_convention=INDEXES_NAMING_CONVENTION)

def get_current_db_type():
    """Get current database type from active connection"""
    try:
        return db.engine.dialect.name
    except:
        # Fallback to environment variable
        scheme = os.getenv('SQLALCHEMY_DATABASE_URI_SCHEME', 'postgresql')
        if 'mysql' in scheme:
            return 'mysql'
        return 'postgresql'

def get_current_db_version():
    """Get current database version from active connection"""
    try:
        return db.engine.dialect.server_version_info
    except:
        # Fallback to environment variable
        version = os.getenv('SQLALCHEMY_DATABASE_URI_VERSION', '15.3')
        return tuple(map(int, version.split('.')))

# ****** IMPORTANT NOTICE ******
#
# NOTE(QuantumGhost): Avoid directly importing and using `db` in modules outside of the
# `controllers` package.
#
# Instead, import `db` within the `controllers` package and pass it as an argument to
# functions or class constructors.
#
# Directly importing `db` in other modules can make the code more difficult to read, test, and maintain.
#
# Whenever possible, avoid this pattern in new code.
db = SQLAlchemy(metadata=metadata)
