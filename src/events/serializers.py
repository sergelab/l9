from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class AttrsListSerializer(serializers.ListField):
    name = serializers.CharField(required=True)
    pattern = serializers.CharField(required=True)


class EventSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    pattern = serializers.CharField(required=True)
    data = AttrsListSerializer(min_length=1)

    def create(self, validated_data):
        return validated_data


class EventOutSerializer(EventSerializer):
    id = serializers.CharField(required=True)


class EventsListSerializer(serializers.Serializer):
    events = serializers.ListField(EventOutSerializer())
