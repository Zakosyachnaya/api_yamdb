from django.urls import include, path
# from DjangoAPIapp.views import RegistrationAPIView
from rest_framework.routers import DefaultRouter

from .views import ProfileAPI, SignupAPIView, TokenView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', ProfileAPI, basename='profile')

urlpatterns = [
    path('v1/', include(router.urls)),
    # # path('v1/users/{username}/', )
    path('v1/auth/signup/', SignupAPIView.as_view(), name='signup'),
    # path('v1/auth/login', TokenObtainPairView.as_view(), name='login'),
    path('v1/auth/token', TokenView.as_view(), name='token'),
    # path('v1/categories')
    
]