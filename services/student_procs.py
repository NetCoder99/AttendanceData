from sqlalchemy   import select

import constants
from data.Models import Students, StudentsV1
from services.image_procs import GetImageTypeBase64, GetImageTypeBytes
from services.sqlite_procs import getDbSession, getNewDbSession
from dateutil.parser import parse, ParserError


srce_db_name    = 'AttendanceV2_20260612.db'
srce_db_session = getNewDbSession(srce_db_name)

dest_db_name    = 'AttendanceV3.db'
dest_db_session = getNewDbSession(dest_db_name)

student_records = []

def LoadStudentRecords(force_reload: bool = False):
    global student_records
    if len(student_records) == 0 or force_reload:
        student_records_tmp = srce_db_session.scalars(select(StudentsV1)).all()
        student_records = [students.to_dict() for students in student_records_tmp]

def GetStudentRecord(badge_number: int):
    filter_tmp = [student_record for student_record in student_records if student_record['badgeNumber'] == badge_number]
    if len(filter_tmp) == 1:
        return filter_tmp[0]
    else:
        return None

# ------------------------------------------------------------------
# Import the student records to the V3 database
# ------------------------------------------------------------------
def UpdateStudentRecords():
    srce_student_records = srce_db_session.scalars(select(StudentsV1)).all()

    for student_record in srce_student_records:
        ProcessStudentUpsert(student_record)

# ------------------------------------------------------------------
# Outer loop to iterate over the imported/new student records
# ------------------------------------------------------------------
def ProcessStudentUpsert(student_record: StudentsV1):
    if student_record.firstName.endswith('\n'):
        student_record.firstName = student_record.firstName.strip()
    student_record_tmp = dest_db_session.scalars(select(Students).where(Students.badgeNumber == student_record.badgeNumber)).all()
    print(f'{student_record.badgeNumber} ::  {len(student_record_tmp)} : {student_record.firstName} {student_record.lastName} ')
    if len(student_record_tmp) == 0:
        InsertNewStudentRecord(student_record)
    elif len(student_record_tmp) == 1:
        UpdateOldStudentRecord(student_record, student_record_tmp[0])
    else:
        raise Exception("Invalid dest record count!")

#insert_count = 0
# ------------------------------------------------------------------
# Create, populate and insert the ORM student record
# ------------------------------------------------------------------
def InsertNewStudentRecord(student_record_srce: StudentsV1):
    #global insert_count
    try:
        # insert_count += 1
        # if insert_count > 4:
        #     raise Exception("Count limit exceeded!")
        print(f'Inserting new student: {student_record_srce.badgeNumber} :: {student_record_srce.firstName} {student_record_srce.lastName}')
        student_record_dest = Students()
        student_record_dest.badgeNumber = student_record_srce.badgeNumber
        student_record_dest.firstName   = student_record_srce.firstName
        student_record_dest.lastName    = student_record_srce.lastName
        student_record_dest.middleName  = None
        student_record_dest.namePrefix  = None
        student_record_dest.email       = student_record_srce.email
        student_record_dest.address     = student_record_srce.address
        student_record_dest.address2    = student_record_srce.address2
        student_record_dest.city        = student_record_srce.city
        student_record_dest.country     = student_record_srce.country
        student_record_dest.state       = student_record_srce.state
        student_record_dest.zip         = student_record_srce.zip
        student_record_dest.birthDate   = student_record_srce.birthDate
        student_record_dest.phoneHome   = student_record_srce.phoneHome
        student_record_dest.phoneMobile      = None
        student_record_dest.status           = 'Active'
        student_record_dest.memberSince      = student_record_srce.memberSince
        student_record_dest.memberSinceDate  = GetParsedDateTime(student_record_srce.memberSince)
        student_record_dest.gender     = student_record_srce.gender
        student_record_dest.ethnicity  = student_record_srce.ethnicity

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #student_record_dest.studentImageName    = student_record_srce.studentImagePath
        image_meta_base64 = GetImageTypeBase64(student_record_srce.imageBase64)
        student_record_dest.studentImagePath    = student_record_srce.studentImagePath
        student_record_dest.studentImageBase64  = student_record_srce.imageBase64
        student_record_dest.studentImageType    = image_meta_base64['image_type']
        student_record_dest.studentImageDate    = GetParsedDateTime(image_meta_base64['image_date'])

        student_record_dest.createDateTime      = GetParsedDateTime(image_meta_base64['image_date'])
        dest_db_session.add(student_record_dest)
        dest_db_session.commit()

        print(f'Was inserted : {student_record_dest.to_dict()}')
    except Exception as ex:
        print(f'{str(ex)}')

def GetParsedDateTime(input_date_str: any) -> str | None:
    if input_date_str is not None:
        return parse(input_date_str).strftime(constants.fmtDateTime)
    else:
        return None

def UpdateOldStudentRecord(student_record_srce: StudentsV1, student_record_dest: Students):
    print(f'Update existing student: {student_record_srce.badgeNumber} :: {student_record_srce.firstName} {student_record_srce.lastName}')
    if student_record_srce.badgeNumber != student_record_dest.badgeNumber:
        raise Exception("Invalid badge number check!")
    if student_record_srce.firstName != student_record_dest.firstName:
        raise Exception("Invalid first name check!")
    if student_record_srce.lastName != student_record_dest.lastName:
        raise Exception("Invalid first name check!")

    pass

# ------------------------------------------------------------------
# Update the member since date to a standard format, use to sort
# on the GUI
# ------------------------------------------------------------------
def FixMemberSinceDates():
    student_records_dest = dest_db_session.scalars(select(Students))
    for student_record in student_records_dest:
        if student_record.firstName.endswith('\n'):
            student_record.firstName = student_record.firstName.strip()
            dest_db_session.commit()
        print(f'{student_record.badgeNumber} :: {student_record.memberSince} :: {student_record.firstName} {student_record.lastName} ')
        try:
            parsed_member_since_date       = parse(student_record.memberSince,    fuzzy=False)
            parsed_created_date            = parse(student_record.createDateTime, fuzzy=False)
            student_record.memberSinceDate = parsed_member_since_date.strftime(constants.fmtDateTime)
            print(f'{student_record.badgeNumber} :: {parsed_member_since_date} :: {parsed_created_date.strftime(constants.fmtDateTime)}')
            dest_db_session.commit()
        except Exception as ex:
            print(f'{str(ex)}')
