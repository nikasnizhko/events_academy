from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from events.models import Event, Guest
from events.serializers import EventSerializer, EventGuestsSerializer


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventDetail(APIView):
    def get(self, request, pk):
        try:
            event = Event.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response(data={"message": "Not found"}, status=404)
        serializer = EventSerializer(instance=event)

        return Response(data=serializer.data)

    def delete(self, request, pk):
        try:
            event = Event.objects.get(id=pk).delete()
        except Event.DoesNotExist:
            return Response(data={"message": "Not found"}, status=404)

        return Response(data={"message": "Object deleted successfully"}, status=204)


#
# ALready have this functionality inside ListCreate Api view
# class EventCreate(APIView):
#
#     def post(self, request):
#         payload = request.data
#         serializer = EventSerializer(data=payload)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=201)
#         else:
#             return Response(data={"message":"Invalid"}, status=400)


class AllEventsGuests(generics.ListAPIView):
    queryset = Event.objects.all().prefetch_related("guests")
    serializer_class = EventGuestsSerializer


class EventGuests(generics.RetrieveAPIView):
    pass
