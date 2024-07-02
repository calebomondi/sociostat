import requests

def genLLAT_PAT(appid,appsec,slTok,pgid):
    #get ig user id
    urlIg = f'https://graph.facebook.com/v19.0/{pgid}?fields=instagram_business_account&access_token={slTok}'
    outputIg = requests.get(urlIg).json()
    if 'instagram_business_account' in outputIg:
        igId = outputIg['instagram_business_account']['id']
        print(f'IGID: {igId}')
    #get long lived token
    url = F'https://graph.facebook.com/v19.0/oauth/access_token?grant_type=fb_exchange_token&client_id={appid}&client_secret={appsec}&fb_exchange_token={slTok}'
    output = requests.get(url).json()
    print(output)
    if 'access_token' in output:
        llTok = output['access_token'] 
        #get ll page token
        url2 = f"https://graph.facebook.com/{pgid}?fields=access_token&access_token={llTok}"
        output2 = requests.get(url2).json()
        print(output2)
        if 'access_token' in output2:
            pgTok = output2['access_token']
            return {'access_token': llTok, 'page_token': pgTok, 'ig_user': igId}
    return 'NULL'
