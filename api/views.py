'''Contains the views of the API.'''

from rest_framework import status
from .models import Auth
from django.conf import settings
from jwt import encode
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializer import UserSerializer
from cerberus import Validator
from django.db.models import Q
from .constans import PASSWORD_REGEX, _STATUS_400_MESSAGE, _STATUS_401_MESSAGE


class UserAPI(APIView):
    ''' Definition of User API'''

    def post(self, request):
        """ Creates a new user.

        Parameters
        ----------

        request: dict
            Contains http transaction information.

        Returns
        -------

        Response: (dict, int)
            Body response and status code.

        """
        validator = Validator({
            'user': {'type': 'string', 'required': True},
            'last_name': {'type': 'string', 'required': True},
            "password": {
                "required": True, "type": "string",
                "regex": PASSWORD_REGEX
            }
        })
        
        if not validator.validate(request.data):
            return Response({
                "code": "invalid_body",
                "detailed": _STATUS_400_MESSAGE,
                "data": validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        existPerson = User.objects.filter(Q(user=request.data["user"]))
        if existPerson:
            return Response({
                "code": "integrity_error",
                "detailed": "Ya existe una persona registrada con ese User"
            }, status=status.HTTP_409_CONFLICT)
        
        userCreated = User.objects.create(**request.data)
        return Response({
            "id" : userCreated.id,
            "user_name": userCreated.user
        }, status=status.HTTP_200_OK)


    def get(self, request):
        """ Gets all users.

        Parameters
        ----------

        request: dict
            Contains http transaction information.

        Returns
        -------

        Response: (dict, int)
            Body response and status code.

        """
        header = request.headers.get("Authorization", None)
        if not header:
            return Response({
                "code": "invalid_header",
                "detailed": "Token de acceso inválido"
            }, status=status.HTTP_401_UNAUTHORIZED)
        header = header.split(" ")[1]
        if not Auth.objects.filter(token=header):
            return Response({
                "code": "invalid_header",
                "detailed": "Token de acceso inválido"
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        print(header)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=200)
    
class AuthAPI(APIView):
    ''' Definition of Auth API'''
    def post(self, request):
        """ Creates a new session.

        Parameters
        ----------

        request: dict
            Contains http transaction information.

        Returns
        -------

        Response: (dict, int)
            Body response and status code.

        """
        validator = Validator({
            'user': {'type': 'string', 'required': True},
            'password': {"required": True, "type": "string", "minlength": 7}
        })
        if not validator.validate(request.data):
            return Response({
                "code": "invalid_body",
                "detailed": _STATUS_400_MESSAGE,
                "data": validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(
                Q(user=request.data["user"]) &
                Q(password=request.data["password"])):
            return Response({
                "code": "invalid_credentials",
                "detailed": _STATUS_401_MESSAGE
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        token = encode({
            "user": request.data["user"]
        }, settings.SECRET_KEY, algorithm="HS256")
        
        print(token)
        
        Auth.objects.create(token=token)
        return Response({
            "token": token,
            "user_name": request.data["user"]
            }, status=status.HTTP_201_CREATED)
