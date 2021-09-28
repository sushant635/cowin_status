from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import RegexValidator
import base64

# Create your models here.


class Image(models.Model):
    
    image_file = models.ImageField(upload_to='images/',default='favicon.ico')
    imgae_b64 = models.BinaryField(blank=True,null=True)


    def save(self, *args, **kwargs):
        if self.image_file:
            image_file = open(self.image_file.url,'rb')
            self.imgae_b64 = base64.b64encode(img_file.read())


class Company(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'company'



class RegisterModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'registermodel'


class Company_HR(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=False,blank=False)
    user = models.OneToOneField(to=User,on_delete=models.CASCADE,related_name='company_Hr',)

    def __str__(self):
        return self.company.name

    class Meta:
        db_table = 'company_hr'


class Available(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=False,blank=False)
    company_hr = models.ForeignKey(Company_HR,on_delete=models.CASCADE,null=False,blank=False)
    availabel = models.CharField(max_length=100,null=False,blank=False,default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.availabel

    class Meta:
        db_table = 'availabe_request'

class Purchase(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=False,blank=False)
    company_hr = models.ForeignKey(Company_HR,on_delete=models.CASCADE,null=False,blank=False)    
    purchase = models.CharField(max_length=100,null=False,blank=False,default=0)
    today_purchase = models.CharField(max_length=100,null=False,default=0)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.purchase

    class Meta:
        db_table = 'purchase_request'


class Consumed(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=False,blank=False)
    company_hr = models.ForeignKey(Company_HR,on_delete=models.CASCADE,null=False,blank=False)      
    Consumed = models.CharField(max_length=100,null=False,blank=False,default=0)
    today_consumed = models.CharField(max_length=100,null=False,default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Consumed

    class Meta:
        db_table = 'consume_request'

    
class ApiCount(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=False,blank=False)
    company_hr = models.ForeignKey(Company_HR,on_delete=models.CASCADE,null=False,blank=False)      
    availabel = models.ForeignKey(Available,on_delete=models.CASCADE,null=False,blank=False)
    purchase = models.ForeignKey(Purchase,on_delete=models.CASCADE,null=False,blank=False)
    consumed = models.ForeignKey(Consumed,on_delete=models.CASCADE,null=False,blank=False)

    def __str__(self):
        return self.company

    class Meta:
        db_table = 'apicount'


class Employeeprofile(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=False,blank=False)
    company_HR = models.ForeignKey(Company_HR,on_delete=models.CASCADE,null=False,blank=False)
    employee = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    employee_name = models.CharField(max_length=500,blank=True,null=True)
    employee_code = models.CharField(max_length=100,blank=True,null=True)
    employee_branch = models.CharField(max_length=500,blank=True,null=True)
    employee_department = models.CharField(max_length=500,blank=True,null=True)
    employee_cowin_pdf = models.BinaryField(blank = True, null = True, editable = True)
    last_checked  = models.DateField(null=True,blank=True)
    Beneficiary_Id = models.CharField(max_length=500,blank=True,null=True)
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    phoneNumber = models.CharField(validators = [phoneNumberRegex], max_length = 16,)
    gender = models.CharField(max_length=100,null=True,blank=True)
    cowin_status = models.CharField(max_length=50,null=True,blank=True,default='Not Checked')
    birth_year = models.PositiveSmallIntegerField(blank=True, null=True)
    does1_date = models.DateField(null=True,blank=True)
    does2_date = models.DateField(null=True,blank=True)
    vaccine = models.CharField(max_length=100,null=True,blank=True)
    test = models.TextField(blank=True,null=True,db_column='data')
    text = models.TextField(blank=True,null=True)
    # def set_data(self, data):
    #     self.test = base64.encodestring(data)

    # def get_data(self):
    #     return base64.decodestring(self.test)

    # data = property(get_data, set_data)

    def __str__(self):
        return self.employee_name

    class  Meta :
        db_table = 'employee_profile'











