# sqlacodegen sqlite:///C:\Users\jdugger01\AppData\Roaming\Attendance\AttendanceV2_20260316.db
# sqlacodegen sqlite:///C:\Users\jdugger01\AppData\Roaming\Attendance\AttendanceV3.db
# sqlacodegen sqlite:///C:\Users\jdugger01\AppData\Roaming\Attendance\AttendanceV2_20251107.db

from services.attendance import GetAttendanceOriginalRawData

#from services.table_procs_sqlite import list_all_tables, get_table_info, open_sqlite_conn, close_sqlite_conn


# Press the green button in the gutter to run the script.

# def display_all_tables(all_tables: list[dict]):
#     for table_name in all_tables:
#         print(f'------------------------------')
#         print(f'table name: {table_name}')
#         table_def_cols = get_table_info(table_name)
#         for table_col in table_def_cols:
#             print(f'table_def name: {table_col['name']} : {table_col['type']}')



if __name__ == '__main__':
    # db_path = getDbPath()
    try:
        GetAttendanceOriginalRawData()
        #ImportRequirementsRecords()
    except Exception as e:
        print(f"An error occurred: {e}")
        # close_sqlite_conn()

