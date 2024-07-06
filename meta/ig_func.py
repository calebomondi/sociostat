from . import config
import requests
import facebook as fb
import urllib.parse
from .models import UsrCredentials, Followers

mediaIDS = []
recent = None

#DASHBOARD
def pageInfo(email):
    print('Inside PageInfo')
    user = UsrCredentials.objects.get(email=email)
    igAT = user.llat
    ig_user_id = user.iguserid
    #---
    fields = 'followers_count,follows_count,media_count'
    page_info_url = f'https://graph.facebook.com/v19.0/{ig_user_id}?fields={fields}&access_token={igAT}'
    info = requests.get(page_info_url).json()
    return info

def postInsights(email):
    user = UsrCredentials.objects.get(email=email)
    igAT = user.llat
    ig_user_id = user.iguserid
    #----
    metrics = 'impressions, reach,profile_views,total_interactions, likes, comments, shares, saves, replies,'
    post_insights_url = f'https://graph.facebook.com/{ig_user_id}/insights?metric={metrics}&period=day&metric_type=total_value&access_token={igAT}'
    insights = requests.get(post_insights_url).json()
    return insights

def totalCLS(email):
    print(f'totalCLS')
    user = UsrCredentials.objects.get(email=email)
    igAT = user.llat
    #ig_user_id = user.iguserid
    #---
    global mediaIDS
    #---
    metrics = 'likes, comments, shares'
    likes = 0
    comments = 0
    shares = 0
    #get media objects
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
    return {'likes': likes, 'comments':comments, 'shares':shares}
        
def dayInsights(email):
    insights = postInsights(email)

    for dat in insights['data']:
        if dat['name'] == 'impressions':
            impressions = dat['total_value']['value']
        if dat['name'] == 'reach':
            reach = dat['total_value']['value']
        if dat['name'] == 'profile_views':
            pviews = dat['total_value']['value']
        if dat['name'] == 'total_interactions':
            interact = dat['total_value']['value']
        if dat['name'] == 'likes':
            likes = dat['total_value']['value']
        if dat['name'] == 'comments':
            comments = dat['total_value']['value']
        if dat['name'] == 'shares':
            shares = dat['total_value']['value']
        if dat['name'] == 'saves':
            saves = dat['total_value']['value']
    return {'impressions':impressions,'reach':reach,'pviews':pviews,'interact':interact,'likes':likes,'comments':comments,'shares':shares,'saves':saves}

def most(email):
    print('MOST')
    user = UsrCredentials.objects.get(email=email)
    igAT = user.llat
    ig_user_id = user.iguserid
    #--
    global mediaIDS, recent
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
    #--
    recent = mediaIDS[0]['id']
    #get media objects
    for mediaObj in mediaIDS[:10]:
        media_info = getObject(mediaObj['id'],igAT)
        for dat in media_info['data']:
            if dat['name'] == 'likes':
                Likes.append(dat['values'][0]['value'])
            if dat['name'] == 'shares':
                Shares.append(dat['values'][0]['value'])
            if dat['name'] == 'comments':
                Comments.append(dat['values'][0]['value'])
    Likes.sort(reverse=True)
    Comments.sort(reverse=True)
    Shares.sort(reverse=True)
    for mediaObj in mediaIDS[:10]:
        media_info = getObject(mediaObj['id'],igAT)
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
    return {'shared': most_shares, 'liked': most_likes, 'commented': most_comm}

def getURL(pID,igAT):
    fields = 'permalink,media_url,timestamp,thumbnail_url'
    url_link = f'https://graph.facebook.com/v15.0/{pID}?fields={fields}&access_token={igAT}'
    return requests.get(url_link).json()

def getObject(pID,igAT):
    metrics = 'likes,comments, shares, video_views'
    url_media = f'https://graph.facebook.com/{pID}/insights?metric={metrics}&access_token={igAT}'
    return requests.get(url_media).json()

def recentlyPosted(email):
    print('RECENT')
    user = UsrCredentials.objects.get(email=email)
    igAT = user.llat
    ig_user_id = user.iguserid
    #--
    global recent
    #--
    print(recent)
    #get likes,shares,comments
    media_info = getObject(recent,igAT)
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
        views = reelViews(recent,igAT)
        return {'url':post_url,'likes':post_likes, 'shares':post_shares, 'comments':post_comments, 'views':views}
    elif 'media_url' in post_url:
        return {'url':post_url,'likes':post_likes, 'shares':post_shares, 'comments':post_comments}

def reelViews(id,igAT):
    url = f'https://graph.facebook.com/{id}/insights?metric=video_views&access_token={igAT}'
    response = requests.get(url).json()
    return response['data'][0]['values'][0]['value']

