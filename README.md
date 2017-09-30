# AdTech API Project

### Data Model 

I chose to use a normalized data model to avoid redundancy issues. See the ERD.
Because I'm not interacting with users, I've not created a schema for the "user" table. The user is referenced in the "impression" table via the "uuid" field (a foreign key should be used there).

For the development and testing I have used SQLite as my database.
However for production environment Postgres should be used, because I'm using an ORM (SQLAlchemy) to interact with the database, changing the database service would require no code change.

In order to meet the low-latency requirement I rely on partitions and indexes (they are not created in this code).

Partitions: (used for small cardinalities)
- The "ad" table is partitioned by "campaign_id"
- The "impression" table is partitioned by day ("dt") and "ad_id"

Indexes: (used for high cardinalities)
- The "impression" table is indexed by "ad_id"
- The "interaction" table is indexed by "impression_id"

### API implementation

I'm using [Flask-restful](http://flask-restful.readthedocs.io/) and SQLAlchemy.
The application is stateless which allows it to scale horizontally.

### Installation
To run this code you will need Python and Sqlite3.

**Installation steps**:

1. Create a Python virtual environment and activate it
2. Install the required Python packages
```
pip install requirement.txt
```
3. In the file "config.py" set the database URI
4. Create the tables and populate them with test data :
```
python db_setup.py
```
5. Start the service
```
python run.py
```
6. Open "home.html" in your browser (static homepage that showcases the various API endpoints) 



### Objective 1

_"Make a HTTP request to your service to get number of impressions, interactions, and swipes for each ad in a specific campaign (we expect you have some fake data)"_

This is accomplished by this endpoint : http://127.0.0.1:5000/campaigns/campaign_id

Because the "ad" table is partitioned by "campaign_id" the database will only read ad records that we care about to answer this request. As for the counts of "impressions" and "interactions" these tables will be joined respectively on "ad_id" and "impression_id" which are both indexed by these fields.

Example of what the endpoint returns:
```
{
    "campaign_ads": [
        {
            "ad_id": 1, 
            "ad_name": "ORP jerseys", 
            "count_impressions": 1, 
            "count_interactions": 1, 
            "count_swipes": 1
        }, 
        {
            "ad_id": 2, 
            "ad_name": "ORP tourism", 
            "count_impressions": 1, 
            "count_interactions": 1, 
            "count_swipes": 0
        }
    ], 
    "campaign_id": "1"
}
```


### Objective 2

_"Make another HTTP request to get number of uniqueUsers and impressions for each ad in the last week"_

This is accomplished by this endpoint : http://127.0.0.1:5000/ads

Because the ad table is partitioned by day (field "dt"), to answer this request we will only read the ad records that matters.


Example of what the endpoint returns:
```
{
    "ad_roll_up_last_week": [
        {
            "ad_id": 1, 
            "ad_name": "ORP jerseys", 
            "count_impressions": 3, 
            "count_uniqueUsers": 2
        }, 
        {
            "ad_id": 2, 
            "ad_name": "ORP tourism", 
            "count_impressions": 1, 
            "count_uniqueUsers": 1
        }
    ]
}
```

### Remarks

- Ingestion system is not included and the API is not set up to do any inserts. However Flask-Restful makes this easy, I would need to define a "post" method on the views for each object. The function receiving the request will simply call the Class constructor (which is implemented).
- I've not implemented any pagination of results provided by the API. This would be required to be consumed by a front-end application displaying the user-facing dashboard. (Here is an example where I did that in a Django project using Posgres: [Tipcharts API](https://tipcharts.herokuapp.com/api/scrapes/))
- I've included several other endpoints to list objects (/interactions, /impression, /campaigns)
- The impression endpoint can be parametarized to look up impressions on a given time frame only using epoch timestamps (ex: "/impressions?start_ts=1505912646&end_ts=10000000000")
- Errors related to query string parameters need to be returned with the appropriate HTTP status (right now it's 200 )

