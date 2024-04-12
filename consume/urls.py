from django.contrib import admin
from django.urls import path, include
from root.views import index, order

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="home"),
    path("order/", order, name="order"),
    path("accounts/", include("django.contrib.auth.urls")),
]