#VIEW
def getPostsData(email):
    user = UsrCredentials.objects.get(email=email)
    igAT = user.llat
    ig_user_id = user.iguserid
    #---
    global mediaIDS
    #---
    metrics = 'likes,comments, shares,reach,video_views'
    fields = 'permalink,media_url,timestamp,thumbnail_url'
    data = []
    links = []
    #get media objects
    for mediaObj in mediaIDS[:10]:
        #media insites
        url_media = f'https://graph.facebook.com/{mediaObj['id']}/insights?metric={metrics}&access_token={igAT}'
        media_info = requests.get(url_media).json()
        data.append(media_info)
        #post link and short code
        url_link = f'https://graph.facebook.com/v15.0/{mediaObj['id']}?fields={fields}&access_token={igAT}'
        post_url = requests.get(url_link).json()
        links.append(post_url)
    
    return {'data':data,'links':links}

def compilePosts(email):
    final = []
    rawDat = getPostsData(email)
    size = len(rawDat['data'])
    
    i = 0
    while i < size:
        addData = {}
        addData['date'] = rawDat['links'][i]['timestamp'][:10]
        if 'media_url' in rawDat['links'][i]:
            addData['imgUrl'] = rawDat['links'][i]['media_url']
            addData['reel'] = 0
        elif 'thumbnail_url' in rawDat['links'][i]:
            addData['imgUrl'] = rawDat['links'][i]['thumbnail_url']
            addData['reel'] = 1
        addData['postUrl'] = rawDat['links'][i]['permalink']
        addData['views'] = rawDat['data'][i]['data'][0]['values'][0]['value']
        addData['likes'] = rawDat['data'][i]['data'][1]['values'][0]['value']
        addData['comments'] = rawDat['data'][i]['data'][2]['values'][0]['value']
        addData['shares'] = rawDat['data'][i]['data'][3]['values'][0]['value']
        addData['reach'] = rawDat['data'][i]['data'][4]['values'][0]['value']
        #print(addData)
        final.append(addData)
        i += 1      
    
    return final

#POST
def makePost(imgUrl,caption,email):    
    user = UsrCredentials.objects.get(email=email)
    igAT = user.llat
    ig_user_id = user.iguserid
    #--
    encoded_url = urllib.parse.quote(imgUrl, safe='')
    encoded_cap = urllib.parse.quote(caption, safe='')
    #get container ID
    url = f'https://graph.facebook.com/v19.0/{ig_user_id}/media?image_url={encoded_url}&caption={encoded_cap}&access_token={igAT}'
    container_id = requests.post(url).json()
    #make post 
    if 'id' in container_id:
        print(f"container-id: {container_id['id']}")

        url2 = f'https://graph.facebook.com/v19.0/{ig_user_id}/media_publish?creation_id={container_id['id']}&access_token={igAT}'
        media_id = requests.post(url2).json()

        if 'id' in media_id:
            print(f"media-id: {media_id['id']}")
            return media_id['id']
        else:
            print('Media ID Not Found!')
    else:
        print('Container ID Not Found!')

def makeStory(imgUrl,email):
    user = UsrCredentials.objects.get(email=email)
    igAT = user.llat
    ig_user_id = user.iguserid
    #--
    encoded_url = urllib.parse.quote(imgUrl, safe='')
    print(f'AM IN!! {encoded_url}')
    #get container id
    url = f'https://graph.facebook.com/{ig_user_id}/media?media_type=STORIES&image_url={encoded_url}&access_token={igAT}'
    '''
    response = requests.post(
        f'https://graph.facebook.com/{config.ig_user_id}/media',
        data={
            'media_type': 'STORIES',
            'image_url': encoded_url,
            'access_token': config.igAT,
        }
    )
    '''
    container_id = requests.post(url).json().get('id')
    print(f'Story: {container_id}')
    #publish
    url = f'https://graph.facebook.com/{ig_user_id}/media_publish?creation_id={container_id}&access_token={igAT}'
    post_id = requests.post(url).json().get('id')
    print(f'>>> {post_id}')
    return post_id

def postAll(file,caption,typ, email):
    user = UsrCredentials.objects.get(email=email)
    page_AT = user.pgat
    #facebook object
    fbObj = fb.GraphAPI(page_AT)
    #upload in fb to get post id
    res = fbObj.put_photo(file,message=caption)
    post_id = res['post_id']
    print(f'post id: {post_id}')
    #post FB only
    if typ == 0:
        print('FB Posted Successfully!')
        return 200
    #get post picture url
    url = f'https://graph.facebook.com/{post_id}?fields=full_picture&access_token={page_AT}'
    output = requests.get(url).json()
    #post both FB and IG
    if output and typ == 1:
        print('FB yes!')
        #post to IG
        res = makePost(output['full_picture'],caption,email)
        return res
    #post IG only
    if output and typ == 2:
        res = makePost(output['full_picture'],caption,email)
        print(f'ig: {res}')
        url = f'https://graph.facebook.com/{post_id}?access_token={page_AT}'
        resp = requests.delete(url).json().get('success')
        print(f'del: {resp}')
        return resp
    #post IG Story
    if output and typ == 3:
        res = makeStory(output['full_picture'],email)
        print(f'story: {res}')
        url = f'https://graph.facebook.com/{post_id}?access_token={page_AT}'
        resp = requests.delete(url).json().get('success')
        print(f'del: {resp}')
        return res

