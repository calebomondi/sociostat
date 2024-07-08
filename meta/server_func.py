import requests
import facebook as fb
import urllib.parse
import json
from .models import UsrCredentials, Followers

#FACEBOOK
def viewCompiler(email):
    print('ViewCompiler')
    #------------------
    user = UsrCredentials.objects.get(email=email)
    page_AT = user.pgat
    page_id = user.fbpageid
    #--
    dat1 = []
    dat2 = []
    cData = []
    #--
    fields = 'attachments,created_time,permalink_url,full_picture,likes.summary(true),comments.summary(true),shares.summary(true)'
    #get post IDs
    url = f'https://graph.facebook.com/v19.0/{page_id}/posts?access_token={page_AT}&limit=10'
    res = requests.get(url).json()
    if res:
        for dat in res['data']:
            #get post info
            url1 = f'https://graph.facebook.com/v19.0/{dat['id']}?fields={fields}&access_token={page_AT}'
            res1 = requests.get(url1).json()
            dat1.append(res1)
            url2 = f'https://graph.facebook.com/v19.0/{dat['id']}/insights?metric=post_impressions_unique&access_token={page_AT}'
            res2 = requests.get(url2).json()
            dat2.append(res2)
    #----------------
    size = len(dat1)
    print(f'VIEW COMPILER FB: {size}')
    i = 0
    while i < size:
        try:
            dicti = {}
            #--dat1
            if 'full_picture' in dat1[i]:
                dicti['imgUrl'] = dat1[i]['full_picture']
            else:
                dicti['imgUrl'] = 'https://scontent.cdninstagram.com/v/t51.29350-15/448631213_820384950019850_7615961932364156545_n.jpg?_nc_cat=105&ccb=1-7&_nc_sid=18de74&_nc_ohc=OCreUA8HzfYQ7kNvgGBv061&_nc_ht=scontent.cdninstagram.com&edm=AEQ6tj4EAAAA&oh=00_AYCxF94YLn5mkRnj0c2OYRV5MMwrI3dv46KSvRiOgXANjg&oe=667C7D66'
            dicti['postUrl'] = dat1[i]['permalink_url']
            dicti['date'] = dat1[i]['created_time'][:10]
            dicti['likes'] = dat1[i]['likes']['summary']['total_count']
            dicti['comments'] = dat1[i]['comments']['summary']['total_count']
            if 'attachments' in dat1[i]:
                mediaTyp = dat1[i]['attachments']['data'][0]['type']
                if mediaTyp == 'video_inline':
                    dicti['type'] = 'V'
                    video_id = dat1[i]['attachments']['data'][0]['target']['id']
                    #--
                    url = f'https://graph.facebook.com/v19.0/{video_id}/video_insights?metric=total_video_views&access_token={page_AT}'
                    res = requests.get(url).json()
                    dicti['views'] = res['data'][0]['values'][0]['value']
                    #--
                elif mediaTyp == 'album':
                    dicti['type'] = 'A'
                elif mediaTyp == 'photo':
                    dicti['type'] = 'P'
            else:
                dicti['type'] = 'T'
            #--dat2
            dicti['reach'] = dat2[i]['data'][0]['values'][0]['value']

            if 'shares' in dat1[i]:
                dicti['shares'] = dat1[i]['shares']['count']
            else:
                dicti['shares'] = 0
            cData.append(dicti)
        except KeyError as e:
            print(f"KeyError at index {i}: {e}")
        except IndexError as e:
            print(f"IndexError at index {i}: {e}")
        except Exception as e:
            print(f"Unexpected error at index {i}: {e}")
        i += 1
    return cData

