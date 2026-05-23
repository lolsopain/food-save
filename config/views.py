from django.shortcuts import render

def home(request):
    
    return render(request, "login.html")

def foods_page(request):
    
    return render(request, "food.html")