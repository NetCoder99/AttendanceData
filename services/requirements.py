import csv
import json
import os
import re

from sqlalchemy import select, create_engine
from datetime import datetime

from sqlalchemy.orm import Session

import constants
from data.Models import Ranks, Stripes, Requirements, Belts
from services.sqlite_procs import getDbSession, getDbPath

db_session = None
db_name = 'AttendanceRanks.db'

def ImportRequirementsRecords():
    requirements = GetRanksRawData()
    requirements_dict = [requirement.to_dict() for requirement in requirements]
    print(json.dumps(requirements_dict, indent=4))
    DumpRequirementsToCSV(requirements_dict)
    SaveRequirementsToDb(requirements)


def GetRanksRawData():
    global db_session
    rtn_list = []

    db_session   = getDbSession(db_name)
    ranks_stmt   = (select(Ranks)
                    .where(Ranks.RankName.like("White%")
                           | Ranks.RankName.like("Orange%")
                           | Ranks.RankName.like("Yellow%")
                           | Ranks.RankName.like("Blue%")
                           | Ranks.RankName.like("Green%")
                           | Ranks.RankName.like("Purple%")
                           | Ranks.RankName.like("Brown%")
                           | Ranks.RankName.like("Black%")
                           )
                    #.where(Ranks.RankName.like("Orange%"))
                    .order_by(Ranks.RankNumId)
                    )
    rank_records = db_session.execute(ranks_stmt).scalars().all()
    for rank_record in rank_records:
        print(f'rank_record: {rank_record.RankName.strip()}')
        #rank_name_parts = rank_record.RankName.strip().split(' ')
        rank_name_parts = re.split(r'[\s]+', rank_record.RankName.strip())
        stripe_name     = GetStripeName(rank_name_parts)
        stripe_records_stmt  = (select(Stripes)
                          .where(Stripes.beltId      == rank_record.beltId)
                          .where(Stripes.stripeName.like(stripe_name + '%'))
                          )
        stripe_records = db_session.execute(stripe_records_stmt).scalars().all()
        if len(stripe_records) == 0:
            print(f'  !!! No stripe record found for: {rank_record.RankName} : {stripe_name}')
        elif len(stripe_records) > 1:
            print(f'  !!! Multiple stripe records found for: {rank_record.RankName} : {stripe_name}')
        else:
            print(f'  stripe_record: {stripe_records[0].stripeId} : {stripe_records[0].stripeName}')
            requirement_record = BuildRequirementRecord(rank_record, stripe_records[0])
            rtn_list.append(requirement_record)

    return rtn_list

requirement_id = 0
def BuildRequirementRecord(rank_record: Ranks, stripe_record: Stripes) -> Requirements:
    global requirement_id
    requirement_id += 5
    rtn_record = Requirements()
    rtn_record.requirementId = requirement_id
    rtn_record.beltId        = rank_record.beltId
    rtn_record.beltTitle     = GetBeltTitle(rank_record.beltId)
    rtn_record.stripeId      = stripe_record.stripeId
    rtn_record.stripeTitle   = stripe_record.stripeName
    rtn_record.stripeSeqNum  = stripe_record.seqNum
    rtn_record.requiredClasses = rank_record.TotalRequiredClasses
    rtn_record.createDateTime  = datetime.now().strftime(constants.fmtDateTime)
    return rtn_record

def GetBeltTitle(beltId: int) -> str:
    global db_session
    stmt    = select(Belts.beltId, Belts.beltTitle).where(Belts.beltId == beltId)
    results = db_session.execute(stmt).first()
    return results.beltTitle

def GetStripeName(rank_name_parts: list[str]) -> str:
    try:
        if len(rank_name_parts) == 2:
            return 'No stripe earned'
        else:
            return rank_name_parts[2] + ' ' + rank_name_parts[3] # + ' ' + rank_name_parts[4]
    except Exception as ex:
        print(f'ex: {str(ex)}')

def DumpRequirementsToCSV(requirement_records:  list[dict]):
    output_path = os.path.join(os.getcwd(), 'data', 'requirements.csv')
    with open(output_path, 'w', newline='', encoding='utf-8') as csv_file:
        # Use DictWriter to automatically map dictionary keys to columns
        fieldnames = requirement_records[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(requirement_records)

def SaveRequirementsToDb(requirement_records: list[Requirements]):
    engine = create_engine(f'sqlite:///{getDbPath(db_name)}', echo=True)
    with Session(engine) as session:
        for requirement_record in requirement_records:
            session.add(requirement_record)
        session.commit()