def dashData(data,email):
    user = UsrCredentials.objects.get(email=email)
    page_AT = user.pgat
    page_id = user.fbpageid
    #---
    tot_likes = 0
    tot_com = 0
    tot_posts = 0
    tot_shares = 0
    #get page likes and followers
    url = f'https://graph.facebook.com/v19.0/{page_id}?fields=fan_count,followers_count&access_token={page_AT}'
    res = requests.get(url).json()
    #get posts data
    urlP = f'https://graph.facebook.com/v19.0/{page_id}/posts?access_token={page_AT}'
    while urlP:
        response = requests.get(urlP)
        urldata = response.json()
        if 'data' in urldata:
            tot_posts += len(urldata['data'])
            urlP = urldata.get('paging', {}).get('next', None)
        else:
            break
    #---
    #get LCS
    for dat in data:
        tot_likes += dat['likes']
        tot_com += dat['comments']
        tot_shares += dat['shares']
    
    return {'plikes':res['fan_count'], 'followers':res['followers_count'], 'likes':tot_likes, 'comments': tot_com, 'shares':tot_shares, 'posts':tot_posts}

def most(email):
    comments = []
    likes = []
    shares = []
    #return
    final = {}
    #get LCS
    data = viewCompiler(email)
    print('MOST')
    for dat in data:
        comments.append(dat['comments'])
        likes.append(dat['likes'])
        shares.append(dat['shares'])
    shares.sort(reverse=True)
    likes.sort(reverse=True)
    comments.sort(reverse=True)
    #get post
    for dat in data:
        if dat['comments'] == comments[0]:
            final['comments'] = dat
        if dat['likes'] == likes[0]:
            final['likes'] = dat
        if dat['shares'] == shares[0]:
            final['shares'] = dat
    recent = data[0]
    final['recent'] = recent
    dash = dashData(data,email)
    return {'final': final, 'dash':dash}

def trendsCompilerFb(email):
    print('Trends Compiler!')
    #--
    user = UsrCredentials.objects.get(email=email)
    page_AT = user.pgat
    page_id = user.fbpageid
    #--
    dat1 = []
    dat2 = []
    final = {}
    likes = []
    reach = []
    comments = []
    #--
    url = f'https://graph.facebook.com/v19.0/{page_id}/posts?access_token={page_AT}&limit=20'
    res = requests.get(url).json()
    if res:
        for dat in res['data']:
            url1 = f'https://graph.facebook.com/v19.0/{dat['id']}?fields=likes.summary(true),comments.summary(true)&access_token={page_AT}'
            res1 = requests.get(url1).json()
            dat1.append(res1)
            url2 = f'https://graph.facebook.com/v19.0/{dat['id']}/insights?metric=post_impressions_unique&access_token={page_AT}'
            res2 = requests.get(url2).json()
            dat2.append(res2)
    #--
    size = len(dat1)
    while i < size:
        likes.append(dat1[i]['likes']['summary']['total_count'])
        comments.append(dat1[i]['comments']['summary']['total_count'])
        reach.append(dat2[i]['data'][0]['values'][0]['value'])
   
    final['likes1'] = likes[:10][::-1]
    final['comments1'] = comments[:10][::-1]
    final['reach1'] = reach[:10][::-1]
    final['likes2'] = likes[10:][::-1]
    final['comments2'] = comments[10:][::-1]
    final['reach2'] = reach[10:][::-1]

    return final

#INSTAGRAM
def mediaIDs(email):
    user = UsrCredentials.objects.get(email=email)
    igAT = user.llat
    ig_user_id = user.iguserid
    #get media objects
    url = f'https://graph.facebook.com/v19.0/{ig_user_id}/media?access_token={igAT}&limit=20'
    response = requests.get(url).json()
    if 'data' in response:
        return response['data']

