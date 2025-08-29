from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.serializers import UserSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["is_admin"] = user.is_staff
        return token


@api_view(["POST"])
@permission_classes([AllowAny])
def signin(request):
    email = request.data.get("email")
    password = request.data.get("password")
    userModel = get_user_model()
    user = userModel.objects.filter(email__iexact=email).first()
    if user.check_password(password):
        return Response(UserSerializer(user).data)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    email = request.POST.get("email")
    username = request.POST.get("username")
    password = request.POST.get("password")
    user_model = get_user_model()
    existing_user = user_model.objects.filter(username__iexact=username).first()
    if existing_user:
        return Response(status=status.HTTP_409_CONFLICT)
    user = user_model.objects.create(username=username, email=email)
    user.set_password(password)
    user.save()
    return Response(UserSerializer(user).data)
