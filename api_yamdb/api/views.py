from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator    
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from http import HTTPStatus
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, action, permission_classes
# from rest_framework.authentication import (BasicAuthentication,
#                                            SessionAuthentication)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import filters
from django.db import IntegrityError

from users.models import User

from .serializers import (TokenSerializer,
                          SignupSerializer, UserSerializer)
from .permissions import (IsAdmin, IsOwnerOrReadOnlyPermission,)
                        #   IsAuthenticatedOrReadOnly,)
from rest_framework.pagination import PageNumberPagination



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin, IsAuthenticated,]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
            methods=['get', 'patch'],
            detail=False, url_path='me',
            permission_classes=(
                IsAuthenticated, IsOwnerOrReadOnlyPermission,
            )
    )
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user.username)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=400)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny,])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    try:
        user, created = User.objects.get_or_create(
            username=username, email=email
        )
        
    except IntegrityError:
        return Response('Email уже существует', status=status.HTTP_400_BAD_REQUEST)
    confirmation_code = default_token_generator.make_token()
    print(confirmation_code)
    send_mail(
        subject='Ваш код подтверждения',
        message=confirmation_code,
        from_email=None,
        recipient_list=[email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny,])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.data.get('username')
    confirmation_code = serializer.data.get('confirmation_code')

    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        token = RefreshToken.for_user(user)
        return Response({token:'token'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=404)
