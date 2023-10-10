from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permisions import  IsOwnerOrReadOnly
from articles.Serializers import ArticleSerializer, CommentSerializer
from articles.models import Article, Comment, Like


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    def get_permissions(self):
        """
           Instantiates and returns the list of permissions that this view requires.
           """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsOwnerOrReadOnly,]
        return [permission() for permission in permission_classes]
    def update(self, request, pk=None, **kwargs):
        instance = Article.objects.get(id=pk)
        self.check_object_permissions(request, instance)
        serializer = ArticleSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(instance=instance, validated_data=serializer.validated_data)
            return Response({"response": "updated"})
        return Response({"response": serializer.errors})
    def create(self, request, **kwargs):
        serializer = ArticleSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.validated_data["user"] = request.user
            serializer.save()
            return Response({"response": "done"})
        return Response({"response": serializer.errors})


class HelloUserView(APIView):
    def get(self, request):
        print(request.user)
        return Response({"response": f"hello {request.user.username}"})


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_permissions(self):
        """
           Instantiates and returns the list of permissions that this view requires.
           """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated,]
        else:
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def update(self, request, pk=None, **kwargs):
        instance = Comment.objects.get(id=pk)
        self.check_object_permissions(request, instance)
        serializer = CommentSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(instance=instance, validated_data=serializer.validated_data)
            return Response({"response": "updated"})
        return Response({"response": serializer.errors})

    def create(self, request, **kwargs):
        serializer = CommentSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.validated_data["user"] = request.user
            serializer.save()
            return Response({"response": "done"})
        return Response({"response": serializer.errors})


# def like(request,slug,pk):
    # try:
    #     like= Like.objects.get(article__slug=slug, user_id=request.user.id)
    #     like.delete()
    # except:
    #     Like.objects.create(article_id=pk, user_id=request.user.id)
class LikeAPIView(APIView):
    def post(self,request,pk):
        try:
            int(pk)
            try:
                like = Like.objects.get(comment=pk, user_id=request.user.id)
                like.delete()
                return Response({"response": "unliked"})
            except:
                Like.objects.create(comment_id=pk, user_id=request.user.id)
                return Response({"response": "liked"})

        except:
            try:
                like = Like.objects.get(article__slug=pk, user_id=request.user.id)
                like.delete()
                return Response({"response": "unliked"})
            except:
                pk=Article.objects.get(slug=pk).id
                Like.objects.create(article_id=pk, user_id=request.user.id)
                return Response({"response": "liked"})


