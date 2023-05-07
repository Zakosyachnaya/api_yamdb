from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import UserViewSet
from . import views
from django.conf import settings

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

app_name = 'api'

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', views.signup, name='signup'),
    path('v1/auth/token/', views.token, name='token'),
]
