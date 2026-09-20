from django.urls import path
from . import views
urlpatterns=[
    path("place_order/",views.place_order),
    path("view_orders/",views.my_orders),
    path("assign_orders/<int:pk>/",views.assign_orders),
    path("pending_orders/",views.pending_orders),
    path("mark_delivered/<int:pk>/",views.mark_delivered),
]