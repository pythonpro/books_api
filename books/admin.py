from django.contrib import admin

from .models import Book, Shop, Publisher, ShopBookInfo


class ShopBookInfoInline(admin.TabularInline):
    model = ShopBookInfo


class ShopAdmin(admin.ModelAdmin):
    inlines = [ShopBookInfoInline]


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'publisher']


admin.site.register(Book, BookAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Publisher)
