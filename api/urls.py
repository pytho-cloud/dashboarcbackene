from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"/users", UsersViewset, basename="user")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("/images/<str:image_id>/", ServeImageView.as_view(), name="img"),
    path("", include(router.urls)),
]
