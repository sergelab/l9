from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


from .serializers import EventSerializer, EventOutSerializer, EventsListSerializer
from .handler import EventApi


class EventAPIView(APIView):
    def __init__(self, *args, **kwargs):
        self.api = EventApi()
        super(EventAPIView, self).__init__(*args, **kwargs)

    def get(self, request):
        return Response(
            EventsListSerializer(
                self.api.get_events()
            ).data
        )

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                EventOutSerializer(
                    self.api.add_event(serializer.save())
                ).data
            )

        return Response(status=422)
