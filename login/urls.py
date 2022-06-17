from django.urls import path, include
from login.views import   login_page


urlpatterns = [
    path('', login_page, name='login_page'),

]
