from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
import requests
from django.contrib.auth import authenticate, login, logout
import sys
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from requests.auth import HTTPBasicAuth
import  json
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

# Create your views here.
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))





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
                    return redirect('dashboard')
                else:
                    return HttpResponse('You account was inactive')
            else:
                print("someone tried to login and failed")
                print("They used username:{} and {}".format(username,password))
                return HttpResponse("Invalid login details given")
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



@login_required
def dashboard(request):
    try:
        if request.method == "POST":
            print(request.POST)
            print(request.FILES)

            csv_file = request.FILES["upload"]

            if not csv_file.name.endswith('.csv'):
                    messages.error(request,'File is not CSV type')
                    return HttpResponseRedirect(reverse('dashboard'))
            if csv_file.multiple_chunks():
                messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(5000*5000),))
                return HttpResponseRedirect(reverse("dashboard"))
            file_data = csv_file.read().decode("utf-8")
            lines = file_data.split("\n")
            print(lines)
            first = 0
            branch = []
            for line in lines:
                if line != '':
                    if first != 0:
                        fields = line.split(',')
                        employee_name = fields[0]
                        emp_code = fields[1]
                        request.session['emp_code'] = emp_code
                        branch = fields[2]
                        
                        request.session['branch'] = branch
                        department = fields[3]
                        request.session['department'] = department
                        beneficiary_reference_id = fields[4]
                        request.session['beneficiary_reference_id'] = beneficiary_reference_id
                        mobile_number = fields[5] 

                        url = 'https://cdn-api.co-vin.in/api/v2/auth/generateMobileOTP'
                        headers = {
                            'accept':'application/json',
                            'Content-Type':'application/json',
                            'x-api-key':'3sjOr2rmM52GzhpMHjDEE1kpQeRxwFDr4YcBEimi',
                            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
                            }
                        print(type(mobile_number))
                        params = { 
                            "mobile": mobile_number,
                            "secret": "U2FsdGVkX19HvlZ24aYsLH4ncDKvIjMrmIkcElUW3NvyjjA9JOLb1eFJBcJZIGLcNKYksm9Wm8aGhGNGt5aFwQ=="

                            }
                        print(params,type(params))
                        print(params)
                        res = json.dumps(params)

                        # print(type(res))
                        # auth = HTTPBasicAuth('x-api-key', '3sjOr2rmM52GzhpMHjDEE1kpQeRxwFDr4YcBEimi')
                        # try:
                        res = requests.post(url,headers=headers,data=res)
                        print(res.text,type(res.text))
                        print(res.status_code)
                        if res.status_code == 200:
                            re = json.loads(res.text)
                            txnId = re['txnId']
                            print('txndid',txnId)
                            request.session['txnId'] = txnId
                            # return confirmOTP(request)
                            return redirect('/confirmotp/')
                        else:
                            print('not working')
                        # except Exception as e:
                            # print(e,'error of line number {}'.format(sys.exc_info()[-1].tb_lineno))
                first+=1
            return render(request,'dashboard.html')
        else:
            return render(request,'dashboard.html')

    except Exception as e:
        print(e,'error of line number {}'.format(sys.exc_info()[-1].tb_lineno))

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

