from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
import requests
from django.contrib.auth import authenticate, login, logout
import sys
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from requests.auth import HTTPBasicAuth
import json
import hashlib
from requests.structures import CaseInsensitiveDict
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
import pandas as pd 
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from cowin_status_app import settings
from io import StringIO
import csv
from django.contrib import messages
from frontend.models import User
from frontend import models
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import mimetypes
import os
from frontend.decorators import unauthenticated_user,type_user
from datetime import datetime,date,time
from dateutil import tz
from django.http import FileResponse
import io,csv
from frontend.forms import UserForm
from django.contrib.auth.models import Group
from .task import send_mail_func
import pytz



def test(request):
    email = 'shindesushant818@gmail.com'
    message = 'Hi this'
    send_mail_func(email,message)
    return HttpResponse('DONE')



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
# Create your views here.





@unauthenticated_user
def user_login(request):
    try:
        if request.method == "POST":
            # print(request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    print(request.POST.get('chek'))
                    if request.POST.get('chek'):
                        print('working')
                        response = HttpResponseRedirect(reverse('dashboard'))
                        # response = HttpResponse('working')
                        response.set_cookie('username',request.POST.get('username'),max_age=1209600)
                        response.set_cookie('password',request.POST.get('password'),max_age=1209600)
                        # print(response)
                        return response
                    group = request.user.groups.get().name
                    print(group)
                    if group != 'employee':
                        return redirect('dashboard')
                    else:
                        return redirect('user_profile')
                else:
                    return HttpResponse('You account was inactive')
            else:
                print("someone tried to login and failed")
                print("They used username:{} and {}".format(username,password))
                messages.error(request,"Invalid login details given")
                # return HttpResponse("Invalid login details given")
                return redirect('/')
        else:
            if request.COOKIES.get('username'):
                print('working')
                print(request.COOKIES['username'])
                return render(request, 'login.html', {'username':request.COOKIES['username'],'password':request.COOKIES['password']})
            else:
                print('not working')
                return render(request,'login.html')
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)



# @login_required
# def dashboard(request):
#     try:
#         if request.method == "POST":
#             print(request.POST)
#             print(request.FILES)

#             csv_file = request.FILES["upload"]

#             if not csv_file.name.endswith('.csv'):
#                     messages.error(request,'File is not CSV type')
#                     return HttpResponseRedirect(reverse('dashboard'))
#             if csv_file.multiple_chunks():
#                 messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(5000*5000),))
#                 return HttpResponseRedirect(reverse("dashboard"))
#             file_data = csv_file.read().decode("utf-8")
#             lines = file_data.split("\n")
#             print(lines)
#             first = 0
#             branch = []
#             for line in lines:
#                 if line != '':
#                     if first != 0:
#                         fields = line.split(',')
#                         employee_name = fields[0]
#                         request.session['emp_name'] = employee_name
#                         emp_code = fields[1]
#                         request.session['emp_code'] = emp_code
#                         branch = fields[2]
                        
#                         request.session['branch'] = branch
#                         department = fields[3]
#                         request.session['department'] = department
#                         beneficiary_reference_id = fields[4]
#                         request.session['beneficiary_reference_id'] = beneficiary_reference_id
#                         mobile_number = fields[5] 

#                         url = 'https://cdn-api.co-vin.in/api/v2/auth/generateMobileOTP'
#                         headers = {
#                             'accept':'application/json',
#                             'Content-Type':'application/json',
#                             'x-api-key':'3sjOr2rmM52GzhpMHjDEE1kpQeRxwFDr4YcBEimi',
#                             'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
#                             }
#                         print(type(mobile_number))
#                         params = { 
#                             "mobile": mobile_number,
#                             "secret": "U2FsdGVkX19HvlZ24aYsLH4ncDKvIjMrmIkcElUW3NvyjjA9JOLb1eFJBcJZIGLcNKYksm9Wm8aGhGNGt5aFwQ=="

#                             }
#                         print(params,type(params))
#                         print(params)
#                         res = json.dumps(params)

#                         # print(type(res))
#                         # auth = HTTPBasicAuth('x-api-key', '3sjOr2rmM52GzhpMHjDEE1kpQeRxwFDr4YcBEimi')
#                         # try:
#                         res = requests.post(url,headers=headers,data=res)
#                         print(res.text,type(res.text))
#                         print(res.status_code)
#                         if res.status_code == 200:
#                             re = json.loads(res.text)
#                             txnId = re['txnId']
#                             print('txndid',txnId)
#                             request.session['txnId'] = txnId
#                             # return confirmOTP(request)
#                             return redirect('/confirmotp/')
#                         else:
#                             print('not working')
#                             return redirect('/dashboard/')
#                         # except Exception as e:
#                             # print(e,'error of line number {}'.format(sys.exc_info()[-1].tb_lineno))
#                 first+=1
#             return render(request,'dashboard.html')
#         else:
#             return render(request,'dashboard.html')

#     except Exception as e:
#         print(e,'error of line number {}'.format(sys.exc_info()[-1].tb_lineno))


import base64

