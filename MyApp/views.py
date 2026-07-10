from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect,redirect
from MyApp.forms import yform, eform
from MyApp.models import ymodel, emodel
import datetime
from PIL import ImageFilter,Image
import os
import psutil
import time
import subprocess
import cv2
import fnmatch
import glob
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import traceback
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import tempfile
import mimetypes
import re
import requests
import random
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# Module-level logger
logger = logging.getLogger(__name__)

# Email sender configuration dynamically falling back to SMTP host user
FROM_EMAIL = getattr(settings, 'DEFAULT_FROM_EMAIL', settings.EMAIL_HOST_USER)


# Legacy OTP storage removed

# Create your views here.
def reg(request):
	return render(request,'registration.html')

def index(request):
	return render(request,'index.html')
	
def regaction(request):
    if request.method == "GET":
        # Get registration data
        a = request.GET['fname']
        b = request.GET['lname']
        c = request.GET['email']
        d = request.GET['dob']
        e = request.GET['address']
        h = request.GET['phone']
        i = request.GET['password']
        j = request.GET['gender']
        
        # Check if email already exists
        with connection.cursor() as cursor:
            # FIX: Column is EMAIL (uppercase) in registration table on Linux MySQL
            cursor.execute("SELECT EMAIL FROM registration WHERE EMAIL = %s", [c])
            existing_user = cursor.fetchone()
        
        if existing_user:
            return render(request, 'registration.html', {"error": "Email already registered. Please use a different email or login."})
        
        # Check if user came from Google OAuth
        google_email = request.session.get('google_email')
        google_name = request.session.get('google_name')
        
        if google_email and google_email == c:
            # User came from Google OAuth, skip OTP verification and register directly
            try:
                with connection.cursor() as cursor:
                    # Insert into registration table
                    sql = """INSERT INTO registration 
                            (FIRST_NAME, LAST_NAME, ADDRESS, PHONE, EMAIL, GENDER, DOB, status) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, '')"""
                    
                    cursor.execute(sql, [a, b, e, h, c, j, d])
                    
                    # B9 FIX: was SELECT max(RID) which is a race condition in multi-user scenarios
                    # LAST_INSERT_ID() returns the ID from THIS connection's last INSERT
                    cursor.execute("SELECT LAST_INSERT_ID()")
                    user_id = cursor.fetchone()[0]
                    
                    # Insert into login table
                    # D4 FIX: Hash user password on Google OAuth registration
                    from django.contrib.auth.hashers import make_password
                    sql2 = "INSERT INTO login (UID, UNAME, upass, UTYPE, status) VALUES (%s, %s, %s, 'user', '')"
                    cursor.execute(sql2, [user_id, c, make_password(i)])
                    
                    # Set session variables for automatic login
                    request.session['UID'] = user_id
                    request.session['UNAME'] = c
                    # A6 FIX: UPASSWORD must never be stored in session — removed
                    request.session['UTYPE'] = 'user'
                    request.session['status'] = None
                    
                    # Clear Google session data
                    if 'google_email' in request.session:
                        del request.session['google_email']
                    if 'google_name' in request.session:
                        del request.session['google_name']
                    
                    # Redirect directly to user home
                    return redirect('/userhome/')
                    
            except Exception as e:
                print(f"Error creating Google OAuth user: {str(e)}")
                return render(request, "registration.html", {"error": "Failed to create account. Please try again."})
        else:
            # Regular registration flow - Direct database insert (No OTP)
            try:
                with connection.cursor() as cursor:
                    # Insert into registration table
                    sql = """INSERT INTO registration 
                            (FIRST_NAME, LAST_NAME, ADDRESS, PHONE, EMAIL, GENDER, DOB, status) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, '')"""
                    cursor.execute(sql, [a, b, e, h, c, j, d])
                    
                    # Get user ID
                    cursor.execute("SELECT LAST_INSERT_ID()")
                    user_id = cursor.fetchone()[0]
                    
                    # Insert into login table
                    from django.contrib.auth.hashers import make_password
                    sql2 = "INSERT INTO login (UID, UNAME, upass, UTYPE, status) VALUES (%s, %s, %s, 'user', '')"
                    cursor.execute(sql2, [user_id, c, make_password(i)])
                    
                    return render(request, "login.html", {"success": "Registration completed successfully! Please login with your email and password."})
                    
            except Exception as e:
                logger.error(f"Error directly registering user: {str(e)}")
                import traceback
                logger.error(traceback.format_exc())
                return render(request, "registration.html", {"error": f"Failed to create account: {str(e)}"})
    
    return render(request, "registration.html")

def viewreg(request):
	# C1 FIX: No auth check existed — anyone could see all user data
	if request.session.get('UTYPE') != 'admin':
		return HttpResponse("<script>alert('Admin access required');window.location='/login/';</script>")
	cur=connection.cursor()
	s="select * from registration"
	cur.execute(s)
	list=[]
	result=cur.fetchall()
	for row in result:
		w={'RID':row[0],'FIRST_NAME':row[1],'LAST_NAME':row[2],'ADDRESS':row[3],'PHONE':row[4],'EMAIL':row[5],'GENDER':row[6],'DOB':row[7],'status':row[8]}
		list.append(w)
	return render(request,'viewreg.html',{'list':list})
from django.shortcuts import render
from django.db import connection

def viewstatus(request):
    # Get the 'RID' from the session (assuming it's stored in session)
    RID = request.session.get('UID')  # Using .get() to safely retrieve 'RID' from session
    
    # Check if RID exists, if not, handle it appropriately
    
    
    # Using parameterized query to avoid SQL injection
    cur = connection.cursor()
    s = "SELECT * FROM registration WHERE RID=%s"
    
    # Execute the query with the RID
    cur.execute(s, [RID])  # Pass the RID as a list to use parameterized query
    
    list = []
    result = cur.fetchall()
    for row in result:
        w = {
            'RID': row[0],
            'FIRST_NAME': row[1],
            'LAST_NAME': row[2],
            'ADDRESS': row[3],
            'PHONE': row[4],
            'EMAIL': row[5],
            'GENDER': row[6],
            'DOB': row[7],
            'status': row[8]
        }
        list.append(w)
    
    return render(request, 'viewstatus.html', {'list': list})


def approve(request):
    # C1 FIX: Admin-only action
    if request.session.get('UTYPE') != 'admin':
        return HttpResponse("<script>alert('Admin access required');window.location='/login/';</script>")
    cursor = connection.cursor()
    sid = request.GET['id']
    # FIX: parameterized queries — was SQL injection via string formatting
    cursor.execute("UPDATE registration SET status='approve' WHERE RID=%s", [sid])
    cursor.execute("UPDATE login SET status='approve' WHERE uid=%s", [sid])
    msg = "<script>alert('Success');window.location='/viewreg/';</script>"
    return HttpResponse(msg)

def deletereg(request):
	# C1 FIX: Admin-only action
	if request.session.get('UTYPE') != 'admin':
		return HttpResponse("<script>alert('Admin access required');window.location='/login/';</script>")
	cursor = connection.cursor()
	n = request.GET['id']
	# FIX: parameterized queries — was SQL injection
	cursor.execute("DELETE FROM registration WHERE RID=%s", [n])
	cursor.execute("DELETE FROM login WHERE UID=%s AND UTYPE='user'", [n])
	h = "<script>alert('DATA DELETED SUCCESSFULLY');window.location='/viewreg/';</script>"
	return HttpResponse(h)
	
def login(request):
	return render(request,'login.html')

def searchlogin(request):
    cursor = connection.cursor()
    p = request.GET['email']
    q = request.GET['password']

    # D2 FIX: Use Two-Pass Password Verification to check hashed passwords and support legacy plaintext
    cursor.execute("SELECT * FROM login WHERE uname=%s", [p])
    result1 = cursor.fetchall()

    if result1:
        from django.contrib.auth.hashers import check_password, make_password
        authenticated = False
        user_row = None
        
        for row1 in result1:
            db_pass = row1[2]
            # Try to verify via Django's hash check
            try:
                if check_password(q, db_pass):
                    authenticated = True
                    user_row = row1
                    break
            except Exception:
                pass
            
            # Fallback to plain-text match (legacy)
            if q == db_pass:
                authenticated = True
                user_row = row1
                # Auto-upgrade the plaintext password to a strong hash upon successful login
                hashed_pass = make_password(q)
                cursor.execute("UPDATE login SET upass=%s WHERE uid=%s AND uname=%s", [hashed_pass, row1[0], p])
                break

        if authenticated and user_row:
            request.session['UID'] = user_row[0]
            request.session['UNAME'] = user_row[1]
            request.session['UTYPE'] = user_row[3]
            request.session['status'] = user_row[4]

            if request.session['UTYPE'] == 'admin':
                return redirect('/adminhome/')
            elif request.session['UTYPE'] == 'user':
                if request.session['status'] == 'paid':
                    return redirect('/userhome/')
                else:
                    msg = "<script>alert('Payment is pending'); window.location='/home/';</script>"
                    return HttpResponse(msg)
            elif request.session['UTYPE'] == 'dietician':
                return redirect('/dieticianhome/')
        else:
            html = "<script>alert('Invalid username or password'); window.location='/login/';</script>"
            return HttpResponse(html)
    else:
        html = "<script>alert('Invalid username or password'); window.location='/login/';</script>"
        return HttpResponse(html)

def logout_session(request):
	# Safely delete session keys if they exist
	session_keys = ['UID', 'UNAME', 'UPASSWORD', 'UTYPE', 'status', 'google_email', 'google_name', 'google_oauth_state']
	for key in session_keys:
		if key in request.session:
			del request.session[key]
	
	html="<script>alert('Logged Out Successfully');window.location='/login/';</script>"
	return HttpResponse(html)
    #return render(request,'login.html')

def viewprofile(request):
	# Check if user is logged in
	logger.debug(f"DEBUG: viewprofile - Session key: {request.session.session_key}")
	logger.debug(f"DEBUG: viewprofile - All session data: {dict(request.session)}")
	logger.debug(f"DEBUG: viewprofile - UID in session: {'UID' in request.session}")
	logger.debug(f"DEBUG: viewprofile - Request cookies: {dict(request.COOKIES)}")
	
	if 'UID' not in request.session:
		html="<script>alert('Please login first');window.location='/login/';</script>"
		return HttpResponse(html)
	
	cur = connection.cursor()
	uid = request.session['UID']
	# FIX: parameterized query — was SQL injection
	cur.execute("SELECT * FROM registration WHERE RID=%s", [uid])
	list=[]
	result=cur.fetchall()
	for row in result:
		w={'RID':row[0],'FIRST_NAME':row[1],'LAST_NAME':row[2],'ADDRESS':row[3],'PHONE':row[4],'EMAIL':row[5],'GENDER':row[6],'DOB':row[7]}
		list.append(w)
	return render(request,'viewprofile.html',{'list':list})

def editprofile(request):
	# Check if user is logged in
	if 'UID' not in request.session:
		html="<script>alert('Please login first');window.location='/login/';</script>"
		return HttpResponse(html)
	
	cur = connection.cursor()
	uid = request.session['UID']
	# FIX: parameterized query — was SQL injection
	cur.execute("SELECT * FROM registration WHERE RID=%s", [uid])
	list=[]
	result=cur.fetchall()
	for row in result:
		w={'RID':row[0],'FIRST_NAME':row[1],'LAST_NAME':row[2],'ADDRESS':row[3],'PHONE':row[4],'EMAIL':row[5],'GENDER':row[6],'DOB':row[7]}
		list.append(w)
	return render(request,'editprofile.html',{'list':list})

def editprofileaction(request):
	# Check if user is logged in
	if 'UID' not in request.session:
		html="<script>alert('Please login first');window.location='/login/';</script>"
		return HttpResponse(html)
	cursor=connection.cursor()
	a=request.GET['fname']
	b=request.GET['lname']
	e=request.GET['address']
	h=request.GET['phone']
	j=request.GET['gender']
	uid=request.session['UID']
	# FIX: was hardcoded rid='1' — now uses the actual logged-in user's ID
	cursor.execute(
		"UPDATE registration SET FIRST_NAME=%s, LAST_NAME=%s, ADDRESS=%s, PHONE=%s, GENDER=%s WHERE RID=%s",
		[a, b, e, h, j, uid]
	)
	msg="<script>alert('Profile Updated Successfully');window.location='/viewprofile/';</script>"
	return HttpResponse(msg)

