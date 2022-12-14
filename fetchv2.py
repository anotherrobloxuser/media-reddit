# =======================================================
# heavily modified grab_pictures (most of the code is in utils.py), original: https://github.com/nobodyme/reddit-fetch
# modified by Terminal#6623, aka anotherrobloxuser
#
# utils.py expects re, argparse, requests, termcolor, and redvid to be present
#
# USAGE: py fetchv2.py -s [subreddit here] -n 100 -t all -loc D:/ -nsfw True -only True
#
# -s     Subreddit(s)
# -n     Amount desired
# -t     Popularity
# -loc   Location
# -nsfw  True/False (case sensitive)
# -only  nsfw applicability (True/False) (makes -nsfw useless if -only is False)
# =======================================================
import termcolor
from utils import other,wifi_related


args = other.makeargs()

subreddits = args.subreddit
amount = args.number
popularity = args.top
location = args.location

nsfw = args.nsfw
only = args.only

print('checking wifi...',end='\r')
if not wifi_related.chkwifi():
    exit()
print('checking wifi... OK')

print('Retrieving useragent...',end='\r')
agent = wifi_related.get_userAgent()
print('Retrieving useragent... OK')

for i in range(0,len(subreddits)):
    response = wifi_related.retrieve_data(subreddits,i,popularity,amount,agent)
    if response != None:
        data = response.json()['data']['children']

        for b in range(len(data)):
            if other.nsfwcheck(data=data,num=b,userwantsnsfw=nsfw,only=only):
                wifi_related.add(data,b,location,subreddits,i)
            string = str(b)+'/'+str(len(data))+' Complete'
            print(termcolor.colored(string,on_color='on_white'),end='\r')
            