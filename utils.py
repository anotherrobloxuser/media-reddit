
import re, argparse, os, requests,termcolor, redvid
from fake_useragent import UserAgent



class other:
    def nsfwcheck(data={},num=0,userwantsnsfw=False,only=False):
        if str.lower(userwantsnsfw) == 'true' and str.lower(only) == 'true':
            if data[num]['data']['over_18'] == True:
                return True
            else:
                return False

        elif str.lower(userwantsnsfw) == 'false' and str.lower(only) == 'true':
            if data[num]['data']['over_18'] == False:
                return True
            else:
                return False
        return True

    def makeargs():
        parser = argparse.ArgumentParser(
        description='Modified Grab_pictures. USAGE: py fetch.py -s furry -n 100 -t all -loc D:/pogchampinc')
        parser.add_argument('-s', '--subreddit', nargs='+', type=str, metavar='',
                            required=True, help='Exact name of the subreddits you want to grab pictures')
        parser.add_argument('-n', '--number', type=int, metavar='', default=10,
                            help='specify amount to download. Max=1000,Def=10')
        parser.add_argument('-t', '--top', type=str, metavar='', choices=['day', 'week', 'month', 'year', 'all'],
                            default='all', help='Specify if top is [day, week, month, year or all] (optional)')
        parser.add_argument('-loc', '--location', type=str, metavar='',
                            help='Specify directory for items. REQUIRED', required=True)
        parser.add_argument('-nsfw', type=str, metavar='', default=False, required=False,
                            help='Handles NSFW content')
        parser.add_argument('-only', type=str, metavar='', default=False, required=False,
                            help='nsfw handler becomes useless if only is not True')
        return parser.parse_args()





class wifi_related:
    def add(data,num,location,sub,subnum):
        blank = '            '

        location = os.path.join(location,sub[subnum])
        if not os.path.exists(location):
            os.makedirs(location)


        listlocation = os.listdir(location) 

        post = data[num]['data']
        img_url = post['url']
        filetype,img_url2 = file_related.filenamecheck(img_url)

        title = file_related.get_valid_filename(post['title'])

        with open(location+'\log.txt','a+') as log:
            for i in range(len(listlocation)):
                    if title in listlocation[i]:
                        print(termcolor.colored(title+' has a match, skipping..',on_color='on_yellow'),blank)
                        log.write(title+' has a match, skipping..\n')
                        return

            
            if filetype == 'video' and img_url2 != False:
                downloader = redvid.Downloader(path=location,max_q=True,)
                downloader.url = img_url2
                try:
                    video = downloader.download()
                    os.rename(video, os.path.join(location,title)+'.mp4')
                    print(termcolor.colored(title,on_color='on_green'),blank)
                except:
                    print(termcolor.colored(title+'     RETRIEVE ERROR 2',on_color='on_red'),blank)
                    log.write(title+'     RETRIEVE ERROR 2\n')

            elif filetype != False and img_url2 != False:

                try:
                    image = requests.get(img_url2, allow_redirects=True)                                    
                except:
                    image = None
                    print(termcolor.colored(title+'      RETRIEVE ERROR',on_color='on_red'),blank)
                    log.write(title+'      RETRIEVE ERROR '+img_url+'\n')
                
                if image != None:
                    
                    try: 
                        with open(location+'/'+ title + filetype, mode='bx') as file:
                            file.write(image.content)
                        print(termcolor.colored(title,on_color='on_green'),blank)
                    except:
                        print(termcolor.colored(title+'     WRITE ERROR',on_color='on_red'),blank)
                        log.write(title+'     WRITE ERROR\n')


                print(termcolor.colored(title,on_color='on_green'),blank)
            else:
                print(termcolor.colored(title+'      DID NOT PASS FILECHECK. LINK '+img_url,on_color='on_red'),blank)
                log.write(title+'      DID NOT PASS FILECHECK. LINK '+img_url+'\n')


    def chkwifi():
        try:
            attmpt = requests.get('https://reddit.com')
            if attmpt.status_code != 200:
                print('no internet connection: Error '+str(attmpt.status_code))
                attmpt = False
        except:
            print('no internet connection')
            attmpt = False
        return attmpt

    
    def get_userAgent():
        return UserAgent(fallback='Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11')

    def retrieve_data(subreddit,num,popularity,amount,agent):
        url = 'https://www.reddit.com/r/' + subreddit[num] + '/top/.json?sort=top&t='+popularity + '&limit=' + str(amount)
        try:
            response = requests.get(url, headers={'User-agent': agent.random})
        except:
            response = None
        return response

class file_related:
    def filenamecheck(post):
        if '.png' in post:
            return '.png',post
        elif '.jpg' in post or '.jpeg' in post:
            return '.jpeg',post
        elif 'imgur' in post:
            if '.gif' in post:
                return '.gif',post
            post += '.jpeg'
            return '.jpeg',post
        elif '.gif' in post:
            return '.gif',post
        elif 'v.redd.it' in post:
            return 'video',post
        else:
            return False,False

    def get_valid_filename(s):
        ''' strips out special characters and replaces spaces with underscores, len 200 to avoid file_name_too_long error '''
        s = str(s).strip().replace(' ', '_')
        return re.sub(r'[^\w.]', '', s)[:200]