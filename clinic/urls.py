from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/book/', views.book_appointment, name='book_appointment'),
    path('api/chat/', views.ai_chat, name='ai_chat'),
]