@login_required
# @type_user
def dashboard(request):
    try:
        if request.method == 'POST':
            current_user = request.user
            print(current_user)
            user_id = current_user.id
            user = User.objects.get(id=user_id)
            company = models.Company_HR.objects.get(user=user)
            company_name = company.company
            print('company',company)
            csv_file = request.FILES["upload"]
            if not csv_file.name.endswith('.csv'):
                messages.error(request,'Please upload proper file template')
                return HttpResponseRedirect(reverse('dashboard'))
            file_data = csv_file.read().decode("utf-8")
            
            lines = file_data.split("\n")
            first = 0
            emp_details = []
            for line in lines:                     
                if line != '':
                    if first != 0:
                        print('***************************************************',line)
                        
                        fields = line.split(',')
                        # print(fields)
                        username1 = fields[2]
                        password1 = fields[1]
                        emp_name = fields[0]
                        emp_code = fields[1]
                        branch = fields[3]
                        department = fields[4]
                        beneficialy_id = fields[5]
                        mobile_number = fields[6]
                        # print(fields)
                        if User.objects.filter(username=username1).exists():
                            # print(emp_name)
                            emp_details.append(emp_name)
                            pass
                        else:
                            if username1 != '' and password1 != '':
                                try:
                                    user = User.objects.create_user(username=username1,password=password1)
                                    group = Group.objects.get(name='employee')
                                    user.groups.add(group)
                                    user.save()
                                    register = models.RegisterModel.objects.create(user=user,company=company_name)
                                    # print(user)
                                except Exception as e:
                                    print(e,'error of line number {}'.format(sys.exc_info()[-1].tb_lineno))
                                    messages.error(request,e,username1)
                                    return redirect('dashboard')
                                
                                try:
                                    employee = models.Employeeprofile.objects.create(company=company_name,company_HR=company,employee=user,\
                                        employee_name = emp_name, employee_code = emp_code , employee_branch = branch,employee_department=department,\
                                        Beneficiary_Id = beneficialy_id ,phoneNumber = mobile_number)

                                    email = username1
                                    url = 'http://35.154.107.216/'
                                    # message1 = get_template("emails/alert_login.html").render(({'name':emp_name,'url':url,'username':email,'password':password1}))
                                    messages1 = 'Hello ' + emp_name + '\n You are requested to please log in to the system \n '+url+'  and check your vaccinations status \n' + '\n Your Original login credtails were: \n' + 'Username   : ' + username1 + '\n password : ' +password1
                                    send_mail_func(email,messages1)

                                except  Exception as e:
                                    print(e,'error of line number {}'.format(sys.exc_info()[-1].tb_lineno))
                                    messages.error(request,e,username1)
                                    return redirect('dashboard')               
                            else:
                                messages.error(request,'Please fill in the required employee details in csv file')
                                return redirect('dashboard') 
                    first+=1
                # else:
                #     messages.error(request,'Please upload proper file template')
                #     return HttpResponseRedirect(reverse('dashboard'))
                # 
            print(emp_details)
            if len(emp_details) >= 1:
                    print('working')
                    listToStr = ','.join([str(elem) for elem in emp_details])
                    messages.error(request,'Employee(s) already exists.  ' + listToStr)  
                    print(listToStr)
                    return redirect('dashboard')  
            else:
                return redirect('dashboard')
            
        else:
            current_user = request.user
            print(current_user)
            user_id = current_user.id
            user = User.objects.get(id=user_id)
            company = models.Company_HR.objects.get(user=user).company
            id = models.Company.objects.get(name=company).id
            print(id)
            print(company)
            data = models.Employeeprofile.objects.filter(company=id).values('employee_name','employee_code','employee_branch','employee_department','employee_cowin_pdf',\
                'last_checked','Beneficiary_Id','phoneNumber','gender','cowin_status','birth_year','does1_date','does2_date','vaccine')
            print(data)
            emp_list = []
            total = 0
            partial_vaccinated = 0
            fully_vaccinated = 0
            not_vaccinated = 0
            not_checked = 0
            for i in data:
                print(i)
                name = i['employee_name']
                emp_code = i['employee_code']
                branch = i['employee_branch']
                department = i['employee_department']
                status = i['cowin_status']
                last_checked = i['last_checked']
                last_checked1 = None
                if last_checked != None:
                    last_checked1 =last_checked.strftime('%d-%m-%Y')
                beneficialy_id = i['Beneficiary_Id']
                gender = i['gender']
                birth_year = i['birth_year']
                does1_date = i['does1_date']
                does1_date1 = None
                if does1_date != None:
                    does1_date1 = does1_date.strftime('%d-%m-%Y')
                print(does1_date1)
                does2_date = i['does2_date']
                does2_date1 = None
                if does2_date != None:
                    does2_date1 = does2_date.strftime('%d-%m-%Y')
                vaccine = i['vaccine']
                total += 1
                if status == 'Partially Vaccinated':
                    partial_vaccinated += 1
                elif status == 'Fully Vaccinated':
                    fully_vaccinated += 1
                elif status == 'Not Checked':
                    not_checked += 1
                else:
                    not_vaccinated += 1 
                emp_list.append({'name':name,'emp_code':emp_code,'branch':branch,'department':department,'status':status,'last_checked':last_checked1,'beneficialy_id':beneficialy_id,'gender':gender,'birth_year':birth_year,'does1_date':does1_date1,'does2_date':does2_date1,'vaccine':vaccine})
            print(emp_list)
            branch_details = models.Employeeprofile.objects.all().values('employee_branch','employee_department')
            branch_li = []
            department_li = []
            for i in branch_details:
                branch_li.append(i['employee_branch'])
                department_li.append(i['employee_department'])

            branches = []
            for i in branch_li:
                if i not in branches:
                    branches.append(i)

            departments = []
            for i in department_li:
                if i not in departments:
                    departments.append(i)

            print(branches,departments)


            context = {'emp':emp_list,'partial_vaccinated':partial_vaccinated,'fully_vaccinated':fully_vaccinated,'not_vaccinated':not_vaccinated,'not_checked':not_checked,'total':total,'branch':branches,'department':departments}
            return render(request,'dashboard.html',context)

    except Exception as e:
        print(e,'error of line number {}'.format(sys.exc_info()[-1].tb_lineno))


