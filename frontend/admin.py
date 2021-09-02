from django.contrib import admin
from frontend.models import Company_HR,Company,Available,Consumed,Purchase,ApiCount
# Register your models here.

admin.site.register(Company_HR)
admin.site.register(Available)
admin.site.register(Purchase)
admin.site.register(Company)
admin.site.register(Consumed)
admin.site.register(ApiCount)

