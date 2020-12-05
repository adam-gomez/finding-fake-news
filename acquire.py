import pandas as pd
import numpy as np
import warnings
import re
import csv
import time
import datetime
import json
import requests
import os

warnings.filterwarnings('ignore')

def getTimeStamp(date_input):
    '''
    This function takes in a date string in MM/DD/YYYY format and returns the same point in time as UTC timecode integer
    '''
    return time.mktime(datetime.datetime.strptime(date_input, "%m/%d/%Y").timetuple())

def create_UTC_list(start_year, start_month, start_day, end_year, end_month, end_day):
    '''
    This function creates a list of dates one month apart formatted into a UTC datetime integer format
    that is compatible with Reddit's RESTFUL api. 
    '''
    utc_dates = []
    sdate = datetime.date(start_year, start_month, start_day)
    edate = datetime.date(end_year, end_month, end_day)
    
    dates = pd.date_range(sdate,edate-datetime.timedelta(days=1),freq='D')
    for i in range(len(dates)):
        dt = datetime.datetime(dates[i].year, dates[i].month, dates[i].day)
        timestamp = int(dt.replace(tzinfo=datetime.timezone.utc).timestamp())
        utc_dates.append(timestamp)
    return utc_dates

dates = create_UTC_list(2008, 10, 1, 2020, 12, 3)

def getPushshiftData(after, before, sub):
    '''
    This function takes in a UTC formatted timecode for a starting date (after) and an ending date (before)
    along with the reddit subreddit of inquiry and returns a dictionary of the response body
    '''
    url = ('https://api.pushshift.io/reddit/search/submission/?size=100&after='+
           str(after)+'&before='+str(before)+'&subreddit='+str(sub)+'&sort_type=score'+'&sort=desc')
    print(url)
    r = requests.get(url)
    data = r.json()
    return data

def acquire_cache_json_onion(dates):
    '''
    This function checks for the 'onion.json' file and reads from it if present. If absent, this
    function pulls data from Reddit's API using the intervals between a list of dates (dates) on the subreddit r/TheOnion 
    and caches the data as 'onion.json'. In either case, a dictionary object is returned from the 'onion.json' file.
    '''
    if not os.path.isfile('onion.json'):
        json_dict = {}
        for i in range(len(dates)-1):
            after = dates[i]
            before = dates[i+1]
            time.sleep(0.40)
            post = getPushshiftData(after, before, 'theonion')
            if len(post['data']) == 0:
                continue
            else:
                if 'data' in json_dict:
                    for i in range(len(post['data'])):
                        json_dict['data'].append(post['data'][i])
                else:
                    json_dict['data'] = list(post['data'])
        with open('onion.json', 'w') as fp:
            json.dump(json_dict, fp, sort_keys = True, indent = 4)
        return json_dict
    else:
        with open('onion.json') as f:
            json_dict = json.load(f)
        return json_dict

def acquire_cache_json_not_onion(dates):
    '''
    This function checks for the 'not_onion.json' file and reads from it if present. If absent, this
    function pulls data from Reddit's API using the intervals between a list of dates (dates) on the subreddit r/NotTheOnion 
    and caches the data as 'onion.json'. In either case, a dictionary object is returned from the 'onion.json' file.
    '''
    if not os.path.isfile('not_onion.json'):
        json_dict = {}
        for i in range(len(dates)-1):
            after = dates[i]
            before = dates[i+1]
            time.sleep(0.40)
            post = getPushshiftData(after, before, 'nottheonion')
            if len(post['data']) == 0:
                continue
            else:
                if 'data' in json_dict:
                    for i in range(len(post['data'])):
                        json_dict['data'].append(post['data'][i])
                else:
                    json_dict['data'] = list(post['data'])
        with open('not_onion.json', 'w') as fp:
            json.dump(json_dict, fp, sort_keys = True, indent = 4)
        return json_dict
    else:
        with open('not_onion.json') as f:
            json_dict = json.load(f)
        return json_dict

def acquire_headlines():
    '''
    This function combines the output of several previous functions to return a single dataframe
    made of two columns:

    'headlines' - contains all of the titles from all captured posts in r/TheOnion and r/NotTheOnion
    'label' - 1 for coming from r/TheOnion and 0 for coming from r/NotTheOnion
    '''
    # Creating a labeled dataframe of all The Onion article headlines
    onion_dict = acquire_cache_json_onion(dates)
    onion_titles = [post['title'] for post in onion_dict['data']]
    onion_titles = list(set(onion_titles))
    onion_dict = {'headline': onion_titles}
    onion_df = pd.DataFrame.from_dict(onion_dict)
    onion_df['label'] = 1

    # Creating a labeled dataframe of all article headlines from r/NotTheOnion
    not_onion_dict = acquire_cache_json_not_onion(dates)
    not_onion_titles = [post['title'] for post in not_onion_dict['data']]
    not_onion_titles = list(set(not_onion_titles))
    not_onion_dict = {'headline': not_onion_titles}
    not_onion_df = pd.DataFrame.from_dict(not_onion_dict)
    not_onion_df['label'] = 0

    # Concatenating the two dataframes together
    headlines = pd.concat([onion_df, not_onion_df], axis=0)
    
    headlines = headlines.reset_index(drop=True)
    return headlines[['label', 'headline']]