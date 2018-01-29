'''
@author: Thordis Stella
'''
import json
import random
import re
import pandas as pd
from sodapy import Socrata
from urllib.request import urlretrieve
from Analysis import External_info
import time

app_token = 'hjud0ot8XxK9PvVzqLx5pKIec'
username = 'thordisstella@gmail.com'
password = External_info.password
data_id ="fhrw-4uyv"


def get_client():
    return Socrata("data.cityofnewyork.us"
            , app_token
            , username=username
            , password=password)
    
def get_data_id():
    return data_id

def extract_data(url, file_name):
    urlretrieve(url, file_name)    
    json_data = open(file_name)
    return json.load(json_data)

def get_query_url(org_url,list_and_queries):
    query_url=org_url+"?1=1"
    for query in list_and_queries:
        query_url+="&"+query
    return query_url

def get_json_name_from_url(url):
    return re.findall('[^/]+?.json$',url)[0]         # Here we look for the last '/' in sample_url and identify the rest of the string as the json name if it ends with '.json', and includes at least 1 character between '/' and '.json'

# Note that the select string should only contain names of columns, no aggregated functions
def page_through_data(client, dataset=data_id, num_per_iter=1000, select="*", where="True=True",limit=-1, group_by=[]):
    index=0
    result_df=pd.DataFrame()
    while(True and (limit==-1 or index<limit)):
        curr_result = client.get(dataset, select=select, where=where, limit=num_per_iter, offset=index, order='unique_key')
        curr_result_df = pd.DataFrame.from_records(curr_result)
        if result_df.empty:
            result_df=pd.DataFrame.from_records(curr_result_df)
        else:
            result_df=result_df.append(curr_result_df,ignore_index=True)
        index+=num_per_iter
    if len(group_by)>0:
        return result_df.groupby(group_by).count()
    return result_df

def get_population():
    client = Socrata("data.cityofnewyork.us",
                  app_token,
                  username,
                  password) 
    result = client.get("27iv-9uub", limit=2000)
    return pd.DataFrame.from_records(result)  

def get_n_dist_random_ints(n,range):
    if n>(range[1]-range[0]):       return
    rands=[]
    len = 0
    while(len<n):
        curr_rand = random.randint(range[0],range[1])
        if not (curr_rand in rands):
            rands.append(curr_rand)
            len+=1
    return rands

def timetaken(func,*args):
    def measure_time():
        start=time.time()
        output=func(*args)
        end=time.time()
        print("Run function took {:.13f} seconds.".format(end-start))
        return output
    return measure_time
        