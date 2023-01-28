from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views import generic

from cart.cart import Cart
from cart.forms import CartAddBookForm
from .forms import OrderCreateForm
# from shop.core import settings
from .models import Book, OrderItem
from .tasks import api_send_order


class BooksListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'shop_site/book_details.html'


def book_details(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart_book_form = CartAddBookForm()
    return render(request, 'shop_site/book_details.html', {'book': book,
                                                           'cart_book_form': cart_book_form})


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            order_items = list()
            for item in cart:
                order_item = OrderItem(order=order, book=item['book'], quantity=item['quantity'])
                order_items.append(order_item)
            OrderItem.objects.bulk_create(order_items)
            api_send_order.delay(order.id)
            # очистка корзины
            cart.clear()
            return render(request, 'shop_site/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'shop_site/order/create.html',
                  {'cart': cart, 'form': form})
