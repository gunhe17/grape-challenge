from datetime import datetime, timezone, timedelta
from typing import Optional


def kst(dt: Optional[datetime]) -> Optional[str]:
    if not dt:
        return None
    
    from grapechallenge.config import get_app_env
    app_env = get_app_env()

    if app_env is "dev":
        return dt.isoformat()
    
    if app_env is "prod":
        kst = timezone(timedelta(hours=9))
        return dt.replace(tzinfo=timezone.utc).astimezone(kst).isoformat()