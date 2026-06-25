# ------------------------------------------------------------------------------------------
from typing import Optional

from sqlalchemy import Index, Integer, Text, ForeignKey, LargeBinary
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import NullType


# ------------------------------------------------------------------------------------------
class Base(DeclarativeBase): pass
class BaseSrce(DeclarativeBase): pass
class BaseDest(DeclarativeBase): pass

# ------------------------------------------------------------------------------------------
class Belts(Base):
    __tablename__ = 'belts'
    # __table_args__ = (
    #     Index('belts_beltTitle_IDX', 'beltTitle', unique=True),
    # )
    beltId: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    beltTitle: Mapped[Optional[str]] = mapped_column(Text)
    stripeTitle: Mapped[Optional[str]] = mapped_column(Text)
    classCount: Mapped[Optional[int]] = mapped_column(Integer)
    imageSource: Mapped[Optional[str]] = mapped_column(Text)
    stripeCount: Mapped[Optional[int]] = mapped_column(Integer)

    def to_dict(self):
        return {
            'beltId': self.beltId,
            'beltTitle': self.beltTitle,
            'stripeTitle': self.stripeTitle,
            'classCount': self.classCount,
            'imageSource': self.imageSource,
            'stripeCount': self.stripeCount
        }

class Stripes(Base):
    __tablename__ = 'stripes'

    stripeId: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    stripeName: Mapped[Optional[str]] = mapped_column(Text)
    beltId: Mapped[Optional[int]] = mapped_column(ForeignKey('belts.beltId'))
    classCount: Mapped[Optional[int]] = mapped_column(Integer)
    seqNum: Mapped[Optional[int]] = mapped_column(Integer)
    createDateTime: Mapped[Optional[str]] = mapped_column(Text)
    updateDateTime: Mapped[Optional[str]] = mapped_column(Text)

    # belts: Mapped[Optional['Belts']] = relationship('Belts', back_populates='stripes')
    # requirements: Mapped[list['Requirements']] = relationship('Requirements', back_populates='stripes')

class StripePrefixes(Base):
    __tablename__ = 'stripePrefixes'
    stripePrefixId: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    stripePrefix: Mapped[Optional[str]] = mapped_column(Text)
    stripePrefixSeq: Mapped[Optional[int]] = mapped_column(Integer)


class Ranks(Base):
    __tablename__ = 'ranks'

    RankName:         Mapped[Optional[str]] = mapped_column(Text)
    RequirementType:  Mapped[Optional[str]] = mapped_column(Text)
    RequirementValue: Mapped[Optional[int]] = mapped_column(Integer)
    TotalRequiredClasses: Mapped[Optional[int]] = mapped_column(Integer)
    RankNumId:        Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    beltId:           Mapped[Optional[int]] = mapped_column(Integer)
    stripeId:         Mapped[Optional[int]] = mapped_column(Integer)

class Requirements(Base):
    __tablename__ = 'requirements'

    requirementId:   Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    beltId:          Mapped[Optional[int]] = mapped_column(ForeignKey('belts.beltId'))
    beltTitle:       Mapped[Optional[str]] = mapped_column(Text)
    stripeId:        Mapped[Optional[int]] = mapped_column(ForeignKey('stripes.stripeId'))
    stripeTitle:     Mapped[Optional[str]] = mapped_column(Text)
    stripeSeqNum:    Mapped[Optional[int]] = mapped_column(Integer)
    requiredClasses: Mapped[Optional[int]] = mapped_column(Integer)
    createDateTime:  Mapped[Optional[str]] = mapped_column(Text)
    updateDateTime:  Mapped[Optional[str]] = mapped_column(Text)

    def to_dict(self):
        return {
            'requirementId': self.requirementId,
            'beltId': self.beltId,
            'beltTitle': self.beltTitle,
            'stripeId': self.stripeId,
            'stripeTitle': self.stripeTitle,
            'stripeSeqNum': self.stripeSeqNum,
            'requiredClasses': self.requiredClasses,
            'createDateTime': self.createDateTime,
            'updateDateTime': self.updateDateTime,
        }


