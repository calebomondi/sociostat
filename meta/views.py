from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.template import loader
from . import ig_func, fb_func, gen_func, server_func
from .forms import myForm,formSet,storyForm,FileCaro, CreateUserForm,LoginForm, FBText
from .models import UsrCredentials,Followers
#------
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
#----
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#---
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

# Create your views here.
@login_required(login_url='login')
def welcome(request):
    template = loader.get_template('index.html')
    #--
    if request.user.is_authenticated:
        email = request.user.email
    else:
        email = "Guest"
    #--
    request.session['final'] = server_func.getPostsDataTrends(email)
    return HttpResponse(template.render())

#authenticate
def register(request):
    form = CreateUserForm()
    template = loader.get_template('registration/register.html')
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    context = {
        'formReg' : form,
    }
    return HttpResponse(template.render(context,request))

def login(request):
    form = LoginForm()
    template = loader.get_template('registration/login.html')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,username=username, password=password)

            if user is not None:
                auth.login(request,user)
                return redirect('home-page')
            else:
                messages.error(request, 'User not found or invalid credentials')
                return redirect('login')
    context = {
        'formLog': form,
    }
    return HttpResponse(template.render(context,request))

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change_form.html', {'form': form})

#FACEBOOK
@login_required(login_url='login')
def facebook_dashboard(request):
    template = loader.get_template('fb_dashboard.html')
    #--
    if request.user.is_authenticated:
        email = request.user.email
    else:
        email = "Guest"
    #--
    request.session['finalFb'] = server_func.trendsCompilerFb(email)
    most = server_func.most(email)
    last = fb_func.last24hrs(email)
    context = {
        'recent': most['final']['recent'],
        'liked' : most['final']['likes'],
        'shared' : most['final']['shares'],
        'commented' : most['final']['comments'],
        'data':most['dash'],
        'last': last
    }
    return HttpResponse(template.render(context,request))

@login_required(login_url='login')
def facebook_view(request):
    template = loader.get_template('fb_views.html')
    if request.user.is_authenticated:
        email = request.user.email
    else:
        email = "Guest"
    viewData = server_func.viewCompiler(email)
    context = {
        'posts': viewData,
    }
    return HttpResponse(template.render(context,request))
'''
@login_required(login_url='login')
def facebook_post(request):
    form = myForm()
    template = loader.get_template('fb_post.html')
    context = {
        'form':form
    }
    return HttpResponse(template.render(context,request))

def face_make_post(request):
    if request.user.is_authenticated:
        email = request.user.email
    else:
        email = "Guest"
    #--
    if request.method == 'POST':
        form = myForm(request.POST,request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            caption = form.cleaned_data['caption']
        
        status = ig_func.postAll(file, caption,0,email)
        if status:
            return JsonResponse({'message': 'Posting To Facebook Completed'})
        else:
            return JsonResponse({'message': 'Post Not Successful'}, status=400)
        
    return JsonResponse({'message': 'Method Not Post'}, status=405)

@login_required(login_url='login')
def face_carousel(request):
    form = FileCaro()
    template = loader.get_template('fb_carousel.html')
    context = {
        'form':form
    }
    return HttpResponse(template.render(context,request))

def face_make_carousel(request):
    if request.user.is_authenticated:
        email = request.user.email
    else:
        email = "Guest"
    #--
    if request.method == 'POST':
        form = FileCaro(request.POST,request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('images')
            caption = form.cleaned_data['caption']
            print(f'files > {files}, caption > {caption}')
            post_id = fb_func.multiFileHandlers(files,caption,email)
            print(f'VIEW: {post_id}')
            if post_id:
                return JsonResponse({'message': 'Posting Carousel To Facebook Completed'})
            else:
                return JsonResponse({'message': 'Posting Carousel Not Successful'}, status=400)
    return JsonResponse({'message': 'Method Not Post'}, status=405)

@login_required(login_url='login')
def facebook_text(request):
    form = FBText()
    template = loader.get_template('fb_mssg.html')
    context = {
        'form':form,
    }
    return HttpResponse(template.render(context,request))

def face_make_text(request):
    if request.user.is_authenticated:
        email = request.user.email
    else:
        email = "Guest"
    #--
    if request.method == 'POST':
        form = FBText(request.POST)
        if form.is_valid():
            mssg = form.cleaned_data['text']
        status = fb_func.postText(mssg,email)
        if status:
            return JsonResponse({'message': 'Posting Text To Facebook Completed'})
        else:
            return JsonResponse({'message': 'Post Not Successful'}, status=400)
        
    return JsonResponse({'message': 'Method Not Post'}, status=405)
'''
#INSTAGRAM
@login_required(login_url='login')
def instagram_dashboard(request):
    template = loader.get_template('ig_dashboard.html')
    #--
    if request.user.is_authenticated:
        email = request.user.email
        print(f'email ig: {email}')
    else:
        email = "Guest"
    #--
    info = ig_func.pageInfo(email)
    CLS = server_func.totalCLS(email)
    most = server_func.mostIg(email)
    daily_ins = ig_func.dayInsights(email)
    context = {
        'followers':info['followers_count'],
        'following':info['follows_count'],
        'posts':info['media_count'],
        'tot_likes': CLS['likes'],
        'tot_comment': CLS['comments'],
        'tot_shares': CLS['shares'],
        'impressions': daily_ins['impressions'], 
        'reach': daily_ins['reach'], 
        'pviews': daily_ins['pviews'], 
        'interact': daily_ins['interact'], 
        'likes': daily_ins['likes'], 
        'comments': daily_ins['comments'], 
        'shares': daily_ins['shares'], 
        'saves': daily_ins['saves'],
        'most_liked':most['liked'],
        'most_shared':most['shared'],
        'most_comments':most['commented'],
        'recent':most['recent'],
    }
    return HttpResponse(template.render(context,request))

