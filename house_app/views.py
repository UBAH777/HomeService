from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import HouseCreateSerializer
from .serializers import FlatCreateSerializer
from .serializers import HouseFlatListSerializer
from .serializers import FlatStatusUpdateSerializer
from .models import Houses, Flats


class HouseCreateView(APIView):
    def post(self, request):
        serializer = HouseCreateSerializer(data=request.data)
        if serializer.is_valid():
            house = serializer.save()
            return Response(
                HouseCreateSerializer(house).data,
                status=200,
            )
        return Response(serializer.errors, status=400)
    


class FlatCreateView(APIView):    
    def post(self, request):
        serializer = FlatCreateSerializer(
            data=request.data,
            context={'request': request}  # Передаем запрос в контекст
        )
        
        if serializer.is_valid():
            flat = serializer.save()
            return Response(serializer.data, status=200)
        
        return Response(serializer.errors, status=400)
    

class HouseFlatListView(APIView):
    def get(self, request, id):
        try:
            house = Houses.objects.get(pk=id)
        except Houses.DoesNotExist:
            raise Exception("Дом с указанным ID не найден")
        
        serializer = HouseFlatListSerializer(
            house,
            #context={'request': request}  # Передаем запрос для проверки прав
        )
        return Response(serializer.data)
    

class FlatUpdateStatusView(APIView):
    """"""
    def patch(self, request, id):
        try:
            flat = Flats.objects.get(pk=id)
        except Flats.DoesNotExist:
            raise Exception("Квартира с указанным ID не найдена")
        
        serializer = FlatStatusUpdateSerializer(
            instance=flat,
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)
    