class AttendanceV1(BaseSrce):
    __tablename__ = 'attendance'

    attendance_id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    badgeNumber: Mapped[Optional[int]] = mapped_column(Integer)
    checkinDateTime: Mapped[Optional[str]] = mapped_column(Text)
    checkinDate: Mapped[Optional[str]] = mapped_column(Text)
    checkinTime: Mapped[Optional[str]] = mapped_column(Text)
    studentName: Mapped[Optional[str]] = mapped_column(Text)
    studentStatus: Mapped[Optional[str]] = mapped_column(Text)
    className: Mapped[Optional[str]] = mapped_column(Text)
    rankName: Mapped[Optional[str]] = mapped_column(Text)
    classStartTime: Mapped[Optional[str]] = mapped_column(Text)

    def to_dict(self):
        return {
            'attendance_id': self.attendance_id,
            'badgeNumber': self.badgeNumber,
            'checkinDateTime': self.checkinDateTime,
            'checkinDate': self.checkinDate,
            'checkinTime': self.checkinTime,
            'studentName': self.studentName,
            'studentStatus': self.studentStatus,
            'className': self.className,
            'rankName': self.rankName,
            'classStartTime': self.classStartTime

        }

class Attendance(Base):
    __tablename__ = 'attendance'

    attendance_id    : Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    badgeNumber      : Mapped[Optional[int]] = mapped_column(Integer)
    checkinDateTime  : Mapped[Optional[str]] = mapped_column(Text)
    checkinDate      : Mapped[Optional[str]] = mapped_column(Text)
    checkinTime      : Mapped[Optional[str]] = mapped_column(Text)
    studentFirstName : Mapped[Optional[str]] = mapped_column(Text)
    studentLastName  : Mapped[Optional[str]] = mapped_column(Text)
    studentStatus    : Mapped[Optional[str]] = mapped_column(Text)
    studentRankNum   : Mapped[Optional[int]] = mapped_column(Integer)
    studentRankName  : Mapped[Optional[str]] = mapped_column(Text)
    studentStripeId  : Mapped[Optional[int]] = mapped_column(Integer)
    studentStripeName: Mapped[Optional[str]] = mapped_column(Text)
    classNum         : Mapped[Optional[int]] = mapped_column(Integer)
    className          : Mapped[Optional[str]] = mapped_column(Text)
    classStartTime     : Mapped[Optional[str]] = mapped_column(Text)
    styleNum           : Mapped[Optional[int]] = mapped_column(Integer)
    appliesPromotion   : Mapped[Optional[str]] = mapped_column(Text)
    attendanceRankName : Mapped[Optional[str]] = mapped_column(Text)
    studentName        : Mapped[Optional[str]] = mapped_column(Text)
    missingBadge       : Mapped[Optional[str]] = mapped_column(Text)

    def to_dict(self):
        return {
            'attendance_id': self.attendance_id,
            'badgeNumber': self.badgeNumber,
            'checkinDateTime': self.checkinDateTime,
            'checkinDate': self.checkinDate,
            'checkinTime': self.checkinTime,
            'studentName' : self.studentName,
            'studentFirstName': self.studentFirstName,
            'studentLastName': self.studentLastName,
            'studentStatus': self.studentStatus,
            'studentRankNum': self.studentRankNum,
            'studentRankName': self.studentRankName,
            'studentStripeId': self.studentStripeId,
            'studentStripeName': self.studentStripeName,
            'classNum': self.classNum,
            'className': self.className,
            'classStartTime': self.classStartTime,
            'styleNum': self.styleNum,
            'appliesPromotion': self.appliesPromotion,
            'attendanceRankName' : self.attendanceRankName,
            'missingBadge' : self.missingBadge
        }

# class AttendanceTemp(BaseDest):
#     __tablename__ = 'attendanceTemp'
#
#     attendance_id    : Mapped[Optional[int]] = mapped_column(Integer, primary_key=True, nullable=False)
#     badgeNumber      : Mapped[Optional[int]] = mapped_column(Integer)
#     checkinDateTime  : Mapped[Optional[str]] = mapped_column(Text)
#     checkinDate      : Mapped[Optional[str]] = mapped_column(Text)
#     checkinTime      : Mapped[Optional[str]] = mapped_column(Text)
#     studentFirstName : Mapped[Optional[str]] = mapped_column(Text)
#     studentLastName  : Mapped[Optional[str]] = mapped_column(Text)
#     studentStatus    : Mapped[Optional[str]] = mapped_column(Text)
#     studentRankNum   : Mapped[Optional[int]] = mapped_column(Integer)
#     studentRankName  : Mapped[Optional[str]] = mapped_column(Text)
#     studentStripeId  : Mapped[Optional[int]] = mapped_column(Integer)
#     studentStripeName: Mapped[Optional[str]] = mapped_column(Text)
#     classNum         : Mapped[Optional[int]] = mapped_column(Integer)
#     className          : Mapped[Optional[str]] = mapped_column(Text)
#     classStartTime     : Mapped[Optional[str]] = mapped_column(Text)
#     styleNum           : Mapped[Optional[int]] = mapped_column(Integer)
#     appliesPromotion   : Mapped[Optional[str]] = mapped_column(Text)
#     attendanceRankName : Mapped[Optional[str]] = mapped_column(Text)
#     def to_dict(self):
#         return {
#             'attendance_id': self.attendance_id,
#             'badgeNumber': self.badgeNumber,
#             'checkinDateTime': self.checkinDateTime,
#             'checkinDate': self.checkinDate,
#             'checkinTime': self.checkinTime,
#             'studentFirstName': self.studentFirstName,
#             'studentLastName': self.studentLastName,
#             'studentStatus': self.studentStatus,
#             'studentRankNum': self.studentRankNum,
#             'studentRankName': self.studentRankName,
#             'studentStripeId': self.studentStripeId,
#             'studentStripeName': self.studentStripeName,
#             'classNum': self.classNum,
#             'className': self.className,
#             'classStartTime': self.classStartTime,
#             'styleNum': self.styleNum,
#             'appliesPromotion': self.appliesPromotion,
#             'attendanceRankName' : self.attendanceRankName
#         }