def exercise(request):
	id = request.GET.get('id')
	if not id:
		return HttpResponse("<script>alert('Invalid Request: User ID is required.');window.location='/viewreg/';</script>")
	# Get user type from session for dynamic home link
	user_type = request.session.get('UTYPE', 'admin')
	return render(request,'exercise.html',{'id':id, 'user_type': user_type})

'''def exerciseaction(request):
	cursor=connection.cursor()
	#ccode=request.GET['ccode']
	a=request.GET['ename']
	b=request.GET['etype']
	c=request.GET['description']
	sql="insert into exercise (ENAME,ETYPE,EDESC) values ('%s','%s','%s')"%(a,b,c)
	cursor.execute(sql)
	h="<script>alert('Exercise Added Successfully');window.location='/exercise/';</script>"
	return HttpResponse(h)'''

def exerciseaction(request):
	if request.method=="POST":
		MyProfileForm=eform(request.POST,request.FILES)
		if MyProfileForm.is_valid():
			profile=emodel()
			profile.UID=request.POST["uid"]
			profile.ENAME=MyProfileForm.cleaned_data["ENAME"]
			profile.ETYPE=request.POST["etype"]
			profile.EDESC=request.POST["edesc"]
			profile.EVIDEO=MyProfileForm.cleaned_data["EVIDEO"]
			profile.save()
			html="<script>alert('Exercise Added Successfully');window.location='/viewdietplanreqdietician/';</script>"
		else:
			# FIX: was UnboundLocalError if form was invalid
			html="<script>alert('Invalid form data. Please check your inputs.');window.history.back();</script>"
	else:
		# GET request — render the empty form
		return render(request, 'exercise.html', {'form': eform()})
	return HttpResponse(html)


def viewexercise(request):
	cur=connection.cursor()
	s="select * from exercise"
	cur.execute(s)
	list=[]
	result=cur.fetchall()
	for row in result:
		w={'EXID':row[0],'UID':row[1],'ENAME':row[2],'ETYPE':row[3],'EDESC':row[4],'EVIDEO':row[5]}
		list.append(w)
	
	# Get user type from session for dynamic home link
	user_type = request.session.get('UTYPE', 'admin')
	return render(request,'viewexercise.html',{'list':list, 'user_type': user_type})

# NOTE: First definition of viewuserexercise removed — it was dead code (overwritten by the
# correct version below that includes auth check and joins on UID).

def delexercise(request):
	cursor = connection.cursor()
	n = request.GET['id']
	# FIX: parameterized query — was SQL injection
	cursor.execute("DELETE FROM exercise WHERE EXID=%s", [n])
	h = "<script>alert('DATA DELETED SUCCESSFULLY');window.location='/viewexercise/';</script>"
	return HttpResponse(h)
def viewuseryoga(request):
	# Check if user is logged in
	if 'UID' not in request.session:
		html="<script>alert('Please login first');window.location='/login/';</script>"
		return HttpResponse(html)
	
	cur = connection.cursor()
	uid = request.session['UID']
	# FIX: parameterized query — was SQL injection
	cur.execute("SELECT * FROM yoga WHERE yoga.UID=%s", [uid])
	list=[]
	result=cur.fetchall()
	for row in result:
		w={'YID':row[0],'UID':row[1],'YNAME':row[2],'YTYPE':row[3],'YDESC':row[4],'YPIC':row[5]}
		list.append(w)
	return render(request,'viewuseryoga.html',{'list':list})
def yoga(request):
	id = request.GET.get('id')
	if not id:
		return HttpResponse("<script>alert('Invalid Request: User ID is required.');window.location='/viewreg/';</script>")
	# Get user type from session for dynamic home link
	user_type = request.session.get('UTYPE', 'admin')
	return render(request,'yoga.html',{'id':id, 'user_type': user_type})
def viewuserexercise(request):
	# Check if user is logged in
	if 'UID' not in request.session:
		html="<script>alert('Please login first');window.location='/login/';</script>"
		return HttpResponse(html)
	
	cur = connection.cursor()
	uid = request.session['UID']
	# FIX: parameterized query — was SQL injection
	cur.execute("SELECT * FROM exercise WHERE exercise.UID=%s", [uid])
	list=[]
	result=cur.fetchall()
	for row in result:
		w={'EXID':row[0],'UID':row[1],'ENAME':row[2],'ETYPE':row[3],'EDESC':row[4],'EVIDEO':row[5]}
		list.append(w)
	return render(request,'viewuserexercise.html',{'list':list})
'''def yogaaction(request):
	cursor=connection.cursor()
	a=request.GET['yname']
	b=request.GET['etype']
	c=request.GET['description']
	sql="insert into yoga (YNAME,YTYPE,YDESC) values ('%s','%s','%s')"%(a,b,c)
	cursor.execute(sql)
	h="<script>alert('Yoga Added Successfully');window.location='/yoga/';</script>"
	return HttpResponse(h)'''

def yogaaction(request):
	if request.method=="POST":
		MyProfileForm=yform(request.POST,request.FILES)
		if MyProfileForm.is_valid():
			profile=ymodel()
			profile.YNAME=MyProfileForm.cleaned_data["YNAME"]
			profile.YTYPE=request.POST["ytype"]
			profile.YDESC=request.POST["ydesc"]
			profile.UID=request.POST["uid"]
			profile.YPIC=MyProfileForm.cleaned_data["YPIC"]
			profile.save()
			html="<script>alert('Yoga Added Successfully');window.location='/viewdietplanreqdietician/';</script>"
		else:
			# FIX: was UnboundLocalError if form was invalid
			html="<script>alert('Invalid form data. Please check your inputs.');window.history.back();</script>"
	else:
		# GET request — render the empty form
		return render(request, 'yoga.html', {'form': yform()})
	return HttpResponse(html)

def viewyoga(request):
	cur=connection.cursor()
	s="select * from yoga"
	cur.execute(s)
	list=[]
	result=cur.fetchall()
	for row in result:
		w={'YID':row[0],'UID':row[1],'YNAME':row[2],'YTYPE':row[3],'YDESC':row[4],'YPIC':row[5]}
		list.append(w)
	
	# Get user type from session for dynamic home link
	user_type = request.session.get('UTYPE', 'admin')
	return render(request,'viewyoga.html',{'list':list, 'user_type': user_type})

# def viewuseryoga(request):
# 	cur=connection.cursor()
# 	s="select * from yoga"
# 	cur.execute(s)
# 	list=[]
# 	result=cur.fetchall()
# 	for row in result:
# 		w={'YID':row[0],'UID':row[1],'YNAME':row[2],'YTYPE':row[3],'YDESC':row[4],'YPIC':row[5]}
# 		list.append(w)
# 	return render(request,'viewuseryoga.html',{'list':list})

def deleteyoga(request):
	cursor = connection.cursor()
	n = request.GET['id']
	# FIX: parameterized query — was SQL injection
	cursor.execute("DELETE FROM yoga WHERE YID=%s", [n])
	h = "<script>alert('DATA DELETED SUCCESSFULLY');window.location='/viewyoga/';</script>"
	return HttpResponse(h)

def dietmaster(request):
	id = request.GET.get('id')
	if not id:
		return HttpResponse("<script>alert('Invalid Request: Patient Request ID is required.');window.location='/viewdietplanreqdietician/';</script>")
	return render(request,'dietmaster.html',{'id':id})

def dietmasteraction(request):
	# C2 FIX: Add dietician role check (was only checking login, not role)
	if request.session.get('UTYPE') not in ['dietician', 'admin']:
		return HttpResponse("<script>alert('Dietician access required');window.location='/login/';</script>")
	# Check if user is logged in
	if 'UID' not in request.session:
		html="<script>alert('Please login first');window.location='/login/';</script>"
		return HttpResponse(html)
	
	cursor = connection.cursor()
	a = request.GET['sdate']
	b = request.GET['edate']
	c = request.GET['days']
	d = request.GET['rid']
	uid = request.session['UID']
	# FIX: parameterized query — was SQL injection
	cursor.execute(
		"INSERT INTO dietmaster (SDATE,EDATE,NOD,RQID) VALUES (%s,%s,%s,%s)",
		[a, b, c, d]
	)
	h = "<script>alert('Diet Added Successfully');window.location='/dietchild/';</script>"
	return HttpResponse(h)

def viewdietmaster(request):
	# C2 FIX: Dietician-only view
	if request.session.get('UTYPE') not in ['dietician', 'admin']:
		return HttpResponse("<script>alert('Dietician access required');window.location='/login/';</script>")
	cur=connection.cursor()
	uid=request.session['UID']
	rid=request.GET['rid']
	# FIX: parameterized query — was SQL injection (line 515 original)
	cur.execute("SELECT * FROM dietmaster, dietchild WHERE RQID=%s AND dietmaster.DTID=dietchild.DTID", [rid])
	list=[]
	result=cur.fetchall()
	for row in result:
		w={'DTID':row[0],'SDATE':row[1],'EDATE':row[2],'NOD':row[3],'DAY':row[7],'PBF':row[8],'BF':row[9],'BR':row[10],'LU':row[11],'EV':row[12],'DN':row[13],'TNOT':row[14]}
		list.append(w)
	return render(request,'viewdietuser.html',{'list':list})

def deldietmaster(request):
	# C1 FIX: Admin-only delete
	if request.session.get('UTYPE') != 'admin':
		return HttpResponse("<script>alert('Admin access required');window.location='/login/';</script>")
	cursor = connection.cursor()
	n = request.GET['id']
	# FIX: parameterized query — was SQL injection
	cursor.execute("DELETE FROM dietmaster WHERE DTID=%s", [n])
	h = "<script>alert('DATA DELETED SUCCESSFULLY');window.location='/viewdietmaster/';</script>"
	return HttpResponse(h)

def dietchild(request):
	# C2 FIX: Dietician-only view
	if request.session.get('UTYPE') not in ['dietician', 'admin']:
		return HttpResponse("<script>alert('Dietician access required');window.location='/login/';</script>")
	cursor=connection.cursor()
	sql1="select max(DTID) from dietmaster"
	cursor.execute(sql1)
	result=cursor.fetchone()
	# FIX: was crashing with TypeError when table is empty (row[0] was None)
	if not result or result[0] is None:
		return HttpResponse("<script>alert('No diet master record found. Please add a diet plan first.');window.history.back();</script>")
	id=int(result[0])
	return render(request,'dietchild.html',{'id':id,'d':'d'})

def dietchildaction(request):
	# C2 FIX: Dietician-only action
	if request.session.get('UTYPE') not in ['dietician', 'admin']:
		return HttpResponse("<script>alert('Dietician access required');window.location='/login/';</script>")
	cursor = connection.cursor()
	a = request.GET['day']
	b = request.GET['pbf']
	c = request.GET['bf']
	d = request.GET['br']
	e = request.GET['lu']
	f = request.GET['ev']
	g = request.GET['di']
	h = request.GET['tnot']
	i = request.GET['id']
	# FIX: parameterized query — was SQL injection
	cursor.execute(
		"INSERT INTO dietchild (DAY,PBF,BF,BR,LU,EV,DN,TNOT,DTID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
		[a, b, c, d, e, f, g, h, i]
	)
	cursor.execute("SELECT RQID FROM dietmaster WHERE DTID=%s", [i])
	result = cursor.fetchall()
	for row in result:
		rid = row[0]
	# Don't update status immediately - let dietician add yoga and exercise first
	cursor.execute("UPDATE reqdietplan SET status='Diet Plan Added' WHERE RQID=%s", [rid])
	h = "<script>alert('Diet Plan Added Successfully! You can now add Yoga and Exercise, then submit the complete plan.');window.location='/viewdietplanreqdietician/';</script>"
	return HttpResponse(h)

def viewdietchild(request):
	# C1 FIX: Admin-only view
	if request.session.get('UTYPE') != 'admin':
		return HttpResponse("<script>alert('Admin access required');window.location='/login/';</script>")
	cur=connection.cursor()
	s="select * from dietchild"
	cur.execute(s)
	list=[]
	result=cur.fetchall()
	for row in result:
		w={'CDTID':row[0],'DTID':row[1],'DAY':row[2],'PBF':row[3],'BF':row[4],'BR':row[5],'LU':row[6],'EV':row[7],'DN':row[8],'TNOT':row[9]}
		list.append(w)
	return render(request,'viewdietchild.html',{'list':list})

