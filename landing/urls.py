from django.urls import path
from landing import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('upload/', views.upload, name='upload'),
    path('customerjourneyupload/', views.customerjourneyupload, name='customerjourneyupload')

]