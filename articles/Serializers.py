from datetime import datetime
from rest_framework import serializers
from persiantools.jdatetime import JalaliDate
from articles.models import Article, Comment, Like
from persiantools import characters, digits


def diffNowDate(DateStr):
   fmt = '%Y-%m-%d'
   d2 = datetime.strptime(str(datetime.now().year)+'-'+str(datetime.now().month)+'-'+str(datetime.now().day), fmt)
   d1 = datetime.strptime(DateStr, fmt)
   return (d2-d1).days
class CommentSerializer(serializers.ModelSerializer):
    days_ago =serializers.SerializerMethodField()
    created_at=serializers.SerializerMethodField()
    user = serializers.SlugRelatedField("username", read_only=True)
    class Meta:
        model = Comment
        fields = "__all__"

    def get_days_ago(self,obj):
        day = diffNowDate(str(obj.created_at))
        date=digits.to_word(day)
        if day ==0:
            return f"امروز"
        return f"{date} روز پیش "
    def get_created_at(self,obj):
        date=JalaliDate(obj.created_at,locale="fa")
        return date.strftime("%c")



class ArticleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(many=True,read_only=True,slug_field="title")
    status = serializers.BooleanField(write_only=True)
    comments = CommentSerializer(many=True,required=False)
    created_at = serializers.SerializerMethodField()
    user = serializers.SlugRelatedField("username",read_only=True)
    likes=serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields ="__all__"
    def get_created_at(self, obj):
        date = JalaliDate(obj.created_at, locale="fa")
        return date.strftime("%c")

    def validate(self, attrs):
        title = attrs.get('title')
        if Article.objects.filter(title=title).exists():
            raise serializers.ValidationError("your title is already exists")

        return attrs
    def create(self,validated_data):
        request = self.context["request"]
        if request.user.is_authenticated:
            validated_data["user"]= request.user
        return Article.objects.create(**validated_data)

    def get_comments(self,obj):
        serializer=CommentSerializer(instance=obj.comments.all(),many=True)
        return serializer.data
    def get_likes(self,obj):
        return len(Like.objects.filter(article_id=obj.id))

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField("username", read_only=True)
    class Meta:
        model = Like
        fields ="__all__"

    def create(self,validated_data):
        request = self.context["request"]
        if request.user.is_authenticated:
            validated_data["user"]= request.user
        return Article.objects.create(**validated_data)

