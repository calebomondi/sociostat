import requests
from . import config
import facebook as fb
import urllib.parse
import json
from .models import UsrCredentials, Followers

likesComms = []
reach = []
info1 = []
info2 = []

def allPostsView(email):
    print('INSIDE allPostsView!')
    #--
    user = UsrCredentials.objects.get(email=email)
    page_AT = user.pgat
    page_id = user.fbpageid
    #--
    global likesComms,reach,info1,info2
    if likesComms != []:
        print('Global Not Empty!')
        likesComms = []
        reach = []
        info1 = []
        info2 = []
    #--
    fields = 'attachments,created_time,permalink_url,full_picture,likes.summary(true),comments.summary(true),shares.summary(true)'
    #get post IDs
    url = f'https://graph.facebook.com/v19.0/{page_id}/posts?access_token={page_AT}&limit=20'
    res = requests.get(url).json()
    if res:
        i = 0
        for dat in res['data']:
            url1 = f'https://graph.facebook.com/v19.0/{dat['id']}?fields=likes.summary(true),comments.summary(true)&access_token={page_AT}'
            res1 = requests.get(url1).json()
            likesComms.append(res1)
            url2 = f'https://graph.facebook.com/v19.0/{dat['id']}/insights?metric=post_impressions_unique&access_token={page_AT}'
            res2 = requests.get(url2).json()
            reach.append(res2)
            if i < 10:
                #get post info
                url1 = f'https://graph.facebook.com/v19.0/{dat['id']}?fields={fields}&access_token={page_AT}'
                res1 = requests.get(url1).json()
                info1.append(res1)
                url2 = f'https://graph.facebook.com/v19.0/{dat['id']}/insights?metric=post_impressions_unique&access_token={page_AT}'
                res2 = requests.get(url2).json()
                info2.append(res2)
            i += 1

def chartsLoader(email):
    print('INSIDE chartsLoader!')
    #--
    user = UsrCredentials.objects.get(email=email)
    page_AT = user.pgat
    page_id = user.fbpageid
    #--
    global likesComms,reach
    if likesComms:
        likesComms = []
        reach = []
    #--
    url = f'https://graph.facebook.com/v19.0/{page_id}/posts?access_token={page_AT}&limit=20'
    res = requests.get(url).json()
    if res:
        for dat in res['data']:
            url1 = f'https://graph.facebook.com/v19.0/{dat['id']}?fields=likes.summary(true),comments.summary(true)&access_token={page_AT}'
            res1 = requests.get(url1).json()
            likesComms.append(res1)
            url2 = f'https://graph.facebook.com/v19.0/{dat['id']}/insights?metric=post_impressions_unique&access_token={page_AT}'
            res2 = requests.get(url2).json()
            reach.append(res2)

def viewCompiler():
    print('ViewCompiler')
    global info1, info2
    cData = []
    dat1 = info1
    dat2 = info2
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
                    dicti['views'] = getVideoViews(video_id,email)
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

def getVideoViews(video_id,email):
   user = UsrCredentials.objects.get(email=email)
   page_AT = user.pgat
   #---
   url = f'https://graph.facebook.com/v19.0/{video_id}/video_insights?metric=total_video_views&access_token={page_AT}'
   res = requests.get(url).json()
   return res['data'][0]['values'][0]['value']

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
    tot_posts = get_total_posts(urlP)
    #get LCS
    for dat in data:
        tot_likes += dat['likes']
        tot_com += dat['comments']
        tot_shares += dat['shares']
    
    return {'plikes':res['fan_count'], 'followers':res['followers_count'], 'likes':tot_likes, 'comments': tot_com, 'shares':tot_shares, 'posts':tot_posts}

def get_total_posts(url):
    total_posts = 0
    while url:
        response = requests.get(url)
        data = response.json()
        if 'data' in data:
            total_posts += len(data['data'])
            url = data.get('paging', {}).get('next', None)
        else:
            break
    return total_posts

def most(email):
    comments = []
    likes = []
    shares = []
    #return
    final = {}
    #get LCS
    data = viewCompiler()
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