@login_required(login_url='login')
def insta_views(request):
    template = loader.get_template('ig_views.html')
    if request.user.is_authenticated:
        email = request.user.email
    else:
        email = "Guest"
    data = server_func.compilePosts(email)
    context = {
        'posts': data
    }
    return HttpResponse(template.render(context,request))
'''
@login_required(login_url='login')
def insta_post(request):
    form = myForm()
    template = loader.get_template('ig_post.html')
    context = {
        'form':form
    }
    return HttpResponse(template.render(context,request))

def insta_make_post(request):
    if request.user.is_authenticated:
        email = request.user.email
    else:
        email = "Guest"
    #--
    if request.method == 'POST':
        form = myForm(request.POST,request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            caption = form.cleaned_data['caption']
        
        post_id = ig_func.postAll(file, caption, 2,email)
        print(f'VIEW: {post_id}')
        if post_id:
            return JsonResponse({'message': 'Posting To Instagram Completed'})
        else:
            return JsonResponse({'message': 'Post Not Successful'}, status=400)
        
        #return HttpResponse(f'{file} - {caption}')
    return JsonResponse({'message': 'Method Not Post'}, status=405)

@login_required(login_url='login')
def insta_carousel(request):
    form = FileCaro()
    template = loader.get_template('ig_carousel.html')
    context = {
        'form':form
    }
    return HttpResponse(template.render(context,request))

def insta_make_carousel(request):
    if request.user.is_authenticated:
        email = request.user.email
    else:
        email = "Guest"
    #--
    if request.method == 'POST':
        form = FileCaro(request.POST,request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('images')
            caption = form.cleaned_data['caption']
            print(f'files > {files}, caption > {caption}')
            post_id = ig_func.multiFileHandlers(files,caption,email)
            print(f'VIEW: {post_id}')
            if post_id:
                return JsonResponse({'message': 'Posting Carousel To Instagram Completed'})
            else:
                return JsonResponse({'message': 'Post Not Successful'}, status=400)
    return JsonResponse({'message': 'Method Not Post'}, status=405)

@login_required(login_url='login')
def insta_story(request):
    form = storyForm()
    template = loader.get_template('ig_story.html')
    context = {
        'form':form
    }
    return HttpResponse(template.render(context,request))

def insta_make_story(request):
    if request.user.is_authenticated:
        email = request.user.email
    else:
        email = "Guest"
    #--
    if request.method == 'POST':
        form = storyForm(request.POST,request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']

            post_id = ig_func.postAll(file, 'story', 3,email)
            print(f'VIEW: {post_id}')
            if post_id:
                return JsonResponse({'message': 'Posting To Instagram Story Completed'})
            else:
                return JsonResponse({'message': 'Post Not Successful'}, status=400)
        
        #return HttpResponse(f'{file} - {caption}')
    return JsonResponse({'message': 'Method Not Post'}, status=405)

#ALL
@login_required(login_url='login')
def postAll(request):
    form = myForm()
    template = loader.get_template('all_post.html')
    context = {
        'form':form
    }
    return HttpResponse(template.render(context,request))

def all_make_post(request):
    if request.user.is_authenticated:
        email = request.user.email
    else:
        email = "Guest"
    #--
    if request.method == 'POST':
        form = myForm(request.POST,request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            caption = form.cleaned_data['caption']
        
        post_id = ig_func.postAll(file, caption, 1,email)
        if post_id:
            return JsonResponse({'message': 'Posting To All Socials Completed'})
        else:
            return JsonResponse({'message': 'Post Not Successful'}, status=400)
        
        #return HttpResponse(f'{file} - {caption}')
    return JsonResponse({'message': 'Method Not Post'}, status=405)

@login_required(login_url='login')
def all_carousel(request):
    form = FileCaro()
    template = loader.get_template('all_carousel.html')
    context = {
        'form':form
    }
    return HttpResponse(template.render(context,request))

def all_make_carousel(request):
    if request.user.is_authenticated:
        email = request.user.email
    else:
        email = "Guest"
    #--
    if request.method == 'POST':
        form = FileCaro(request.POST,request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('images')
            caption = form.cleaned_data['caption']
            print(f'files > {files}, caption > {caption}')
            post_id = fb_func.multiFileHandlersAll(files,caption,email)
            print(f'VIEW: {post_id}')
            if post_id:
                return JsonResponse({'message': 'Posting Carousel To All Socials Completed'})
            else:
                return JsonResponse({'message': 'Post Not Successful'}, status=400)
    return JsonResponse({'message': 'Method Not Post'}, status=405)
'''

