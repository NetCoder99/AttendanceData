import os
import platform

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_session = None

def getDbPath(db_name: str = 'AttendanceV2.db'):
    if platform.system() == 'Windows':
        return os.path.join(os.getenv('APPDATA'), 'Attendance', db_name)
    else:
        return os.path.join('/', 'Attendance', db_name)

def getDbSession(db_name: str = 'AttendanceV2.db'):
    global db_session
    if db_session is None:
        engine = create_engine(f'sqlite:///{getDbPath(db_name)}')
        Session = sessionmaker(bind=engine)
        db_session = Session()
    return db_session