def last24hrs(email):
    user = UsrCredentials.objects.get(email=email)
    page_AT = user.pgat
    page_id = user.fbpageid
    # last 24 hours performance
    metrics = 'page_impressions_unique,page_impressions_paid_unique,page_impressions_organic_unique_v2,page_posts_impressions_unique,page_consumptions_unique,page_total_actions,page_fans_online,page_daily_follows'
    url = f'https://graph.facebook.com/v19.0/{page_id}/insights?metric={metrics}&period=day&access_token={page_AT}'
    res = requests.get(url).json()
    pgImpress = res['data'][0]['values'][1]['value']
    pgImpressPaid = res['data'][1]['values'][1]['value']
    pgImpressOrg = res['data'][2]['values'][1]['value']
    poImpress = res['data'][3]['values'][1]['value']
    contClicks = res['data'][4]['values'][1]['value']
    ctaCont = res['data'][5]['values'][1]['value']
    dailyFol = res['data'][7]['values'][1]['value']

    return {'pgImpress':pgImpress,'pgImpressPaid':pgImpressPaid,'pgImpressOrg':pgImpressOrg,'poImpress':poImpress,'contClicks':contClicks,'ctaCont':ctaCont,'dailyFol':dailyFol}

#chart
def trendsCompilerFb():
    global likesComms, reach
    dat1 = likesComms
    dat2 = reach
    final = {}
    likes = []
    reach = []
    comments = []
    size = len(dat1)
    print(f'size trnds FB: {size}')
    
    i = 0
    while i < size:
        likes.append(dat1[i]['likes']['summary']['total_count'])
        comments.append(dat1[i]['comments']['summary']['total_count'])
        reach.append(dat2[i]['data'][0]['values'][0]['value'])
        i += 1
   
    final['likes1'] = likes[:10][::-1]
    final['comments1'] = comments[:10][::-1]
    final['reach1'] = reach[:10][::-1]
    final['likes2'] = likes[10:][::-1]
    final['comments2'] = comments[10:][::-1]
    final['reach2'] = reach[10:][::-1]

    return final

def fbFollowers(email):
    user = UsrCredentials.objects.get(email=email)
    page_AT = user.pgat
    page_id = user.fbpageid
    #---
    url = f'https://graph.facebook.com/v19.0/{page_id}?fields=followers_count&access_token={page_AT}'
    res = requests.get(url).json()
    return res['followers_count']

def followersFB(email):
    followers = Followers.objects.get(email=email)
    #--
    current = fbFollowers(email)
    past = followers.fbfollowers
    change = current - past
    followers.fbfollowers = current
    followers.save()
    return {'current':current,'past':past,'change':change}

def multiFileHandlers(files,caption,email):
    user = UsrCredentials.objects.get(email=email)
    page_id = user.fbpageid
    page_AT = user.pgat
    #--
    print('Am In FB CAROUSEL!!')
    fbObj = fb.GraphAPI(page_AT)
    postIDs = []
    imgUrls = []
    media_ids = []
    #get post ids for images
    for file in files:
        print(file)
        res = fbObj.put_photo(file,message = caption)
        post_id = res['post_id']
        print(f'post-id: {post_id}')
        postIDs.append(post_id)
    #get image urls
    for postID in postIDs:
        url = f'https://graph.facebook.com/{postID}?fields=full_picture&access_token={page_AT}'
        output = requests.get(url).json()
        if output:
            imgUrls.append(output['full_picture'])
            print(f'img-url: {output['full_picture']}')
    #get media ids for each url
    for url in imgUrls:
        encoded_url = urllib.parse.quote(url, safe='')
        myUrl = f'https://graph.facebook.com/{page_id}/photos?url={encoded_url}&published=False&access_token={page_AT}'
        response = requests.post(myUrl)
        media_ids.append(response.json()['id'])
    print(f'media_ids: {media_ids}')
    #Create the carousel post with the media IDs
    attached_media = [{'media_fbid': media_id} for media_id in media_ids]
    encoded_cap = urllib.parse.quote(caption, safe='')
    urlCar = f'https://graph.facebook.com/{page_id}/feed?message={encoded_cap}&attached_media={attached_media}&access_token={page_AT}'
    response = requests.post(urlCar).json()['id']
    if response:
        print(f'FB Carousel ID: {response}')
    else:
        print('NO ID!')
    #delete FB single posts
    deleteFb(postIDs,email)
    #return
    return response

