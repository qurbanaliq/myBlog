from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as _login, logout as _logout
from django.contrib.auth.decorators import login_required

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
        return HttpResponse(request.POST.get("username"))
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
                    nxt = request.POST.get("next")
                    if nxt:
                        return redirect(nxt)
                    return redirect(reverse("blog:index"))
                return HttpResponse("Inactive user")
            return render(request, "blog/login.html", context={"error": "Wrong credidentials"})
        return render(request, "blog/login.html", context={})
    return redirect("/blog")

def logout(request):
    """logs a user out
    """
    if request.user.is_authenticated:
        _logout(request)
        return HttpResponse("You're logged out.")
    return HttpResponse("You're not logged in.")
