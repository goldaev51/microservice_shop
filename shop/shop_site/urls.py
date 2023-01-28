from django.urls import path

from . import views

app_name = 'books'
urlpatterns = [
    path('', views.BooksListView.as_view(), name='books-list'),
    path('book/<int:book_id>', views.book_details, name='books-details'),
    path('create/', views.order_create, name='order-create'),

]

