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
from django.urls import path, re_path

from .views import POSView, transaction_success, CreateEventView, event_created

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', POSView.as_view(), name='pos'),
    re_path('^success/(?P<transaction_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', transaction_success, name='transaction_success'),
    path('create_event/', CreateEventView.as_view(), name='create_event'),
    path('event_created/(?P<event_id>\d+)/', event_created, name='event_success'),
]
