from django.urls import path
from . import views

urlpatterns = [
    path('tracker/', views.transaction, name='transaction'),
    path('',views.index, name='index'),
    path('add_transaction/',views.add_transaction, name ="add_transaction"),
   path('delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),
   path('edit/<int:pk>/', views.edit_transaction, name='edit_transaction'),

]