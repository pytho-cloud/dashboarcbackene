from django.contrib import admin
from django.urls import path ,include
from .views import * 


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",UsersViewset.as_view({'get': 'list','post':'create'}),name="user") ,
    path("<str:image_id>",ServeImageView.as_view(),name="img")
   
]
