import csv
import json
import os
import re

from dateutil.parser import parse, ParserError
from sqlalchemy import select, create_engine, delete, insert, inspect
from datetime import date, datetime
from dateutil import parser

from sqlalchemy.orm import Session

import constants
from data.Models import Ranks, Stripes, Requirements, Belts, AttendanceV1, Attendance, Classes, Attendance
from services.belts_procs import GetRankAtCheckin
from services.class_schedules import FindClosestClass
from services.sqlite_procs import getDbSession, getDbPath, getNewDbSession
from services.student_procs import GetStudentRecord

#srce_db_name    = 'AttendanceV2_20251107.db'
srce_db_name    = 'AttendanceV2_20260612.db'
srce_db_session = getNewDbSession(srce_db_name)

#dest_db_name    = 'AttendanceRanks.db'
dest_db_name    = 'AttendanceV3.db'
dest_db_session = getDbSession(dest_db_name)

def GetAttendanceOriginalRawData():
    # global srce_db_session
    # srce_db_session   = getDbSession(srce_db_name)
    srce_records_slct = select(AttendanceV1).order_by('attendance_id')   #.limit(1000)
    srce_records_rslt = srce_db_session.execute(srce_records_slct).scalars().all()
    srce_records_list = [requirement.to_dict() for requirement in srce_records_rslt]
    updated_attendance_records = CheckAttendanceTimeStamps(srce_records_list)
    PushAttendanceRecordsToDb(dest_db_name, updated_attendance_records)

    return srce_records_list

def CheckAttendanceTimeStamps(old_attendance_records: list[dict]):
    new_attendance_records = []
    missing_badge_numbers = {}
    existin_badge_numbers = {}
    try:
        for old_attendance_record in old_attendance_records:
            if not is_date(old_attendance_record['checkinDateTime']):
                print(f'bad datetime: {old_attendance_record['checkinDateTime']}')
            else:
                class_record = FindClosestClass(old_attendance_record['checkinDateTime'])
                new_attendance_record = (CreateNewAttendanceRecord
                                         (old_attendance_record, class_record, missing_badge_numbers, existin_badge_numbers)
                                         )
                new_attendance_records.append(new_attendance_record)

        sorted_data = dict(sorted(missing_badge_numbers.items()))
        DisplayMissingStudentRecords(sorted_data, old_attendance_records)
        return new_attendance_records
    except Exception as ex:
        print(f'Error: {str(ex)}')

def CreateNewAttendanceRecord(old_attendance_record: dict, class_record: dict, missing_badge_numbers, existin_badge_numbers):
    try:
        new_attendance_record = Attendance()

        new_attendance_record.badgeNumber      = old_attendance_record['badgeNumber']
        new_attendance_record.checkinDateTime  = old_attendance_record['checkinDateTime']
        new_attendance_record.checkinDate      = old_attendance_record['checkinDate']

        checkInDayOfWeek = parse(old_attendance_record['checkinDateTime']).weekday() + 1
        new_attendance_record.checkinDayOfWeek = checkInDayOfWeek

        new_attendance_record.checkinTime        = old_attendance_record['checkinTime']
        new_attendance_record.attendanceRankName = old_attendance_record['rankName']
        new_attendance_record.studentName        = old_attendance_record['studentName']

        student_record = GetStudentRecord(old_attendance_record['badgeNumber'])
        new_attendance_record.missingBadge = 'T'
        if student_record is not None:
            new_attendance_record.missingBadge = 'F'
            existin_badge_numbers[old_attendance_record['badgeNumber']] = existin_badge_numbers.get(old_attendance_record['badgeNumber'], 0) + 1
            new_attendance_record.studentFirstName    = student_record['firstName']
            new_attendance_record.studentLastName     = student_record['lastName']
            rank_at_checkin = GetRankAtCheckin(old_attendance_record)
            if rank_at_checkin:
                new_attendance_record.studentRankNum    = rank_at_checkin['beltId']
                new_attendance_record.studentRankName   = rank_at_checkin['beltTitle']
        else:
            missing_badge_numbers[old_attendance_record['badgeNumber']] = missing_badge_numbers.get(old_attendance_record['badgeNumber'], 0) + 1
            #print(f'No student record found: {old_attendance_record['badgeNumber']}')

        if class_record is not None:
            new_attendance_record.classNum   = class_record['classNum']
            new_attendance_record.className  = class_record['className']
            new_attendance_record.classStartTime  = class_record['classStartTime']
            new_attendance_record.styleNum        = class_record['styleNum']
            new_attendance_record.styleName       = class_record['styleName']
        return new_attendance_record
    except Exception as ex:
        print(f'Error: {str(ex)}')

def is_date(date_string):
    try:
        # Automatically detects and parses most English date formats
        parsed_date = parse(date_string, fuzzy=False)
        return parsed_date
    except (ParserError, ValueError, TypeError):
        return False


def DisplayMissingStudentRecords(missing_badge_numbers: dict, old_attendance_records: list[dict]):
    for missing_badge_number, attendance_count in missing_badge_numbers.items():
        old_attendance_record = GetOldStudentDetails(missing_badge_number, old_attendance_records)
        print (f'badge_number-{missing_badge_number} : student Name-{old_attendance_record['studentName']}')

def GetOldStudentDetails(badge_number, old_attendance_records: list[dict]):
    filter_tmp = [attendance_record for attendance_record in old_attendance_records if attendance_record['badgeNumber'] == badge_number]
    if len(filter_tmp) > 0:
        return filter_tmp[0]
    else:
        return None

def PushAttendanceRecordsToDb(db_name: str, attendance_records: list[Attendance], truncate_table: bool = True):
    engine    = create_engine(f'sqlite:///{getDbPath(db_name)}', echo=True)
    # inspector = inspect(engine)
    # columns = inspector.get_columns('Attendance')
    if truncate_table:
        with engine.connect() as connection:
            with connection.begin():  # Manages transaction commit automatically
                connection.execute(delete(Attendance))
                #connection.commit()
    with engine.connect() as connection:
        attendance_records_list = [attendance_record.to_dict() for attendance_record in attendance_records]
        connection.execute(insert(Attendance), attendance_records_list)
        connection.commit()

