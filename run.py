from app import api, app
from views import CampaignListR, CampaignR, AdRollUpLastWeek, ImpressionListR, InteractionListR

api.add_resource(CampaignListR, '/campaigns')
api.add_resource(CampaignR, '/campaigns/<campaign_id>')
api.add_resource(ImpressionListR, '/impressions')
api.add_resource(InteractionListR, '/interactions')
api.add_resource(AdRollUpLastWeek, '/ads')

if __name__ == '__main__':

    app.run(debug=True)
