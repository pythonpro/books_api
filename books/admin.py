from django.contrib import admin

from .models import Book, Shop, Publisher, ShopBookInfo


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'publisher']


class ShopBookInfoAdmin(admin.ModelAdmin):
    list_display = ['book', 'shop', 'stock']


admin.site.register(Book, BookAdmin)
admin.site.register(Shop)
admin.site.register(Publisher)
admin.site.register(ShopBookInfo, ShopBookInfoAdmin)
