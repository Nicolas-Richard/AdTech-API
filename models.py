from app import db
from datetime import date, datetime

class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    impression_id = db.Column(db.Integer, db.ForeignKey('impression.id'))
    impression = db.relationship('Impression', backref=db.backref('interactions', lazy='dynamic'))
    # Epoch ts
    ts = db.Column(db.Integer)
    event = db.Column(db.String(30))

    def __init__(self, impression, event, ts):
        self.impression = impression
        self.event = event
        self.ts = ts

    def __repr__(self):
        return 'Interaction: %s %s ' % (self.id, self.event)

    def serialize(self):
        return {'interaction_id': self.id, 'event': self.event, 'ts': str(datetime.fromtimestamp(self.ts))}

class Impression(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_id = db.Column(db.Integer, db.ForeignKey('ad.id'))
    ad = db.relationship('Ad', backref=db.backref('impressions', lazy='dynamic'))
    uuid = db.Column(db.Integer)
    # Epoch ts
    ts = db.Column(db.Integer)
    dt = db.Column(db.Integer)

    def __init__(self, ad, uuid, ts):
        self.ad = ad
        self.uuid = uuid
        self.ts = ts
        self.dt = date.fromtimestamp(ts).strftime('%Y%m%d')

    def __repr__(self):
        return 'Impression: %s' % self.id

    def serialize(self):
        return {'impression_id': self.id, 'uuid': self.uuid, 'ts': str(datetime.fromtimestamp(self.ts))}

class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    campaign = db.relationship('Campaign', backref=db.backref('ads', lazy='dynamic'))

    def __init__(self, name, campaign):
        self.name = name
        self.campaign = campaign

    def __repr__(self):
        return 'Ad: %s' % self.name

    def serialize(self):
        return {'ad_id': self.id, 'ad_name': self.name}

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Campaign: %s' % self.name

    def serialize(self):
        return {'id': self.id, 'name': self.name}

    def serialize_with_ads(self):
        return {'id': self.id, 'name': self.name, 'ads': [ a.serialize() for a in self.ads]}

