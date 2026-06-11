from datetime import date, datetime

from sqlalchemy import select

import constants
from data.Models import Classes
from services.sqlite_procs import getDbSession

db_name    = 'AttendanceRanks.db'
db_session = getDbSession(db_name)

def LoadCheckinTimes():
    pass

def FindClosestClass(checkinDateTimeStr):
    # 2023-01-01 10:13:00
    checkinDateTime = datetime.strptime(checkinDateTimeStr, constants.fmtDateTime)
    day_of_week     = checkinDateTime.weekday() + 1

    classes_stmt  = (select(Classes).where(Classes.classDayOfWeek == day_of_week))
    classes_list  = db_session.execute(classes_stmt).scalars().all()

    print(f'checkinDateTimeStr: {checkinDateTimeStr} -- day_of_week: {day_of_week}')

    return -1

