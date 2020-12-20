from rest_framework import serializers
from .models import Tasks


class TaskSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Tasks
        fields = ('id', 'name', 'description', 'done')