def multiFileHandlers(files,caption,email):
    user = UsrCredentials.objects.get(email=email)
    igAT = user.llat
    ig_user_id = user.iguserid
    page_AT = user.pgat
    #--
    print('Am In Ig!!')
    fbObj = fb.GraphAPI(page_AT)
    postIDs = []
    imgUrls = []
    contIds = []
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
    print(f'children: {children}')
    urlCar = f'https://graph.facebook.com/v19.0/{ig_user_id}/media?caption={encoded_cap}&media_type=CAROUSEL&children={children}&access_token={igAT}'
    carId = requests.post(urlCar).json().get('id')
    print(f'Caroussel ContId: {carId}')
    #publish carousel post
    urlPost = f'https://graph.facebook.com/v19.0/{ig_user_id}/media_publish?creation_id={carId}&access_token={igAT}'
    carAlbId = requests.post(urlPost).json().get('id')
    print(f'album id: {carAlbId}')
    #delete FB posts
    for postID in postIDs:
        url = f'https://graph.facebook.com/{postID}?access_token={page_AT}'
        resp = requests.delete(url).json().get('success')
        print(f'del: {resp}')
    #return album id
    return carAlbId

#TRNDS
def getPostsDataTrends(email):
    user = UsrCredentials.objects.get(email=email)
    igAT = user.llat
    ig_user_id = user.iguserid
    #---
    global mediaIDS
    if mediaIDS != []:
        mediaIDS = []
    #---
    metrics = 'likes,comments,reach'
    final = {}
    likes = []
    reach = []
    comments = []
    #get media objects
    url = f'https://graph.facebook.com/v19.0/{ig_user_id}/media?access_token={igAT}&limit=20'
    response = requests.get(url).json()
    if 'data' in response:
        mediaObjArr = response['data']
        mediaIDS = response['data']
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
    else:
        print('NO DATA IG!')
    
    return final

def trendData(fromApi):
    data = totalTrend(fromApi)
    print(f'DATA SUMMATION: {data}')
    #percentage
    likeP1 = (data['l1'] / data['r1']) * 100
    likeP2 = (data['l2'] / data['r2']) * 100
    likeP1 = round(likeP1)
    likeP2 = round(likeP2)
    likePC = likeP1 - likeP2
    commP1 = (data['c1'] / data['r1']) * 100
    commP2 = (data['c2'] / data['r2']) * 100
    commP1 = round(commP1)
    commP2 = round(commP2)
    commPC = commP1 - commP2 
    #rate
    likeR1 = data['l1'] / 10
    likeR2 = data['l2'] / 10
    likeR1 = round(likeR1)
    likeR2 = round(likeR2)
    likeRC = likeR1 - likeR2
    commR1 = data['c1'] / 10
    commR2 = data['c2'] / 10
    commR1 = round(commR1)
    commR2 = round(commR2)
    commRC = commR1 - commR2
    reachR1 = data['r1'] / 10
    reachR2 = data['r2'] / 10
    reachR1 = round(reachR1)
    reachR2 = round(reachR2)
    reachRC = reachR1 - reachR2

    final = {
        'likeP': {
            'likeP1':likeP1, 
            'likeP2': likeP2,
            'likePC':likePC
        },
        'commP': {
            'commP1':commP1, 
            'commP2': commP2,
            'commPC':commPC
        }, 
        'likeR': {
            'likeR1':likeR1, 
            'likeR2': likeR2,
            'likeRC':likeRC
        },
        'commR': {
            'commR1':commR1, 
            'commR2': commR2,
            'commRC':commRC
        },
        'reachR': {
            'reachR1':reachR1, 
            'reachR2': reachR2,
            'reachRC':reachRC
        },
    }

    return final

def totalTrend(final):
    like1 = like2 = comments1 = comments2 = reach1 = reach2 = 0
    i = 0
    while i < 10:
        like1 += final['likes1'][i]
        like2 += final['likes2'][i]
        comments1 += final['comments1'][i]
        comments2 += final['comments2'][i]
        reach1 += final['reach1'][i]
        reach2 += final['reach2'][i]
        i += 1
    return {'l1':like1,'l2':like2,'c1':comments1,'c2':comments2,'r1':reach1,'r2':reach2}

def igFollowers(email):
    user = UsrCredentials.objects.get(email=email)
    igAT = user.llat
    ig_user_id = user.iguserid
    #---
    fields = 'followers_count'
    url = f'https://graph.facebook.com/v19.0/{ig_user_id}?fields={fields}&access_token={igAT}'
    res = requests.get(url).json()
    return res['followers_count']  

def followersIG(email):
    followers = Followers.objects.get(email=email)
    #---
    current = igFollowers(email)
    past = followers.igfollowers
    change = current - past
    #---
    followers.igfollowers = current
    followers.save()
    return {'current':current,'past':past,'change':change}
