# # ------------------------------------------------------------------------------------------
# from data.Models import Belts, Stripes, StripePrefixes
# from services.sqlite_procs import getDbSession
#
# db_session = getDbSession()
#
# def getEligibilityCounts():
#     belt_records     = db_session.query(Belts).order_by(Belts.beltId).all()
#     eligibility_counts = []
#     for belt_record in belt_records:
#         for seq_num in range(0, belt_record.stripeCount):
#             stripe_prefix = db_session.query(StripePrefixes).filter_by(stripePrefixSeq=seq_num).first()
#             eligibility_record = {
#                 'seq_num'        : seq_num,
#                 'belt_id'        : belt_record.beltId,
#                 'stripe_prefix'  : stripe_prefix.stripePrefix,
#                 'stripe_title'   : belt_record.stripeTitle,
#                 'class_count'    : belt_record.classCount,
#                 'eligible_count' : 0
#             }
#             eligibility_counts.append(eligibility_record)
#
#     accum_count = 0
#     for index, eligibility_record in enumerate(eligibility_counts):
#         print(f'{eligibility_record}')
#         accum_count += eligibility_record['class_count']
#
#     print(f'accum_count: {accum_count}')
#
