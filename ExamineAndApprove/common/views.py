#from django.shortcuts import render
from common.models import UserLogin
from common import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
import jwt
import datetime
# Create your views here.
from common.extensions.auth import JwtAuthentication,create_token
from common.code import code
class Login(APIView):
    authentication_classes = []
    def post(self,request,format=None):
        user = request.data['account']
        pwd = request.data['password']
        queryset = UserLogin.objects.get(account=user)
        user_object = UserLogin.objects.filter(account=user, password=pwd).first()
        s = serializers.UserLoginSerializer(queryset)
        login_time = datetime.datetime.now()
        if not user_object:
            return Response({'status':{'code':code.error_2000[0],'msg':code.error_2000[1]}})
        token = create_token({'id': user_object.id, 'user': user_object.account})
        queryset.last_login = login_time
        queryset.save()
        return Response({
                            "current_user":{"user":user,"name":s.data['name'],"user_id":s.data['id'],"login_time":login_time,"department_name":s.data['department_name'],"department_id":s.data['department_id'],"type":s.data['type']},
                            'status':{'code':code.sucess_code1001[0],'msg':code.sucess_code1001[1]},
                            "token":token,"token_prefix":""

                         })
