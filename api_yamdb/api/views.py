from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator    
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
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

from .serializers import (TokenSerializer, MeSerializer,
                          SignupSerializer, UserSerializer)
from .permissions import (IsAdmin, IsOwnerOrReadOnlyPermission,)
                        #   IsAuthenticatedOrReadOnly,)
from rest_framework.pagination import PageNumberPagination



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = MeSerializer
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
            methods=['get', 'patch'],
            detail=False, url_path='me',
            permission_classes=(
                IsAuthenticated, IsOwnerOrReadOnlyPermission
            )
    )
    def profile(self, request):
        user = get_object_or_404(User, username=self.request.user.username)
        if request.method == 'GET':
            serializer = MeSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
        # if self.action == 'PATCH':
        #     if request.user.admin:
        #         serializer = UserSerializer(
        #             request.user,
        #             data=request.data,
        #             patial=True
        #         )
            # if request.user.user:
            #     serializer = UserSerializer(
            #         request.user,
            #         data=request.data,
            #         patial=True
            #     )
            return Response(serializer.errors, status=400)
        # serializer = MeSerializer(
        #             request.user,
        #             data=request.data,
        #             partial=True
        #         )
        # if serializer.is_valid():
        #     if 'role' in request.data:
        #         if user.role != 'user':
        #             serializer.save()
        #     else:
        #         serializer.save()
        serializer = MeSerializer(request.user)
        return Response(serializer.data, status=200)

        # elif self.action == 'GET':
        #     self.permission_classes = [IsOwnerOrReadOnlyPermission]
        # return super(self.__class__, self).get_permissions()



@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    # serializer.save()
    email = serializer.data['email']
    username = serializer.data['username']
    user, _ = User.objects.get_or_create(
                email=email,
                username=username
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Ваш код подтверждения',
        message=f'Код {confirmation_code}',
        from_email=None,
        recipient_list=[email],
        fail_silently=False,
    )
    return Response(serializer.data, status.HTTP_200_OK)

# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)

#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }

@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data['username']
    confirmation_code = serializer.data['confirmation_code']
    user = get_object_or_404(
            username=username
        )
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user()
        return Response({token:'token'}, status=200)
    return Response(serializer.errors, status=400)
# class SignupAPIView(APIView):
#     serializer_class = SignupSerializer
#     permission_classes = [AllowAny,]

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         user,_ = request.objects.get_or_create(
#             username=request.data.get('username'),
#             email=request.data.get('email')
#         )

#         confirmation_code = default_token_generator.make_token(user)
#         send_mail(
#             subject='Ваш код подтверждения',
#             message=f'Код {confirmation_code}',
#             from_email=None,
#             recipient_list=[user.email],
#             fail_silently=False,
#         )
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class ProfileAPI(viewsets.ModelViewSet):
#     serializer = ProfileSerializer
#     permission_classes = [IsAdmin,]

#     def get(self, request, *args, **kwargs):
#         user = get_object_or_404(User, pk=kwargs['username'])
#         profile_serializer = ProfileSerializer(user.profile)
#         return Response(profile_serializer.data)


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
