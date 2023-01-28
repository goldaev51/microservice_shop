from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    title = models.TextField(max_length=3000)
    price = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0.01'))])

    def __str__(self):
        return self.title


class BookItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    place = models.CharField(max_length=1000)
    sold = models.BooleanField(default=False)


class Order(models.Model):
    user_email = models.EmailField()
    STATUS_CHOICES = [
        ('i', 'in_work'),
        ('s', 'success'),
        ('f', 'fail'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='o')
    delivery_address = models.TextField(max_length=4000)
    order_id_in_shop = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


    def __str__(self):
        return f'Order {self.id}'



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.id}'


class OrderItemBookItem(models.Model):
    order_item = models.ForeignKey(OrderItem, related_name='order_items', on_delete=models.CASCADE)
    book_item = models.ForeignKey(BookItem, related_name='book_items', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}'
