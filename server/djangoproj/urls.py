"""djangoproj URL Configuration

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
# chatgpt idea 
# from .views import RegisterView
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings





urlpatterns = [
    # path for showing the dealer page
    path('dealer/<int:dealer_id>',TemplateView.as_view(template_name="index.html")),
    # Assuming your app is named 'djangoapp'
    #  wrong place should add to the 
    #  django app urls.py -> learn why? path(route='get_dealers/', view=views.get_dealerships, name='get_dealers'),
    # add the routes for Dealers and Dealer in it. add abd set up REACT component for Dealers page 
    path('dealers/', TemplateView.as_view(template_name="index.html")),
    # new path adding for getting cars
    path('admin/', admin.site.urls),
    path('', include('djangoapp.urls')), 
    #* new path added 
    # path('logout/', TemplateView.as_view(template_name="index.html")),
    path('register/', TemplateView.as_view(template_name="index.html")),
    path('login/', TemplateView.as_view(template_name="index.html")), #LOGIN FROM Django app
    path('contact/', TemplateView.as_view(template_name="Contact.html")), # this is added 
    path('about/', TemplateView.as_view(template_name="About.html")), # this is added 
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),
    path('', TemplateView.as_view(template_name="Home.html")),
    path('postreview/<int:dealer_id>',TemplateView.as_view(template_name="index.html")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