def deldietchild(request):
	# C1 FIX: Admin-only delete
	if request.session.get('UTYPE') != 'admin':
		return HttpResponse("<script>alert('Admin access required');window.location='/login/';</script>")
	cursor = connection.cursor()
	n = request.GET['id']
	# FIX: parameterized query — was SQL injection
	cursor.execute("DELETE FROM dietchild WHERE CDTID=%s", [n])
	h = "<script>alert('DATA DELETED SUCCESSFULLY');window.location='/viewdietchild/';</script>"
	return HttpResponse(h)

def submit_complete_plan(request):
	# C2 FIX: Dietician-only action
	if request.session.get('UTYPE') not in ['dietician', 'admin']:
		return HttpResponse("<script>alert('Dietician access required');window.location='/login/';</script>")
	cursor = connection.cursor()
	rid = request.GET['rid']
	# FIX: parameterized query — was SQL injection
	cursor.execute("UPDATE reqdietplan SET status='Completed' WHERE RQID=%s", [rid])
	h = "<script>alert('Complete Plan Submitted Successfully! The patient will be notified.');window.location='/viewdietplanreqdietician/';</script>"
	return HttpResponse(h)

def calorie(request):
	return render(request,'calorie.html')

def uchat(request):
	# Check if user is logged in
	if 'UID' not in request.session:
		html="<script>alert('Please login first');window.location='/login/';</script>"
		return HttpResponse(html)
	
	cursor=connection.cursor()
	uid=request.session['UID']
	# FIX: was raw string formatting — SQL injection vulnerability; now uses parameterized query
	s="SELECT * FROM chatm INNER JOIN chats ON chats.chat_id=chatm.chid WHERE uid=%s ORDER BY ctid ASC"
	
	cursor.execute(s, [uid])
	rs=cursor.fetchall()
	clist1=[]
	for row in rs:
		w={'chatid':row[0],'uid':row[1],'cdate':row[2],'msg':row[5],'typ':row[6]}
		clist1.append(w)
		""" s1="select * from chats where chat_id=%s"%(row[0])
		cursor.execute(s1)
		rs1=cursor.fetchall()
		slist1=[]
		for row1 in rs1:
			w1={'msg':row1[1],'typ':row1[2]}
			slist1.append(w1) """


	return render(request,'uchat.html',{'clist':clist1,'uid':uid})

def chatact(request):
	# Check if user is logged in
	if 'UID' not in request.session:
		html="<script>alert('Please login first');window.location='/login/';</script>"
		return HttpResponse(html)
	
	cursor = connection.cursor()
	uid = request.session['UID']
	msg = request.GET['msg']
	cd = datetime.today().strftime('%Y-%m-%d')

	# FIX: parameterized queries — were SQL injection
	cursor.execute("SELECT * FROM chatm WHERE uid=%s AND cdate=%s", [uid, cd])
	if cursor.rowcount > 0:
		cursor.execute("SELECT max(chid) as chatid FROM chatm")
		rss = cursor.fetchall()
		for row in rss:
			chid = row[0]
			cursor.execute("INSERT INTO chats (chat_id,msg,typ) VALUES (%s,%s,'U')", [chid, msg])
	else:
		cursor.execute("INSERT INTO chatm (cdate,uid) VALUES (%s,%s)", [cd, uid])
		cursor.execute("SELECT max(chid) as chatid FROM chatm")
		rss = cursor.fetchall()
		for row in rss:
			chid = row[0]
			cursor.execute("INSERT INTO chats (chat_id,msg,typ) VALUES (%s,%s,'U')", [chid, msg])

	return redirect('/uchat/')


def dchat(request):
	cursor=connection.cursor()
	uid = request.GET.get('id')
	if not uid:
		return HttpResponse("<script>alert('Invalid Request: User ID is required.');window.location='/dieticianhome/';</script>")
	s="select * from chatm inner join chats on chats.chat_id=chatm.chid where uid=%s order by ctid asc"
	cursor.execute(s, [uid])
	rs=cursor.fetchall()
	clist1=[]
	for row in rs:
		w={'chatid':row[0],'uid':row[1],'cdate':row[2],'msg':row[5],'typ':row[6]}
		clist1.append(w)
		""" s1="select * from chats where chat_id=%s"%(row[0])
		cursor.execute(s1)
		rs1=cursor.fetchall()
		slist1=[]
		for row1 in rs1:
			w1={'msg':row1[1],'typ':row1[2]}
			slist1.append(w1) """
	uidd=[]
	w={'uid':uid}
	uidd.append(w)

	return render(request,'dchat.html',{'clist':clist1,'uid':uidd})

def dchatact(request):
	cursor = connection.cursor()
	uid = request.GET['uid']
	msg = request.GET['msg']
	cd = datetime.today().strftime('%Y-%m-%d')
	
	# FIX: parameterized queries — were SQL injection
	cursor.execute("SELECT * FROM chatm WHERE uid=%s AND cdate=%s", [uid, cd])
	if cursor.rowcount > 0:
		cursor.execute("SELECT max(chid) as chatid FROM chatm")
		rss = cursor.fetchall()
		for row in rss:
			chid = row[0]
			cursor.execute("INSERT INTO chats (chat_id,msg,typ) VALUES (%s,%s,'D')", [chid, msg])
	else:
		cursor.execute("INSERT INTO chatm (cdate,uid) VALUES (%s,%s)", [cd, uid])
		cursor.execute("SELECT max(chid) as chatid FROM chatm")
		rss = cursor.fetchall()
		for row in rss:
			chid = row[0]
			cursor.execute("INSERT INTO chats (chat_id,msg,typ) VALUES (%s,%s,'D')", [chid, msg])
	
	cursor.execute(
		"SELECT * FROM chatm INNER JOIN chats ON chats.chat_id=chatm.chid WHERE uid=%s ORDER BY cdate ASC",
		[uid]
	)
	rs = cursor.fetchall()
	clist1 = []
	for row in rs:
		w = {'chatid': row[0], 'uid': row[1], 'cdate': row[2], 'msg': row[5], 'typ': row[6]}
		clist1.append(w)
	uidd = [{'uid': uid}]
	return render(request, 'dchat.html', {'clist': clist1, 'uid': uidd})

def calorieaction(request):
	# C1 FIX: Admin-only action
	if request.session.get('UTYPE') != 'admin':
		return HttpResponse("<script>alert('Admin access required');window.location='/login/';</script>")
	cursor=connection.cursor()
	a=request.GET['fname']
	b=request.GET['amount']
	c=request.GET['calories']
	# FIX: was raw string formatting — SQL injection vulnerability
	sql="INSERT INTO calories (fname,amount,calories) VALUES (%s,%s,%s)"
	cursor.execute(sql, [a, b, c])
	h="<script>alert('Item Added Successfully');window.location='/calorie/';</script>"
	return HttpResponse(h)

def caloriecalculator(request):
	cursor=connection.cursor()
	s="select * from calories"
	cursor.execute(s)
	list=[]
	result=cursor.fetchall()
	for row in result:
		w={'calid':row[0],'fname':row[1],'amount':row[2],'calories':row[3]}
		list.append(w)
	# On initial load, do not calculate calories
	calo = None
	return render(request,'caloriecalculator.html',{'list':list,'calo':calo})

def calo(request):
    cursor = connection.cursor()
    # Support multiple foods: getlist returns all values for the key
    fn_list = request.GET.getlist('fname')
    amount_list = request.GET.getlist('amount')
    error = None
    calo = None
    total_calories = 0
    details = []

    if not fn_list or not amount_list or len(fn_list) != len(amount_list):
        error = "Please select food(s) and enter valid amount(s)."
    else:
        for fn, amount_str in zip(fn_list, amount_list):
            try:
                am = float(amount_str)
                if am <= 0:
                    error = "Please enter a positive amount for all foods."
                    break
            except (ValueError, TypeError):
                error = "Please enter a valid number for all amounts."
                break

            cursor.execute("SELECT calories FROM calories WHERE fname=%s", [fn])
            result = cursor.fetchone()
            if result:
                cl = float(result[0])
                food_cal = (am / 100) * cl
                total_calories += food_cal
                details.append({'food': fn, 'amount': am, 'calories': food_cal})
            else:
                error = f"Selected food '{fn}' not found."
                break

    if not error:
        calo = total_calories

    # Fetch food list for the dropdown
    cursor.execute("SELECT * FROM calories")
    food_list = [{'calid': row[0], 'fname': row[1], 'amount': row[2], 'calories': row[3]} for row in cursor.fetchall()]

    context = {'list': food_list, 'calo': calo, 'error': error, 'details': details}
    return render(request, 'caloriecalculator.html', context)

def reqdietplan(request):
	return render(request,'reqdietplan.html')

def reqdietplanaction(request):
	# Check if user is logged in
	if 'UID' not in request.session:
		html="<script>alert('Please login first');window.location='/login/';</script>"
		return HttpResponse(html)
	
	cursor=connection.cursor()
	a=float(request.GET['hght'])
	b=float(request.GET['wght'])
	uid=request.session['UID']
	d=a/100
	c=d*d
	bmi=b/c
	if bmi<=18.4:
		res="Under Weight"
	elif bmi>18.4 and bmi<=24.9:
		res="Normal Weight"
	elif bmi>24.9 and bmi<=29.9:
		res="Over Weight"
	elif bmi>29.9 and bmi<=34.9:
		res="Obesity (Class 1)"
	elif bmi>34.9 and bmi<=39.9:
		res="Obesity (Class 2)"
	else:
		res="Obesity (Class 3)"

	sql="INSERT INTO reqdietplan(cid,wght,hght,bmi,res,status) VALUES (%s,%s,%s,%s,%s,'Pending')"
	cursor.execute(sql, [uid, b, a, bmi, res])  # FIX: parameterized + swapped a/b to match wght/hght order
	return render(request,'reqdietplan1.html',{'res':res,'bmi':bmi})

def reqdietplan1action(request):
	# Check if user is logged in
	if 'UID' not in request.session:
		html="<script>alert('Please login first');window.location='/login/';</script>"
		return HttpResponse(html)
	cursor = connection.cursor()
	uid = request.session['UID']
	# FIX: was using SELECT max(rqid) — race condition in multi-user scenario
	# Now scoped to the current user's own pending request
	cursor.execute(
		"UPDATE reqdietplan SET status='Request Sent' WHERE cid=%s AND status='Pending' ORDER BY rqid DESC LIMIT 1",
		[uid]
	)
	h = "<script>alert('Request Successfully Added');window.location='/reqdietplan/';</script>"
	return HttpResponse(h)

def viewdietplanreq(request):
	# Check if user is logged in
	if 'UID' not in request.session:
		html="<script>alert('Please login first');window.location='/login/';</script>"
		return HttpResponse(html)
	
	cur = connection.cursor()
	uid = request.session['UID']
	# FIX: parameterized query — was SQL injection
	cur.execute("SELECT * FROM reqdietplan WHERE cid=%s", [uid])
	list=[]
	result=cur.fetchall()
	for row in result:
		w={'rqid':row[0],'cid':row[1],'wght':row[2],'hght':row[3],'bmi':row[4],'res':row[5],'status':row[6]}
		list.append(w)
	return render(request,'viewdietreq.html',{'list':list})

def deletedietplan(request):
	# C3 FIX: Added login check + ownership scoping
	# Previously: any user could delete any diet plan by guessing rqid
	if 'UID' not in request.session:
		return HttpResponse("<script>alert('Please login first');window.location='/login/';</script>")
	uid = request.session['UID']
	cursor = connection.cursor()
	n = request.GET['id']
	# Only allow deletion of THIS user's own diet plan requests
	cursor.execute("DELETE FROM reqdietplan WHERE rqid=%s AND cid=%s", [n, uid])
	h = "<script>alert('DATA DELETED SUCCESSFULLY');window.location='/viewdietplanreq/';</script>"
	return HttpResponse(h)

