"""UUID handling for different database versions"""

import uuid
from sqlalchemy import event
from sqlalchemy.orm import Session

from .db_compat import get_uuid_default


def generate_uuid():
    """Generate a new UUID string"""
    return str(uuid.uuid4())


def setup_uuid_handlers(Base):
    """Setup UUID generation for models that need it"""
    
    # Only setup handlers if MySQL < 8.0 (when get_uuid_default returns None)
    if get_uuid_default() is None:
        
        @event.listens_for(Base, 'before_insert', propagate=True)
        def receive_before_insert(mapper, connection, target):
            """Generate UUID for new records if not already set"""
            # Check if the model has an 'id' field that should be a UUID
            if hasattr(target, 'id') and target.id is None:
                # Check if the id column is a StringUUID type
                id_column = mapper.columns.get('id')
                if id_column is not None and hasattr(id_column.type, 'python_type'):
                    target.id = generate_uuid()