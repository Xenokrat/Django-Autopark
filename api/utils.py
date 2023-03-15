from datetime import datetime

import pytz


def convert_local_to_utc(local_datetime: str) -> str:
    parced_local_datetime = datetime.strptime(local_datetime, "%Y-%m-%dT%H:%M:%SZ")
    utc_timezone = pytz.timezone("UTC")
    utc_datetime = parced_local_datetime.astimezone(utc_timezone)
    return utc_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
