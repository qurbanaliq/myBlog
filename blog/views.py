from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("You are at blog's index.")

def register(request):
    if request.method == "POST":
        return HttpResponse(request.POST.get("username"))
    else:
        return render(request, "blog/register.html", context={})