from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-quote/', views.add_quote, name='add_quote'),
    path('edit-quote/<str:q_id>/', views.edit_quote, name='edit_quote'),
    path('delete-quote/<str:q_id>/', views.delete, name='delete'),
    path('like/<str:q_id>/', views.like, name='like')
]