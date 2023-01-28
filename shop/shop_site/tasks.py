from celery import shared_task
from .models import Order


@shared_task
def api_send_order(order_id):
    print(f'order_id: {order_id}')
    order = Order.objects.get(id=order_id)
    order_items = order.items.all()
    print(order)
    print(order_items)
