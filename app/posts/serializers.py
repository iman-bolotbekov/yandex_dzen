from django.db import IntegrityError
from rest_framework import serializers

from .models import Post, Comment, StatusPost,StatusType
from .telegramBot import bot


class PostSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source='get_status')

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author', ]

    def create(self, validated_data):
        user = self.context['request'].user
        chat_id = user.author.telegram_chat_id
        try:
            obj = Post.objects.create(**validated_data)
            obj.save(
                bot.sendMessage(chat_id, 'New post created!')
            )
        except IntegrityError:
            return obj


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'post']


class StatusPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusPost
        fields = '__all__'
        read_only_fields = ['author', ]


class StatusTypeSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source='get_status')

    class Meta:
        model = StatusType
        fields = '__all__'
        read_only_fields = ['post', 'author']