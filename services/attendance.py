import csv
import json
import os
import re

from dateutil.parser import parse, ParserError
from sqlalchemy import select, create_engine
from datetime import date, datetime
from dateutil import parser

from sqlalchemy.orm import Session

import constants
from data.Models import Ranks, Stripes, Requirements, Belts, AttendanceV1
from services.class_schedules import FindClosestClass
from services.sqlite_procs import getDbSession, getDbPath

srce_db_session = None
dest_db_session = None

srce_db_name = 'AttendanceV2_20251107.db'
dest_db_name = 'AttendanceRanks.db'

def GetAttendanceOriginalRawData():
    global srce_db_session
    global dest_db_session
    srce_db_session   = getDbSession(srce_db_name)
    srce_records_slct = (select(AttendanceV1).order_by('attendance_id'))
    srce_records_rslt = srce_db_session.execute(srce_records_slct).scalars().all()
    srce_records_list = [requirement.to_dict() for requirement in srce_records_rslt]
    CheckAttendanceTimeStamps(srce_records_list)
    return srce_records_list

def CheckAttendanceTimeStamps(attendance_records: list[dict]):
    for attendance_record in attendance_records:
        if not is_date(attendance_record['checkinDateTime']):
            print(f'bad datetime: {attendance_record['checkinDateTime']}')
        else:
            class_weekday = FindClosestClass(attendance_record['checkinDateTime'])
            print(f'class_weekday: {class_weekday}')

def is_date(date_string):
    try:
        # Automatically detects and parses most English date formats
        parsed_date = parse(date_string, fuzzy=False)
        return parsed_date
    except (ParserError, ValueError, TypeError):
        return False

    # try:
    #     date.fromisoformat(date_string)
    #     return True
    # except ValueError:
    #     return False


