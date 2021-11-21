from django.urls import path
from .views import BlogsList, BlogDetail

urlpatterns = [
    path('', BlogsList.as_view(), name='posts_list'),
    path('<int:pk>/', BlogDetail.as_view(), name='posts_detail'),
]