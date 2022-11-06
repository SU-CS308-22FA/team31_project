from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm,UserForm,UserProfileForm
from .models import StaffProfile
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.

def Login(request):
    if(request.method == "GET"):
        if(request.user.is_authenticated):
            return redirect("/dashboard/")
        else:
            return render(request,'auth/login2.html')
    elif(request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username,password = password)
        if user is not None:
            if user.is_active:
                login(request, user) 
                return redirect('/dashboard/')
            else:
                msg=('You account has been deactivated!')
        else:
            msg=('Invalid Login credentials, try again!')
        return render(request,'auth/login2.html',{'message':msg})

def Signup(request):
    if(request.method=='GET'):
        user = UserCreationForm()
        return render(request,'auth/register2.html',{'form':user,'title':"Registration"})
    elif(request.method=='POST'):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            form.is_active = True
            user = form.save()
            login(request, user) 
            return redirect('/dashboard/')
        else:
            print(form.errors.as_data()) # here you print errors to terminal
            return render(request,'auth/register2.html',{'error_form':form,'form':form,'title':"Registration"})
    else:
        return "page_not_found(request)"

@login_required()
def DashboardUser(request):
    if(request.method == 'POST'):
        profile = UserProfileForm(request.POST,instance=request.user.user_profile)
        if(profile.is_valid()):
            profile.save()
        return redirect('/dashboard/')
    elif(request.method=="GET"):
        return render(request,'dashboard/profile.html')
    else:
        return page_not_found(request)

@login_required()
def UpdateProfile(request):
    if(request.method == "GET"):
        return render(request,'dashboard/profile.html')
    elif(request.method == "POST"):
        user =  UserForm(request.POST,instance=request.user)
        profile = UserProfileForm(request.POST,instance=request.user.user_profile)
        print(user.errors)
        if(user.is_valid()):
            print(request.user.first_name)
            user.save()
        if(profile.is_valid()):
            profile.save()
        return redirect('/dashboard/profile')

@login_required()
def DeleteAccount(request):
    if(request.method == "GET"):
        user = request.user
        user.is_active = False
        user.save()
        return redirect('/signup')


@login_required()
def Logout(request):
    logout(request)
    return redirect("/login")
