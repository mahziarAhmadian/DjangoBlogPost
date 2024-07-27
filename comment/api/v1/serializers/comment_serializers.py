from rest_framework import serializers
from comment.models.comments import Comment


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'user_profile', 'content']
        # required_fields = ['post', 'user_profile', 'content']


class ReplayCreateSerializer(serializers.ModelSerializer):
    parent_id = serializers.CharField(max_length=200, write_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'parent_id']
        # required_fields = ['post', 'user_profile', 'content']

    def create(self, validated_data):
        print("validated_data", validated_data)
        parent_instance = Comment.objects.get(id=validated_data.get('parent_id'))
        post = parent_instance.post
        user_profile = parent_instance.user_profile
        content = validated_data.get('content')
        obj = Comment.objects.create(content=content, post=post, user_profile=user_profile, parent=parent_instance)
        return obj


class CommentUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']


class PeriodicDeleteSerializer(serializers.ModelSerializer):
    date_time = serializers.DateTimeField(required=True)

    class Meta:
        model = Comment
        fields = ['date_time']