import shutil

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

@login_required
def confirmOTP(request):
    try:
        if request.method == 'POST':
            current_user = request.user
            print(current_user)
            user_id = current_user.id
            company = models.Employeeprofile.objects.get(employee=user_id).company
            print(company)
            print(user_id)
            print(request.POST)
            otp = request.POST.get('otp')
            txtId = request.session.get('txnId')
            sha_signature = encrypt_string(otp)
            print(sha_signature)
            print(otp,txtId)
            url = 'https://cdn-api.co-vin.in/api/v2/auth/validateMobileOtp'
            headers = {
                'accept':'application/json',
                'Content-Type':'application/json',
                'x-api-key':'3sjOr2rmM52GzhpMHjDEE1kpQeRxwFDr4YcBEimi',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
            }
            params = {
                "otp":sha_signature,
                "txnId":txtId
            }
            res = json.dumps(params)
            res = requests.post(url,headers=headers,data=res)
            print(res.text)
            print(res)
            today = date.today()
            if res.status_code == 200:
                consumed = models.Consumed.objects.filter(company=company).values('Consumed').last()
                if consumed == None or consumed == 0:
                    messages.error(request,'employee name  and Cowin name are not same ')
                    return redirect('user_profile')
                today_min = datetime.combine(date.today(), time.min)
                today_max = datetime.combine(date.today(), time.max)
                today_cosumed = models.Consumed.objects.filter(company=company,created__range=(today_min, today_max)).values('today_consumed').last() 
                print(today_cosumed)              
                available = models.Available.objects.filter(company=company).values('availabel').last()
                hr = models.Company_HR.objects.get(company=company)
                if today_cosumed !=  None :
                    y = today_cosumed['today_consumed']
                else:
                    y = 0
                available1 = available['availabel']
                available2 = int(available1)
                available3 = 1
                sub = available2 - available3
                p = int(y)
                q = 1
                add = p +q 
                x = consumed['Consumed']
                a = int(x)
                b = 1 
                c = a + b
                consumed = models.Consumed.objects.create(company=company,Consumed=c,company_hr=hr,today_consumed=add)
                available = models.Available.objects.create(company=company,company_hr=hr,availabel=sub)
                # for i in consumed:
                #      x = i['Consumed']
                
                re = json.loads(res.text)
                del request.session['txnId']
                token = re['token']
                # request.session['token'] = token
                url = 'https://cdn-api.co-vin.in/api/v2/appointment/beneficiaries'
                resp = requests.get(url, auth=BearerAuth(token))
                print(resp)
                data = models.Employeeprofile.objects.filter(employee=user_id).values('employee_name','Beneficiary_Id')
                emp_name = ''
                Beneficiary_Id = ''
                for i in data:
                    emp_name = i['employee_name']
                    Beneficiary_Id = i['Beneficiary_Id']
                emp_first_name = emp_name.split(' ')[0]
                print(emp_first_name)
                print(emp_first_name)
                print(resp.status_code)
                if resp.status_code == 200:
                    re = json.loads(resp.text)
                    print(re)
                    beneficiaries = re['beneficiaries']
                    for i in beneficiaries:
                        beneficiary_reference_id = i['beneficiary_reference_id']
                        name = i['name']
                        first_name = name.split(' ')[0]
                        print(first_name)
                        print(first_name)
                        if beneficiary_reference_id == Beneficiary_Id:
                            print('working')
                            if emp_first_name.upper() == first_name.upper():
                                print('working')
                                print(i['vaccination_status'])
                                vaccination_status = i['vaccination_status']
                                if vaccination_status == 'Partially Vaccinated':
                                    vaccination_status = vaccination_status
                                elif  vaccination_status == 'Vaccinated':
                                    vaccination_status= 'Fully Vaccinated'
                                print(vaccination_status)
                                vaccine = i['vaccine']
                                dose1_date = i['dose1_date']
                                dose2_date = i['dose2_date']
                                birth_year = i['birth_year']
                                beneficiary_reference_id = i['beneficiary_reference_id']
                                gender = i['gender']
                                # purchase_date = datetime.strptime(date_purchase, "%d/%m/%Y %H:%M:%S")
                                if dose1_date == '':
                                    data = models.Employeeprofile.objects.filter(employee=user_id).update(gender=gender,cowin_status=vaccination_status,vaccine=vaccine,birth_year=birth_year,last_checked=today)

                                dose1_date1 = datetime.strptime(dose1_date, '%d-%m-%Y').strftime('%Y-%m-%d')
                                today = datetime.today().strftime('%Y-%m-%d')
                                if dose2_date != '':
                                    dose2_date2 = datetime.strptime(dose2_date, '%d-%m-%Y').strftime('%Y-%m-%d')
                                    data = models.Employeeprofile.objects.filter(employee=user_id).update(gender=gender,cowin_status=vaccination_status,does1_date=dose1_date1,does2_date=dose2_date2,vaccine=vaccine,birth_year=birth_year,last_checked=today)
                                else:
                                    data = models.Employeeprofile.objects.filter(employee=user_id).update(gender=gender,cowin_status=vaccination_status,does1_date=dose1_date1,vaccine=vaccine,birth_year=birth_year,last_checked=today)
                                params = {
                                "beneficiary_reference_id":beneficiary_reference_id,
                                    }
                                headers ={
                                "accept": "application/pdf"
                                }
                                res = json.dumps(params)
                                print(type(params))
                                print(type(res))
                                print(res)
                                print(beneficiary_reference_id)
                                resp = requests.get("https://cdn-api.co-vin.in/api/v2/registration/certificate/download?beneficiary_reference_id={}".format(beneficiary_reference_id),headers=headers, auth=BearerAuth(token),timeout=90)
                                print(resp)
                                if resp.status_code == 200:
                                    # print(resp)
                                    re = resp.text
                                    print(type(re))
                                    re = resp.text
                                    chunk_size = 2000

                                    with open(os.path.join(settings.MEDIA_ROOT,'download_certificate.pdf'),'wb') as fd:
                                        for chunk in resp.iter_content(chunk_size):
                                            print(type(chunk))
                                            fd.write(chunk)
                                    encoded_string = None
                                    with open(os.path.join(settings.MEDIA_ROOT,'download_certificate.pdf'), "rb") as pdf_file:
                                        encoded_string = base64.b64encode(pdf_file.read())
                                    data = models.Employeeprofile.objects.filter(employee=user_id).values('employee_name').update(test=encoded_string)
                                    # print(data)
                                    print('data are saved is successfully')
                                else:
                                    print(resp.text)
                                    print('data not store in database')
                                    messages.error(request,resp.text)
                                    return redirect('user_profile')

                                print(dose1_date1)
                                print(type(birth_year),birth_year,type(dose1_date),)
                            else:
                                messages.error(request,'employee name  and Cowin name are not same ')
                                return redirect('user_profile')
                        else:
                            pass
                else:
                    messages.error(request,'getting error for'+resp.text)
                    return redirect('user_profile')
                return redirect('user_profile')
            else:
                messages.error(request,"OTP Doest not match please try again")
                return redirect('user_profile')
    except Exception as e:
        print(e,'error of line number {}'.format(sys.exc_info()[-1].tb_lineno))






