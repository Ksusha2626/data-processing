from pprint import pprint

from HTMLParsing.hh_jobs_parsing import parse_jobs
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['jobs']
hh_jobs = db.hh_jobs
# hh_jobs.create_index([('link', pymongo.TEXT)], name='index', unique=True)


def db_load():
    if hh_jobs.count_documents({}) == 0:
        hh_jobs.insert_many(parse_jobs())
    else:
        for job in parse_jobs():
            if not hh_jobs.find_one({'link': job['link']}):
                hh_jobs.insert_one(job)


def db_find(query):
    for job in hh_jobs.find(query):
        pprint(job)


db_load()
db_find({'$or': [{'salary.min': {'$gt': 500}}, {'salary.max': {'$gt': 500}}]})

# for job in hh_jobs.find({}):
#     pprint(job)
# hh_jobs.drop()
# client.drop_database('jobs')
