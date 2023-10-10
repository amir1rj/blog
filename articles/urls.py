from django.urls import path
from rest_framework.routers import DefaultRouter

from articles.views import *

urlpatterns=[
    path("hello",HelloUserView.as_view()),
    path("like/<pk>",LikeAPIView.as_view()),

]
router =DefaultRouter()
router.register(r"viewset",ArticleViewSet,basename="articles")
router.register(r"comments",CommentViewSet,basename="comments")
urlpatterns +=router.urls