@login_required
def dashboard2(request):
    try:

        token = request.session.get('token')
        print(token)
        
        # headers = {
        #         'accept':'application/json',
        #         'Content-Type':'application/json',
        #         'x-api-key':'3sjOr2rmM52GzhpMHjDEE1kpQeRxwFDr4YcBEimi',
        #         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
        #     }

        url = 'https://cdn-api.co-vin.in/api/v2/appointment/beneficiaries'
        # headers["Authorization"] = "Bearer"+token
        # headers['accept'] = 'application/json'
        # headers['x-api-key'] = '3sjOr2rmM52GzhpMHjDEE1kpQeRxwFDr4YcBEimi'
        resp = requests.get(url, auth=BearerAuth(token))
        print(resp)
        data = []
        print(resp.status_code)
        if resp.status_code == 200:
            re = json.loads(resp.text)
            print(re)
            
            beneficiaries = re['beneficiaries']
            vaccination_status = ''
            vaccine = ''
            dose1_date = ''
            name = ''
            total = 0
            partial_vaccinated = 0
            fully_vaccinated = 0
            not_vaccinated = 0
            for i in beneficiaries:
                print(i)
                total =+ 1  
                beneficiary_reference_id = i['beneficiary_reference_id']
                beneficiaries = request.session.get('beneficiary_reference_id')
                emp_name = request.session.get('emp_name')
                name = i['name']
                emp_code = request.session.get('emp_code')
                branch = request.session.get('branch')
                department = request.session.get('department')
                if emp_name == name:
                    print('working')
                    if beneficiary_reference_id == beneficiaries:
                        print(i['vaccination_status'])
                        vaccination_status = i['vaccination_status']
                        if vaccination_status == 'Partially Vaccinated':
                            vaccination_status = vaccination_status
                        elif  vaccination_status == 'Vaccinated':
                            vaccination_status= 'Fully Vaccinated'
                        print(vaccination_status)
                        vaccine = i['vaccine']
                        dose1_date = i['dose1_date']
                        dose2_date = i['dose2_date']
                        
                        birth_year = i['birth_year']
                        beneficiary_reference_id = i['beneficiary_reference_id']
                        gender = i['gender']

                        temp = {'name':name,'emp_code':emp_code,'branch':branch,'department':department,'vaccination_status':vaccination_status,\
                            'vaccine':vaccine,'dose1_date':dose1_date,'dose2_date':dose2_date,'birth_year':birth_year,'beneficiary_reference_id':beneficiary_reference_id,'gender':gender}
                        data.append(temp)
                        if vaccination_status == 'Partially Vaccinated':
                            partial_vaccinated =+ 1
                        elif vaccination_status == 'Fully Vaccinated':
                            fully_vaccinated =+ 1
                        else:
                            not_vaccinated =+1 
                        print(partial_vaccinated)
                    else:
                        messages.error(request,'beneficiary reference id not match ')
                        return redirect('/dashboard2/')  
                else:
                    messages.error(request,'csv file employee name  and Cowin name are not same')
                    return redirect('/dashboard2/')

                context ={'emp':data,'partial_vaccinated':partial_vaccinated,'fully_vaccinated':fully_vaccinated,'not_vaccinated':not_vaccinated,'total':total}
                print(context)
                return render(request,'dashboard.html',context)
            else:
                messages.error(request,'error message'+resp.status_code)
                return redirect('/dashboard2/') 
    except Exception as e:
        print(e,'line number of error {}'.format(sys.exc_info()[-1].tb_lineno))



