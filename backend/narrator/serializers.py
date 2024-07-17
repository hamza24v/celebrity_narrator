from rest_framework import serializers
from .models import Narration

class NarrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Narration
        fields = '__all__'
        extra_kwargs = {
            'analysis': {'required': False},
        }