def viewdietplanreqdietician(request):
	# C2 FIX: Dietician-only view — was accessible to any logged-in user
	if request.session.get('UTYPE') not in ['dietician', 'admin']:
		return HttpResponse("<script>alert('Dietician access required');window.location='/login/';</script>")
	cur=connection.cursor()
	# Join with registration table to get user names
	s="select r.rqid, r.cid, r.wght, r.hght, r.bmi, r.res, r.status, reg.FIRST_NAME, reg.LAST_NAME from reqdietplan r inner join registration reg on r.cid = reg.RID where r.status='Request Sent' or r.status='Diet Plan Added' order by r.rqid desc"
	cur.execute(s)
	list=[]
	result=cur.fetchall()
	for row in result:
		w={'rqid':row[0],'cid':row[1],'wght':row[2],'hght':row[3],'bmi':row[4],'res':row[5],'status':row[6],'first_name':row[7],'last_name':row[8]}
		list.append(w)
	return render(request,'viewdietreqdietician.html',{'list':list})

def adminhome(request):
	return render(request,'admin_home.html')

def userhome(request):
    # Debug session
    logger.debug(f"DEBUG: userhome - Session key: {request.session.session_key}")
    logger.debug(f"DEBUG: userhome - All session data: {dict(request.session)}")
    logger.debug(f"DEBUG: userhome - UID in session: {'UID' in request.session}")
    logger.debug(f"DEBUG: userhome - Request cookies: {dict(request.COOKIES)}")
    
    # Check if user is logged in
    if 'UID' not in request.session:
        logger.debug(f"DEBUG: userhome - No UID in session, redirecting to login")
        html="<script>alert('Please login first');window.location='/login/';</script>"
        return HttpResponse(html)
    
    # Fetch all YouTube videos from the database
    # FIX: Wrapped in try/except — youtube_videos table may not exist on all deployments
    video_ids = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT url FROM youtube_videos ORDER BY id DESC")
            rows = cursor.fetchall()
            for row in rows:
                url = row[0]
                match = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]+)", url)
                if match:
                    video_id = match.group(1).split('?')[0]
                    video_ids.append(video_id)
    except Exception:
        pass  # Table may not exist; fall through to default
    if not video_ids:
        video_ids = ["5zOHSysMmH0"]  # fallback default
    print("video_ids being sent to template:", video_ids)
    youtube_api_key = os.getenv("YOUTUBE_API_KEY", "")
    return render(request, 'user_home.html', {
        'youtube_video_ids': json.dumps(video_ids),
        'youtube_api_key': youtube_api_key,
    })
	
def dieticianhome(request):
	# Check if user is logged in and is a dietician
	if 'UID' not in request.session or 'UTYPE' not in request.session:
		html="<script>alert('Please login first');window.location='/login/';</script>"
		return HttpResponse(html)
	
	if request.session['UTYPE'] != 'dietician':
		html="<script>alert('Access denied. Only dieticians can access this page.');window.location='/login/';</script>"
		return HttpResponse(html)
	
	try:
		cur=connection.cursor()
		# Only show users who have actually started conversations (have entries in chatm table)
		s="select distinct r.RID, r.FIRST_NAME, r.LAST_NAME from registration r inner join chatm c on r.RID = c.uid order by r.FIRST_NAME, r.LAST_NAME"
		logger.debug(f"DEBUG: dieticianhome - Executing query: {s}")
		cur.execute(s)
		list=[]
		result=cur.fetchall()
		logger.debug(f"DEBUG: dieticianhome - Query result: {result}")
		for row in result:
			w={'RID':row[0],'FIRST_NAME':row[1],'LAST_NAME':row[2]}
			list.append(w)
		logger.debug(f"DEBUG: dieticianhome - Final list: {list}")
		cur.close()
		
		# Add some debugging to the template context
		context = {
			'list': list,
			'debug_info': f"Query returned {len(list)} results"
		}
		return render(request,'dietician_home.html', context)
	except Exception as e:
		# If there's an error, return empty list but don't crash
		print(f"Error in dieticianhome: {str(e)}")
		return render(request,'dietician_home.html',{'list':[], 'debug_info': f"Error: {str(e)}"})
	
def home(request):
	return render(request,'home.html')




def adietplan(request):
	return render(request,'adietplan.html')

def output(request):
	cur=connection.cursor()
	s="select * from ftemp"
	cur.execute(s)
	
	rs=cur.fetchall()
	list=[]
	for row in rs:
		w={'f':row[0]}
		list.append(w)

	return render(request,'output.html',{'fl':list})

def userinputwl(request):
	cur=connection.cursor()
	s="select * from ftemp"
	cur.execute(s)
	
	rs=cur.fetchall()
	fl=[]
	for row in rs:
		w={'f':row[0]}
		
		fl.append(w)

	return render(request,'userinputwl.html',{'fl':fl})

def userinputwg(request):
	cur=connection.cursor()
	s="select * from ftemp"
	cur.execute(s)
	
	rs=cur.fetchall()
	fl=[]
	for row in rs:
		w={'f':row[0]}
	
		fl.append(w)

	return render(request,'userinputwg.html',{'fl':fl})

def userinputh(request):
	return render(request,'userinputh.html')

def fpass(request):
	return render(request, 'fpass.html')

def fpass1(request):
	return render(request, 'fpass1.html')
	
def fpassact(request):
	if request.method == "POST":
		email = request.POST.get("un")
		phone = request.POST.get("up")
		new_pass = request.POST.get("np")
		cpass = request.POST.get("cp")

		if new_pass != cpass:
			return render(request, 'fpass.html', {'error': 'Passwords do not match.'})

		with connection.cursor() as cursor:
			# Verify email and phone match registration table
			cursor.execute("SELECT RID FROM registration WHERE EMAIL = %s AND PHONE = %s", [email, phone])
			user = cursor.fetchone()

			if user:
				from django.contrib.auth.hashers import make_password
				hashed_pw = make_password(new_pass)
				cursor.execute("UPDATE login SET upass = %s WHERE uid = %s", [hashed_pw, user[0]])
				return render(request, 'login.html', {'success': 'Password successfully reset. Please login with your new password.'})
			else:
				return render(request, 'fpass.html', {'error': 'Invalid Email or Phone Number.'})
	return redirect('/fpass/')

from django.shortcuts import render
from django.db import connection
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from django.db import transaction
import os

def prepare_training_data(cat_data, labels):
    cat_fin = []
    cat_labels = []
    for zz in range(5):
        for jj in range(len(cat_data)):
            cat_fin.append(list(cat_data[jj]) + [zz, zz])
            cat_labels.append(labels[jj])
    return np.array(cat_fin), np.array(cat_labels)

def Weight_Loss(request):
    try:
        age, veg, weight, height = int(request.GET['age']), float(request.GET['vng']), float(request.GET['wght']), float(request.GET['hght'])
    except: return render(request, 'userinputh.html', {'error': 'Invalid input.'})

    if not (50 <= height <= 280): return render(request, 'userinputh.html', {'error': 'Please enter a valid height between 50 and 280 cm.'})
    if not (10 <= weight <= 300): return render(request, 'userinputh.html', {'error': 'Please enter a valid weight between 10 and 300 kg.'})
    if not (10 <= age <= 120): return render(request, 'userinputh.html', {'error': 'Please enter a valid age between 10 and 120.'})

    height_m = height / 100
    bmi = weight / (height_m ** 2)
    agecl = round(age / 20)
    clbmi = 4 if bmi < 16 else (3 if bmi < 18.5 else (2 if bmi < 25 else (1 if bmi < 30 else 0)))
    
    _BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data = pd.read_csv(os.path.join(_BASE_DIR, 'input.csv'))
    brklbl = KMeans(n_clusters=3, random_state=0).fit(np.array(data.iloc[[i for i, v in enumerate(data['Breakfast']) if v == 1]].iloc[:, 5:15])).labels_
    
    datafin = pd.read_csv(os.path.join(_BASE_DIR, 'inputfin.csv')).to_numpy()
    weightlosscat = datafin[:, [1, 2, 7, 8]]
    
    weightlosscatfin, yt = prepare_training_data(weightlosscat, brklbl)
    clf = RandomForestClassifier(n_estimators=100).fit(weightlosscatfin, yt)
    
    X_test = np.array([list(weightlosscat[jj]) + [agecl, clbmi] for jj in range(len(weightlosscat))]) * ((clbmi + agecl) / 2)
    y_pred = clf.predict(X_test)
    
    fitems = [data.iloc[j]['Food_items'] for i in range(len(y_pred)) for j in range(len(brklbl)) if y_pred[i] == brklbl[j]]
    
    cur = connection.cursor()
    with transaction.atomic():
        cur.execute("DELETE FROM ftemp")
        for i in list(set(fitems)):
            if not (veg == 1 and i == 'Chicken Burger'): cur.execute("INSERT INTO ftemp (food) VALUES (%s)", [i])
            
    return render(request, 'userinputwl.html', {'fl': list(set(fitems)), 'flag': 1})

def Weight_Gain(request):
    try:
        age, veg, weight, height = int(request.GET['age']), float(request.GET['vng']), float(request.GET['wght']), float(request.GET['hght'])
    except: return render(request, 'userinputh.html', {'error': 'Invalid input.'})
    
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    agecl = round(age / 20)
    clbmi = 4 if bmi < 16 else (3 if bmi < 18.5 else (2 if bmi < 25 else (1 if bmi < 30 else 0)))
    
    _BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data = pd.read_csv(os.path.join(_BASE_DIR, 'input.csv'))
    lnchlbl = KMeans(n_clusters=3, random_state=0).fit(np.array(data.iloc[[i for i, v in enumerate(data['Lunch']) if v == 1]].iloc[:, 5:15])).labels_
    
    datafin = pd.read_csv(os.path.join(_BASE_DIR, 'inputfin.csv')).to_numpy()
    weightgaincat = datafin[:, [0, 1, 2, 3, 4, 7, 9, 10]]
    
    weightgaincatfin, yr = prepare_training_data(weightgaincat, lnchlbl)
    clf = RandomForestClassifier(n_estimators=100).fit(weightgaincatfin, yr)
    
    X_test = np.array([list(weightgaincat[jj]) + [agecl, clbmi] for jj in range(len(weightgaincat))]) * ((clbmi + agecl) / 2)
    y_pred = clf.predict(X_test)
    
    fitems = [data.iloc[j]['Food_items'] for i in range(len(y_pred)) for j in range(len(lnchlbl)) if y_pred[i] == lnchlbl[j]]
    
    cur = connection.cursor()
    with transaction.atomic():
        cur.execute("DELETE FROM ftemp")
        for i in list(set(fitems)):
            if not (veg == 1 and i == 'Chicken Burger'): cur.execute("INSERT INTO ftemp (food) VALUES (%s)", [i])
            
    return render(request, 'userinputwg.html', {'fl': list(set(fitems)), 'flag': 1})

def Healthy(request):
    try:
        age, veg, weight, height = int(request.GET['age']), float(request.GET['vng']), float(request.GET['wght']), float(request.GET['hght'])
    except: return render(request, 'userinputh.html', {'error': 'Invalid input.'})
    
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    agecl = round(age / 20)
    clbmi = 4 if bmi < 16 else (3 if bmi < 18.5 else (2 if bmi < 25 else (1 if bmi < 30 else 0)))
    
    _BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data = pd.read_csv(os.path.join(_BASE_DIR, 'input.csv'))
    dnrlbl = KMeans(n_clusters=3, random_state=0).fit(np.array(data.iloc[[i for i, v in enumerate(data['Dinner']) if v == 1]].iloc[:, 5:15])).labels_
    
    datafin = pd.read_csv(os.path.join(_BASE_DIR, 'inputfin.csv')).to_numpy()
    healthycat = datafin[:, [1, 2, 3, 4, 6, 7, 9]]
    
    healthycatfin, ys = prepare_training_data(healthycat, dnrlbl)
    clf = RandomForestClassifier(n_estimators=100).fit(healthycatfin, ys)
    
    X_test = np.array([list(healthycat[jj]) + [agecl, clbmi] for jj in range(len(healthycat))]) * ((clbmi + agecl) / 2)
    y_pred = clf.predict(X_test)
    
    fitems = [data.iloc[j]['Food_items'] for i in range(len(y_pred)) for j in range(len(dnrlbl)) if y_pred[i] == dnrlbl[j]]
    
    cur = connection.cursor()
    with transaction.atomic():
        cur.execute("DELETE FROM ftemp")
        for i in list(set(fitems)):
            if not (veg == 1 and i == 'Chicken Burger'): cur.execute("INSERT INTO ftemp (food) VALUES (%s)", [i])
            
    return render(request, 'userinputh.html', {'fl': list(set(fitems)), 'flag': 1})

