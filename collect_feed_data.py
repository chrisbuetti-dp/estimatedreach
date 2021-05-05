#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Non-modulized script for creating data
"""

import os
import requests
import secrets
import time


os.environ['MONGODB_SECRET_LOCATION'] = 'dev/influencer-reporting-v2/mongodb'
os.environ['DB_NAME'] = 'influencerReporting'
os.environ['INFLUENCER_CAMPAIGN_DETAILS_COLLECTION'] = 'campaignDetails'
os.environ['INFLUENCER_TRACKING_COLLECTION'] = 'influencers'
os.environ['INFLUENCER_REPORTING_QUEUE'] = 'dev-influencer-reporting-queue-v2'
os.environ['PROXY_SECRET_LOCATION'] = 'dev/influencer-reporting-v2/proxy'

from start_tracking import db
reach_collection = db['reachData']

reach_data = db['reach_data']

username = 'joelnunez'
proxy = secrets.get_proxy()

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ' \
           '(KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36'
}


r = requests.get("https://www.instagram.com/" + username + '/reels/?__a=1', headers=headers)


res = r.json()

feed = res['graphql']['user']['edge_owner_to_timeline_media']['edges']
user_info = res['graphql']['user']

for i in range(len(user_info['edge_owner_to_timeline_media']['edges'])):
    
    print(i + 1)
    
    shortcode = user_info['edge_owner_to_timeline_media']['edges'][i]['node']['shortcode']
    
    print('https://www.instagram.com/p/' + shortcode)
    
    reach = int(input('Enter reach: '))
    user_info['edge_owner_to_timeline_media']['edges'][i]['node']['reach'] = reach
    
    
    impressions = int(input('Enter impressions: '))
    user_info['edge_owner_to_timeline_media']['edges'][i]['node']['impressions'] = impressions
    
    
    user_info['edge_owner_to_timeline_media']['edges'][i]['node']['record_time'] = time.time()
    
    
reach_data.insert_one(user_info)
    
######################################################################
    ###############################################################
    ###############################################################
    
username = 'ashley_devore'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ' \
           '(KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36'
}    
    

    
r = requests.get("https://www.instagram.com/" + username + '/reels/?__a=1', headers=headers)


res = r.json()


user_info = res['graphql']['user']


docs = reach_collection.find({'owner.username':username})
for doc in docs:
    doc['user_info'] = user_info
    reach_collection.find_and_modify(
        query={'_id': doc['_id']},
        update=doc,
        new=True,
        upsert=True)
    
    
#################################################################
    #################################################################
    #################################################################
    
username = 'thehondaclassic'
docs = reach_collection.find({'owner.username':username})
user_info = docs[0]['user_info']
for i in range(len(user_info['edge_owner_to_timeline_media']['edges'])):
    
    shortcode = user_info['edge_owner_to_timeline_media']['edges'][i]['node']['shortcode']
    
    
    
    temp = reach_collection.find({'shortcode':shortcode})
    try:
        temppost = temp[0]
        
        reach = temppost['reach']
        impressions = temppost['impressions']
        record_time = temppost['record_time']
        
        user_info['edge_owner_to_timeline_media']['edges'][i]['node']['reach'] = reach
        user_info['edge_owner_to_timeline_media']['edges'][i]['node']['impressions'] = impressions
        user_info['edge_owner_to_timeline_media']['edges'][i]['node']['record_time'] = record_time
        
    except:
        print(shortcode)
        

for i in range(len(user_info['edge_owner_to_timeline_media']['edges'])):
    if 'reach' not in user_info['edge_owner_to_timeline_media']['edges'][i]['node']:
        user_info['edge_owner_to_timeline_media']['edges'][i]['node']['reach'] = 0
        user_info['edge_owner_to_timeline_media']['edges'][i]['node']['impressions'] = 0
        user_info['edge_owner_to_timeline_media']['edges'][i]['node']['record_time'] = time.time()
    
reach_data.insert_one(user_info)