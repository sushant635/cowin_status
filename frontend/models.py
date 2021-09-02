from django.db import models
from django.contrib.auth.models import User 
# Create your models here.



class Company(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'company'


class Company_HR(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=False,blank=False)
    user = models.OneToOneField(to=User,on_delete=models.CASCADE,related_name='company_Hr',)

    def __str__(self):
        return self.company

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
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.purchase

    class Meta:
        db_table = 'purchase_request'


class Consumed(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=False,blank=False)
    company_hr = models.ForeignKey(Company_HR,on_delete=models.CASCADE,null=False,blank=False)      
    Consumed = models.CharField(max_length=100,null=False,blank=False,default=0)
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