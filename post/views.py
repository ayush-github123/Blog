from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .models import post
# Create your views here.


def home(request):
    return render(request, 'home.html')

def register(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']


        if User.objects.filter(username=username).exists(): # check if username already exists
            messages.error(request, 'Username already exists')
            return render(request, 'register.html')
        
        if User.objects.filter(email=email).exists(): # check if email already exists
            messages.error(request, 'Email aleardy exists')
            return render(request, 'register.html')

        if(password != confirm_password): # check if password and confirm password are the same
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')
        
        user = User.objects.create_user(username=username, email=email, password=password) # create user
        user.save()
        messages.success(request, 'Registration Successfull, Please Login')
        return redirect('login-page')

    else:
        return render(request, 'register.html')



def login_page(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password) # authenticate user

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {username}!")
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'login.html')

    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def blogs(request):
    posts = post.objects.all().order_by('-created_at')
    return render(request, 'blogs.html', {'posts': posts})

@login_required(login_url='login-page')
def add_blog(request):
    if request.method == "POST":
        title = request.POST['Title']
        content = request.POST['Content']
        author = request.user.username
        post.objects.create(title=title, content=content, user=request.user)
        # messages.success(request, 'Blog Added Successfully')

        return redirect('blogs')
    
    return render(request, 'add_blog.html')


@login_required(login_url='login-page')
def blog_detail(request, pk):
    posts = get_object_or_404(post, pk=pk)
    return render(request, 'blog_detail.html', {'posts': posts})


@login_required(login_url='login-page')
def delete_blog(request, pk):
    posts = get_object_or_404(post, pk=pk)
    if request.method == "POST":
        posts.delete()
        return redirect('blogs')
    return redirect('blogs')

@login_required(login_url='login-page')
def edit_blog(request, pk):
    posts = get_object_or_404(post, pk=pk, user=request.user)
    
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        
        if not title.strip() or not content.strip():
            messages.error(request, 'Both field are required')
            return render(request, 'edit_blog.html')
        
        posts.title = title
        posts.content = content
        posts.save()
        return redirect('blogs')
    return render(request, 'edit_blog.html', {'posts': posts})