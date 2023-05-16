"""
URL configuration for pos project.

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
from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from .views import POSView, transaction_success, CreateEventView, event_created, NewUserView, new_user_created, EventListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', POSView.as_view(), name='pos'),
    re_path('^success/(?P<transaction_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', transaction_success, name='transaction_success'),
    path('create_event/', CreateEventView.as_view(), name='create_event'),
    re_path('event_created/(?P<event_id>\d+)/', event_created, name='event_success'),
    path('users/login/', auth_views.LoginView.as_view(), name='auth_login'),
    path('users/logout/', auth_views.LogoutView.as_view(), name='auth_logout'),
    path('create_user/', NewUserView.as_view(), name='create_new_user'),
    re_path('user_created/(?P<user_id>\d+)/', new_user_created, name='new_user_success'),
    path('events/', EventListView.as_view(), name='event_list'),
]
