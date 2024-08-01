from rest_framework import serializers
from accounts.models import Profile, User
from blog.models import Post, Category
from comment.models.comments import Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "UserSerializer"
        model = User
        fields = ["id", "phone_number"]


class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, help_text="UserSerializer")

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "description",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "CategorySerializer"
        model = Category
        fields = ["id", "name"]


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    comment_level = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "user_profile",
            "content",
            "comment_level",
            "replies",
        ]

    def get_replies(self, obj):
        descendants = obj.get_descendants()
        return CommentSerializer(descendants, many=True).data


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    # category = CategorySerializer(read_only=True, help_text="UserSerializer")

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "image",
            "title",
            "content",
            "category",
            "status",
            "created_date",
            "published_date",
            "category",
        ]
        read_only_fields = ["author"]

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if request.method == "GET" or request.parser_context.get(
            "kwargs"
        ).get("pk"):
            # check for post comments
            post_comments = Comment.objects.filter(
                post__id=instance.id, comment_level=0
            )
            rep["comments"] = CommentSerializer(post_comments, many=True).data
            # get post category information
            if instance.category is not None:
                rep["category"] = CategorySerializer(
                    instance.category, context={"request": request}
                ).data
            else:
                rep["category"] = None
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("id", None)
        return rep

    def create(self, validated_data):
        validated_data["author"] = Profile.objects.get(
            user__id=self.context.get("request").user.id
        )
        return super().create(validated_data)
