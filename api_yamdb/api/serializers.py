from rest_framework import serializers

from .models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)