from django.shortcuts import render
from django.http import HttpResponse
from MyApp.forms import BMRForm

def calculate_bmr(weight, height, age, gender, activity):
    if gender == 'Male':
        cal = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender == 'Female':
        cal = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        # A5 FIX: was UnboundLocalError if gender was anything other than Male/Female
        cal = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)  # default to Male

    activity_multiplier = {
        'Sedentary (little or no exercise)': 1.2,
        'Lightly active (1-3 days/week)': 1.375,
        'Moderately active (3-5 days/week)': 1.55,
        'Very active (6-7 days/week)': 1.725,
        'Super active (twice/day)': 1.9
    }

    cal *= activity_multiplier.get(activity, 1.2)
    return cal

def get_meal_plan(cal, has_diabetes=False, has_blood_pressure=False):
    protein = ['Yogurt(1 cup)', 'Cooked meat(3 Oz)', 'Cooked fish(4 Oz)', '1 whole egg + 4 egg whites', 'Tofu(5 Oz)']
    fruit = ['Berries(80 Oz)', 'Apple', 'Orange', 'Banana', 'Dried Fruits(Handful)', 'Fruit Juice(125ml)']
    vegetable = ['Any vegetable(80g)']
    grains = ['Cooked Grain(150g)', 'Whole Grain Bread(1 slice)', 'Half Large Potato(75g)', 'Oats(250g)', '2 corn tortillas']
    ps = ['Soy nuts(1 Oz)', 'Low fat milk(250ml)', 'Hummus(4 Tbsp)', 'Cottage cheese (125g)', 'Flavored yogurt(125g)']
    taste_en = ['2 TSP (10 ml) olive oil', '2 TBSP (30g) reduced-calorie salad dressing', '1/4 medium avocado', 'Small handful of nuts', '1/2 ounce grated Parmesan cheese', '1 TBSP (20g) jam, jelly, honey, syrup, sugar']

    # Adjustments for medical conditions
    if has_diabetes:
        fruit = ['Berries(80 Oz)', 'Apple', 'Orange']  # Lower sugar fruits
        taste_en = [t for t in taste_en if 'jam' not in t and 'sugar' not in t]  # Remove sugary items

    if has_blood_pressure:
        taste_en = [t for t in taste_en if 'cheese' not in t and 'salad dressing' not in t]  # Reduce salt content

    def rand(lst): return lst[random.randint(0, len(lst)-1)]

    if cal < 1500:
        meal_plan = {
            'Breakfast': f"{rand(protein)} + {rand(fruit)}",
            'Lunch': f"{rand(protein)} + {vegetable[0]} + Leafy Greens + {rand(grains)} + {rand(taste_en)}",
            'Snack': f"{rand(ps)} + {vegetable[0]}",
            'Dinner': f"{rand(protein)} + 2 {vegetable[0]} + Leafy Greens + {rand(grains)} + {rand(taste_en)}",
            'Night Snack': f"{rand(fruit)}"
        }
    elif cal < 1800:
        meal_plan = {
            'Breakfast': f"{rand(protein)} + {rand(fruit)}",
            'Lunch': f"{rand(protein)} + {vegetable[0]} + Leafy Greens + {rand(grains)} + {rand(taste_en)} + {rand(fruit)}",
            'Snack': f"{rand(ps)} + {vegetable[0]}",
            'Dinner': f"2 {rand(protein)} + {vegetable[0]} + Leafy Greens + {rand(grains)} + {rand(taste_en)}",
            'Night Snack': f"{rand(fruit)}"
        }
    elif cal < 2200:
        meal_plan = {
            'Breakfast': f"{rand(protein)} + {rand(fruit)}",
            'Lunch': f"{rand(protein)} + {vegetable[0]} + Leafy Greens + {rand(grains)} + {rand(taste_en)} + {rand(fruit)}",
            'Snack': f"{rand(ps)} + {vegetable[0]}",
            'Dinner': f"2 {rand(protein)} + 2 {vegetable[0]} + Leafy Greens + {rand(grains)} + {rand(taste_en)}",
            'Night Snack': f"{rand(fruit)}"
        }
    else:
        meal_plan = {
            'Breakfast': f"2 {rand(protein)} + {rand(fruit)} + {rand(grains)}",
            'Lunch': f"{rand(protein)} + {vegetable[0]} + Leafy Greens + {rand(grains)} + {rand(taste_en)} + {rand(fruit)}",
            'Snack': f"{rand(ps)} + {vegetable[0]}",
            'Dinner': f"2 {rand(protein)} + 2 {vegetable[0]} + Leafy Greens + 2 {rand(grains)} + 2 {rand(taste_en)}",
            'Night Snack': f"{rand(fruit)}"
        }

    return meal_plan

def bmr_view(request):
    if request.method == 'POST':
        form = BMRForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            activity = form.cleaned_data['activity']
            other_conditions = form.cleaned_data.get('other_conditions', '').lower()

            # Check for common medical keywords
            has_diabetes = 'diabetes' in other_conditions
            has_blood_pressure = 'pressure' in other_conditions or 'bp' in other_conditions

            bmr = calculate_bmr(weight, height, age, gender, activity)
            meal_plan = get_meal_plan(bmr, has_diabetes, has_blood_pressure)

            return render(request, 'bmr_result.html', {
                'bmr': round(bmr, 2),
                'meal_plan': meal_plan,
                'has_diabetes': has_diabetes,
                'has_blood_pressure': has_blood_pressure,
                'other_conditions': other_conditions
            })
    else:
        form = BMRForm()

    return render(request, 'bmr_form.html', {'form': form})

def get_chat_history_path(uid):
    from django.conf import settings
    import os
    chat_dir = os.path.join(settings.MEDIA_ROOT, 'chat_history')
    os.makedirs(chat_dir, exist_ok=True)
    return os.path.join(chat_dir, f'user_{uid}.json')

def load_chat_history(uid):
    path = get_chat_history_path(uid)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_chat_history(uid, history):
    path = get_chat_history_path(uid)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(history, f)

def delete_chat_history(uid):
    path = get_chat_history_path(uid)
    if os.path.exists(path):
        os.remove(path)

def recipe_response(request):
    if request.method == 'GET':
        user_message = request.GET.get('message', '')
        if not user_message:
            return JsonResponse({'response': 'Please provide a message.'})
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            generation_config = {
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }
            # B6 FIX: System prompt was injected as a fake 'user' message which confused the model.
            # Now correctly passed via system_instruction parameter at model creation.
            model = genai.GenerativeModel(
                model_name="gemini-2.0-flash",
                generation_config=generation_config,
                system_instruction=(
                    "You are a professional, certified dietician. Give evidence-based, friendly, and practical "
                    "nutrition and diet advice. Always be supportive, non-judgmental, and clear. "
                    "If you don't know something, say so honestly. "
                    "Never give medical advice beyond your scope. Answer the question asked only."
                ),
            )
            uid = request.session.get('UID', None)
            if not uid:
                return JsonResponse({'response': 'User not authenticated.'})
            chat_history = load_chat_history(uid)
            # B7 FIX: Chat history had no size cap — would eventually hit Gemini token limits
            MAX_TURNS = 20
            if len(chat_history) > MAX_TURNS * 2:
                chat_history = chat_history[-(MAX_TURNS * 2):]
            chat_history.append({"role": "user", "parts": [user_message]})
            response = model.generate_content(chat_history)
            chat_history.append({"role": "model", "parts": [response.text]})
            save_chat_history(uid, chat_history)
            return JsonResponse({'response': response.text})
        except Exception as e:
            return JsonResponse({'response': f'An error occurred: {str(e)}'})
    return JsonResponse({'response': 'Invalid request method.'})

@csrf_exempt
def clear_chat_history(request):
    if request.method == 'POST':
        uid = request.session.get('UID', None)
        if uid:
            delete_chat_history(uid)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

def aboutus(request):
    
    if request.method == 'GET':
        return render(request, 'aboutus.html')

# Payment view to display the payment form
def payment(request):
    db = connection.cursor()
    id = request.session.get('UID')  # Retrieve the UID from the session
    amt = request.GET.get('amt', '')  # Get the amount from the GET parameters (e.g., ?amt=100)

    # Render the payment.html template, passing the UID and amount
    return render(request, 'payment.html', {'UID': id, 'amt': amt})  # A1 FIX: was '250' which is invalid as a template variable

# Payment action view to process the form data after submission
from django.db import connection
from django.http import HttpResponse

from django.db import connection
from django.http import HttpResponse

from django.http import HttpResponse
from django.db import connection

def paymentaction(request):
    if request.method == 'POST':
        # Get data from the form
        amount = request.POST.get('amt', '')  # Amount entered in the form (can also be sent as hidden field)
        card_number = request.POST.get('cardnumber', '')  # Card number from the user
        cvv = request.POST.get('cvv', '')  # CVV entered by the user
        expiry_date = request.POST.get('expirydate', '')  # Expiry date
        cardholder_name = request.POST.get('cardholdername', '')  # Cardholder's name

        # FIX: Never log raw card data — PCI-DSS violation
        # Only log non-sensitive payment metadata
        print(f'Payment attempted — Amount: {amount}, User: {request.session.get("UID", "unknown")}')

        # Establishing a connection to the database
        with connection.cursor() as cursor:
            # Get the UID from the session
            user_id = request.session.get('UID')

            if user_id:
                # B8 FIX: Prevent double-payment — check if already paid before updating
                cursor.execute("SELECT status FROM login WHERE uid=%s", [user_id])
                current = cursor.fetchone()
                if current and current[0] == 'paid':
                    return HttpResponse("<script>alert('Your account is already activated. No charge was made.');window.location='/userhome/';</script>")

                # Update the 'login' table status to 'paid'
                sql_update_login = "UPDATE login SET status='paid' WHERE uid=%s"
                cursor.execute(sql_update_login, [user_id])
                print(f"User {user_id} status updated to 'paid'")

                # Update the 'user_details' table status to 'paid'
                sql_update_user_details = """
                    UPDATE registration
                    SET status='paid'
                    WHERE RID=%s
                """
                cursor.execute(sql_update_user_details, [user_id])
                print(f"User {user_id} status updated in 'user_details' table")
                request.session['status'] = 'paid'

        # Return a response (you can redirect to another page, show a success message, etc.)
        msg = "<script>alert('Successfully paid');window.location='/userhome/';</script>"
        return HttpResponse(msg)

@xframe_options_sameorigin
def chat(request):
    uid = request.session.get('UID', None)
    chat_history = []
    if uid:
        chat_history = load_chat_history(uid)
    return render(request, "chat.html", {"chat_history_json": json.dumps(chat_history)})

def bold_headings(text):
    # Convert markdown headings (## Heading, # Heading) to <b>Heading</b>
    def repl(match):
        return f"<b>{match.group(2).strip()}</b>"
    text = re.sub(r'^(#{1,6})\s*(.+)$', repl, text, flags=re.MULTILINE)
    # Replace **bold** with <b>bold</b>
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    return text

