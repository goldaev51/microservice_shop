from django.contrib import admin

from .models import Book, Order, OrderItem


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'quantity', 'id_in_store']
    search_fields = ['title__icontains']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['book']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status']
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'book', 'quantity']