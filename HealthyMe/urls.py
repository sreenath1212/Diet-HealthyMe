"""HealthyMe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MyApp.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name="index"),
	path('reg/',reg,name='reg'),
    path('regaction/',regaction,name='regaction'),
    path('viewreg/',viewreg,name='viewreg'),
     path('viewstatus/',viewstatus,name='viewstatus'),
    path('deletereg/',deletereg,name='deletereg'),
    path('login/',login,name='login'),
	path('index/',index,name='index'),
    path('searchlogin/',searchlogin,name='searchlogin'),
    path('logout/',logout_session,name='logout'),
    path('viewprofile/',viewprofile,name='viewprofile'),
    path('editprofile/',editprofile,name='editprofile'),
    path('editprofileaction/',editprofileaction,name='editprofileaction'),
    path('exercise/',exercise,name='exercise'),
    path('exerciseaction/',exerciseaction,name='exerciseaction'),
    path('viewexercise/',viewexercise,name='viewexercise'),
    path('viewuserexercise/',viewuserexercise,name='viewuserexercise'),
    path('delexercise/',delexercise,name='delexercise'),
    path('yoga/',yoga,name='yoga'),
    path('yogaaction/',yogaaction,name='yogaaction'),
    path('viewyoga/',viewyoga,name='viewyoga'),
    path('viewuseryoga/',viewuseryoga,name='viewuseryoga'),
    path('deleteyoga/',deleteyoga,name='deleteyoga'),
    path('dietmaster/',dietmaster,name='dietmaster'),
    path('dietmasteraction/',dietmasteraction,name='dietmasteraction'),
    path('viewdietmaster/',viewdietmaster,name='viewdietmaster'),
    path('deldietmaster/',deldietmaster,name='deldietmaster'),
    path('dietchild/',dietchild,name='dietchild'),
    path('dietchildaction/',dietchildaction,name='dietchildaction'),
    path('viewdietchild/',viewdietchild,name='viewdietchild'),
    path('deldietchild/',deldietchild,name='deldietchild'),
    path('submit_complete_plan/',submit_complete_plan,name='submit_complete_plan'),
    path('adminhome/',adminhome,name='adminhome'),
    path('userhome/',userhome,name='userhome'),
     path('home/',home,name='home'),
    path('dieticianhome/',dieticianhome,name='dieticianhome'),
    path('calorie/',calorie,name='calorie'),
	path('caloriecalculator/',caloriecalculator,name='caloriecalculator'),
    path('calorieaction/',calorieaction,name='calorieaction'),
    path('calo/',calo,name='calo'),
    path('reqdietplan/',reqdietplan,name='reqdietplan'), 
    path('reqdietplanaction/',reqdietplanaction,name='reqdietplanaction'),
    path('reqdietplan1action/',reqdietplan1action,name='reqdietplan1action'),
    path('viewdietplanreq/',viewdietplanreq,name='viewdietplanreq'),
    path('viewdietplanreqdietician/',viewdietplanreqdietician,name='viewdietplanreqdietician'),
    path('deletedietplan/',deletedietplan,name='deletedietplan'),
    path('uchat/',uchat,name='uchat'),
    path('chatact/',chatact,name='chatact'),
    path('dchat/',dchat,name='dchat'),
    path('dchatact/',dchatact,name='dchatact'),
    path('adietplan/',adietplan,name='adietplan'), 
    path('output/',output,name='output'), 
    path('fpass/',fpass,name='fpass'),
    path('fpass1/',fpass1,name='fpass1'),
    path('fpassact/',fpassact,name='fpassact'),
    # OTP-based password reset URLs
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('send_otp/', send_otp, name='send_otp'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('reset_password/', reset_password, name='reset_password'),
    # OTP-based login URLs
    path('login_with_otp/', login_with_otp, name='login_with_otp'),
    path('send_login_otp/', send_login_otp, name='send_login_otp'),
    path('verify_login_otp/', verify_login_otp, name='verify_login_otp'),
    # Registration verification URL
    path('verify_registration_otp/', verify_registration_otp, name='verify_registration_otp'),
    # Test email URL (for debugging)
    path('test_email_config/', test_email_config, name='test_email_config'),
    # Test Google OAuth URL (for debugging)
    path('test_google_oauth_config/', test_google_oauth_config, name='test_google_oauth_config'),
    # Google OAuth URLs
    path('google-login/', google_login, name='google_login'),
    path('google-login-callback/', google_login_callback, name='google_login_callback'),
    path('test-session/', test_session, name='test_session'),
    path('userinputh/',userinputh,name='userinputh'), 
    path('userinputwl/',userinputwl,name='userinputwl'), 
    path('userinputwg/',userinputwg,name='userinputwg'), 
    path('Weight_Loss/', Weight_Loss, name='Weight_Loss'),
    path('Weight_Gain/', Weight_Gain, name='Weight_Gain'),
    path('Healthy/', Healthy, name='Healthy'), 
    path('chat/', chat, name='chat'),
    path('recipe_response/', recipe_response, name='recipe_response'),
    path('aboutus/',aboutus, name='aboutus'),
    path('payment/', payment, name='payment'),
    path('paymentaction/', paymentaction, name='paymentaction'),
    path('approve/', approve, name='approve'),
    path('bmr_form/', bmr_view, name='bmr_form'),
    path('clear_chat_history/', clear_chat_history, name='clear_chat_history'),
    path('food_image_calorie/', food_image_calorie, name='food_image_calorie'),
    path('addyoutube/', addyoutube, name='addyoutube'),
    path('log_youtube_link/', log_youtube_link, name='log_youtube_link'),
    path('meal_planner/', meal_planner_form, name='meal_planner_form'),
    path('plan_meal/', plan_meal, name='plan_meal'),
    path('view_saved_meal_plan/', view_saved_meal_plan, name='view_saved_meal_plan'),
    path('update_meal_progress/', update_meal_progress, name='update_meal_progress'),

    
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
