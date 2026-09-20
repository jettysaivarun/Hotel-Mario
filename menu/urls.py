from django.urls import path
from . import views


urlpatterns=[
    path("categories/",views.categories,name="categories"),
    path("menu_items/",views.menu_items,name="menu_items"),
    path("menu_items/<int:pk>/item_of_the_day/",views.update_item_of_the_day,name="item_of_the_day"),
]