from django.urls import include, path
# from DjangoAPIapp.views import RegistrationAPIView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainSlidingView,
    TokenRefreshSlidingView,
)

from .views import UserViewSet
from . import views

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
# router.register(r'profiles', ProfileAPI, basename='profile')

urlpatterns = [
    path('v1/', include(router.urls)),
    # # path('v1/users/{username}/', )
    path('v1/auth/signup/', views.signup, name='signup'),
    # path('v1/auth/login', TokenObtainPairView.as_view(), name='login'),
    path('v1/auth/token/', views.token, name='token'),
    path('v1/token/', TokenObtainSlidingView.as_view(), name='token_obtain'),
    path('v1/token/refresh/', TokenRefreshSlidingView.as_view(), name='token_refresh'),
    # path('v1/categories')
]