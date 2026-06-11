# ------------------------------------------------------------------------------------------
from typing import Optional

from sqlalchemy import Index, Integer, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# ------------------------------------------------------------------------------------------
class Base(DeclarativeBase): pass
class BaseSrce(DeclarativeBase): pass

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

    attendance_id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    badgeNumber: Mapped[Optional[int]] = mapped_column(Integer)
    checkinDateTime: Mapped[Optional[str]] = mapped_column(Text)
    checkinDate: Mapped[Optional[str]] = mapped_column(Text)
    checkinTime: Mapped[Optional[str]] = mapped_column(Text)
    studentFirstName: Mapped[Optional[str]] = mapped_column(Text)
    studentLastName: Mapped[Optional[str]] = mapped_column(Text)
    studentStatus: Mapped[Optional[str]] = mapped_column(Text)
    studentRankNum: Mapped[Optional[int]] = mapped_column(Integer)
    studentRankName: Mapped[Optional[str]] = mapped_column(Text)
    studentStripeId: Mapped[Optional[int]] = mapped_column(Integer)
    studentStripeName: Mapped[Optional[str]] = mapped_column(Text)
    classNum: Mapped[Optional[int]] = mapped_column(Integer)
    className: Mapped[Optional[str]] = mapped_column(Text)
    classStartTime: Mapped[Optional[str]] = mapped_column(Text)
    styleNum: Mapped[Optional[int]] = mapped_column(Integer)
    appliesPromotion: Mapped[Optional[str]] = mapped_column(Text)



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
