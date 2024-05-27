from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from ...serializers.auth.auth_serializers import LoginSerializers
from ...serializers.resources.resources_serializers import ResourcesSerializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.response import Response
from django.contrib.auth import logout
from rest_framework import status
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.models import Group
from ....models import Resources, Persons, Resources_roles, User



class AuthLoginFuncionario(APIView):
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def post(self, request, *args, **kwargs):
        
        serializers = LoginSerializers(
            data=request.data, context={"request": self.request}
        )
        if not serializers.is_valid():
            return Response(serializers.errors, status.HTTP_400_BAD_REQUEST)


        login(request, serializers.validated_data)  # type: ignore
        token = self.get_tokens_for_user(serializers.validated_data)


        rol_usuario = serializers.validated_data.groups.first()
        
        resources = []

        if rol_usuario is not None:
            recursos_roles = Resources_roles.objects.filter(rolesId=rol_usuario)
            recursos = [resource.resourcesId for resource in recursos_roles]
            resources =recursos
        else:
            recursos_roles = Resources_roles.objects.filter(rolesId=3)
            recursos = [resource.resourcesId for resource in recursos_roles]
            resources =recursos
        

        menu = ResourcesSerializers(resources, many=True)

        persons = Persons.objects.filter(id=serializers.validated_data.person_id).first()
        request.session["refresh-token"] = token["refresh"]
        return Response(
            {
                "token": token,
                "user": {
                    "name": serializers.validated_data.username,  # type: ignore
                    "id": serializers.validated_data.id,
                    "full_name": persons.fullname if hasattr(persons, 'fullname') else "",
                },  # type: ignore
                "menu": menu.data,
            },
            status.HTTP_200_OK,
        )


class LogoutView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            jwt_token = request.session.get("refresh-token", None)
            resp = HttpResponse("content")
            resp.cookies.clear()
            resp.flush()
            token = RefreshToken(jwt_token)
            token.blacklist()
            logout(request)
            request.session.clear()
            resp.flush()
            request.session.flush()
            return Response({"message": "Ok"}, status.HTTP_200_OK)
        except TokenError as TkError:
            return Response(f"{TkError}", status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e, status.HTTP_400_BAD_REQUEST)
        
