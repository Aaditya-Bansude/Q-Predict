# from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='indexpage'),
    path('aboutus', views.about, name='aboutuspage'),
    path('contactus', views.contactus, name='contactuspage'),
    path('questionbank', views.question_bank, name='questionbank'),
    path('questionpaper', views.question_paper, name='questionpaper'),
]