#SETUP
@login_required(login_url='login')
def setup(request):
    form = formSet()
    template = loader.get_template('setup.html')
    context = {
        'form':form
    }
    return HttpResponse(template.render(context,request))

def setup_process(request):
    if request.method == 'POST':
        form = formSet(request.POST)
        if form.is_valid():
            #get form inputs
            email = form.cleaned_data['email'] 
            slToken = form.cleaned_data['slToken']
            fbPgId = form.cleaned_data['fbPgId']
            appId = form.cleaned_data['appId']
            appSecret = form.cleaned_data['appSecret']
            #get LLTKN and PGTKN
            res = gen_func.genLLAT_PAT(appId,appSecret,slToken,fbPgId)

            if res['access_token']:
                print('Am In Setup!')
                usr, created = UsrCredentials.objects.update_or_create(
                    email=email,
                    defaults = {
                        'email':email,
                        'llat':res['access_token'],
                        'pgat':res['page_token'],
                        'iguserid':res['ig_user'],
                        'fbpageid':fbPgId,
                        'appid':appId,
                        'appsecret':appSecret
                    }
                )
                fllwrs, createdF = Followers.objects.update_or_create(
                    email=email,
                    defaults = {
                        'email':email,
                        'igfollowers':0,
                        'fbfollowers':0,
                    }
                )
                #usr = UsrCredentials(usrname=usrname,llAT=res['access_token'],pgAT=res['page_token'],igUserId=igUsrId,fbPageId=fbPgId,appID=appId,appSecret=appSecret)
                #usr.save()
                if usr and fllwrs:
                    print(f'usr: {usr} - fllwrs: {fllwrs}')
                    return JsonResponse({'message': 'Data Processing Completed!'})
                else:
                    return JsonResponse({'message': 'Data Processing Not Successful'}, status=400)
            
    return JsonResponse({'message': 'Method Not Post'}, status=405)

