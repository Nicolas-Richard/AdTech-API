from models import db
from models import Ad, Campaign, Impression, Interaction

db.create_all()

# Inserting campaigns
a = Campaign('Oi Rio Pro')
b = Campaign('Hurley Lower Trestles')
db.session.add(a)
db.session.add(b)
db.session.commit()

# Inserting ads
c = Ad('ORP jerseys', a)
d = Ad('ORP tourism', a)
e = Ad('ORP hotels', a)
f = Ad('HLT San Clemente Tourism Offices', b)
db.session.add(c)
db.session.add(d)
db.session.add(e)
db.session.add(f)
db.session.commit()

# Inserting impressions
# 1 month ago
imps = [Impression(c, 12345, 1504247734), Impression(c, 12346, 1504255934), Impression(c, 12346, 1504254934), Impression(d, 12345, 1504337734)]
# # last week
imps += [Impression(c, 12345, 1505909046), Impression(c, 12346, 1505909046), Impression(c, 12346, 1505909046), Impression(d, 12345, 1505909046)]
# current week (25th sept +)
imps += [Impression(c, 12345, 1506427386), Impression(c, 12346, 1506427446), Impression(c, 12346, 1504254934), Impression(d, 12345, 1506513846)]
for i in imps:
    db.session.add(i)
db.session.commit()

# Inserting interactions
interactions = [Interaction(imps[11], 'click', 1505912646), Interaction(imps[10], 'swipe', 1505912546)]
for i in imps:
    db.session.add(i)
db.session.commit()

