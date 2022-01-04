from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as _login, logout as _logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from . import models

@login_required
def index(request):
    """shwo the index page for the blog
    """
    return HttpResponse("You are at blog's index, {}".format(
            request.user.first_name
        ))

def register(request):
    """shows the registration form to the user and registers the user
    """
    if request.method == "POST":
        # assume fields are validated on client side
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        # create user when it doesn't already exist
        if not User.objects.filter(Q(username=username) | Q(email=email)):
            if password:
                User.objects.create_user(username=username, email=email,
                    first_name=first_name, last_name=last_name,
                    password=password)
                # on success, redirect to login page
                return redirect(reverse("blog:login"))
            return render(request, "blog/register.html",
                context={"error": "Password field can't be empty."})
        return render(request, "blog/register.html",
            context={"error": "User already registered."})
    return render(request, "blog/register.html", context={})

def login(request):
    """logs a user in
    """
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    _login(request, user)
                    # on success, get the 'next' arg and redirect
                    nxt = request.GET.get("next")
                    print(nxt)
                    if nxt:
                        return redirect(nxt)
                    return redirect(reverse("blog:index"))
                return render(request, "blog/login.html",
                    context={"error": "Inactive user."})
            return render(request, "blog/login.html",
                context={"error": "Wrong credidentials."})
        return render(request, "blog/login.html", context={})
    return redirect(reverse("blog:index"))

def logout(request):
    """logs a user out
    """
    if request.user.is_authenticated:
        _logout(request)
        return HttpResponse("You're logged out.")
    return HttpResponse("You're not logged in.")

@login_required
def post_create(request):
    """create a new blog post
    """
    if request.method == "POST":
        # assume fields are validated on client side
        title = request.POST.get("title")
        body = request.POST.get("body")
        new_post = models.Post.objects.create(title=title, post_text=body,
            author=request.user)
        return redirect(reverse("blog:post_detail", args=(new_post.id,)))
    return render(request, "blog/post_create.html", context={})

def post_detail(request, pk):
    """displays a specific blog post
    """
    post = models.Post.objects.get(pk=pk)
    return render(request, "blog/post_detail.html", context={"post": post})
