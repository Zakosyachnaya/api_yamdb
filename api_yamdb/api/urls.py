from api.views import CommentViewSet, ReviewViewSet, UserViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    UserViewSet,
    signup,
    token,
)

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("titles", TitleViewSet, basename="titles")
router.register("genres", GenreViewSet, basename="genres")
router.register("categories", CategoryViewSet, basename="categories")
router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename="reviews")
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)


urlpatterns = [
    path("v1/auth/token/", token, name="token"),
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", signup, name="signup"),
]
