from contextlib import redirect_stderr
from email import contentmanager, message
from multiprocessing import context
import re
import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import forms
from .models import Post
from django.utils.text import slugify
from django.db.models import Q
from datetime import datetime

# Create your views here.

from .models import *


def post_list_view(request):
    post_objects = Post.objects.all()
    post_filtered = []

    for post in post_objects:
        if not request.user in post.author.profile.blockedUsers.all():
            post_filtered.append(post)
    post_objects=post_filtered
    context = {
        'post_objects':post_objects
    }
    return render(request,'posts.html',context)

# def post_list_view(request):
#     post_objects = Post.objects.all()
#     context = {
#         'post_objects':post_objects
#     }
#     return render(request,'posts.html',context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('posts')
    else:
        form = AuthenticationForm()
    return render(request,"login.html",{'form':form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('posts')

# def homepage_view(request):
#     if request.user.is_authenticated:
#         return redirect('posts')
#     else:
#         return redirect('login')

@login_required(login_url="../../login/")
def blog_create(request):
    if request.method == 'POST':
        form = forms.CreateBlog(request.POST,request.FILES)
        if form.is_valid:
            instance = form.save(commit=False)
            instance.slug = slugify(instance.title)
            instance.author = request.user
            instance.save()
            return redirect('posts')
    else:
        form = forms.CreateBlog()
    return render(request,'add-blog.html',{'form':form})

@login_required(login_url="../login/")
def profile_view(request):
    posts=Post.objects.filter(author=request.user)
    return render(request,'profile.html',{'posts':posts})

@login_required(login_url="../../login/")
def post_detail_view(request,pk):
    post = get_object_or_404(Post, id=pk)


    if request.user in post.author.profile.blockedUsers.all():
        return redirect('blocked_post')

    if request.method == 'POST':
        form=forms.CommentForm(request.POST)

        if form.is_valid():
            comment=form.save(commit=False)
            comment.author=request.user
            comment.post=post
            comment.save()

            return redirect('post_detail',pk=post.id)
    else:
        form=forms.CommentForm()

    return render(request, 'post_detail.html',{'post':post,'form':form})

@login_required(login_url="../../login/")
def user_view(request,username):
    user = User.objects.get(username=username)
    if user == request.user:
        return redirect('profile')
    posts=Post.objects.filter(author=user)
    return render(request,'user.html',{'user':user,'posts':posts})

@login_required(login_url="../login/")
def search(request):

    if request.method == "POST":
        searched = request.POST['searched']
        posts=Post.objects.filter(Q(title__icontains=searched) |  Q(body__icontains=searched))
        return render(request, 'search.html', {'posts':posts,'searched':searched})
    else:
        return render(request,'search.html',{})

def filterDate(request):

    if request.method == "POST":
        searched = request.POST['searched']
        startDate = request.POST['startDate']
        endDate = request.POST['endDate']
        if not startDate:
            startDate='1900-01-01'
        if not endDate:
            endDate='2100-01-01'
        sdt = datetime.strptime(startDate, "%Y-%m-%d")
        startDate = sdt.replace(hour=0, minute=0)
        
        sdt = datetime.strptime(endDate, "%Y-%m-%d")
        endDate = sdt.replace(hour=23, minute=59)


        posts=Post.objects.filter(Q(title__icontains=searched) |  Q(body__icontains=searched))
        posts=posts.filter(created_at__range=[startDate,endDate])
        return render(request, 'search.html', {'posts':posts,'searched':searched})
    else:
        return render(request,'search.html',{})

def about_view(request):
    return render(request,'about.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['inputUsername']
        password = request.POST['inputPassword']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('posts')
            # Redirect to a success page. 
        else:
            # Return an 'invalid login' error message.
            messages.success(request,("Error logging in... Try again..."))
            return redirect('login')
    else:
        return render(request,'newlogin.html')

@login_required(login_url="../../login/")
def blocked_users_view(request):

    return render(request,'blocked-users.html',{})

def blocked_post_view(request):
    return render(request,'blocked-post-page.html')


def unblock_user_view(request,username):
    user = User.objects.get(username=username)
    request.user.profile.blockedUsers.remove(user)
    posts=Post.objects.filter(author=user)
    return render(request,'user.html',{'user':user,'posts':posts})

def block_user_view(request,username):
    user = User.objects.get(username=username)
    request.user.profile.blockedUsers.add(user)
    posts=Post.objects.filter(author=user)
    return render(request,'user.html',{'user':user,'posts':posts})



def edit_profile_view(request):
    profileForm = forms.EditProfile(instance=request.user.profile)
    userForm = forms.EditUser(instance=request.user)
    
    if request.method == 'POST':
        profileForm = forms.EditProfile(request.POST,request.FILES,instance=request.user.profile)
        userForm = forms.EditUser(request.POST,instance=request.user)
        if profileForm.is_valid and userForm.is_valid:
            profile = profileForm.save(commit=False)
            user = userForm.save(commit=False)
            user.save()
            profile.user=user
            profile.save()
            
            return redirect('profile')
    
    return render(request,'edit-profile.html',{'profileForm':profileForm, 'userForm':userForm})

def edit_post_view(request,pk):
    post=get_object_or_404(Post, id=pk)
    form = forms.EditPost(instance=post)

    if(request.user != post.author):
        return render(request,'error-page.html',{})

    if request.method == 'POST':
        form = forms.EditPost(request.POST,request.FILES,instance=post)
        if form.is_valid:
            updatedPost = form.save(commit=False)
            updatedPost.last_edited_at = datetime.now()
            updatedPost.save()
            return redirect('post_detail',pk=post.id)

    return render(request,'edit-blog.html',{'form':form})

def edit_comment_view(request,pk):
    comment = get_object_or_404(Comment, id=pk)
    form = forms.CommentForm(instance=comment)


    if request.user in comment.post.author.profile.blockedUsers.all() or (request.user != comment.author and request.user != comment.post.author):
        return render(request, 'error-page')
    
    if request.method == 'POST':
        form=forms.CommentForm(request.POST,instance=comment)

        if form.is_valid():
            updatedComment=form.save(commit=False)
            updatedComment.author=comment.author
            updatedComment.createdAt=comment.created_at
            updatedComment.save()

            return redirect('post_detail',pk=comment.post.id)

    return render(request, 'edit-comment.html',{'form':form})

def newlogin_view(request):
    return render(request,'newlogin.html',{})
    