# @login_required
# def confirmOTP(request):
#     try:
#         if request.method == 'POST':
#             print(request.POST)
#             otp = request.POST.get('otp')
#             txtId = request.session.get('txnId')
#             sha_signature = encrypt_string(otp)
#             print(sha_signature)
#             print(otp,txtId)
#             url = 'https://cdn-api.co-vin.in/api/v2/auth/validateMobileOtp'
#             headers = {
#                 'accept':'application/json',
#                 'Content-Type':'application/json',
#                 'x-api-key':'3sjOr2rmM52GzhpMHjDEE1kpQeRxwFDr4YcBEimi',
#                 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
#             }
#             params = {
#                 "otp":sha_signature,
#                 "txnId":txtId
#             }
#             res = json.dumps(params)
#             res = requests.post(url,headers=headers,data=res)
#             print(res.text)
#             print(res)
#             if res.status_code == 200:
#                 re = json.loads(res.text)
#                 print(re)
#                 del request.session['txnId']
#                 token = re['token']
#                 request.session['token'] = tokenMEDIA_ROOT

#                 return redirect('dashboard2')
#             else:
#                 messages.error(request,"OTP Doest not match please try again")
#                 return redirect('confirmotp')
                
#         else:
#             return render(request,'confirmotp.html')
#     except Exception as e:
#         print(e,'error of line number {}'.format(sys.exc_info()[-1].tb_lineno))







@login_required
@csrf_exempt
def exportcsv(request):
    try:
        if request.method == 'POST':
            current_user = request.user
            print(current_user)
            print(request.POST)
            data = request.POST.getlist('data[]')
            print(data) 
            csvfile = StringIO()
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Name','Last Checked','Branch','Department','Status','Emp Code','Gender','Birth Year','Beneficiary Id','vaccine','Dose1 Date','Does2 Date','Difference between Dose 1 to today(in Days)','Difference between Dose 2 to today(in Days)'])
            for i in data:
                print(i.split(','))
                list_data = i.split(',')
                print(list_data)
                csvwriter.writerow([list_data[0],list_data[1],list_data[2],list_data[3],list_data[4],list_data[5],list_data[6],list_data[7],list_data[8],list_data[9],list_data[10],list_data[11],list_data[12],list_data[13]])            
            mail_subject = "Hi! CoWin Status CSV"
            message = "This is csv file where all details about cowin status"
            email = EmailMessage(
                mail_subject,
                message,
                settings.EMAIL_HOST_USER,
                [current_user],
            )
            email.attach('media/status.csv',csvfile.getvalue() ,'text/csv')
            email.send()
            return HttpResponse('Email send successfully')
    except Exception as e:
        print(e,'line number of error {}'.format(sys.exc_info()[-1].tb_lineno))