@login_required
def confirmOTP(request):
    try:
        if request.method == 'POST':
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
            if res.status_code == 200:
                re = json.loads(res.text)
                print(re)
                del request.session['txnId']
                token = re['token']
                request.session['token'] = token

                return redirect('dashboard2')
            else:
                messages.error(request,"OTP Doest not match please try again")
                return redirect('confirmotp')
                
        else:
            return render(request,'confirmotp.html')
    except Exception as e:
        print(e,'error of line number {}'.format(sys.exc_info()[-1].tb_lineno))


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r



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
                total =+ 1  
                beneficiary_reference_id = i['beneficiary_reference_id']
                beneficiaries = request.session.get('beneficiary_reference_id')
                emp_code = request.session.get('emp_code')
                branch = request.session.get('branch')
                department = request.session.get('department')
                if beneficiary_reference_id == beneficiaries:
                    print(i['vaccination_status'])
                    vaccination_status = i['vaccination_status']
                    vaccine = i['vaccine']
                    dose1_date = i['dose1_date']
                    dose2_date = i['dose2_date']
                    name = i['name']
                    birth_year = i['birth_year']
                    beneficiary_reference_id = i['beneficiary_reference_id']
                    gender = i['gender']

                    temp = {'name':name,'emp_code':emp_code,'branch':branch,'department':department,'vaccination_status':vaccination_status,\
                        'vaccine':vaccine,'dose1_date':dose1_date,'dose2_date':dose2_date,'birth_year':birth_year,'beneficiary_reference_id':beneficiary_reference_id,'gender':gender}
                    data.append(temp)
                    if vaccination_status == 'Partially Vaccinated':
                        partial_vaccinated =+ 1
                    elif vaccination_status == 'Vaccinated':
                        fully_vaccinated =+ 1
                    else:
                        not_vaccinated =+1 
        context ={'emp':data,'partial_vaccinated':partial_vaccinated,'fully_vaccinated':fully_vaccinated,'not_vaccinated':not_vaccinated,'total':total}
        print(context)
        return render(request,'dashboard.html',context)
    except Exception as e:
        print(e,'line number of error {}'.format(sys.exc_info()[-1].tb_lineno))


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
            csvwriter.writerow(['Name','Emp Code','Branch','Gender','Department','Status','Dose1 Date','Does2 Date','Birth Year','Beneficiary Id','vaccine','Difference between Dose 1 to today(in Days)','Difference between Dose 2 to today(in Days)'])
            for i in data:
                print(i.split(','))
                list_data = i.split(',')
                print(list_data)
                csvwriter.writerow([list_data[0],list_data[1],list_data[2],list_data[3],list_data[4],list_data[5],list_data[6],list_data[7],list_data[8],list_data[9],list_data[10],list_data[11],list_data[12]])            
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


@csrf_exempt
def download_certificate(request):
    try:
        if request.method == 'POST':
            print(request.POST)
            beneficiary_reference_id = request.POST.get('data')
            token = request.session.get('token')
            url = "https://cdn-api.co-vin.in/api/v2/registration/certificate/download?beneficiary_reference_id=[beneficiary_reference_id]"
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
            resp = requests.get("https://cdn-api.co-vin.in/api/v2/registration/certificate/download?beneficiary_reference_id={}".format(beneficiary_reference_id),headers=headers, auth=BearerAuth(token))
            print(resp)
            if resp.status_code == 200:
                re = resp.text
                chunk_size = 2000
                with open('/tmp/download_certificate.pdf', 'wb') as fd:
                    for chunk in resp.iter_content(chunk_size):
                        fd.write(chunk)
            # re = json.loads(resp.text)
            # print(re)

            return HttpResponse('File download in tmp folder')


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
        print(company_obj)
        available = models.Available.objects.get(company=company_obj)
        print(available.availabel,available.created)
        consumed = models.Consumed.objects.get(company=company_obj)
        purchase = models.Purchase.objects.get(company=company_obj)
        print(consumed,purchase)
        password = user.password
        context = {'company':company,'available':available,'consumed':consumed,'purchase':purchase,'user':user,'password':password}
        
        return render(request,'user_profile.html',context)
    except Exception as e:
        print(e,'line numberof error {}'.format(sys.exc_info()[-1].tb_lineno))



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
                return redirect('change_password')
            else:
                messages.error(request,'Please correct the error below')
                return redirect('change_password')
        else:
            form = PasswordChangeForm(request.user)
            return render (request,'change_password.html',{'form':form})
    except Exception as e:
        print(e,'line numberof error {}'.format(sys.exc_info()[-1].tb_lineno))




    
