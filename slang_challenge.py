import requests
import json
from itertools import groupby
from itertools import groupby

# some auxiliar functions to sort the dictionary
def key_func(k):
    return k['user_id']
def key_func_2(k):
    return k['first_seen_at']
def key_func_3(k):
    return k['answered_at']

# group by user_id
def  build_user_sessions(parse_json):
    INFO = parse_json['activities']
    INFO = sorted(INFO, key=key_func)
    dic = {}
    for key, value in groupby(INFO, key_func):
        dic[key] = list(value)

    # order by started at
    sorted_new = dic
    for key in dic:
        sorted_new[key] = sorted(dic[key], key=key_func_3)
        sorted_new[key][0]['ended_at'] = sorted_new[key][-1]['answered_at'] # the last "answered at" of the activities
        sorted_new[key] = sorted(dic[key], key=key_func_2)
        sorted_new[key][0]['started_at'] = sorted_new[key][0]['first_seen_at'] # first "first_seen_at" or started_at 
        id_list = []                    
        for i in range(len(sorted_new[key])):
            id_list.append(sorted_new[key][i]['id']) # to storage the activities ids for each user
            del sorted_new[key][i]['answered_at']   # no needed information
            del sorted_new[key][i]['first_seen_at']
            
        sorted_new[key][0]['activities_ids'] = id_list
    return sorted_new

# I get the informaction and put it in a dictionary
response_API = requests.get('https://api.slangapp.com/challenges/v1/activities',
                            headers={"Authorization":"Basic MTU4Ok5OeE5IdU4rRElybkVBSjh0bU9WNUdnVW4wME5QWlZ6Z2UzNkJUV2pDN1E9"})
parse_json = response_API.json()
    
## post
api_url = "https://api.slangapp.com/challenges/v1/activities/sessions"
user_sessions = {"user_sessions": build_user_sessions(parse_json)}
requests.post(api_url,
                        headers={'Authorization':'Basic MTU4Ok5OeE5IdU4rRElybkVBSjh0bU9WNUdnVW4wME5QWlZ6Z2UzNkJUV2pDN1E9'}, 
                        json=user_sessions)