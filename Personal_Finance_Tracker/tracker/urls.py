from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.index, name='index'),
    path('transactions/', views.transaction, name='transaction'),
    path('transaction/add/', views.add_transaction, name='add_transaction'),
    path('transaction/edit/<int:pk>/', views.edit_transaction, name='edit_transaction'),
    path('transaction/delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]