class Classes(Base):
    __tablename__ = 'classes'
    __table_args__ = (
        Index('idx_classes_n1', 'classDayOfWeek'),
    )

    classNum: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    className: Mapped[Optional[str]] = mapped_column(Text)
    styleNum: Mapped[Optional[int]] = mapped_column(Integer)
    styleName: Mapped[Optional[str]] = mapped_column(Text)
    classDayOfWeek: Mapped[Optional[int]] = mapped_column(Integer)
    classStartTime: Mapped[Optional[str]] = mapped_column(Text)
    classFinisTime: Mapped[Optional[str]] = mapped_column(Text)
    classDuration: Mapped[Optional[int]] = mapped_column(Integer)
    allowedRanks: Mapped[Optional[str]] = mapped_column(Text)
    classDisplayTitle: Mapped[Optional[str]] = mapped_column(Text)
    allowedAges: Mapped[Optional[str]] = mapped_column(Text)
    classCheckinStart: Mapped[Optional[str]] = mapped_column(Text)
    classCheckInFinis: Mapped[Optional[str]] = mapped_column(Text)
    isPromotions: Mapped[Optional[str]] = mapped_column(Text)
    createDateTime: Mapped[Optional[str]] = mapped_column(Text)
    updateDateTime: Mapped[Optional[str]] = mapped_column(Text)

    def to_dict(self):
        return {
            'classNum': self.classNum,
            'className': self.className,
            'styleNum': self.styleNum,
            'styleName': self.styleName,
            'classDayOfWeek': self.classDayOfWeek,
            'classStartTime': self.classStartTime,
            'classFinisTime': self.classFinisTime,
            'classDuration': self.classDuration,
            'allowedRanks': self.allowedRanks,
            'classDisplayTitle': self.classDisplayTitle,
            'allowedAges': self.allowedAges,
            'classCheckinStart': self.classCheckinStart,
            'classCheckInFinis': self.classCheckInFinis,
            'isPromotions': self.isPromotions,
            'createDateTime': self.createDateTime,
            'updateDateTime': self.updateDateTime
        }

