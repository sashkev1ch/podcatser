from datetime import datetime
from typing import Dict, Optional
from re import search
from dateutil.parser import parse
from library.constants import TIMEZONE_INFO


def get_tz_info(date_string: str) -> Optional[Dict[str, int]]:
    possible_tzs = list(TIMEZONE_INFO.keys())
    for tz_name in possible_tzs:
        position = date_string.find(tz_name)
        if position > 0:
            if search("[A-Z]", date_string[position + len(tz_name):]):
                continue
            return {tz_name: TIMEZONE_INFO[tz_name]}

    return None


def get_datetime(date_string: str) -> datetime:
    tz_info = get_tz_info(date_string)
    return parse(date_string, tzinfos=tz_info)
