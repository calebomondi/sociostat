from django.urls import path
from . import views

urlpatterns = [
    path('',views.welcome,name="home-page"),
    #facebook
    path('facebook/dashboard/',views.facebook_dashboard,name='fb-dashboard'),
    path('facebook/views/',views.facebook_view,name='fb-views'),
    path('facebook/post/',views.facebook_post,name='fb-post'),
    path('facebook/show/',views.face_make_post,name='fb-process-form'),
    path('facebook/post/carousel',views.face_carousel,name='fb-carousel'),
    path('facebook/show/carousel',views.face_make_carousel,name='fb-process-carousel'),
    path('facebook/post/text',views.facebook_text,name='fb-text'),
    path('facebook/show/text',views.face_make_text,name='fb-process-text'),
    #---chart paths---
    path('facebook/trends',views.facebook_trends,name='fb-trends'),
    path('facebook/trends/process', views.LineChartDataFb.as_view(), name='fb-chart-data'),

    #instagram
    path('instagram/dashboard/',views.instagram_dashboard,name='ig-dashboard'),
    path('instagram/views/',views.insta_views,name='ig-views'),
    path('instagram/post/',views.insta_post,name='ig-post'),
    path('instagram/show/',views.insta_make_post,name='ig-process-form'),
    path('instagram/post/carousel',views.insta_carousel,name='ig-carousel'),
    path('instagram/show/carousel',views.insta_make_carousel,name='ig-process-carousel'),
    path('instagram/post/story',views.insta_story,name='ig-story'),
    path('instagram/story',views.insta_make_story,name='ig-process-story'),
    #---chart paths---
    path('instagram/trends',views.insta_trends,name='ig-trends'),
    path('instagram/trends/process', views.LineChartDataIg.as_view(), name='ig-chart-data'),

    #---compare chart paths---
    path('facebook/comparison',views.compare_trends_fb,name='comp-trends-fb'),
    path('instagram/comparison',views.compare_trends_ig,name='comp-trends-ig'),
    path('all/trends/process', views.LineChartDataComp.as_view(), name='ig-chart-data'),

    #all
    path('all/post/',views.postAll,name='ig-post'),
    path('all/show/',views.all_make_post,name='all-process-form'),
    path('all/post/carousel',views.all_carousel,name='all-carousel'),
    path('all/show/carousel',views.all_make_carousel,name='all-process-carousel'),

    #set-up
    path('setup/',views.setup,name='set-up'),
    path('setup/process',views.setup_process,name='set-up-process'),

    #authenticate
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.register,name='register'),
    path('password_change/', views.password_change, name='password_change'),
]