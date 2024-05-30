from django.contrib import admin
from django.urls import path ,include
from .views import * 


urlpatterns = [
    path('admin/', admin.site.urls),
    path("/users",UsersViewset.as_view({'get': 'list','post':'create'}),name="users") ,
    path("/images/<str:image_id>/",ServeImageView.as_view(),name="img")
   
]
