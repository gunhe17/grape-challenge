from datetime import datetime, timezone, timedelta
from typing import Optional, Union


def kst(dt: Optional[Union[datetime, str]]) -> Optional[str]:
    if not dt:
        return None

    # 이미 문자열인 경우 그대로 반환
    if isinstance(dt, str):
        return dt

    from grapechallenge.config import get_app_env
    app_env = get_app_env()

    if app_env == "dev":
        return dt.isoformat()

    if app_env == "prod":
        kst_tz = timezone(timedelta(hours=9))
        return dt.replace(tzinfo=timezone.utc).astimezone(kst_tz).isoformat()