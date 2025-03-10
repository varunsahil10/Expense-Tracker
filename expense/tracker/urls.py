from django.urls import path
from tracker.views import *

urlpatterns = [
    path('', index, name = 'index'),
    path('delete/<id>', deleteTransaction, name = 'delete'),
    path('signup/', sign_up, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
