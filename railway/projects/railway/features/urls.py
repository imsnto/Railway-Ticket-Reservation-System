from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('contact', views.contact, name='contact'),
    path('train', views.train, name='train'),
    path('edit', views.edit, name='edit'),
    path('show', views.show, name='show'),
]