class Students(Base):
    __tablename__ = 'students'

    badgeNumber: Mapped[int] = mapped_column(Integer, primary_key=True)
    firstName: Mapped[Optional[str]] = mapped_column(Text)
    lastName: Mapped[Optional[str]] = mapped_column(Text)
    namePrefix: Mapped[Optional[str]] = mapped_column(Text)
    email: Mapped[Optional[str]] = mapped_column(Text)
    address: Mapped[Optional[str]] = mapped_column(Text)
    address2: Mapped[Optional[str]] = mapped_column(Text)
    city: Mapped[Optional[str]] = mapped_column(Text)
    country: Mapped[Optional[str]] = mapped_column(Text)
    state: Mapped[Optional[str]] = mapped_column(Text)
    zip: Mapped[Optional[str]] = mapped_column(Text)
    birthDate: Mapped[Optional[str]] = mapped_column(Text)
    phoneHome: Mapped[Optional[str]] = mapped_column(Text)
    phoneMobile: Mapped[Optional[str]] = mapped_column(Text)
    status:       Mapped[Optional[str]] = mapped_column(Text)
    memberSince:  Mapped[Optional[str]] = mapped_column(Text)
    gender:       Mapped[Optional[str]] = mapped_column(Text)
    ethnicity:    Mapped[Optional[str]] = mapped_column(Text)
    studentImageBytes:  Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    studentImagePath:   Mapped[Optional[str]] = mapped_column(Text)
    studentImageBase64: Mapped[Optional[str]] = mapped_column(Text)
    middleName:         Mapped[Optional[str]] = mapped_column(Text)
    studentImageName:  Mapped[Optional[str]] = mapped_column(Text)
    studentImageType:  Mapped[Optional[str]] = mapped_column(Text)
    currentRankNum:    Mapped[Optional[int]] = mapped_column(Integer)
    currentRankName:   Mapped[Optional[str]] = mapped_column(Text)
    currentStripeId:   Mapped[Optional[int]] = mapped_column(Integer)
    currentStripeName: Mapped[Optional[str]] = mapped_column(Text)
    createDateTime:    Mapped[Optional[str]] = mapped_column(Text)
    updateDateTime:    Mapped[Optional[str]] = mapped_column(NullType)
    memberSinceDate:   Mapped[Optional[str]] = mapped_column(Text)
    studentImageDate:  Mapped[Optional[str]] = mapped_column(Text)
    def to_dict(self):
        return {
            'badgeNumber': self.badgeNumber,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'namePrefix': self.namePrefix,
            'email': self.email,
            'address': self.address,
            'address2': self.address2,
            'city': self.city,
            'country': self.country,
            'state': self.state,
            'zip': self.zip,
            'birthDate': self.birthDate,
            'phoneHome': self.phoneHome,
            'phoneMobile': self.phoneMobile,
            'status': self.status,
            'memberSince': self.memberSince,
            'gender': self.gender,
            'ethnicity': self.ethnicity,
            'studentImageBytes': self.studentImageBytes,
            'studentImagePath': self.studentImagePath,
            'studentImageBase64': self.studentImageBase64,
            'middleName': self.middleName,
            'studentImageName': self.studentImageName,
            'studentImageType': self.studentImageType,
            'currentRankNum': self.currentRankNum,
            'currentRankName': self.currentRankName,
            'currentStripeId': self.currentStripeId,
            'currentStripeName': self.currentStripeName,
            'createDateTime': self.createDateTime,
            'updateDateTime': self.updateDateTime,
            'memberSinceDate': self.memberSinceDate,
            'studentImageDate' : self.studentImageDate
        }

class StudentsV1(BaseSrce):
    __tablename__ = 'students'

    badgeNumber: Mapped[int] = mapped_column(Integer, primary_key=True)
    firstName: Mapped[Optional[str]] = mapped_column(Text)
    lastName: Mapped[Optional[str]] = mapped_column(Text)
    namePrefix: Mapped[Optional[str]] = mapped_column(Text)
    email: Mapped[Optional[str]] = mapped_column(Text)
    address: Mapped[Optional[str]] = mapped_column(Text)
    address2: Mapped[Optional[str]] = mapped_column(Text)
    city: Mapped[Optional[str]] = mapped_column(Text)
    country: Mapped[Optional[str]] = mapped_column(Text)
    state: Mapped[Optional[str]] = mapped_column(Text)
    zip: Mapped[Optional[str]] = mapped_column(Text)
    birthDate: Mapped[Optional[str]] = mapped_column(Text)
    phoneHome: Mapped[Optional[str]] = mapped_column(Text)
    phoneMobile: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[Optional[str]] = mapped_column(Text)
    memberSince: Mapped[Optional[str]] = mapped_column(Text)
    gender: Mapped[Optional[str]] = mapped_column(Text)
    currentRank: Mapped[Optional[str]] = mapped_column(Text)
    ethnicity: Mapped[Optional[str]] = mapped_column(Text)
    studentImage: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    studentImagePath: Mapped[Optional[str]] = mapped_column(Text)
    imageBase64: Mapped[Optional[str]] = mapped_column(Text)

    def to_dict(self):
        return {
            'badgeNumber': self.badgeNumber,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'namePrefix': self.namePrefix,
            'email': self.email,
            'address': self.address,
            'address2': self.address2,
            'city': self.city,
            'country': self.country,
            'state': self.state,
            'zip': self.zip,
            'birthDate': self.birthDate,
            'phoneHome': self.phoneHome,
            'phoneMobile': self.phoneMobile,
            'status': self.status,
            'memberSince': self.memberSince,
            'gender': self.gender,
            'currentRank': self.currentRank,
            'ethnicity': self.ethnicity,
            'studentImage': self.studentImage,
            'studentImagePath': self.studentImagePath,
            'imageBase64': self.imageBase64
        }
