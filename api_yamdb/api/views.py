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

from users.models import User

from .serializers import (TokenSerializer,
                          SignupSerializer, UserSerializer)
from .permissions import (IsAdmin, IsOwnerOrReadOnlyPermission,)
                        #   IsAuthenticatedOrReadOnly,)
from rest_framework.pagination import PageNumberPagination



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # permission_classes_by_action = {'create': [AllowAny],
    #                                 'list': [IsAdminUser]}
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
    # @api_view(['GET', 'PATCH'])
    # @permission_classes([IsAuthenticated])
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
        # if self.action == 'PATCH':
        #     if request.user.admin:
        #         serializer = UserSerializer(
        #             request.user,
        #             data=request.data,
        #             patial=True
        #         )
            return Response(serializer.errors, status=400)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

        # elif self.action == 'GET':
        #     self.permission_classes = [IsOwnerOrReadOnlyPermission]
        # return super(self.__class__, self).get_permissions()



@api_view(['POST'])
@permission_classes([AllowAny,])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    # serializer.save()
    email = serializer.data.get('email')
    username = serializer.data.get('username')
    user, _ = User.objects.get_or_create(
                email=email,
                username=username
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Ваш код подтверждения',
        message=confirmation_code,
        from_email=None,
        recipient_list=[email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)

# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)

#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }

@api_view(['POST'])
@permission_classes([AllowAny,])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.data.get('username')
    confirmation_code = serializer.data.get('confirmation_code')

    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.get_token_for_user(user)
        return Response({token:'token'}, status=status.HTTP_200_OK)
    user.auth_token.delete()
    return Response(serializer.errors, status=404)

# class TokenView(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     # serializer_class = CustomTokenCreateSerializer

#     def get(self, request, format=None):
#         content = {
#             'username ': str(request.username),
#             'confirmation_code': str(request.confirmation_code),
#             }
#         return Response(content)