def multiFileHandlersAll(files,caption,email): 
    user = UsrCredentials.objects.get(email=email)
    igAT = user.llat
    ig_user_id = user.iguserid
    page_AT = user.pgat
    #--
    print('Am In POST ALL CAROUSEL!!')
    fbObj = fb.GraphAPI(page_AT)
    postIDs = []
    imgUrls = []
    #get post ids for images
    for file in files:
        print(file)
        res = fbObj.put_photo(file,message = caption)
        post_id = res['post_id']
        print(f'post-id: {post_id}')
        postIDs.append(post_id)
    #get image urls
    for postID in postIDs:
        url = f'https://graph.facebook.com/{postID}?fields=full_picture&access_token={page_AT}'
        output = requests.get(url).json()
        if output:
            imgUrls.append(output['full_picture'])
            print(f'img-url: {output['full_picture']}')
    #response
    igRes = PostCaroIg(imgUrls,caption,email)
    fbRes = postCaroFB(imgUrls,caption,email)

    if fbRes and igRes:
        deleteFb(postIDs,email)
        return True
    else:
        deleteFb(postIDs,email)
        return False

def deleteFb(postIDs,email):
    user = UsrCredentials.objects.get(email=email)
    page_AT = user.pgat
    #--
    #delete FB single posts
    for postID in postIDs:
        url = f'https://graph.facebook.com/{postID}?access_token={page_AT}'
        resp = requests.delete(url).json().get('success')
        print(f'del: {resp}')

def PostCaroIg(imgUrls,caption,email):
    user = UsrCredentials.objects.get(email=email)
    igAT = user.llat
    ig_user_id = user.iguserid
    #--
    contIds = []
    #get container ids for each
    for url in imgUrls:
        encoded_url = urllib.parse.quote(url, safe='')
        apiCall = f'https://graph.facebook.com/v19.0/{ig_user_id}/media?image_url={encoded_url}&is_carousel_item=true&access_token={igAT}'
        res = requests.post(apiCall).json().get('id')
        contIds.append(res)
    print(f'Images ContId: {contIds}')
    #get carousel container
    children = ','.join(contIds)
    encoded_cap = urllib.parse.quote(caption, safe='')
    urlCar = f'https://graph.facebook.com/v19.0/{ig_user_id}/media?caption={encoded_cap}&media_type=CAROUSEL&children={children}&access_token={igAT}'
    carId = requests.post(urlCar).json().get('id')
    print(f'Caroussel ContId: {carId}')
    #publish carousel post
    urlPost = f'https://graph.facebook.com/v19.0/{ig_user_id}/media_publish?creation_id={carId}&access_token={igAT}'
    carAlbId = requests.post(urlPost).json().get('id')
    if carAlbId:
        print(f'IG ALBUM ID: {carAlbId}')
        return carAlbId
    else:
        print('NO ALBUM ID!')
        return null 

def postCaroFB(imgUrls,caption,email):
    user = UsrCredentials.objects.get(email=email)
    page_id = user.fbpageid
    page_AT = user.pgat
    #--
    media_ids = []
    #get media ids for each url
    for url in imgUrls:
        encoded_url = urllib.parse.quote(url, safe='')
        myUrl = f'https://graph.facebook.com/{page_id}/photos?url={encoded_url}&published=False&access_token={page_AT}'
        response = requests.post(myUrl)
        media_ids.append(response.json()['id'])
    print(f'media_ids: {media_ids}')
    #Create the carousel post with the media IDs
    attached_media = [{'media_fbid': media_id} for media_id in media_ids]
    encoded_cap = urllib.parse.quote(caption, safe='')
    urlCar = f'https://graph.facebook.com/{page_id}/feed?message={encoded_cap}&attached_media={attached_media}&access_token={page_AT}'
    response = requests.post(urlCar).json()['id']
    if response:
        print(f'FB Carousel ID: {response}')
        return response
    else:
        print('NO ID!')
        return null    
    
def postText(mssg,email):
    user = UsrCredentials.objects.get(email=email)
    page_AT = user.pgat
    page_id = user.fbpageid
    #--
    url = f'https://graph.facebook.com/v19.0/{page_id}/feed?message={mssg}&access_token={page_AT}'
    output = requests.post(url).json()
    
    return output['id']