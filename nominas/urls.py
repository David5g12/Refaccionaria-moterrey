from django.urls import path
from . import views

app_name = 'nominas'

urlpatterns = [
    path('', views.index, name='index'),
    path('tablas_pdf/', views.tablas_pdf, name='tablas_pdf'),
    

]
