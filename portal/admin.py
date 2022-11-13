from django.contrib import admin
from .models import StaffProfile, TradingCard, Favorites, Wishlist, Sold
from django.contrib.sessions.models import Session
import pprint

# Register your models here.
class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return pprint.pformat(obj.get_decoded()).replace('\n', '<br>\n')
    _session_data.allow_tags=True
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']
    exclude = ['session_data']

admin.site.register(Session, SessionAdmin)

class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user','company','address','city','country','postal_code')
    search_fields = ['company','address','city','country','postal_code']

admin.site.register(StaffProfile,StaffProfileAdmin)

class TradingCardAdmin(admin.ModelAdmin):
    list_display = ('card_title','card_explanation','price','stock','image','like')

admin.site.register(TradingCard,TradingCardAdmin)

class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('user','card')

admin.site.register(Favorites,FavoritesAdmin)

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user','card')

admin.site.register(Wishlist,WishlistAdmin)

class SoldAdmin(admin.ModelAdmin):
    list_display = ('user','card')

admin.site.register(Sold,SoldAdmin)


'''
# Register your models here.




class MenuLoadedAdmin(admin.ModelAdmin):
    list_display = ('id','user','menu_title','rest_name','rest_address','rest_city','rest_country','rest_postal','menu','allowed','show_allowed','change_allowed')

class DateByAccess(admin.ModelAdmin):
    list_display = ('menu_id','menu','date','count')

admin.site.register(MenuLoaded,MenuLoadedAdmin)
admin.site.register(DayByAccess,DateByAccess)
'''