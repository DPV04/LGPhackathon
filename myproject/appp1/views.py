from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
import requests
# from .models import NewsArticle

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(f"the username is {username}")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print("failed")
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html',{'message': 'Successfullyy'})


@login_required(login_url='login')
def home_view(request):
    # API_KEY = '76969a6ed5764751b950a1d5e7754e65'
    url = f'https://newsapi.org/v2/everything?q=tesla&from=2025-05-14&sortBy=publishedAt&apiKey=76969a6ed5764751b950a1d5e7754e65'

    response = requests.get(url,timeout=10)
    # print(response)
    data = response.json()
    # print(data)

    articles = data.get('articles', [])
    articles = [article for article in articles if article.get('description') and article.get('title')]
    # print(articles)
    return render(request, 'home.html',{"news":articles[:10]})

def logout_view(request):
    logout(request)
    return redirect('login')