@csrf_exempt
def food_image_calorie(request):
    if request.method == 'POST' and request.FILES.get('food_image'):
        image_file = request.FILES['food_image']
        # B4 FIX: Validate file type before processing — any file extension was accepted before
        ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}
        mime_check, _ = mimetypes.guess_type(image_file.name)
        if not mime_check or mime_check not in ALLOWED_MIME_TYPES:
            return JsonResponse({'response': 'Please upload a valid image file (JPEG, PNG, WebP, or GIF).'})
        food_comment = request.POST.get('food_comment', '').strip()
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image_file.name)[1]) as tmp:
            for chunk in image_file.chunks():
                tmp.write(chunk)
            temp_path = tmp.name
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model = genai.GenerativeModel(
                model_name="gemini-2.0-flash",
                generation_config={
                    "temperature": 0.5,
                    "max_output_tokens": 1024,
                    "response_mime_type": "text/plain",
                }
            )
            prompt = (
                "You are a food recognition and calorie estimation expert. "
                "Given an image, identify the food item (if any) and estimate its calories. "
                "If the image is not a food item, reply: 'Please upload a food item image.'"
            )
            if food_comment:
                prompt += f"\nUser comment about the food: {food_comment}"
            with open(temp_path, "rb") as img:
                image_bytes = img.read()
            mime_type, _ = mimetypes.guess_type(image_file.name)
            if not mime_type:
                mime_type = "image/jpeg"

            def call_gemini():
                try:
                    response = model.generate_content([
                        {"role": "user", "parts": [prompt, {"mime_type": mime_type, "data": image_bytes}]}
                    ])
                    result_holder['result'] = response.text.strip()
                except Exception as e:
                    result_holder['error'] = str(e)

            result_holder = {'result': None, 'error': None}
            thread = threading.Thread(target=call_gemini)
            thread.start()
            thread.join(timeout=30)  # 30 seconds timeout
            if thread.is_alive():
                # A4 FIX: clean up temp file even on timeout — was leaking disk files
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                return JsonResponse({'response': 'The analysis is taking too long. Please try again with a different image.'})
            if result_holder['error']:
                logging.error(f"Gemini API error: {result_holder['error']}")
                return JsonResponse({'response': f"An error occurred while analyzing the image: {result_holder['error']}"})
            result = result_holder['result']
            result = bold_headings(result)
            os.remove(temp_path)
            return JsonResponse({'response': result})
        except Exception as e:
            logging.error(f"Unexpected error in food_image_calorie: {traceback.format_exc()}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return JsonResponse({'response': f"A server error occurred. Please try again later."})
    return JsonResponse({'response': 'No image uploaded or invalid request.'})

def addyoutube(request):
    if request.method == 'POST':
        urls = request.POST.getlist('youtube_url')
        with connection.cursor() as cursor:
            for url in urls:
                if url.strip():
                    cursor.execute("INSERT INTO youtube_videos (url) VALUES (%s)", [url.strip()])
        # Optionally, show a success message or redirect
        return render(request, 'addyoutube.html', {'success': True})
    return render(request, 'addyoutube.html')

def log_youtube_link(request):
    video_id = request.GET.get('video_id')
    if video_id:
        link = f"https://www.youtube.com/watch?v={video_id}"
        print(f"Loaded YouTube link: {link}")
        return JsonResponse({'status': 'ok'})
    else:
        print("No video_id provided to log_youtube_link")
        return JsonResponse({'status': 'error', 'message': 'No video_id provided'})


# A2 FIX: removed duplicate `import random` — already imported at top of file

# Edamam API Configuration
EDAMAM_APP_ID = os.getenv("EDAMAM_APP_ID")
EDAMAM_APP_KEY = os.getenv("EDAMAM_APP_KEY")
EDAMAM_API_URL = "https://api.edamam.com/api/recipes/v2"

# Define a user ID for the Edamam-Account-User header.
# IMPORTANT: For testing, a static string is fine. In a real application,
# this should be a unique identifier for the logged-in user to comply with Edamam's terms.
EDAMAM_USER_ID = "healthy-me-user-001"  # Changed to a more appropriate unique identifier

def calculate_tdee(height_cm, weight_kg, age_years, gender, activity_level):
    """
    Calculates Total Daily Energy Expenditure (TDEE) using Mifflin-St Jeor equation.
    Activity factors are based on common recommendations.
    """
    # Step 1: Calculate Basal Metabolic Rate (BMR)
    if gender == 'male':
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age_years) + 5
    elif gender == 'female':
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age_years) - 161
    else:
        # Fallback for unexpected gender input, defaults to male BMR
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age_years) + 5
    
    # Step 2: Apply Activity Factor to BMR to get TDEE
    # These factors are standard for TDEE calculation
    activity_factors = {
        'sedentary': 1.2,                # Little or no exercise
        'lightly_active': 1.375,         # Light exercise/sports 1-3 days/week
        'moderately_active': 1.55,       # Moderate exercise/sports 3-5 days/week
        'very_active': 1.725,            # Hard exercise/sports 6-7 days a week
        'extra_active': 1.9              # Very hard exercise/physical job
    }
    
    # Get the activity factor based on user selection, default to moderately active if not found
    activity_factor = activity_factors.get(activity_level, 1.55) 
    
    tdee = bmr * activity_factor
    return tdee

def meal_planner_form(request):
    """
    Renders the initial meal planner input form.
    """
    return render(request, 'meal_planner.html')

def plan_meal(request):
    """
    Handles the meal planning request, calculates TDEE,
    calls the Edamam API multiple times for a 7-day, 3-meal-per-day plan,
    and renders the results on 'mealplanner_output.html'.
    """
    # B5 FIX: No login check existed — anyone could trigger 21 expensive API calls
    if 'UID' not in request.session:
        return render(request, 'meal_planner.html', {'error': 'Please login to use the meal planner.'})
        
    if request.method == 'POST':
        # Basic check for API credentials
        if not EDAMAM_APP_ID or not EDAMAM_APP_KEY:
            # Provide a sample meal plan for demonstration purposes
            sample_meal_plan = {
                'Day 1': {
                    'Breakfast': {
                        'label': 'Sample Breakfast - Oatmeal with Berries',
                        'url': '#',
                        'image': 'https://placehold.co/250x250/E2E8F0/475569?text=Sample+Breakfast',
                        'calories': 350,
                        'ingredientLines': ['1 cup rolled oats', '1/2 cup mixed berries', '1 tbsp honey', '1/4 cup almond milk']
                    },
                    'Lunch': {
                        'label': 'Sample Lunch - Grilled Chicken Salad',
                        'url': '#',
                        'image': 'https://placehold.co/250x250/E2E8F0/475569?text=Sample+Lunch',
                        'calories': 450,
                        'ingredientLines': ['4 oz grilled chicken breast', '2 cups mixed greens', '1/4 cup cherry tomatoes', '1 tbsp olive oil']
                    },
                    'Dinner': {
                        'label': 'Sample Dinner - Salmon with Vegetables',
                        'url': '#',
                        'image': 'https://placehold.co/250x250/E2E8F0/475569?text=Sample+Dinner',
                        'calories': 550,
                        'ingredientLines': ['6 oz salmon fillet', '1 cup steamed broccoli', '1/2 cup quinoa', '1 tbsp lemon juice']
                    }
                }
            }
            
            # Generate sample data for 7 days
            seven_day_meal_plan = {}
            for day_num in range(1, 8):
                day_key = f'Day {day_num}'
                seven_day_meal_plan[day_key] = sample_meal_plan['Day 1'].copy()
            
            context = {
                'seven_day_meal_plan': seven_day_meal_plan,
                'user_details': {
                    'height': request.POST.get('height', 'N/A'),
                    'weight': request.POST.get('weight', 'N/A'),
                    'age': request.POST.get('age', 'N/A'),
                    'gender': request.POST.get('gender', 'N/A'),
                    'activity_level': request.POST.get('activity_level', 'N/A'),
                    'medical_conditions': request.POST.get('medical_conditions', 'N/A'),
                    'tdee': 2000
                }
            }
            return render(request, 'mealplanner_output.html', context)

        # Retrieve user details for TDEE calculation
        try:
            height = float(request.POST.get('height'))
            weight = float(request.POST.get('weight'))
            age = int(request.POST.get('age'))
            gender = request.POST.get('gender')
            activity_level = request.POST.get('activity_level')
        except (ValueError, TypeError):
            # Handle cases where height, weight, age are not valid numbers
            return render(request, 'meal_planner.html', {'error': 'Please provide valid numeric values for height, weight, and age.'})

        # Bounds validation — FIX: was no validation, also template name ERROR.HTML would 404
        if not (50 <= height <= 280):
            return render(request, 'meal_planner.html', {'error': 'Please enter a valid height between 50 and 280 cm.'})
        if not (10 <= weight <= 500):
            return render(request, 'meal_planner.html', {'error': 'Please enter a valid weight between 10 and 500 kg.'})
        if not (10 <= age <= 120):
            return render(request, 'meal_planner.html', {'error': 'Please enter a valid age between 10 and 120 years.'})


        # Retrieve optional filter parameters
        medical_conditions = request.POST.get('medical_conditions')
        diet = request.POST.get('diet')
        health = request.POST.get('health')
        cuisineType = request.POST.get('cuisineType')
        time = request.POST.get('time')
        calories_input = request.POST.get('calories') # User's optional target daily calories
        excluded = request.POST.get('excluded')

        # Determine daily calorie target
        daily_target_calories = None
        if calories_input:
            try:
                # Handle calorie ranges (e.g., "1800-2200") or single values (e.g., "2000" or "2000+")
                if '-' in calories_input:
                    min_cal, max_cal = map(int, calories_input.split('-'))
                    daily_target_calories = (min_cal + max_cal) / 2
                elif '+' in calories_input:
                    daily_target_calories = int(calories_input.replace('+', '')) + 200 # Arbitrary buffer for '+'
                else:
                    daily_target_calories = int(calories_input)
            except ValueError:
                # If user input for calories is invalid, fallback to calculated TDEE
                daily_target_calories = calculate_tdee(height, weight, age, gender, activity_level)
        else:
            # If user didn't provide target calories, calculate TDEE
            daily_target_calories = calculate_tdee(height, weight, age, gender, activity_level)

        # Ensure daily_target_calories is a reasonable positive number
        if daily_target_calories is None or daily_target_calories <= 0:
            daily_target_calories = 2000 # Default to a reasonable value if calculation fails or is zero/negative


        # Calorie distribution per meal (% of TDEE)
        breakfast_cal_range = (max(daily_target_calories * 0.20, 100), max(daily_target_calories * 0.30, 200))
        lunch_cal_range = (max(daily_target_calories * 0.30, 200), max(daily_target_calories * 0.40, 300))
        dinner_cal_range = (max(daily_target_calories * 0.35, 250), max(daily_target_calories * 0.45, 400))
        calorie_ranges_per_meal = {
            'Breakfast': breakfast_cal_range,
            'Lunch': lunch_cal_range,
            'Dinner': dinner_cal_range,
        }

        # Curated fallback keywords per meal type — FIX: was generic 'food' query which returned random results
        FALLBACK_KEYWORDS = {
            'Breakfast': ['oatmeal', 'scrambled eggs', 'yogurt parfait', 'smoothie bowl', 'avocado toast'],
            'Lunch':     ['grilled chicken salad', 'vegetable soup', 'grain bowl', 'turkey wrap', 'lentil soup'],
            'Dinner':    ['baked salmon', 'chicken stir fry', 'pasta primavera', 'beef curry', 'roasted vegetables'],
        }

        # FIX: Per-user Edamam header \u2014 was a single static string for all users
        headers = {
            "Edamam-Account-User": f"healthyme-user-{request.session.get('UID', 'anonymous')}"
        }

        # Pre-initialize the plan structure
        seven_day_meal_plan = {f'Day {d}': {} for d in range(1, 8)}
        used_recipe_uris = set()
        meal_types_edamam = ['Breakfast', 'Lunch', 'Dinner']

        def fetch_single_meal(day_num, meal_type_name, base_params):
            """
            FIX: Fetch one meal from Edamam in its own thread.
            Replaces the inner strategy loop \u2014 now runs concurrently for all 21 slots.
            """
            meal_min_cal, meal_max_cal = calorie_ranges_per_meal[meal_type_name]
            min_cal = max(int(meal_min_cal * random.uniform(0.9, 1.1)), 50)
            max_cal = max(int(meal_max_cal * random.uniform(0.9, 1.1)), min_cal + 100)

            search_strategies = [
                # Strategy 1: Specific (includes mealType, calorie range, user filters)
                {**base_params, 'calories': f"{min_cal}-{max_cal}", 'mealType': meal_type_name},
                # Strategy 2: Broader calorie range, no mealType filter
                {
                    'type': 'public', 'app_id': EDAMAM_APP_ID, 'app_key': EDAMAM_APP_KEY,
                    'q': meal_type_name.lower(),
                    'calories': f"{max(50, min_cal - 150)}-{max_cal + 300}"
                },
                # Strategy 3: Curated keyword fallback \u2014 FIX: was 'food' which returned random items
                {
                    'type': 'public', 'app_id': EDAMAM_APP_ID, 'app_key': EDAMAM_APP_KEY,
                    'q': random.choice(FALLBACK_KEYWORDS[meal_type_name]),
                    'calories': '100-800'
                },
            ]

            for strategy_index, strategy_params in enumerate(search_strategies):
                try:
                    response = requests.get(EDAMAM_API_URL, params=strategy_params, headers=headers, timeout=8)
                    response.raise_for_status()
                    data = response.json()
                    if data.get('hits'):
                        for hit in data['hits'][:10]:
                            recipe = hit['recipe']
                            if recipe['uri'] not in used_recipe_uris:
                                if recipe.get('yield', 1) > 0:
                                    recipe['calories_per_serving'] = round(recipe['calories'] / recipe['yield'], 0)
                                else:
                                    recipe['calories_per_serving'] = recipe['calories']
                                return (day_num, meal_type_name, recipe)
                        # All were used \u2014 fall back
                        recipe = data['hits'][0]['recipe']
                        if recipe.get('yield', 1) > 0:
                            recipe['calories_per_serving'] = round(recipe['calories'] / recipe['yield'], 0)
                        else:
                            recipe['calories_per_serving'] = recipe['calories']
                        return (day_num, meal_type_name, recipe)
                except requests.exceptions.HTTPError as http_err:
                    # FIX: was silent continue \u2014 now logged
                    logger.warning(f"Edamam HTTP error (strategy {strategy_index+1}) Day {day_num} {meal_type_name}: {http_err.response.status_code if http_err.response else 'N/A'}")
                    continue
                except requests.exceptions.RequestException as req_err:
                    logger.warning(f"Edamam request error (strategy {strategy_index+1}) Day {day_num} {meal_type_name}: {req_err}")
                    continue
                except Exception as e:
                    logger.error(f"Unexpected Edamam error (strategy {strategy_index+1}) Day {day_num} {meal_type_name}: {e}")
                    continue

            # All strategies exhausted
            return (day_num, meal_type_name, None)

        # Build base params with user filters
        base_params = {
            'type': 'public',
            'app_id': EDAMAM_APP_ID,
            'app_key': EDAMAM_APP_KEY,
            'q': 'healthy',
        }
        if diet and diet != "Any":
            base_params['diet'] = diet.lower()
        if health:
            base_params['health'] = health.lower()
        if cuisineType:
            base_params['cuisineType'] = cuisineType.title()
        if time:
            base_params['time'] = f"1-{time}" if time.isdigit() else time
        if excluded:
            base_params['excluded'] = excluded.split(',')

        # FIX: Run all 21 API calls concurrently instead of sequentially
        # Worst-case: 8s per call sequentially = 168s. Concurrently = ~8s total.
        with ThreadPoolExecutor(max_workers=9) as executor:
            futures = {
                executor.submit(fetch_single_meal, day_num, meal_type_name, base_params.copy()): (day_num, meal_type_name)
                for day_num in range(1, 8)
                for meal_type_name in meal_types_edamam
            }
            for future in as_completed(futures):
                try:
                    day_num, meal_type_name, recipe = future.result()
                    day_key = f'Day {day_num}'
                    if recipe:
                        seven_day_meal_plan[day_key][meal_type_name] = recipe
                        used_recipe_uris.add(recipe['uri'])
                    else:
                        seven_day_meal_plan[day_key][meal_type_name] = {
                            'label': 'No recipe found for these criteria.',
                            'url': '#',
                            'image': 'https://placehold.co/250x250/E2E8F0/475569?text=No+Image',

                        'calories': 0,
                        'ingredientLines': ['Adjust filters for more results or try a different day/meal.']
                    }
                except Exception as e:
                    logger.error(f"Error processing Edamam future result: {e}")

        # Prepare context to pass to the template
        # Save the meal plan to a JSON file - overwrite existing plan
        user_id = request.session.get('UID')
        if user_id:
            try:
                meal_plan_dir = os.path.join(settings.MEDIA_ROOT, 'meal_plans')
                os.makedirs(meal_plan_dir, exist_ok=True)
                
                # Remove any existing meal plan files for this user
                import glob
                existing_files = glob.glob(os.path.join(meal_plan_dir, f'user_{user_id}_meal_plan*.json'))
                for existing_file in existing_files:
                    try:
                        os.remove(existing_file)
                        logger.debug(f"DEBUG: Removed existing meal plan file: {existing_file}")
                    except Exception as e:
                        logger.debug(f"DEBUG: Failed to remove existing file {existing_file}: {e}")
                        # Continue even if removal fails
                
                # Save the new meal plan with timestamp
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_path = os.path.join(meal_plan_dir, f'user_{user_id}_meal_plan.json')
                
                # Calculate total meals correctly
                total_meals = 0
                for day_meals in seven_day_meal_plan.values():
                    total_meals += len(day_meals)
                
                # Add metadata to the meal plan
                meal_plan_with_metadata = {
                    'metadata': {
                        'user_id': str(user_id),
                        'generated_at': datetime.now().isoformat(),
                        'version': '1.0',
                        'total_meals': total_meals,
                        'days': len(seven_day_meal_plan),
                        'meals_per_day': 3
                    },
                    'user_details': {
                        'height': height,
                        'weight': weight,
                        'age': age,
                        'gender': gender,
                        'activity_level': activity_level,
                        'medical_conditions': medical_conditions,
                        'tdee': round(daily_target_calories, 2)
                    },
                    'meal_plan': seven_day_meal_plan,
                    'progress_tracking': {
                        'total_meals': total_meals,
                        'eaten_meals': 0,
                        'eaten_items': {},
                        'last_updated': datetime.now().isoformat()
                    }
                }
                
                with open(file_path, 'w') as f:
                    json.dump(meal_plan_with_metadata, f, indent=4)
                logger.debug(f"DEBUG: Successfully saved new meal plan to: {file_path}")
            except Exception as e:
                logger.debug(f"DEBUG: Failed to save meal plan: {e}")
                # Continue without saving if there's an error

        context = {
            'seven_day_meal_plan': seven_day_meal_plan,
            'user_details': {
                'height': height,
                'weight': weight,
                'age': age,
                'gender': gender,
                'activity_level': activity_level,
                'medical_conditions': medical_conditions,
                'tdee': round(daily_target_calories, 2) # Pass the calculated TDEE
            }
        }
        return render(request, 'mealplanner_output.html', context)
    else:
        # If the request method is not POST, redirect to the form or show an error
        return HttpResponse("This endpoint only accepts POST requests.", status=405)

