from django.shortcuts import render
from django.shortcuts import render

def foods_page(request):
    return render(request, "food.html")
def home(request):
    return render(request, "login.html")
def home(request):
    return render(request, 'food.html')