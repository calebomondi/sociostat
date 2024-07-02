'''
from .models import UsrCredentials, Followers

#get user & details
user = UsrCredentials.objects.get(email='info@zendawa.africa')
followers = Followers.objects.get(email='info@zendawa.africa')
print(user)
print(followers)

#instagram
igAT = user.llAT
ig_user_id = user.igUserId
ig_followers = followers.igFollowers
#facebook
page_id = user.fbPageId
fbAT = user.llAT
page_AT = user.pgAT
fb_followers = followers.fbFollowers
'''
#print(f'page_id: {page_id}')
#print(f'igAT: {igAT}')
#print(f'pgAT: {page_AT}')
#print(f'ig_user_id: {ig_user_id}')
'''
#instagram
#ig_user_id = 17841466905494639

#facebook
#page_id = 304111669454165

#app
app_id = 1377857649597420
app_secret = '00a338585d3a8327fd795f994394ac00'

#link to private policy
'https://www.privacypolicies.com/live/8285540f-02cf-459a-98b7-ff18bd286373'
'''
