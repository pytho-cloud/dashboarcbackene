from django.shortcuts import render, HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view
from .connection import user_collection, db, fs
from .serializer import *
from datetime import datetime
from bson import ObjectId
from django.http import Http404


class UsersViewset(ListModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserModelSerializer

    def get_queryset(self):
        documents = list(user_collection.find({}, {"_id": 0}))
        return documents

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print("data is going")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):

        user = user_collection.find_one({"name": pk}, {"_id": 0})

        if not user:
            raise NotFound(detail="User not found", code=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(user)
        print(serializer.data ,"this is my single data")

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data, "sdffff")

        image = request.FILES.get("img")
        if image:
            image_id = self.handle_image_upload(image)
            image_id_str = str(image_id)
        else:
            image_id_str = None

        user = {
            "name": data.get("name"),
            "email": data.get("email"),
            "created_at": datetime.now(),
            "roll": data.get("roll"),
            "img": image_id_str,
        }

        user_collection.insert_one(user)

        return Response(status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        data = request.data

        user = user_collection.find_one({"name": pk})

        if not user:
            return NotFound(detail="User is not prsent", code=status.HTTP_404_NOT_FOUND)

        image = request.FILES.get("img")

        if image:
            image_id = self.handle_image_upload(image)
            image_id_str = str(image_id)
        else:
            image_id_str = None

        user_data = {
            "$set": {
                "name": data.get("name"),
                "email": data.get("email"),
                "created_at": datetime.now(),
                "roll": data.get("roll"),
                "img": image_id_str,
            }
        }

        users = user_collection.update_one({"name": pk}, user_data)

        return Response("Update data more successfully", status=status.HTTP_200_OK)

    def handle_image_upload(self, image):

        image_id = fs.put(image, filename=image.name, content_type=image.content_type)
        return image_id


class ServeImageView(APIView):
    def get(self, request, image_id):
        try:
            file_id = ObjectId(image_id)
            grid_out = fs.get(file_id)
            # Set the Content-Type header to indicate that the response contains image data
            response = HttpResponse(grid_out.read(), content_type=grid_out.content_type)
            response["Content-Disposition"] = f"inline; filename={grid_out.filename}"
            return response
        except Exception as e:
            print(e)
            raise Http404("Image not found")


# This is View for update more information about user function based views


@api_view(["GET", "POST"])
def add_more_user_data(request, pk=None):
    if request.method == "POST":

        data = request.data
        user = data.get("user_name")
        user_stock = data.get("user_stock", "data is not come")
        user_sales = data.get("user_sales", 0)
        user_special_id = data.get("user_special_id", "not set")

        update_details = {
            "user_stock": user_stock,
            "user_sales": user_sales,
            "user_special_id": user_special_id,
        }

        update_query = {
            "$push": {"user_details": update_details},
            "$currentDate": {"updated_at": True},
        }

        users = user_collection.update_one({"name": user}, update_query)

        return Response(
            "Update data more successfully {}".format(users), status=status.HTTP_200_OK
        )

        return Response({"message": user_stock})

    return Response({"message": "Hello, world!"})