def view_saved_meal_plan(request):
    user_id = request.session.get('UID')
    if not user_id:
        return render(request, 'view_meal_plan.html', {'seven_day_meal_plan': None})

    meal_plan_dir = os.path.join(settings.MEDIA_ROOT, 'meal_plans')
    
    # Look for the latest meal plan file for this user
    import glob
    try:
        meal_plan_files = glob.glob(os.path.join(meal_plan_dir, f'user_{user_id}_meal_plan*.json'))
        
        if meal_plan_files:
            # Sort files by modification time (newest first) and get the latest
            latest_file = max(meal_plan_files, key=os.path.getmtime)
            try:
                with open(latest_file, 'r') as f:
                    meal_plan_data = json.load(f)
                
                # Handle both old and new format
                if isinstance(meal_plan_data, dict) and 'meal_plan' in meal_plan_data:
                    # New format with metadata
                    meal_plan = meal_plan_data['meal_plan']
                    user_details = meal_plan_data.get('user_details', {})
                    metadata = meal_plan_data.get('metadata', {})
                    
                    # Calculate total meals correctly
                    total_meals = 0
                    for day_meals in meal_plan.values():
                        total_meals += len(day_meals)
                    
                    progress_tracking = meal_plan_data.get('progress_tracking', {
                        'total_meals': total_meals,
                        'eaten_meals': 0,
                        'eaten_items': {},
                        'last_updated': datetime.now().isoformat()
                    })
                    
                    # Fix total_meals if it's 0 or incorrect
                    if progress_tracking.get('total_meals', 0) == 0:
                        progress_tracking['total_meals'] = total_meals
                else:
                    # Old format - direct meal plan
                    meal_plan = meal_plan_data
                    user_details = {}
                    metadata = {}
                    
                    # Calculate total meals correctly
                    total_meals = 0
                    for day_meals in meal_plan.values():
                        total_meals += len(day_meals)
                    
                    progress_tracking = {
                        'total_meals': total_meals,
                        'eaten_meals': 0,
                        'eaten_items': {},
                        'last_updated': datetime.now().isoformat()
                    }
                
                logger.debug(f"DEBUG: Loaded meal plan from: {latest_file}")
                return render(request, 'view_meal_plan.html', {
                    'seven_day_meal_plan': meal_plan,
                    'user_details': user_details,
                    'metadata': metadata,
                    'progress_tracking': progress_tracking
                })
            except (json.JSONDecodeError, IOError) as e:
                logger.debug(f"DEBUG: Error reading meal plan file {latest_file}: {e}")
                return render(request, 'view_meal_plan.html', {'seven_day_meal_plan': None})
        else:
            logger.debug(f"DEBUG: No meal plan files found for user {user_id}")
            return render(request, 'view_meal_plan.html', {'seven_day_meal_plan': None})
    except Exception as e:
        logger.debug(f"DEBUG: Error in view_saved_meal_plan: {e}")
        return render(request, 'view_meal_plan.html', {'seven_day_meal_plan': None})

@csrf_exempt
def update_meal_progress(request):
    """Update progress tracking for meal plan items"""
    if request.method == 'POST':
        user_id = request.session.get('UID')
        if not user_id:
            return JsonResponse({'success': False, 'error': 'User not logged in'})
        
        try:
            data = json.loads(request.body)
            day = data.get('day')
            meal_type = data.get('meal_type')
            recipe_label = data.get('recipe_label')
            is_eaten = data.get('is_eaten', False)
            
            if not all([day, meal_type, recipe_label]):
                return JsonResponse({'success': False, 'error': 'Missing required parameters'})
            
            # Load the current meal plan
            meal_plan_dir = os.path.join(settings.MEDIA_ROOT, 'meal_plans')
            meal_plan_files = glob.glob(os.path.join(meal_plan_dir, f'user_{user_id}_meal_plan*.json'))
            
            if not meal_plan_files:
                return JsonResponse({'success': False, 'error': 'No meal plan found'})
            
            latest_file = max(meal_plan_files, key=os.path.getmtime)
            
            with open(latest_file, 'r') as f:
                meal_plan_data = json.load(f)
            
            # Initialize progress tracking if it doesn't exist
            if 'progress_tracking' not in meal_plan_data:
                # Calculate total meals correctly
                total_meals = 0
                for day_meals in meal_plan_data.get('meal_plan', {}).values():
                    total_meals += len(day_meals)
                
                meal_plan_data['progress_tracking'] = {
                    'total_meals': total_meals,
                    'eaten_meals': 0,
                    'eaten_items': {},
                    'last_updated': datetime.now().isoformat()
                }
            else:
                # Fix total_meals if it's 0 or incorrect
                if meal_plan_data['progress_tracking'].get('total_meals', 0) == 0:
                    total_meals = 0
                    for day_meals in meal_plan_data.get('meal_plan', {}).values():
                        total_meals += len(day_meals)
                    meal_plan_data['progress_tracking']['total_meals'] = total_meals
            
            # Create unique key for this meal
            meal_key = f"{day}_{meal_type}_{recipe_label}"
            
            # Update progress tracking
            if is_eaten:
                if meal_key not in meal_plan_data['progress_tracking']['eaten_items']:
                    meal_plan_data['progress_tracking']['eaten_items'][meal_key] = True
                    meal_plan_data['progress_tracking']['eaten_meals'] += 1
            else:
                if meal_key in meal_plan_data['progress_tracking']['eaten_items']:
                    del meal_plan_data['progress_tracking']['eaten_items'][meal_key]
                    meal_plan_data['progress_tracking']['eaten_meals'] -= 1
            
            meal_plan_data['progress_tracking']['last_updated'] = datetime.now().isoformat()
            
            # Save updated meal plan
            with open(latest_file, 'w') as f:
                json.dump(meal_plan_data, f, indent=4)
            
            # Calculate progress percentage
            total_meals = meal_plan_data['progress_tracking']['total_meals']
            eaten_meals = meal_plan_data['progress_tracking']['eaten_meals']
            progress_percentage = (eaten_meals / total_meals * 100) if total_meals > 0 else 0
            
            return JsonResponse({
                'success': True,
                'progress_percentage': round(progress_percentage, 1),
                'eaten_meals': eaten_meals,
                'total_meals': total_meals,
                'is_eaten': is_eaten
            })
            
        except Exception as e:
            logger.debug(f"DEBUG: Error updating meal progress: {e}")
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def fpass(request):
    """Direct password reset view"""
    if request.method == "POST":
        email = request.POST.get("email")
        new_password = request.POST.get("password")
        
        from django.contrib.auth.hashers import make_password
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE login SET upass = %s WHERE uname = %s",
                    [make_password(new_password), email]
                )
            return render(request, "login.html", {"success": "Password reset successfully!"})
        except Exception as e:
            return render(request, "fpass.html", {"error": "Failed to reset password."})
    return render(request, "fpass.html")

