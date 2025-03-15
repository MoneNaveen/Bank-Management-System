from django.urls import path
from . import views
urlpatterns = [
    path('',views.Home,name="Home"),
    path('Profile',views.Profile_creation,name="Profile"),
    path("Pin",views.Pin_generation,name="Pin_generation"),
    path('Balance',views.Balance,name="Balance"),
    path('Money_withdrawl',views.Withdrawl,name="Money_withdrawl"),
    path('Deposit',views.Deposit,name="Deposit"),
    path('Money_transefer',views.Money_transfer,name="Money_transefer"),
]