from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm,UserForm,UserProfileForm
from .models import StaffProfile, Favorites, TradingCard, Wishlist, Sold, Cart, UserPaymentMethod
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q

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
###
@login_required()
def SelfServiceWishlist(request):
    if(request.method == "GET"):
        user = request.user
        wishlists = list(Wishlist.objects.filter(user = user).values())
        wishlist = [wishlist["card_id"] for wishlist in wishlists]
        cards = list(TradingCard.objects.filter(pk__in = wishlist).values())
        return render(request,'dashboard/wishlist.html',{"wishlists":cards})

###
@login_required()
def CreateWishlist(request):
    if(request.method == "GET"):
        id = request.GET.get("id")
        card = TradingCard.objects.get(id = id)
        card.save()
        wishlist =  Wishlist(user = request.user, card = card)
        wishlist.save()
        return HttpResponse(status=200)
###
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
        user = int(request.GET.get("user_id"))
        wishlists = list(Wishlist.objects.filter(user__id = user).values())
        print(wishlists)
        wishlist = [wishlist["card_id"] for wishlist in wishlists]
        print(wishlist)
        cards = list(TradingCard.objects.filter(pk__in = wishlist).values())
        print(cards)
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

def MarketplaceDetail(request):
    if(request.method == "GET"):
        item = request.GET.get("item_id")
        card = TradingCard.objects.get(pk=item)
        print(card)
        if(card != None):
            return render(request,'store/product-details.html',{'card':card})
        else:
            return HttpResponse(status=404)        

#@login_required
def Purchases(request):
    if(request.method == "GET"):
        user = request.user
        sold_list = list(Sold.objects.filter(user = user).values())
        sold = [sold["card_id"] for sold in sold_list]
        cards = list(TradingCard.objects.filter(pk__in = sold).values())
        cards = zip(cards,sold_list)
        return render(request,'dashboard/sold.html',{"sold":cards})

#@login_required
def RemoteCart(request):
    if(request.method == "GET"):
        user = request.user
        cart_list = list(Cart.objects.filter(user = user).values())
        cart = [cart["card_id"] for cart in cart_list]
        cards = list(TradingCard.objects.filter(pk__in = cart).values())
        total = 0
        for card in cards:
            total += card["price"]
        payment = list(UserPaymentMethod.objects.filter(user = user).values())
        cards = zip(cards,cart_list)
        return render(request,'store/cart.html',{"cart":cards,"payment_methods":payment,"total":total})

#@login_required
def AddRemoteCart(request):
    if(request.method == "GET"):
        user = request.user
        id = request.GET.get("item_id")
        card = TradingCard.objects.get(id = id)
        if(card.stock != 0):
            cart = Cart(user = user, card = card, count = 1)
            cart.save()
        return redirect("/store/")
        

#@login_required
def RemoveRemoteCart(request):
    if(request.method == "GET"):
        user = request.user
        id = request.GET.get("item_id")
        cart = Cart.objects.get(pk=id)
        cart.delete()
        return redirect("/store/cart")

#@login_required
def UpdateRemoteCart(request):
    if(request.method == "GET"):
        user = request.user
        id = request.GET.get("item_id")
        count = int(request.POST.get("count"))
        cart = Cart.objects.get(pk=id)
        card = cart.card
        
        if(count>0 and card.stock>=count):
            cart.count = count
            cart.save()
        elif(count == 0):
            user = request.user
            id = request.GET.get("item_id")
            cart = Cart.objects.get(pk=id)
            cart.delete()
        return redirect("/store/cart")

#@login_required
def CreditCardScreen(request):
    if(request.method == "GET"):
        payment = list(UserPaymentMethod.objects.filter(user = request.user).values())
        return render(request,'store/checkout.html',{"payment_methods":payment,"showPayment":len(payment)!=0})

#@login_required
def AddPaymentMethod(request):
    if(request.method == "POST"):
        
        card_number = request.POST["card_number"]
        cvv = request.POST["cvv"]
        expire_date = request.POST["expire_date"]
        card_owner = request.POST["card_owner"]
        payment_method = UserPaymentMethod(user = request.user,cvv = cvv, credit_card = card_number,owner_name = card_owner,date = expire_date)
        payment_method.save()
        return redirect("/store/payment_methods")

#@login_required
def DeletePaymentMethod(request):
    if(request.method == "GET"):
        payment_method = UserPaymentMethod.objects.get(pk = request.GET.get("id"))
        payment_method.delete()
        return redirect("/store/payment_methods")

def TffBranches(request):
    return render(request, "dashboard/branches.html")

def aboutus(request):
    return render(request, "dashboard/aboutus.html")

def buy(request):
    if(request.method == "GET"):
        user = request.user
        cart_list = list(Cart.objects.filter(user = user).values())
        cart = [cart["card_id"] for cart in cart_list]
        cards = list(TradingCard.objects.filter(pk__in = cart).values())
        total = 0
        for card in cards:
            total += card["price"]
        payment = list(UserPaymentMethod.objects.filter(user = user).values())
        cards = zip(cards,cart_list)
        return render(request,"store/buy.html",{"cart":cards,"payment_methods":payment,"showPayment":len(payment)!=0,"total":total})

@login_required
def addPurchase(request):
    if(request.method == "GET"):
        user = request.user
        id = request.GET.get("item_id")
        pk = request.GET.get("pk_id")
        card = TradingCard.objects.get(id = id)
        sold = Sold(user = user, card = card, count = 1)
        sold.save()
        cart = Cart.objects.get(pk=pk)
        cart.delete()
        return redirect("/dashboard/purchases")