def totalCLS(email):
    print(f'totalCLS')
    user = UsrCredentials.objects.get(email=email)
    igAT = user.llat
    #ig_user_id = user.iguserid
    #---
    mediaIDS = mediaIDs(email)
    #---
    metrics = 'likes, comments, shares'
    likes = 0
    comments = 0
    shares = 0
    #get media objects
    i = 1
    for mediaObj in mediaIDS[:10]:
        post_likes = 0
        post_comments = 0
        post_shares = 0
        #media insites
        url_media = f'https://graph.facebook.com/{mediaObj['id']}/insights?metric={metrics}&access_token={igAT}'
        media_info = requests.get(url_media).json()
        for dat in media_info['data']:
            if dat['name'] == 'likes':
                post_likes = dat['values'][0]['value']
            if dat['name'] == 'comments':
                post_comments = dat['values'][0]['value']
            if dat['name'] == 'shares':
                post_shares = dat['values'][0]['value']
        likes += post_likes
        comments += post_comments
        shares += post_shares
        i += 1
    return {'likes': likes, 'comments':comments, 'shares':shares}

def mostIg(email):
    print('MOST')
    user = UsrCredentials.objects.get(email=email)
    igAT = user.llat
    ig_user_id = user.iguserid
    #--
    metrics = 'likes,comments, shares, video_views'
    mediaIDS = mediaIDs(email)
    #Arrays
    Likes = []
    Shares = []
    Comments = []
    #to return
    most_likes = {}
    most_comm = {}
    most_shares = {}
    final = {}
    postIDs = {}
    #get media objects
    i = 1
    for mediaObj in mediaIDS[:10]:
        url_media = f'https://graph.facebook.com/{mediaObj['id']}/insights?metric={metrics}&access_token={igAT}'
        media_info = requests.get(url_media).json()
        #--
        for dat in media_info['data']:
            if dat['name'] == 'likes':
                Likes.append(dat['values'][0]['value'])
            if dat['name'] == 'shares':
                Shares.append(dat['values'][0]['value'])
            if dat['name'] == 'comments':
                Comments.append(dat['values'][0]['value'])
        i += 1
    Likes.sort(reverse=True)
    Comments.sort(reverse=True)
    Shares.sort(reverse=True)
    i = 0
    for mediaObj in mediaIDS[:10]:
        url_media = f'https://graph.facebook.com/{mediaObj['id']}/insights?metric={metrics}&access_token={igAT}'
        media_info = requests.get(url_media).json()
        for dat in media_info['data']:
            if dat['name'] == 'likes':
                if dat['values'][0]['value'] == Likes[0]:
                    most_likes['views'] = media_info['data'][0]['values'][0]['value']
                    most_likes['likes'] = Likes[0]
                    most_likes['comments'] = media_info['data'][2]['values'][0]['value']
                    most_likes['shares'] = media_info['data'][3]['values'][0]['value']
                    most_likes['url'] = getURL(mediaObj['id'],igAT)
            if dat['name'] == 'comments':
                if dat['values'][0]['value'] == Comments[0]:
                    most_comm['views'] = media_info['data'][0]['values'][0]['value']
                    most_comm['likes'] = media_info['data'][1]['values'][0]['value']
                    most_comm['comments'] = Comments[0]
                    most_comm['shares'] = media_info['data'][3]['values'][0]['value']
                    most_comm['url'] = getURL(mediaObj['id'],igAT)
            if dat['name'] == 'shares':
                if dat['values'][0]['value'] == Shares[0]:
                    most_shares['views'] = media_info['data'][0]['values'][0]['value']
                    most_shares['likes'] = media_info['data'][1]['values'][0]['value']
                    most_shares['comments'] = media_info['data'][2]['values'][0]['value']
                    most_shares['shares'] = Shares[0]
                    most_shares['url'] = getURL(mediaObj['id'],igAT)
        i += 1

    recent = mediaIDS[0]['id']
    print(f'recent - {recent}')
    #get likes,shares,comments
    url_media = f'https://graph.facebook.com/{recent}/insights?metric={metrics}&access_token={igAT}'
    media_info = requests.get(url_media).json()
    for dat in media_info['data']:
        if dat['name'] == 'comments':
            post_comments = dat['values'][0]['value']
        if dat['name'] == 'likes':
            post_likes = dat['values'][0]['value']
        if dat['name'] == 'shares':
            post_shares = dat['values'][0]['value']
    #post link and short code
    post_url = getURL(recent,igAT)

    if 'thumbnail_url' in post_url:
        url = f'https://graph.facebook.com/{recent}/insights?metric=video_views&access_token={igAT}'
        response = requests.get(url).json()
        views = response['data'][0]['values'][0]['value']
        most_recent = {'url':post_url,'likes':post_likes, 'shares':post_shares, 'comments':post_comments, 'views':views}
    elif 'media_url' in post_url:
        most_recent = {'url':post_url,'likes':post_likes, 'shares':post_shares, 'comments':post_comments}

    return {'shared': most_shares, 'liked': most_likes, 'commented': most_comm, 'recent': most_recent}

