from sqlalchemy import distinct, func, select, create_engine, case, literal_column
from flask_restful import Resource, reqparse
from datetime import date, timedelta
from models import Campaign, Ad, Impression, Interaction



class CampaignListR(Resource):
    def get(self):
        campaigns = Campaign.query.all()
        campaigns_serialized = [ c.serialize() for c in campaigns]
        return {'campaigns': campaigns_serialized}

class AdRollUpLastWeek(Resource):
    def get(self):
        last_last_monday, last_monday = helper_last_week_boundaries_as_dt()
        print last_last_monday, last_monday
        engine = create_engine('sqlite:////Users/nrichard/celtra/flask-celtra/test.db', echo=True)
        conn = engine.connect()
        s = select([Ad.id, Ad.name, func.count(Impression.id), func.count(distinct(Impression.uuid))])\
            .where(Ad.id == Impression.ad_id)\
            .where(Impression.dt >= last_last_monday)\
            .where(Impression.dt < last_monday)\
            .group_by(Ad.id)
        s_result = conn.execute(s)
        result = {'ad_roll_up_last_week': []}
        for r in s_result:
            print r
            result['ad_roll_up_last_week'].append({'ad_id': r[0],'ad_name': r[1], 'count_impressions': r[2], 'count_uniqueUsers': r[3]})
        return result

class ImpressionListR(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('start_ts', type=int )
        self.reqparse.add_argument('end_ts', type=int)
        super(ImpressionListR, self).__init__()

    # get impressions in the time range specified
    # or 50
    def get(self):
        print self.reqparse.parse_args()
        args = self.reqparse.parse_args()
        # if I'm using the start_ts / end_ts validate start_ts < end_ts
        if args.start_ts and args.end_ts:
            if args.start_ts > args.end_ts:
                return 'ERROR : start_ts > end_ts'
            impressions = Impression.query\
                .filter(Impression.ts >= args.start_ts)\
                .filter(Impression.ts <= args.end_ts)\
                .all()
        elif args.start_ts or args.end_ts:
            return 'ERROR: Providing only start_ts or end_ts is not supported '
        else:
            impressions = Impression.query.limit(50).all()
        impressions_serialized = [i.serialize() for i in impressions]
        return {'impressions': impressions_serialized}

class CampaignR(Resource):
    def get(self, campaign_id):
        engine = create_engine('sqlite:////Users/nrichard/celtra/flask-celtra/test.db', echo=True)
        conn = engine.connect()
        s = select([Ad.id, Ad.name, func.count(Impression.id),
                    func.count(Interaction.id),
                    func.count(case([((Interaction.event == 'swipe'), Interaction.id)], else_=literal_column("NULL")))])\
            .where(Campaign.id == campaign_id)\
            .where(Campaign.id == Ad.campaign_id)\
            .where(Ad.id == Impression.ad_id)\
            .where(Impression.id == Interaction.impression_id)\
            .group_by(Ad.id)
        s_result = conn.execute(s)
        result = {'campaign_id': campaign_id, 'campaign_ads': []}
        for r in s_result:
            print r
            result['campaign_ads'].append({'ad_id': r[0],
                                           'ad_name': r[1],
                                           'count_impressions': r[2],
                                           'count_interactions': r[3],
                                           'count_swipes': r[4]})
        return result

class InteractionListR(Resource):

    # return 50 interactions
    def get(self):
        interactions = Interaction.query.limit(50).all()
        interactions_serialized = [i.serialize() for i in interactions]
        return {'interactions': interactions_serialized}


def helper_last_week_boundaries_as_dt():
    # returns a tuple in the format '%Y%m%d'. Ex: (20170918, 20170925)
    last_monday = (date.today() - timedelta(days=date.today().weekday())).strftime('%Y%m%d')
    last_last_monday = (date.today() - timedelta(days=7+date.today().weekday())).strftime('%Y%m%d')
    return int(last_last_monday), int(last_monday)
