from django.http import HttpResponse
from django.shortcuts import render
def base(request):
    return render(request,'blog/base.html')

def home(request):
    return render(request, 'blog/home.html')


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')
