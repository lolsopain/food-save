from django.shortcuts import render

def home(request):
    # Asosiy manzilga kirganda birinchi bo'lib login oynasi ochiladi
    return render(request, "login.html")

def foods_page(request):
    # Ovqatlar sahifasi uchun mo'ljallangan shablon
    return render(request, "food.html")