def test_email_config(request):
    """Test email configuration - for debugging only"""
    try:
        print("DEBUG: Testing email configuration...")
        logger.debug(f"DEBUG: EMAIL_HOST_USER = {settings.EMAIL_HOST_USER}")
        logger.debug(f"DEBUG: EMAIL_HOST_PASSWORD = {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
        logger.debug(f"DEBUG: EMAIL_HOST = {settings.EMAIL_HOST}")
        logger.debug(f"DEBUG: EMAIL_PORT = {settings.EMAIL_PORT}")
        logger.debug(f"DEBUG: EMAIL_USE_TLS = {settings.EMAIL_USE_TLS}")
        logger.debug(f"DEBUG: FROM_EMAIL = {FROM_EMAIL}")
        
        send_mail(
            subject="Test Email - HealthyMe",
            message="This is a test email to verify email configuration is working.",
            from_email=FROM_EMAIL,
            recipient_list=[FROM_EMAIL],  # Send to yourself
            fail_silently=False,
        )
        return HttpResponse("Test email sent successfully! Check your inbox.")
    except Exception as e:
        return HttpResponse(f"Email test failed: {str(e)}")

def test_google_oauth_config(request):
    """Test Google OAuth configuration - for debugging only"""
    try:
        print("DEBUG: Testing Google OAuth configuration...")
        logger.debug(f"DEBUG: GOOGLE_OAUTH_CLIENT_ID = '{settings.GOOGLE_OAUTH_CLIENT_ID}'")
        logger.debug(f"DEBUG: GOOGLE_OAUTH_CLIENT_SECRET = '{settings.GOOGLE_OAUTH_CLIENT_SECRET}'")
        logger.debug(f"DEBUG: GOOGLE_OAUTH_REDIRECT_URI = '{settings.GOOGLE_OAUTH_REDIRECT_URI}'")
        
        # Check if values are set
        client_id_set = bool(settings.GOOGLE_OAUTH_CLIENT_ID and settings.GOOGLE_OAUTH_CLIENT_ID != '')
        client_secret_set = bool(settings.GOOGLE_OAUTH_CLIENT_SECRET and settings.GOOGLE_OAUTH_CLIENT_SECRET != '')
        
        response_text = f"""
        <h2>Google OAuth Configuration Test</h2>
        <p><strong>GOOGLE_OAUTH_CLIENT_ID:</strong> {'✅ SET' if client_id_set else '❌ NOT SET'}</p>
        <p><strong>GOOGLE_OAUTH_CLIENT_SECRET:</strong> {'✅ SET' if client_secret_set else '❌ NOT SET'}</p>
        <p><strong>GOOGLE_OAUTH_REDIRECT_URI:</strong> {settings.GOOGLE_OAUTH_REDIRECT_URI}</p>
        
        <h3>Environment Variables:</h3>
        <p>Make sure you have a <code>.env</code> file in your project root with:</p>
        <pre>
GOOGLE_OAUTH_CLIENT_ID=your-actual-client-id-here
GOOGLE_OAUTH_CLIENT_SECRET=your-actual-client-secret-here
        </pre>
        
        <h3>Next Steps:</h3>
        <ol>
            <li>Create a <code>.env</code> file in your project root (C:\\Diet-HealthyMe\\.env)</li>
            <li>Add your Google OAuth credentials to the .env file</li>
            <li>Restart your Django server</li>
            <li>Test again</li>
        </ol>
        """
        
        return HttpResponse(response_text)
    except Exception as e:
        return HttpResponse(f"Google OAuth test failed: {str(e)}")

# Google OAuth Login Views
def google_login(request):
    """Initiate Google OAuth login"""
    try:
        # Debug: Print the client_id to see what's being loaded
        logger.debug(f"DEBUG: GOOGLE_OAUTH_CLIENT_ID = '{settings.GOOGLE_OAUTH_CLIENT_ID}'")
        logger.debug(f"DEBUG: GOOGLE_OAUTH_CLIENT_SECRET = '{settings.GOOGLE_OAUTH_CLIENT_SECRET}'")
        logger.debug(f"DEBUG: GOOGLE_OAUTH_REDIRECT_URI = '{settings.GOOGLE_OAUTH_REDIRECT_URI}'")
        
        # Check if client_id is empty
        if not settings.GOOGLE_OAUTH_CLIENT_ID or settings.GOOGLE_OAUTH_CLIENT_ID == '':
            return render(request, "login.html", {"error": "Google OAuth is not configured. Please set GOOGLE_OAUTH_CLIENT_ID in your .env file."})
        
        # Check if client_secret is empty
        if not settings.GOOGLE_OAUTH_CLIENT_SECRET or settings.GOOGLE_OAUTH_CLIENT_SECRET == '':
            return render(request, "login.html", {"error": "Google OAuth is not configured. Please set GOOGLE_OAUTH_CLIENT_SECRET in your .env file."})
        
        # Create OAuth flow with proper configuration
        client_config = {
            "web": {
                "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
                "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.GOOGLE_OAUTH_REDIRECT_URI]
            }
        }
        
        logger.debug(f"DEBUG: Client config = {client_config}")
        
        flow = Flow.from_client_config(
            client_config,
            scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
        )
        
        flow.redirect_uri = settings.GOOGLE_OAUTH_REDIRECT_URI
        
        # Generate authorization URL with proper parameters
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        # Debug: Print the exact authorization URL
        logger.debug(f"DEBUG: Authorization URL = {authorization_url}")
        logger.debug(f"DEBUG: Redirect URI being sent = {settings.GOOGLE_OAUTH_REDIRECT_URI}")
        logger.debug(f"DEBUG: State = {state}")
        
        # Store state in session for security (but don't force save to avoid creating new session)
        request.session['google_oauth_state'] = state
        # Don't call request.session.save() here to avoid creating a new session
        
        logger.debug(f"DEBUG: Stored state in session: {state}")
        logger.debug(f"DEBUG: Session key: {request.session.session_key}")
        
        return HttpResponseRedirect(authorization_url)
        
    except Exception as e:
        print(f"Google OAuth error: {str(e)}")
        import traceback
        traceback.print_exc()
        return render(request, "login.html", {"error": f"Google login error: {str(e)}. Please try again or use email/password login."})

def google_login_callback(request):
    """Handle Google OAuth callback"""
    try:
        # Debug session at start
        logger.debug(f"DEBUG: Google callback - Initial session key: {request.session.session_key}")
        logger.debug(f"DEBUG: Google callback - Initial session data: {dict(request.session)}")
        
        # Debug session at start
        logger.debug(f"DEBUG: Session key: {request.session.session_key}")
        logger.debug(f"DEBUG: Session data: {dict(request.session)}")
        
        # Get authorization code from callback
        code = request.GET.get('code')
        state = request.GET.get('state')
        error = request.GET.get('error')
        
        logger.debug(f"DEBUG: Callback received - code: {code}, state: {state}, error: {error}")
        
        # Check for OAuth errors
        if error:
            logger.debug(f"DEBUG: OAuth error received: {error}")
            return render(request, "login.html", {"error": f"Google OAuth error: {error}. Please try again."})
        
        # Check if code is present
        if not code:
            print("DEBUG: No authorization code received")
            return render(request, "login.html", {"error": "No authorization code received from Google. Please try again."})
        
        # Verify state for security
        stored_state = request.session.get('google_oauth_state')
        logger.debug(f"DEBUG: State verification - received: {state}, stored: {stored_state}")
        logger.debug(f"DEBUG: Session key: {request.session.session_key}")
        logger.debug(f"DEBUG: All session data: {dict(request.session)}")
        
        if state != stored_state:
            logger.debug(f"DEBUG: State mismatch - received: {state}, expected: {stored_state}")
            # FIX: Re-enabled OAuth state verification — was bypassed for testing, now properly enforced
            return render(request, "login.html", {"error": "Security check failed. Please try Google login again."})
        
        # Create OAuth flow
        client_config = {
            "web": {
                "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
                "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.GOOGLE_OAUTH_REDIRECT_URI]
            }
        }
        
        logger.debug(f"DEBUG: Creating flow with config: {client_config}")
        
        flow = Flow.from_client_config(
            client_config,
            scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
        )
        
        flow.redirect_uri = settings.GOOGLE_OAUTH_REDIRECT_URI
        
        # Exchange code for tokens
        logger.debug(f"DEBUG: Fetching token with code: {code}")
        flow.fetch_token(code=code)
        
        # Get user info from Google
        credentials = flow.credentials
        logger.debug(f"DEBUG: Got credentials, verifying token...")
        id_info = id_token.verify_oauth2_token(
            credentials.id_token, 
            google_requests.Request(), 
            settings.GOOGLE_OAUTH_CLIENT_ID
        )
        
        # Extract user information
        google_email = id_info['email']
        google_name = id_info.get('name', '')
        google_picture = id_info.get('picture', '')
        
        logger.debug(f"DEBUG: Google user info - email: {google_email}, name: {google_name}")
        
        # Check if user exists in database
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM login WHERE uname = %s", [google_email])
            existing_user = cursor.fetchone()
            
        logger.debug(f"DEBUG: Database check - existing_user: {existing_user}")
        
        if existing_user:
            # User exists, log them in and redirect to user home
            # Set user login data (same as searchlogin function)
            request.session['UID'] = existing_user[0]
            request.session['UNAME'] = existing_user[1]
            # A6 FIX: UPASSWORD must never be stored in session — removed
            request.session['UTYPE'] = existing_user[3]
            request.session['status'] = existing_user[4] if len(existing_user) > 4 else None
            
            # Let Django handle session management automatically (same as searchlogin function)
            logger.debug(f"DEBUG: Session set for existing user - UID: {existing_user[0]}, UNAME: {existing_user[1]}, UTYPE: {existing_user[3]}")
            logger.debug(f"DEBUG: Session key: {request.session.session_key}")
            logger.debug(f"DEBUG: All session data: {dict(request.session)}")
            
            # Use the same pattern as searchlogin function - let Django handle sessions automatically
            if request.session['UTYPE'] == 'admin':
                return redirect('/adminhome/')
            elif request.session['UTYPE'] == 'user':
                if request.session.get('status') == 'paid':
                    return redirect('/userhome/')
                else:
                    msg = "<script>alert('Payment is pending'); window.location='/home/';</script>"
                    return HttpResponse(msg)
            elif request.session['UTYPE'] == 'dietician':
                return redirect('/dieticianhome/')
            else:
                return redirect('/userhome/')
        else:
            # User doesn't exist, redirect to registration page with email pre-filled
            logger.debug(f"DEBUG: User doesn't exist, redirecting to registration")
            
            # Store Google info in session for registration
            request.session['google_email'] = google_email
            request.session['google_name'] = google_name
            
            logger.debug(f"DEBUG: Stored Google info in session - email: {google_email}, name: {google_name}")
            
            # Redirect to registration page with a message
            try:
                return render(request, "registration.html", {
                    "google_email": google_email,
                    "google_name": google_name,
                    "message": "Please complete your registration. Your email has been pre-filled from Google."
                })
            except Exception as e:
                logger.debug(f"DEBUG: Error rendering registration template: {str(e)}")
                import traceback
                traceback.print_exc()
                # Fallback to simple redirect
                return HttpResponseRedirect('/reg/')
        
    except Exception as e:
        print(f"Google OAuth callback error: {str(e)}")
        import traceback
        traceback.print_exc()
        return render(request, "login.html", {"error": f"Google login failed: {str(e)}. Please try again or use email/password login."})

def test_session(request):
	"""Simple endpoint to test session continuity"""
	logger.debug(f"DEBUG: test_session - Session key: {request.session.session_key}")
	logger.debug(f"DEBUG: test_session - All session data: {dict(request.session)}")
	logger.debug(f"DEBUG: test_session - UID in session: {'UID' in request.session}")
	logger.debug(f"DEBUG: test_session - Request cookies: {dict(request.COOKIES)}")
	
	if 'UID' in request.session:
		return HttpResponse(f"Session working! UID: {request.session['UID']}, Session Key: {request.session.session_key}")
	else:
		return HttpResponse("No session found!")
