from rest_framework import serializers
from .models import Comment, Movie

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'score',]


class MovieSerializer(serializers.ModelSerializer):
    score_set = ScoreSerializer(many=True)
    class Meta:
        model = Movie
        fields = ['id', 'score_set',]
