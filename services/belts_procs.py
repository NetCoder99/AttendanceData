from sqlalchemy   import select
from data.Models import Students, Belts
from services.sqlite_procs import getDbSession

srce_db_name    = 'AttendanceV3.db'
srce_db_session = getDbSession(srce_db_name)

belt_records = []

def LoadBeltRecords(force_reload: bool = False):
    global belt_records
    if len(belt_records) == 0 or force_reload:
        belt_records_records_tmp = srce_db_session.scalars(select(Belts)).all()
        belt_records = [belts.to_dict() for belts in belt_records_records_tmp]

def GetRankAtCheckin(attendance_record: dict) -> dict:
    try:
        if attendance_record['rankName'] is None or len(attendance_record['rankName']) == 0:
            return {}

        attendance_belt_parts = attendance_record['rankName'].split()
        if len(attendance_belt_parts) == 0:
            raise Exception("invalid attendance record")

        if len(attendance_belt_parts) == 2:
            for belt_record in belt_records:
                #print(f'belt_record: {belt_record}')
                if str(belt_record['beltTitle']).startswith(attendance_belt_parts[0]):
                    return belt_record
        else:
            for belt_record in belt_records:
                #print(f'belt_record: {belt_record}')
                if str(belt_record['beltTitle']).startswith(attendance_belt_parts[0]):
                    return belt_record
                elif str(belt_record['beltTitle']).startswith(attendance_belt_parts[2]):
                    return belt_record
    except Exception as ex:
        print(f'Error: {str(ex)}')

    print(f'missing belt record for: {attendance_record['rankName']}')
    return {}
