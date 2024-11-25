"""
URL configuration for djangoapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from . import views  # Import all views from views.py
from .views import RoleBasedLoginView

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin URL
    path('', views.homepage, name='homepage'),  # Homepage view
    path('litigants/', views.litigant_list, name='litigant_list'),  # Litigant list page
    path('account/register/', views.register, name='register'),  # User registration
    path('account/login/', views.user_login, name='login'),  # User login
    path('cases/', views.case_file_list, name='CASE_FILE'),
    #path('cases/create/', views.create_case, name='create_case'),  # URL for creating a case
    #path('cases/update/<int:case_id>/', views.update_case, name='update_case'),  # URL for updating a case
    path('judges/', views.judge_list, name='judge_list'),
    path('judge_dashboard/', views.judge_dashboard, name='judge_dashboard'),
    path('dashboard/', views.litigant_dashboard, name='litigant_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('submit_case/', views.submit_case, name='submit_case'),
    path('judges/<int:judge_id>/cases/', views.judge_case_list, name='judge_case_list'),
    path('drop_case/', views.drop_case, name='drop_case'),
    path('login/', RoleBasedLoginView, name='login')
]