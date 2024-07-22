from rest_framework import serializers
from .models import *
from datetime import date

class PostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title','content']

    def create(self, validated_data):
        # Add author and published_date to validated_data
        validated_data['author'] = self.context.get('user')
        validated_data['published_date'] = date.today()

        # Create the Post instance
        post = Post.objects.create(**validated_data)

        # Return serialized representation of the created instance
        return self.to_representation(post)

    def to_representation(self, instance):
        # Serialize the instance to include all fields
        data = super().to_representation(instance)
        return data
    

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Like
        fields="__all__"

class PostSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'published_date', 'author', 'comment', 'like_count']

    def get_like_count(self, obj):
        return obj.like.count()