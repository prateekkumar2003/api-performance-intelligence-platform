from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import DummyData
import time

# Create your views here.
class HealthCheckView(APIView):
    def get(self, request):
        return Response({
            "status": "ok",
            "message": "API Intelligence Platform running"
        })

class DummyAPIView(APIView):

    def get(self, request):

        data = DummyData.objects.all()

        response = []

        for item in data:
            response.append({
                "id": item.id,
                "name": item.name
            })

        return Response(response)


class SlowAPIView(APIView):

    def get(self, request):

        time.sleep(2)

        return Response({
            "message": "slow api"
        })