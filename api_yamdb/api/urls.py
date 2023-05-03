from django.urls import include, path
# from DjangoAPIapp.views import RegistrationAPIView
# from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

from api.views import CommentViewSet, ReviewViewSet, SignupAPIView, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignupAPIView.as_view(), name='signup'),
    path('v1/auth/login', TokenObtainPairView.as_view(), name='login'),
    path('v1/auth/refresh-token', TokenRefreshView.as_view(),
         name='refreshtoken'),
]
