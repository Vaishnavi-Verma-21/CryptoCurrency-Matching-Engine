from uuid import uuid4
from datetime import datetime, timezone

def generate_id():
    return str(uuid4())

def get_timestamp():
    return datetime.now(timezone.utc)  # timezone-aware UTC datetime