#CHARTS
class LineChartDataIg(APIView):
    def get(self, request, format=None):
        final = request.session.get('final',{})

        if not final:
            return Response({"error": "No data found in session"}, status=status.HTTP_404_NOT_FOUND)
        
        data = {
            "labels": ['p10','p9','p8','p7','p6','p5','p4','p3','p2','p1'],
            "datasets": [
                {
                    "label": "Reach",
                    "backgroundColor": "rgba(255, 99, 132, 0.2)",
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "borderWidth": 1,
                    "data": final['reach1'],
                },
                {
                    "label": "Likes",
                    "backgroundColor": "rgba(0, 128, 128,0.2)",
                    "borderColor": "rgba(0, 128, 128,1)",
                    "borderWidth": 1,
                    "data": final['likes1'],
                },
                {
                    "label": "Comments",
                    "backgroundColor": "rgba(0, 0, 255,0.2)",
                    "borderColor": "rgba(0, 0, 255,1)",
                    "borderWidth": 1,
                    "data": final['comments1'],
                },
            ],
        }
        data2 = {
            "labels": ['p10','p9','p8','p7','p6','p5','p4','p3','p2','p1'],
            "datasets": [
                {
                    "label": "current 10 posts",
                    "backgroundColor": "rgba(75, 192, 192, 0.2)",
                    "borderColor": "rgba(75, 192, 192, 1)",
                    "borderWidth": 1,
                    "data": final['reach1'],
                },
                {
                    "label": "previous 10 posts",
                    "backgroundColor": "rgba(153, 102, 255, 0.2)",
                    "borderColor": "rgba(153, 102, 255, 1)",
                    "borderWidth": 1,
                    "data": final['reach2'],
                },
            ],
        }
        responce = [data,data2]
        return Response(responce, status=status.HTTP_200_OK)

@login_required(login_url='login')
def insta_trends(request):
    template = loader.get_template('ig_trends.html')
    #---
    if request.user.is_authenticated:
        email = request.user.email
    else:
        email = "Guest"
    #---
    trnds = ig_func.trendData(request.session.get('final',{}))
    flwrs = ig_func.followersIG(email)
    context = {
        'data': trnds,
        'flwrs':flwrs,
    }
    return HttpResponse(template.render(context,request))

class LineChartDataFb(APIView):
    def get(self, request, format=None):
        finalFb = request.session.get('finalFb',{})

        if not finalFb:
            return Response({"error": "No data found in session"}, status=status.HTTP_404_NOT_FOUND)
        
        data3 = {
            "labels": ['p10','p9','p8','p7','p6','p5','p4','p3','p2','p1'],
            "datasets": [
                {
                    "label": "Reach",
                    "backgroundColor": "rgba(255, 99, 132, 0.2)",
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "borderWidth": 1,
                    "data": finalFb['reach1'],
                },
                {
                    "label": "Likes",
                    "backgroundColor": "rgba(0, 128, 128,0.2)",
                    "borderColor": "rgba(0, 128, 128,1)",
                    "borderWidth": 1,
                    "data": finalFb['likes1'],
                },
                {
                    "label": "Comments",
                    "backgroundColor": "rgba(0, 0, 255,0.2)",
                    "borderColor": "rgba(0, 0, 255,1)",
                    "borderWidth": 1,
                    "data": finalFb['comments1'],
                },
            ],
        }
        data4 = {
            "labels": ['p10','p9','p8','p7','p6','p5','p4','p3','p2','p1'],
            "datasets": [
                {
                    "label": "current 10 posts",
                    "backgroundColor": "rgba(75, 192, 192, 0.2)",
                    "borderColor": "rgba(75, 192, 192, 1)",
                    "borderWidth": 1,
                    "data": finalFb['reach1'],
                },
                {
                    "label": "previous 10 posts",
                    "backgroundColor": "rgba(153, 102, 255, 0.2)",
                    "borderColor": "rgba(153, 102, 255, 1)",
                    "borderWidth": 1,
                    "data": finalFb['reach2'],
                },
            ],
        }
        responce = [data3,data4]
        print('AM IN FB!!!!!!!!!!')
        return Response(responce, status=status.HTTP_200_OK)