import codecs
import base64
@login_required
@csrf_exempt
def download_certificate(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            emp_code = request.POST.get('emp_code')
            current_user = request.user
            user_id = current_user.id
            user = User.objects.get(id=user_id)
            company = models.Company_HR.objects.get(user=user)
            company_name = company.company
            company_obj = models.Company.objects.get(name=company_name)
            data = models.Employeeprofile.objects.filter(employee_code=emp_code,company=company_obj).values('test')
            # print(data)
            test = None
            for i in data: 
                test = i['test']
            print(test)
            if test != None:
                f = list(test)
                del f[-1]
                del f[0]
                del f[0]
                my_str = ''.join(f)
                # print(my_str)
                my_str_as_bytes = str.encode(my_str)
                with open(os.path.join(settings.MEDIA_ROOT, 'certificate.pdf'), "wb") as f:
                    f.write(codecs.decode(my_str_as_bytes, "base64"))
                # with open(os.path.join(settings.MEDIA_ROOT, 'certificate.pdf'), 'rb') as fh:
                #     response = HttpResponse(fh.read(), content_type="application/pdf")
                #     response['Content-Disposition'] = 'attachment; filename=certificate.pdf '
                #     # return response
                #     # return HttpResponse('File download in tmp folder')
                #     return 
                return HttpResponse('http://35.154.107.216/media/certificate.pdf')
            else:
                return HttpResponse('Certificate not available at present. Please send email to follow-up')
            
    except Exception as e:
        print(e,'line number of error {}'.format(sys.exc_info()[-1].tb_lineno))



# import urllib.request
# pdf_path = ""
# def download_file(download_url, filename):
#     response = urllib.request.urlopen(download_url)    
#     file = open(filename + ".pdf", 'wb')
#     file.write(response.read())
#     file.close()
 
# download_file(pdf_path, "Test")

@login_required
def admin_profile(request):
    try:
        current_user = request.user
        print(current_user)
        user_id = current_user.id
        user = User.objects.get(id=user_id)
        print(user.password)
        company = models.Company_HR.objects.get(user=user).company
        print(company)
        company_obj = models.Company.objects.get(name=company)
        # print(company_obj)
        available_obj = models.Available.objects.filter(company=company_obj).values('availabel').last()
        print(available_obj)
        # available_obj = models.Available.objects.get(company=company_obj)
        available = available_obj['availabel']
        print(available)
        # consumed = models.Consumed.objects.get(company=company_obj)
        consumed1 = models.Consumed.objects.filter(company=company).values('Consumed').last()
        consumed = consumed1['Consumed']
        purchase1 = models.Purchase.objects.filter(company=company_obj).values('purchase','created').last()
        print('purchase',purchase1)
        purchase = purchase1['purchase']

        purchase_date1 = purchase1['created']
        date_purchase = purchase_date1.strftime("%d/%m/%Y %H:%M:%S")
        print(type(date_purchase),date_purchase)
        purchase_date = datetime.strptime(date_purchase, "%d/%m/%Y %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
        date = datetime.strptime(purchase_date, '%Y-%m-%d %H:%M:%S').replace(tzinfo=tz.gettz('Asia/Kolkata'))
        pur = models.Purchase.objects.filter(company=company_obj).values('today_purchase','created').order_by('-created')
        # con = models.Consumed.objects.filter(company=company_obj).values('today_consumed','created').order_by('-created')
        # today = date.today()
        # print('today',today)
        # today_min = datetime.combine(date.today(), time.min)
        # today_max = datetime.combine(date.today(), time.max)
        # print(con)
        # print(pur)
        # print(con)
        data = []
        for i in pur:
            data.append(i)
        # print(data)
        # print(len(data))
        last_date = None
        last_purchase = None
        last_day = None
        last_time = None
        second_day = None
        second_time = None
        second_last_purchase= None
        if len(data) >= 2:
            last_date = data[0]['created']
            last_purchase = data[0]['today_purchase']
            print(last_date)
            date_last = last_date.strftime("%d/%m/%Y %H:%M:%S")
            date_last1 = datetime.strptime(date_last, "%d/%m/%Y %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
            # date_last1 = datetime.strptime(date_last1, '%Y-%m-%d %H:%M:%S').replace(tzinfo=tz.gettz('Asia/Kolkata'))
            local_timezone = pytz.timezone('Asia/Kolkata')
            date_last1  = datetime.strptime(date_last1, '%Y-%m-%d %H:%M:%S').astimezone(local_timezone)
            print(date_last1)
            last_day = date_last1.date().strftime("%Y-%m-%d")
            last_time = date_last1.time()
            second_last_date = data[1]['created']
            second_last_purchase = data[1]['today_purchase']
            last_min = datetime.combine(last_date.today(), time.min)
            last_max = datetime.combine(last_date.today(), time.max)
            print('last_min',last_min,'last_max',last_max)
            date_second = second_last_date.strftime("%d/%m/%Y %H:%M:%S")
            date_second1 = datetime.strptime(date_second, "%d/%m/%Y %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
            date_second1 = datetime.strptime(date_second1, '%Y-%m-%d %H:%M:%S').astimezone(local_timezone)
            second_day = date_second1.date().strftime("%Y-%m-%d")
            today_cosumed = models.Consumed.objects.filter(company=company_obj,created__range=(last_min, last_max)).values('today_consumed','created')
            print('consumed',today_cosumed)
            second_time = date_second1.time()
            print('working')
        else:
            local_timezone = pytz.timezone('Asia/Kolkata')
            last_date = data[0]['created']
            last_purchase = data[0]['today_purchase']
            date_last = last_date.strftime("%d/%m/%Y %H:%M:%S")
            date_last1 = datetime.strptime(date_last, "%d/%m/%Y %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
            date_last1 = datetime.strptime(date_last1, '%Y-%m-%d %H:%M:%S').astimezone(local_timezone)
            last_day = date_last1.date().strftime("%Y-%m-%d")
            last_time = date_last1.time().strftime('%H:%M')
            print(last_day)



        print(last_date,last_purchase)
        print(purchase_date)
        print('date o',date)
        print(consumed,purchase)
        password = user.password
        form = PasswordChangeForm(request.user)
        context = {'company':company,'available':available,'consumed':consumed,'purchase':purchase,'user':user,'password':password,'form':form,'last_day':last_day,'last_time':last_time,'last_purchase':last_purchase,\
            'second_day':second_day,'second_time':second_time,'second_last_purchase':second_last_purchase}
        
        return render(request,'admin_profile.html',context)
    except Exception as e:
        print(e,'line numberof error {}'.format(sys.exc_info()[-1].tb_lineno))


@login_required
def change_password(request):
    try:
        if request.method == 'POST':
            print(request.POST)
            print(request.user)
            form = PasswordChangeForm(request.user,request.POST)
            print(form)
            if form.is_valid():
                user= form.save()
                update_session_auth_hash(request,user)
                print(user)
                messages.success(request,'Your Password was successfully updated !')
                return redirect('profile')
            else:
                messages.error(request,'Please correct the error below')
                return redirect('profile')
    except Exception as e:
        print(e,'line number of error {}'.format(sys.exc_info()[-1].tb_lineno))
@login_required
def change_username_company(request):
    try:
        if request.method == 'POST':
            company_name = request.POST.get('company_name')
            user_name = request.POST.get('user_name')
            print(company_name,user_name)
            current_user = request.user
            print(current_user)
            user = User.objects.get(username = current_user)
            company = models.Company_HR.objects.get(user=user).company
            company_obj = models.Company.objects.get(name=company)
            company_obj.name = company_name
            company_obj.save()
            print(company_obj)
            print(company)
            user.username = user_name
            user.save()
            print(user)
            return redirect('profile')

    except Exception as e:
        print(e,'line number of error {}'.format(sys.exc_info()[-1].tb_lineno))



# @type_user
@login_required
def user_profile(request):
    try:
        if request.method=='POST':
            print('request',request.POST)
            current_user = request.user
            print(current_user)
            user_id = current_user.id
            print(user_id)
            name = request.POST.get('user_name')
            emp_code = request.POST.get('emp_code')
            branch = request.POST.get('branch')
            department = request.POST.get('department')
            phone_number = request.POST.get('mobile_number')
            beneficiary = request.POST.get('beneficiary')
            url = 'https://cdn-api.co-vin.in/api/v2/auth/generateMobileOTP'
            headers = {
                'accept':'application/json',
                'Content-Type':'application/json',
                'x-api-key':'3sjOr2rmM52GzhpMHjDEE1kpQeRxwFDr4YcBEimi',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
                }
            print(type(phone_number))
            params = { 
                "mobile": phone_number,
                "secret": "U2FsdGVkX19HvlZ24aYsLH4ncDKvIjMrmIkcElUW3NvyjjA9JOLb1eFJBcJZIGLcNKYksm9Wm8aGhGNGt5aFwQ=="

                }
            res = json.dumps(params)
            res = requests.post(url,headers=headers,data=res)
            print(res.text,type(res.text))
            print(res.status_code)
            if res.status_code == 200:
                re = json.loads(res.text)
                txnId = re['txnId']
                print('txndid',txnId)
                request.session['txnId'] = txnId
                print(re)
                print(name)
                data = models.Employeeprofile.objects.filter(employee=user_id).update(employee_name=name,employee_code=emp_code,employee_branch=branch,employee_department=department,phoneNumber=phone_number,Beneficiary_Id=beneficiary)
                return redirect('user_profile')
            else:
                messages.error(request,'error are come for api'+res.text)
                return redirect('user_profile')
        else:
            current_user = request.user
            print(current_user)
            user_id = current_user.id
            print(user_id)
            # user = User.objects.get(id=user_id)
            data = models.Employeeprofile.objects.filter(employee=user_id).values('employee_name','employee_code','employee_branch','employee_department','phoneNumber','Beneficiary_Id','cowin_status')
            name = None
            emp_code = None
            branch = None
            department = None
            phone = None
            beneficiary = None
            status = None
            for i in data:
                name = i['employee_name']
                emp_code = i['employee_code']
                branch = i['employee_branch']
                department = i['employee_department']
                phone = i['phoneNumber']
                beneficiary = i['Beneficiary_Id']
                status = i['cowin_status']
                
            print(data)
            
            context = {'name':name,'emp_code':emp_code,'branch':branch,'department':department,'phone':phone,'beneficiary':beneficiary,'status':status}

            return render(request,'user_profile.html',context)
    except Exception as e:
        print(e,'line number of error {}'.format(sys.exc_info()[-1].tb_lineno))


from django.template.loader import get_template
from django.template import Context


@csrf_exempt
def send_user_email(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            emp_code = request.POST.get('emp_code')
            current_user = request.user
            user_id = current_user.id
            user = User.objects.get(id=user_id)
            company = models.Company_HR.objects.get(user=user)
            company_name = company.company
            company_obj = models.Company.objects.get(name=company_name)
            data = models.Employeeprofile.objects.filter(employee_code=emp_code,company=company_obj).values('employee')
            user_id = None
            for i in data:
                user_id = i['employee']
            username = User.objects.filter(id=user_id).values('username')
            email = None
            for i in username:
                email = i['username']
            url = 'http://35.154.107.216/'
            mail_subject = "Hi! Login Alert"
            message = get_template("emails/alert_login.html").render(({'name':name,'url':url,'username':email,'password':emp_code}))
            
            "please Login and check cowin status here is you username  " + email + '  This is your password  ' + emp_code
            email = EmailMessage(
                mail_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
            )
            email.content_subtype = "html"
            email.send()

            return HttpResponse('Email sent to user   ' + name)
    except Exception as e:
        print(e,'line number of error {}'.format(sys.exc_info()[-1].tb_lineno))
def download_csv(request, queryset):
#   if not request.user:
#     raise PermissionDenied

  model = queryset.model
  model_fields = model._meta.fields + model._meta.many_to_many
  field_names = [field.name for field in model_fields]

  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="export.csv"'

  # the csv writer
  writer = csv.writer(response, delimiter=";")
  # Write a first row with header information
  writer.writerow(field_names)
  # Write data rows
  for row in queryset:
      values = []
      for field in field_names:
          value = getattr(row, field)
          if callable(value):
              try:
                  value = value() or ''
              except:
                  value = 'Error retrieving value'
          if value is None:
              value = ''
          values.append(value)
      writer.writerow(values)
  return response



@csrf_exempt
def export_csv_request(request):
    try:
        if request.method =="POST":
            current_user = request.user
            # print(current_user)
            user_id = current_user.id
            user = User.objects.get(id=user_id)
            # print(user.password)
            company = models.Company_HR.objects.get(user=user).company
            # print(company)
            company_obj = models.Company.objects.get(name=company)
            print('request',request.POST)
            # name = request.POST.get('name')
            purchase = models.Purchase.objects.filter(company=company).values('purchase','today_purchase','created')
            # print(purchase)
            purchase = models.Purchase.objects.all();
            consumed = models.Consumed.objects.all();
            con = consumed.filter(company=company_obj)
            ps = purchase.filter(company=company_obj)
            # print(con)
            # print(ps)
            response = HttpResponse(content_type='text/csv')
            # force download.
            response['Content-Disposition'] = 'attachment;filename=export.csv'
            writer = csv.writer(response)
            # writer = csv.writer(response)
            writer.writerow(['Total Purchase','Date ','Date Wish Purchase'])
            local_timezone = pytz.timezone('Asia/Kolkata')
            purchase_list = []
            consumed_list = []
            for obj in con:
                last_date = obj.created
                date_last = last_date.strftime("%d/%m/%Y %H:%M:%S")
                date_last1 = datetime.strptime(date_last, "%d/%m/%Y %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
                date_last1 = datetime.strptime(date_last1, '%Y-%m-%d %H:%M:%S').astimezone(local_timezone)
                consumed_list.append([obj.Consumed,date_last1 , obj.today_consumed, ])
            # print(consumed_list)
            for obj in ps:
                # print(obj.created)
                last_date = obj.created
                date_last = last_date.strftime("%d/%m/%Y %H:%M:%S")
                date_last1 = datetime.strptime(date_last, "%d/%m/%Y %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
                date_last1 = datetime.strptime(date_last1, '%Y-%m-%d %H:%M:%S').astimezone(local_timezone)
                print(date_last1)
                purchase_list.append([obj.purchase,date_last1 , obj.today_purchase, ])
                # writer.writerow([obj.purchase,date_last1 , obj.today_purchase, ])
            # length = len(consumed_list)
            a = [i for i in purchase_list ]
            b = [j for j in consumed_list]
            c = a + b
            # print(c)
            d = None
            
            for i in c:
                writer.writerow(i)
                # d = i
            print('data',d)
            # email.attach('media/status.csv',csvfile.getvalue() ,'text/csv')
            # mail_subject = "Hi! CoWin Status CSV"
            # message = "This is csv file where all details about cowin status"
            # email = EmailMessage(
            #     mail_subject,
            #     message,
            #     settings.EMAIL_HOST_USER,
            #     [current_user],
            # )
            # email.attach('media/export.csv',csvfile.getvalue() ,'text/csv')
            # email.send()
            # csvfile = StringIO()
            # csvwriter = csv.writer(csvfile)
            # data = download_csv(request, models.Consumed.objects.all())
            # response = HttpResponse(data, content_type='text/csv')
            # csvwriter.writerow(['Name','Last Checked','Branch','Department','Status','Emp Code','Gender','Birth Year','Beneficiary Id','vaccine','Dose1 Date','Does2 Date','Difference between Dose 1 to today(in Days)','Difference between Dose 2 to today(in Days)'])
            # data = []
            # for i in purchase:
            #     print(i)
            #     temp = i
                # print(i.split(','))
                # list_data = i.split(',')
                # print(list_data)
                # csvwriter.writerow([list_data[0],list_data[1],list_data[2],list_data[3],list_data[4],list_data[5],list_data[6],list_data[7],list_data[8],list_data[9],list_data[10],list_data[11],list_data[12],list_data[13]]) 
            return response
        else:
            return redirect('profile')

    except Exception as e:
        print(e,'line number of error {}'.format(sys.exc_info()[-1].tb_lineno))

