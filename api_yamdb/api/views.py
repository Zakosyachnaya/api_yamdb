from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator    
from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User

from .serializers import (ProfileSerializer, SignupSerializer,
                               UserSerializer)
from .permissions import IsAdmin, IsOwnerOrReadOnlyPermission


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated,]
    # filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    # search_fields = ('username')


    def get_permissions(self):
        if self.action == 'list':
            self.IsAuthenticated = [IsAdmin,]
        elif self.action == 'retrieve':
            self.permission_classes = [IsOwnerOrReadOnlyPermission]
        return super(self.__class__, self).get_permissions()


class SignupAPIView(APIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny,]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = request.objects.get_or_create(
            username=request.data.get('username'),
            email=request.data.get('email')
        )

        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Ваш код подтверждения',
            message=f'Код {confirmation_code}',
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileAPI(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAdmin,]

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['username'])
        profile_serializer = ProfileSerializer(user.profile)
        return Response(profile_serializer.data)


class TokenView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),
            'confirmation_code': str(request.confirmation_code),
            }
        return Response(content)

# def profile(request, username):
#     author = get_object_or_404(User, username=username)
#     post_list = author.posts.select_related("group")
#     page_obj = paginate_page(request, post_list)
#     if (request.user.is_authenticated
#             and request.user != author):
#         following = Follow.objects.filter(
#             user=request.user,
#             author=author
#         ).exists()
#     else:
#         following = False
#     context = {
#         'page_obj': page_obj,
#         'author': author,
#         'following': following,
#     }
#     return render(request, 'posts/profile.html', context)