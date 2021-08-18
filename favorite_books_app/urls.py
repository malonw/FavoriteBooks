from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('update/<int:id>', views.update),
    path('edit/<int:id>', views.edit),
    path('books', views.books),
    path('add_book', views.add_book),
    path('favorite/<int:id>', views.favorite),
    path('destroy/<int:id>', views.destroy),
    path('details/<int:id>', views.details),
    path('my_favorites', views.my_favs),
]
