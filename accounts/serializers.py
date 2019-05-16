from rest_framework import serializers
from .models import Message
class MessageSerializer(serializers.ModelSerializer):
    from_name = serializers.CharField(source='message_from.username')
    to_name = serializers.CharField(source='message_to.username')
    class Meta:
        model = Message
        fields =['id','content','from_name','to_name']
    