def getURL(pID,igAT):
    fields = 'permalink,media_url,timestamp,thumbnail_url'
    url_link = f'https://graph.facebook.com/v15.0/{pID}?fields={fields}&access_token={igAT}'
    return requests.get(url_link).json()

def compilePosts(email):
    final = []
    #--
    user = UsrCredentials.objects.get(email=email)
    igAT = user.llat
    ig_user_id = user.iguserid
    #---
    mediaIDS = mediaIDs(email)
    #---
    metrics = 'likes,comments, shares,reach,video_views'
    fields = 'permalink,media_url,timestamp,thumbnail_url'
    data = []
    links = []
    #get media objects
    i = 1
    for mediaObj in mediaIDS[:10]:
        print(i)
        #media insites
        url_media = f'https://graph.facebook.com/{mediaObj['id']}/insights?metric={metrics}&access_token={igAT}'
        media_info = requests.get(url_media).json()
        data.append(media_info)
        #post link and short code
        url_link = f'https://graph.facebook.com/v15.0/{mediaObj['id']}?fields={fields}&access_token={igAT}'
        post_url = requests.get(url_link).json()
        links.append(post_url)
        i += 1
    #--
    size = len(data)
    
    i = 0
    while i < size:
        addData = {}
        addData['date'] = links[i]['timestamp'][:10]
        if 'media_url' in links[i]:
            addData['imgUrl'] = links[i]['media_url']
            addData['reel'] = 0
        elif 'thumbnail_url' in links[i]:
            addData['imgUrl'] = links[i]['thumbnail_url']
            addData['reel'] = 1
        addData['postUrl'] = links[i]['permalink']
        addData['views'] = data[i]['data'][0]['values'][0]['value']
        addData['likes'] = data[i]['data'][1]['values'][0]['value']
        addData['comments'] = data[i]['data'][2]['values'][0]['value']
        addData['shares'] = data[i]['data'][3]['values'][0]['value']
        addData['reach'] = data[i]['data'][4]['values'][0]['value']
        #print(addData)
        final.append(addData)
        i += 1      
    
    return final

def getPostsDataTrends(email):
    user = UsrCredentials.objects.get(email=email)
    igAT = user.llat
    ig_user_id = user.iguserid
    #---
    metrics = 'likes,comments,reach'
    final = {}
    likes = []
    reach = []
    comments = []
    #get media objects
    mediaObjArr = mediaIDs(email)
    print(f'size trnds IG: {len(mediaObjArr)}')
    #get single post metrics
    i = 0
    for mediaObj in mediaObjArr:
        #media insites
        url_media = f'https://graph.facebook.com/{mediaObj['id']}/insights?metric={metrics}&access_token={igAT}'
        media_info = requests.get(url_media).json()
        likes.append(media_info['data'][0]['values'][0]['value'])
        comments.append(media_info['data'][1]['values'][0]['value'])
        reach.append(media_info['data'][2]['values'][0]['value'])
        i +=1 
    
    final['likes1'] = likes[:10][::-1]
    final['comments1'] = comments[:10][::-1]
    final['reach1'] = reach[:10][::-1]
    final['likes2'] = likes[10:][::-1]
    final['comments2'] = comments[10:][::-1]
    final['reach2'] = reach[10:][::-1]
    
    return final