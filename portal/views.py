from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm,UserForm,UserProfileForm
from .models import StaffProfile, Favorites, TradingCard, Wishlist
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

# Favorites
@login_required()
def SelfServiceFavorites(request):
    if(request.method == "GET"):
        user = request.user
        favorites = list(Favorites.objects.filter(user = user).values())
        favorites = [favorite["card_id"] for favorite in favorites]
        cards = list(TradingCard.objects.filter(pk__in = favorites).values())
        return render(request,'dashboard/favorites.html',{"favorites":cards})

@login_required()
def CreateLike(request):
    if(request.method == "GET"):
        id = request.GET.get("id")
        card = TradingCard.objects.get(id = id)
        card.like += 1
        card.save()
        favorite =  Favorites(user = request.user, card = card)
        favorite.save()
        return HttpResponse(status=200)

@login_required()
def RemoveLike(request):
    if(request.method == "GET"):
        id = request.GET.get("id")
        from_ = request.GET.get("from")
        card = TradingCard.objects.get(id = id)
        card.like -= 1
        card.save()
        favorite =  Favorites.objects.get(user = request.user, card = card)
        favorite.delete()
        
        if(from_ == "favorites"):
            return redirect("/dashboard/favorites")
        else:
            return HttpResponse(status=200)
    
@login_required()
def SelfServiceWishlist(request):
    if(request.method == "GET"):
        user = request.user
        wishlists = list(Wishlist.objects.filter(user = user).values())
        wishlist = [wishlist["card_id"] for wishlist in wishlists]
        cards = list(TradingCard.objects.filter(pk__in = wishlist).values())
        return render(request,'dashboard/wishlist.html',{"wishlists":cards})

@login_required()
def CreateWishlist(request):
    if(request.method == "GET"):
        id = request.GET.get("id")
        card = TradingCard.objects.get(id = id)
        card.save()
        wishlist =  Wishlist(user = request.user, card = card)
        wishlist.save()
        return HttpResponse(status=200)

@login_required()
def RemoveWishlist(request):
    if(request.method == "GET"):
        id = request.GET.get("id")
        from_ = request.GET.get("from")
        card = TradingCard.objects.get(id = id)
        card.save()
        wishlist =  Wishlist.objects.get(user = request.user, card = card)
        wishlist.delete()
        if(from_ == "wishlist"):
            return redirect("/dashboard/wishlist")
        else:
            return HttpResponse(status=200)

def PublicWishlist(request):
    if(request.method == "GET"):
        user = request.GET.get("id")
        wishlists = list(Wishlist.objects.filter(user__id = user).values())
        wishlist = [wishlist["card_id"] for wishlist in wishlists]
        cards = list(TradingCard.objects.filter(pk__in = wishlist).values())
        return render(request,'dashboard/public_wishlist.html',{"wishlists":cards})

def MarketplaceHome(request):
    if(request.method == "GET"):
        items = []
        if( request.GET.get("searchText")):
            items = list(TradingCard.objects.filter(
                Q(card_title__contains=request.GET.get("searchText")) |
                Q(card_explanation__contains=request.GET.get("searchText"))
            ))
        elif(request.GET.get("priceRate") or request.GET.get("filterType")):
            filterType = request.GET.get("filterType")

            if(filterType == "1"):
                items = list(TradingCard.objects.all().order_by('-like')[:6])
            elif(filterType == "2"):
                items = list(TradingCard.objects.all().order_by('-price')[:6])
            elif(filterType == "3"):
                items = list(TradingCard.objects.all().order_by('price')[:6])
            elif(filterType == "4"):
                items = list(TradingCard.objects.all().order_by('-id')[:6])
            elif(filterType == "5"):
                items = list(TradingCard.objects.all().order_by('id')[:6])
        else:
            items = list(TradingCard.objects.all().order_by('-id')[:6])
        return render(request,'store/index.html',{'items':items})