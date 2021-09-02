"""cowin_status_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from frontend import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('',views.user_login,name='login'),
    path('confirmotp/',views.confirmOTP,name='confirmotp'),
    path('dashboard2/',views.dashboard2,name='dashboard2'),
    path('exportfile/',views.exportcsv,name='exportfile'),
    path('download_certificate',views.download_certificate,name='download_certificate'),
    path('profile/',views.admin_profile,name='profile'),
    path('change_password/',views.change_password,name='change_password')
] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT) +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
