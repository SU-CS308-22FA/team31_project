"""ff_web_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from portal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.Login,name="Login Page"),
    path('signup/',views.Signup,name="Sign Up Page"),
    path('dashboard/',views.DashboardUser,name="Edit Profile Page"),
    path('dashboard/profile',views.UpdateProfile,name="Edit Profile Page"),
    path('dashboard/favorites',views.SelfServiceFavorites,name="Favorites Page"),
    path('dashboard/like',views.CreateLike,name=" Save Favorite Page"),
    path('dashboard/dislike',views.RemoveLike,name="Delete Favorites Page"),
    path('dashboard/wishlist',views.SelfServiceWishlist,name="Wishlist Page"),
    path('dashboard/add_wishlist',views.CreateWishlist,name=" Save Wishlist Page"),
    path('dashboard/remove_wishlist',views.RemoveWishlist,name="Delete Wishlist Page"),
    path('public/wishlist',views.PublicWishlist,name="Public Wishlist Page"),

    path('delete_account',views.DeleteAccount,name="Delete Account Page"),
    path('logout',views.Logout,name="Logout Page")

]
