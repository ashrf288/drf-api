from django.shortcuts import render
# Create your views here.
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Blog
from .serializers import BlogSterilizer


class BlogsList(ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSterilizer

class BlogDetail(RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSterilizer