from datetime import date, datetime, time, timedelta

from dateutil.parser import parse
from sqlalchemy import select

import constants
from data.Models import Classes
from services.sqlite_procs import getDbSession

srce_db_name    = 'AttendanceV3.db'
srce_db_session = getDbSession(srce_db_name)

class_schedules = []

def LoadClassTimes(force_reload: bool = False):
    global class_schedules
    if len(class_schedules) == 0 or force_reload:
        class_schedules_tmp = srce_db_session.scalars(select(Classes)).all()
        class_schedules = [classes.to_dict() for classes in class_schedules_tmp]


def FindClosestClass(checkinDateTimeStr):
    # 2023-01-01 10:13:00
    global class_schedules
    checkinDateTime = datetime.strptime(checkinDateTimeStr, constants.fmtDateTime)
    day_of_week     = checkinDateTime.weekday() + 1
    classes_by_day  = [classes for classes in class_schedules if classes['classDayOfWeek'] == day_of_week]
    for class_by_day in classes_by_day:
        class_start_datetime      = parse(class_by_day['classStartTime'], fuzzy=False)
        checkin_start_time      = class_start_datetime - timedelta(minutes=20)
        checkin_finis_time      = class_start_datetime + timedelta(minutes=15)
        #print(f'{checkin_start_time.time()} : {checkinDateTime.time()} : {checkin_finis_time.time()}')
        if checkin_start_time.time() <= checkinDateTime.time() <= checkin_finis_time.time():
            return class_by_day
    return None

def is_time_between(start, end, check_time):
    # Works when start time is earlier than end time
    return start <= check_time <= end