@login_required(login_url='login')
def facebook_trends(request):
    template = loader.get_template('fb_trends.html')
    #--
    if request.user.is_authenticated:
        email = request.user.email
    else:
        email = "Guest"
    #---
    finalFb = request.session.get('finalFb',{})
    #--
    trnds = ig_func.trendData(finalFb)
    flwrs = fb_func.followersFB(email)
    context = {
        'data': trnds,
        'flwrs':flwrs,
    }
    return HttpResponse(template.render(context,request))

#COMPARISON Fb & IG
class LineChartDataComp(APIView):
    def get(self, request, format=None):
        final = request.session.get('final',{})
        finalFb = request.session.get('finalFb',{})

        data5 = {
            "labels": ['p10','p9','p8','p7','p6','p5','p4','p3','p2','p1'],
            "datasets": [
                {
                    "label": "Reach",
                    "backgroundColor": "rgba(255, 99, 132, 0.2)",
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "borderWidth": 1,
                    "data": finalFb['reach1'],
                },
                {
                    "label": "Likes",
                    "backgroundColor": "rgba(0, 128, 128,0.2)",
                    "borderColor": "rgba(0, 128, 128,1)",
                    "borderWidth": 1,
                    "data": finalFb['likes1'],
                },
                {
                    "label": "Comments",
                    "backgroundColor": "rgba(0, 0, 255,0.2)",
                    "borderColor": "rgba(0, 0, 255,1)",
                    "borderWidth": 1,
                    "data": finalFb['comments1'],
                },
            ]
        }
        data6 = {
            "labels": ['p10','p9','p8','p7','p6','p5','p4','p3','p2','p1'],
            "datasets": [
                {
                    "label": "Reach",
                    "backgroundColor": "rgba(255, 99, 132, 0.2)",
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "borderWidth": 1,
                    "data": final['reach1'],
                },
                {
                    "label": "Likes",
                    "backgroundColor": "rgba(0, 128, 128,0.2)",
                    "borderColor": "rgba(0, 128, 128,1)",
                    "borderWidth": 1,
                    "data": final['likes1'],
                },
                {
                    "label": "Comments",
                    "backgroundColor": "rgba(0, 0, 255,0.2)",
                    "borderColor": "rgba(0, 0, 255,1)",
                    "borderWidth": 1,
                    "data": final['comments1'],
                },
            ],
        }
        responce = [data5,data6]
        return Response(responce, status=status.HTTP_200_OK)

@login_required(login_url='login')
def compare_trends_fb(request):
    template = loader.get_template('compare_trends_fb.html')
    #--
    if request.user.is_authenticated:
        email = request.user.email
    else:
        email = "Guest"
    #--
    final = request.session.get('final',{})
    finalFb = request.session.get('finalFb',{})
    #--
    fb = ig_func.trendData(finalFb)
    fbFol = fb_func.followersFB(email)
    igFol = ig_func.followersIG(email)
    ig = ig_func.trendData(final)
    context = {
        'fb': fb,
        'ig': ig,
        'fbFol':fbFol,
        'igFol':igFol
    }
    return HttpResponse(template.render(context,request))

@login_required(login_url='login')
def compare_trends_ig(request):
    template = loader.get_template('compare_trends_ig.html')
    #--
    if request.user.is_authenticated:
        email = request.user.email
    else:
        email = "Guest"
    #--
    final = request.session.get('final',{})
    finalFb = request.session.get('finalFb',{})
    #--
    if not finalFb:
        print('FinalFb not found!')
        request.session['finalFb'] = fb_func.trendsCompilerFb(email)
        finalFb = request.session.get('finalFb',{})
    #--
    fb = ig_func.trendData(finalFb)
    fbFol = fb_func.followersFB(email)
    igFol = ig_func.followersIG(email)
    ig = ig_func.trendData(final)
    context = {
        'fb': fb,
        'ig': ig,
        'fbFol':fbFol,
        'igFol':igFol
    }
    return HttpResponse(template.render(context,request))
