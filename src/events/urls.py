from django.urls import path
from rest_framework.schemas import get_schema_view

from .views import EventAPIView


app_name = 'events'


urlpatterns = [
    path('', get_schema_view(
        title='Lot 9',
        description='API for events',
        version='0.0.1'
    ), name='openapi-schema'),
    path('events/', EventAPIView.as_view()),
]
