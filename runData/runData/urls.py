"""
URL configuration for runData project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from apps.Average_annual_total_salary_in_city import views as Average_annual_total_salary_in_city_views
from apps.Number_of_newborns import views as Number_of_newborns_views
from apps.main_web import views as main_web_views
from apps.Income_and_expenses import views as Income_and_expenses_views
from apps.Population_to_age_ratio import views as Population_to_age_ratio_views
from apps.Cram_school import views as Cram_school_views
from apps.Occupational_ratio import views as Occupational_ratio_views
from apps.Course import views as Course_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',main_web_views.index,name=''),
    path('Number_of_newborns_views/',Number_of_newborns_views.index,name='Number_of_newborns_views'),
    path('Average_annual_total_salary_in_city_views/',Average_annual_total_salary_in_city_views.index,name='Average_annual_total_salary_in_city_views'),
    path('Income_and_expenses_views/',Income_and_expenses_views.index,name='Income_and_expenses_views'),
    path('Population_to_age_ratio_views/',Population_to_age_ratio_views.index,name='Population_to_age_ratio_views'),
    path('Cram_school_views/',Cram_school_views.index,name='Cram_school_views'),
    path('Occupational_ratio_views/',Occupational_ratio_views.index,name='Occupational_ratio_views'),
    path('Course_views/',Course_views.index,name='Course_views'),
]

