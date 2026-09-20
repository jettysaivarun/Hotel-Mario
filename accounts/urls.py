from django.urls import path
from . import views
urlpatterns=[
    path("test/",views.test_api),
    path("register/",views.RegistrationView,name="register"),
    path("assign_crew/",views.assign_orders_to_deliverycrew),
]